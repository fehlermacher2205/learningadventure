``` mermaid
sequenceDiagram
    autonumber
    actor User as Frontend / User
    participant BE as Backend
    participant AI as OpenAI API
    participant DB as Database

    User->>BE: Send Input (App Input)
    BE->>AI: Send prompt to generate story
    AI-->>BE: Return raw node text
    BE->> BE: Process 
    BE->>DB: Save structured node data
    BE-->>User: Return success / Display data
```