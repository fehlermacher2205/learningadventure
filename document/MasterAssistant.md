``` mermaid
classDiagram

class MasterAssistant{
    +profile_id
    +user_id
}

class ProfileRules {
    +rules_id
    +profile_id
}

class BackgroundQuestion {
    +question_id
    +profile_id
}

class PredefinedGoal {
    +template_goal_id
}

User "1" --> "many" MasterAssistant : owns
MasterAssistant "1" --> "1" ProfileRules : has
MasterAssistant "1" --> "many" BackgroundQuestion : has
MasterAssistant "1" --> "many" PredefinedGoal : has
```