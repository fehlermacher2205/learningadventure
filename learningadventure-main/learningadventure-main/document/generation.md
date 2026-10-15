## Sequence
``` mermaid
sequenceDiagram
    participant C as Client
    participant S as System
    participant P as PersonalAssistant
    participant M as MasterAssistant
    participant L as LanguageModel

    loop until is_active is false
        C ->>S: Send Text
        S->>S: getSystemRules

        M->>S: Fetch Master Assistant Rules

        P->>S: fetchPersonalInformation

        L->>S: Send prompt and get raw text

        S->>S: Parse text and save structured data
        S->>S: Return response Text
    end

```