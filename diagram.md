# Diagram

classDiagram
    class Task {
        +description: str
        +duration_minutes: int
        +priority: int
        +frequency: str
        +completed: bool
        +mark_complete() void
        +mark_incomplete() void
    }

    class Pet {
        +name: str
        +species: str
        +tasks: list~Task~
        +add_task(task: Task) void
        +remove_task(task_description: str) bool
        +get_tasks() list~Task~
    }

    class Owner {
        +name: str
        +daily_time_available: int
        +pets: list~Pet~
        +add_pet(pet: Pet) void
        +get_all_tasks() list~Task~
    }

    class Scheduler {
        +generate_plan(owner: Owner) tuple~list~Task~, list~str~~
    }

    Owner "1" --> "0..*" Pet : owns
    Pet "1" --> "0..*" Task : has
    Scheduler ..> Owner : uses constraints
    Scheduler ..> Task : schedules


# Final Diagram

classDiagram
    class Task {
        +description: str
        +duration_minutes: int
        +priority: int
        +time: int
        +pet_name: str
        +frequency: str
        +completed: bool
        +due_date: date
        +number: int
        +mark_complete() void
        +mark_incomplete() void
    }

    class Pet {
        +name: str
        +species: str
        +tasks: list~Task~
        +add_task(task: Task) void
        +remove_task(task_number: int) void
        +get_tasks() list~Task~
    }

    class Owner {
        +name: str
        +daily_time_available: int
        +pets: list~Pet~
        +add_pet(pet: Pet) void
        +get_all_tasks() list~Task~
        +get_all_task_by_pet() dict
    }

    class Scheduler {
        +generate_plan(owner: Owner) tuple~list~Task~, list~str~~
        +sort_by_time(tasks: list~Task~) list~Task~
        +filter_by_completed(tasks: list~Task~, completed: bool) list~Task~
        +mark_task_complete(owner: Owner, task_number: int) bool
        +detect_conflicts(tasks: list~Task~) list~str~
    }

    Owner "1" --> "0..*" Pet : owns
    Pet "1" --> "0..*" Task : has
    Scheduler ..> Owner : uses
    Scheduler ..> Task : schedules



```mermaid
classDiagram
    class Task {
        +str description
        +int duration_minutes
        +str priority
        +int time
        +str pet_name
        +str frequency = "daily"
        +bool completed = False
        +date due_date
        +int number
        <<ClassVar>> +int _counter
        <<ClassVar>> +dict~str,int~ _PRIORITY_RANKS
        +__post_init__() None
        +_normalize_priority(value: str|int) str
        +priority_rank int
        +priority_label str
        +mark_complete() None
        +mark_incomplete() None
    }

    class Pet {
        +str name
        +str species
        +List~Task~ tasks
        +add_task(task: Task) None
        +remove_task(task_number: int) None
        +get_tasks() List~Task~
    }

    class Owner {
        +str name
        +int daily_time_available
        +List~Pet~ pets
        +add_pet(pet: Pet) None
        +get_all_tasks() List~Task~
        +get_all_task_by_pet() dict
        +save_to_json(owners: List~Owner~, file_path: str = "data.json") None
        +load_from_json(file_path: str = "data.json") List~Owner~
    }

    class Scheduler {
        +generate_plan(owner: Owner) Tuple~List~Task~, List~str~~
        +sort_by_time(tasks: List~Task~) List~Task~
        +filter_by_completed(tasks: List~Task~, completed: bool) List~Task~
        +mark_task_complete(owner: Owner, task_number: int) bool
        +detect_conflicts(tasks: List~Task~) List~str~
    }

    Owner "1" o-- "*" Pet : owns
    Pet "1" o-- "*" Task : has
    Scheduler ..> Owner : plans for
    Scheduler ..> Task : schedules/checks

```