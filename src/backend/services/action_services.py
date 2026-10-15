
from sqlalchemy.orm import Session

from typing import List
from schemas.action import ActionResponse
from services.utility import save_to_db
from core.llm import LLMFactory
from core.prompts import ACTIONS_VALUES_PROMPT, FIND_GOAL_PROMPT
import json
from models.goal_action import Action, ActiveGoalsInProfile, Goal
from models.story import  Story
from models.user import User
from core.exceptions import ObjectNotFoundError, PermissionDeniedError, InvalidSessionError
from services.goals_services import get_goals_as_String
def resolveActionEffect(
    goals_text: str , action_text:str     
):
    response_text = LLMFactory.llm_text_invoker(
        system_prompt= FIND_GOAL_PROMPT,
        user_prompt=f"The action: {action_text}. The list of goals:{goals_text}"
    )
    try:
        response_text = response_text.strip()
        goals_similarity = json.loads(response_text)
        if not isinstance(goals_similarity, list):
            raise ValueError("Response is not a list")
        return goals_similarity
    except Exception as e:
        raise ValueError(f"JSON Parsing Error resolveActionEffect: {str(e)} \nRaw Text: {response_text}") from e
def evaluate_last_action(
    story: Story,
    db: Session,
    user: User
) -> List[ActionResponse]:
    if story.is_active != True:
        raise PermissionDeniedError("This story session has ended. Please start a new story to continue.")

    if story.pages == []:
        raise ObjectNotFoundError("Story has no pages")
    profile = story.profile
# we dont check visibility here
    active_goals = db.query(ActiveGoalsInProfile).filter(ActiveGoalsInProfile.profile_id == profile.id,ActiveGoalsInProfile.user_id == user.id).first().goals
# if there is no goals, then no valuation
    if active_goals == []:
        return []
    goals_text = get_goals_as_String(active_goals)

    background = story.background
    recent_choice_text = story.pages[-1].choice_text
    last_task_text = ""
    if story.page_count > 1:
         last_task_text = story.pages[-2]
    action_prompt_rule = story.profile.prompt.action_prompt
    system_text =ACTIONS_VALUES_PROMPT+ f"additional context: {background}, recent given task: {last_task_text}"
     
    response_text = LLMFactory.llm_text_invoker(
        system_prompt= system_text,
        user_prompt=f"Choice: {recent_choice_text} user's goals:{goals_text}, action prompt rule: {action_prompt_rule}"
    )
    try:
        response_text = response_text.strip()
        consequences = json.loads(response_text)
        if not isinstance(consequences, list):
            raise ValueError("Response is not a list")
    except Exception as e:
        raise ValueError(f"JSON Parsing Error: {str(e)} \nRaw Text: {response_text}") from e
    try:
        saved_consequences = []
        for consequence in consequences:
            type_text = ""
            if consequence["value"] <0:
                type_text = "mistake"
            elif consequence["value"] >0:
                type_text = "progress"

            new_action = Action(
                type= type_text,
                action= consequence["action"],
                title= consequence["title"],
                value= consequence["value"],
                reasoning= consequence.get("reasoning", ""),
                category= consequence.get("category", ""),
                skill= consequence.get("skill", ""),
                story_page_id= story.pages[-1].id,
                story_id = story.id
            )
            action_text = (
                f"{consequence['action']} | "
                f"{consequence['title']} | "
                f"Value: {consequence['value']} | "
                f"Reasoning: {consequence.get('reasoning', '')} | "
                f"Category: {consequence.get('category', '')}"
            )
# we use llm to determine which goals an action belong to            
            goals_similarity = resolveActionEffect(
                goals_text = goals_text, 
                action_text = action_text
            )
            for gs in goals_similarity:
                index = gs["goal_index"]
                similarity = gs["similarity"]
                new_score = active_goals[index].skill_score + similarity * new_action.value   
                active_goals[index].skill_score = round(new_score)
            db.commit()        
            save_to_db(db, new_action)
            saved_consequences.append(new_action)
            
    except Exception as e:
        raise RuntimeError(f"Database Error: {str(e)}") from e
    return saved_consequences