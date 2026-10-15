## Sequence

``` mermaid
sequenceDiagram
    participant U as User
    participant C as Client
    participant S as Server

    Note over U, S: Create, Edit Learning Rules for the Profile/Course

    

    U->>C: Select Profile/Course


    Note over U, S: Update Personal Learning Goals 

    U->>C: Request Tasks

    Note over U, S: Tasks Generation

    S->>S: Store Tasks

    loop until is_active is false
        C->>U: Display tasks
        U->>C: Submit Answer
        C->>S: Send Answer, request evaluation
        S->>S: Store Datas
        S->>C: Return evaluation
        C->>U: Display Result
    end
```