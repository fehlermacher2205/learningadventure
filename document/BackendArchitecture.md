``` mermaid
classDiagram

%% ========== ROUTER LAYER ==========
class Router {
    +handle_request()
}

%% ========== SCHEMA LAYER ==========
class BaseNode {
    +common_fields
}

class RequestNode {
    +validate()
}

class ResponseNode {
    +serialize()
}

BaseNode <|-- RequestNode
BaseNode <|-- ResponseNode

%% ========== COMPONENTS (BUSINESS LOGIC) ==========

class Components {
    +user
    +profile
    +goal
    +story
    +consequences
}


class Service {
    +generate_story()
    +evaluate_action()
    +update_database()
}

%% ========== MODEL / DB LAYER ==========
class Model {
    -attributes
}

class Database {
    +save()
    +load()
}



%% ========== RELATIONSHIPS ==========
Router --> RequestNode : receives
Router --> Components
Router --> ResponseNode : returns

Components --> Model : uses
Components --> Service : processes

Components --> Database 
```