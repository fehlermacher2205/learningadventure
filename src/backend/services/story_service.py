from sqlalchemy.orm import Session
from core.llm import LLMFactory
from core.prompts import (
    QUEST_PROMPT,
    PAGE_PROMPT
)
from typing import List
from core.exceptions import ObjectNotFoundError, PermissionDeniedError, InvalidSessionError
from models.story import Story, StoryPage,StoryTextHistory
from models.goal_action import ActiveGoalsInProfile,Goal
from models.profile import Profile
from models.user import User
from services.utility import (
    save_to_db
)
import json
from schemas.story import  StoryPageResponse
from services.json_parse import safe_parse_llm
from services.goals_services import get_goals_as_String

def generate_story(choice_text: str, story:Story,db:Session, goals: List[Goal]) -> Story: 
    # profile has prompt
    # story session has goals, actions
    goal_text = get_goals_as_String(goals)
    answers_snapshot_string = json.dumps(story.answers_snapshot)
    if goal_text and goal_text == "" and answers_snapshot_string == "[]":
        raise PermissionDeniedError("No goals or answers_snapshot found for the story session. Cannot generate story without context.")
    userprompt = ""
    if choice_text and choice_text != "":
        userprompt = f"The user has made the following choice: {choice_text}. "
    userprompt += f"The task should align with the my goals: {goal_text}"  
    userprompt += f"These are my ecademic backgrounds, you can ignore if it doesn't provide approriated valuable information{answers_snapshot_string}"
    response_text = LLMFactory.llm_text_invoker(
        system_prompt=QUEST_PROMPT,
        user_prompt= userprompt
    )
    parsed = safe_parse_llm(response_text)
    
    version = story.background_version_count+1

    story.title = parsed["title"] 
    story.background = parsed["content"]
    text_history = StoryTextHistory(
        story_id= story.id,
        position_in_story = 0,
        version= version,
        choice_text = choice_text,
        content = parsed["content"]
    )
    save_to_db(db,text_history)
    story.background_ver = version
    story.background_version_count = version
    db.commit()
    db.refresh(story)
    return story



# This is the repeated context generator
# note that this one is only available after first generation background


def generate_story_page(
        db: Session, 
        story: Story,
        choice_text: str,
        goals: List[Goal]
    )->StoryPageResponse:
    
    if not story.is_active:
        raise PermissionDeniedError("This story session has ended. Please start a new story to continue.")
    context =""
    context = story.background
    total_page = story.page_count
    if total_page <10: 
        for page in story.pages:
            context += page.content
    else:
        for i in range(10):
            context += page[total_page-i-1].content
    goals = get_goals_as_String(goals)

    prompt = PAGE_PROMPT + context 

    prompt += f"It is recommended to generate content that aligns with the following goals:{goals}"

    profile_page_prompt_rule = f"Some rules for prompt: {story.profile.prompt.page_prompt}"
    prompt = profile_page_prompt_rule + prompt
    response_text = LLMFactory.llm_text_invoker(
        system_prompt= prompt,
        user_prompt = choice_text
    )
    parsed = safe_parse_llm(response_text)
    new_page = StoryPage(
        story_id=story.id,
        content = parsed["content"],
        choice_text=choice_text,
        page_number= len(story.pages) + 1
    )
    # increase page count
    story.page_count = new_page.page_number
    save_to_db(db, new_page)
    return new_page


def get_story_page(story: Story, page_number: int, db: Session) -> StoryPageResponse:
    try:
        story_id = story.id
        page = db.query(StoryPage).filter(
            StoryPage.story_id == story_id,
            StoryPage.page_number == page_number
        ).first()
        if not page:
            raise ValueError(f"Story page not found for story {story.id} and page_number {page_number}")
        return page
    finally:
        db.close()





# mainly for our action evalue
def get_first_and_last_page(
    story: Story
):
    
    first_page = story.pages[0]
    if not first_page:
        raise ValueError(f"First page not found for story_id {story.id}")
    last_page = story.pages[-1]
    if not last_page:
        raise ValueError(f"Last page not found for story_id {story.id}")
    return first_page, last_page


def createDefaultStory(profile:Profile,user:User,db:Session,answers_snapshot: List ):
    newstory = Story(
            profile_id=profile.id,
            user_id=user.id,
            background = profile.predefined_background,
            title = profile.profile_name,
            answers_snapshot = answers_snapshot
        )
    save_to_db(db,newstory)
    return newstory

    