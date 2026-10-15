from core.prompts import GOALS_PROMPT
from core.llm import LLMFactory
import json
from models.goal_action import Goal
from models.story import  Story
# this one can generate 
# even if story is empty
# this one does not save to db right away

from core.exceptions import (
    InvalidSessionError,
    ObjectNotFoundError,
    PermissionDeniedError,
)
def generate_goals(
    context: str,
    story: Story,
    ):

    background = story.background
    last_page_context = "No content"
    if story.pages:
        last_page_context = f"Previous page content: {story.pages[-1].content}\nUser choice on that page: {story.pages[-1].choice_text}\n"
    
    goal_prompt_rule = story.profile.prompt.goal_prompt

    response_text = LLMFactory.llm_text_invoker(
        system_prompt=GOALS_PROMPT,
        user_prompt=f"Based on the following story context, background, and last page content, generate a list of goals for the user. Story context: {context}, background: {background}, last page context: {last_page_context}, goal prompt rule: {goal_prompt_rule}"
    )

    try:
        parsed_goals = json.loads(response_text)
        created_goals = []
        for goal in parsed_goals:
            new_goal = Goal(
                title=goal["title"],
                category=goal["category"],
                skill=goal["skill"],
                level=goal["level"],
            )
            created_goals.append(new_goal)
        return created_goals

    except Exception as e:
        raise ValueError(f"Invalid LLM response: {response_text}") from e

def get_goals_as_String(goals: list[Goal]) -> str:
    if not goals:
        return "No specific goals."
    goal_lines = []
    goal_lines_focus = []
    for goal in goals:
        line = f"- {goal.title} (Category: {goal.category}, Skill: {goal.skill}, Level: {goal.level})"
        if goal.is_focused:
            goal_lines_focus.append(line)
        else:
            goal_lines.append(line)
    if len(goal_lines_focus)>0:
        return goal_lines_focus
    return "\n".join(goal_lines)

def check_duplicate(goals: list[Goal], new_goal:Goal):
    for goal in goals:
        if (goal.title == new_goal.title and 
            goal.category == new_goal.category and
            goal.skill == new_goal.skill and
            goal.level == new_goal.level
        ):
            raise PermissionDeniedError("You can't have duplicate active goal!")
            