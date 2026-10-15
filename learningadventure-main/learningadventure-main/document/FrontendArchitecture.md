``` mermaid
flowchart LR
    A[Client / UI] --> B[FastAPI Router]
    B --> C[RequestNode]
    C --> D[Service / Engine]
    D --> E[ResponseNode]
    E --> B
    B --> A
```