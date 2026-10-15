
``` mermaid
flowchart LR
    User((User))

    subgraph System["AI Assistant Website"]
        Profile1(Modify Personal Assistant)
        Profile2(Start new session)
        Profile3(Regenerate exercise)
        Profile4(Submit Solution)
        Profile5(Reset Session)
    end

    User --- Profile1
    User --- Profile2
    User --- Profile3
    User --- Profile4
    User --- Profile5
```