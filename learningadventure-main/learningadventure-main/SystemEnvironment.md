``` mermaid
flowchart LR
    Admin([Admin])
    User([User])
    DB[(Database)]
    LLM([LLM API])
    Developer[(Developer)]
    subgraph System["AI Assistant Platform"]
        Profile[Course Profile]
        Personal[Personal Assistant]
        Manager[Generation Manager]
    end

    Admin -->|Manage| Profile
    User -->|Browse| Profile
    Profile -->|Create| Personal
    Personal -->|Controlled by| Manager
    Developer -->|Manage| Manager

    Personal --> DB
    Manager --> LLM
```