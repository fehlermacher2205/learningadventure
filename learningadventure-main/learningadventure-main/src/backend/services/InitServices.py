from models.user import User , UserSession
from models.profile import Profile, ProfileStatus,MAX_QUESTION_NUM
from sqlalchemy.orm import Session
from models.profile import Profile,ProfilePrompt,BackgroundQuestion,PredefinedGoal
from db.database import SessionLocal
import uuid
from datetime import datetime
from core.exceptions import (
    InvalidSessionError, 
    SessionExpiredError,
    ObjectNotFoundError,
    PermissionDeniedError
)
def initAdmin()->User:
    db = SessionLocal()
    admin = db.query(User).filter(
        User.id == 9999999).first()
    if not admin:
        try:
            admin = User(
                id = 9999999, 
                matriculation_number="9999999",
                username="Endministrator",
                password= "99999999",
                is_admin = True
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
        except: 
            PermissionDeniedError(" There must be a duplication in admin creation")   
    return admin
def initProgrammingProfile()->Profile:
    db = SessionLocal()
    werkstatt = db.query(Profile).filter(
        Profile.id == "code_bar_programmierwerkstatt").first()
    if not werkstatt:
        try:
            werkstatt = Profile(
                id = "code_bar_programmierwerkstatt",
                user_id= 9999999,
                profile_name = "Code_bar_programmierwerkstatt"
                )
            prompt = ProfilePrompt()
            werkstatt.predefined_background ="""


## Choose a Difficulty Level

### 1. Beginner

Create a simple calculator that supports the following operations:

* Addition (+)
* Subtraction (-)
* Multiplication (*)
* Division (/)

The calculator should also be able to remember and reuse the last calculated result.

**Concepts to practice:**

* Variables
* Functions
* User input handling
* Conditional statements (if/else)

---

### 2. Intermediate

Create a calculator that:

* Accepts calculations as a string input (e.g., "12+5")
* Uses loops to allow multiple calculations without restarting the program
* Stores the entered expression
* Allows the user to edit a digit in the stored expression and recalculate the result

**Concepts to practice:**

* Loops
* Lists and data structures
* String manipulation
* Problem-solving and program design

"""
            questions = werkstatt.questions

            questions.append(BackgroundQuestion(
                question_text="What is your current programming experience level? (Beginner, Intermediate, Advanced)",
                position=1
            ))

            questions.append(BackgroundQuestion(
                question_text="Which programming languages have you worked with so far?",
                position=2
            ))

            questions.append(BackgroundQuestion(
                question_text="Which programming language do you want to focus on right now? (e.g., Python, JavaScript, Java)",
                position=3
            ))

            questions.append(BackgroundQuestion(
                question_text="What do you expect from programming?",
                position=4
            ))

            questions.append(BackgroundQuestion(
                question_text="Which areas of programming interest you the most? (e.g., Web, AI, Data Science, Game Dev)",
                position=5
            ))

            questions.append(BackgroundQuestion(
                question_text="Do you prefer learning through theory, practice, or projects?",
                position=6
            ))

            questions.append(BackgroundQuestion(
                question_text="How comfortable are you with problem-solving and algorithms?",
                position=7
            ))

            questions.append(BackgroundQuestion(
                question_text="Have you worked on any programming projects before? If yes, briefly describe them.",
                position=8
            ))

            questions.append(BackgroundQuestion(
                question_text="How much time per week can you dedicate to learning programming?",
                position=9
            ))

            questions.append(BackgroundQuestion(
                question_text="What challenges do you usually face when learning programming?",
                position=10
            ))
            goals = werkstatt.predefined_goals

            goals.append(PredefinedGoal(
                title="Fix a Broken Loop",
                category="Debugging",
                skill="Control Flow (loops, conditionals)",
                level="Beginner",
                position_in_profile=1
            ))

            goals.append(PredefinedGoal(
                title="Debug Conditional Logic Errors",
                category="Debugging",
                skill="If/Else Logic",
                level="Beginner",
                position_in_profile=2
            ))

            goals.append(PredefinedGoal(
                title="Work with Lists and Collections",
                category="Data Structures",
                skill="Lists & Dictionaries",
                level="Beginner",
                position_in_profile=3
            ))

            goals.append(PredefinedGoal(
                title="Perform Basic Data Transformations",
                category="Data Handling",
                skill="Variables & Assignments",
                level="Beginner",
                position_in_profile=4
            ))

            goals.append(PredefinedGoal(
                title="Read and Process Input",
                category="Input Handling",
                skill="Input & Output",
                level="Beginner",
                position_in_profile=5
            ))

            goals.append(PredefinedGoal(
                title="Write and Use Helper Functions",
                category="Functions",
                skill="Function Definitions & Calls",
                level="Beginner",
                position_in_profile=6
            ))

            goals.append(PredefinedGoal(
                title="Traverse Data with Loops",
                category="Control Flow",
                skill="Loops & Iteration",
                level="Beginner",
                position_in_profile=7
            ))

            goals.append(PredefinedGoal(
                title="Search for Items in Data Structures",
                category="Problem Solving",
                skill="Loops + Conditions",
                level="Intermediate",
                position_in_profile=8
            ))

            goals.append(PredefinedGoal(
                title="Manipulate and Analyze Strings",
                category="Algorithms",
                skill="String Processing",
                level="Intermediate",
                position_in_profile=9
            ))

            goals.append(PredefinedGoal(
                title="Implement Basic Algorithms",
                category="Algorithms",
                skill="Sorting / Searching",
                level="Intermediate",
                position_in_profile=10
            ))

            goals.append(PredefinedGoal(
                title="Build a Simple Calculator Logic",
                category="Application Logic",
                skill="Math + Control Flow",
                level="Intermediate",
                position_in_profile=11
            ))

            goals.append(PredefinedGoal(
                title="Optimize Basic Code Performance",
                category="Performance",
                skill="Efficiency & Complexity",
                level="Intermediate",
                position_in_profile=12
            ))

            goals.append(PredefinedGoal(
                title="Nested Data Structures",
                category="Data Structures",
                skill="Advanced Lists & Dictionaries",
                level="Intermediate",
                position_in_profile=13
            ))

            goals.append(PredefinedGoal(
                title="Decode and Transform Encoded Data",
                category="Algorithms",
                skill="String & Pattern Logic",
                level="Advanced",
                position_in_profile=14
            ))

            goals.append(PredefinedGoal(
                title="Design Modular Program Structure",
                category="Software Design",
                skill="Separation of Concerns",
                level="Advanced",
                position_in_profile=15
            ))

            goals.append(PredefinedGoal(
                title="Implement Error Handling Strategies",
                category="Robustness",
                skill="Exceptions & Validation",
                level="Advanced",
                position_in_profile=16
            ))

            werkstatt.prompt = prompt
            db.add(werkstatt)
            db.commit()
            db.refresh(werkstatt)

        except: 
            PermissionDeniedError(" There must be a duplication in admin creation")   
    return werkstatt
