``` mermaid
classDiagram

class User
class Admin

class CourseProfile{
}


Admin "1" --> "0..*" CourseProfile : owns


class Session {
    +Background answers
}

class SessionPage {
}

class Action {
}

Session "1" --> "0..*" SessionPage : has
SessionPage "1" --> "0..*" Action : has



class PersonalAssistant {
}

class Goal {
}

User "1" --> "1..*" PersonalAssistant : tracks
CourseProfile "1" ..> "0..*" PersonalAssistant : linked
PersonalAssistant "1" --> "0..*" Goal : contains

PersonalAssistant "1" --> "1..*" Session : owns
```