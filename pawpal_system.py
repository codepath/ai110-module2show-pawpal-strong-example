from dataclasses import dataclass, field
from typing import List, Tuple, ClassVar

@dataclass
class Task:
    description: str
    duration_minutes: int
    priority:  int # scale of 1-5 (5 highest)
    time: int #minutes since midnight
    pet_name: str
    frequency: str = "daily"
    completed: bool = False
    number: int = field(init=False)
    _counter: ClassVar[int] = 0 # class variable for unique numbering

    def __post_init__(self) -> None:
        #assign_number function called after init to assign unique number
        Task._counter += 1
        self.number = self._counter
        

    def mark_complete(self) -> None:
        self.completed = True

    def mark_incomplete(self) -> None:
        self.completed = False


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    '''def remove_task(self, task_description: str) -> None:
        for task in self.tasks:
            if task.description == task_description:
                self.tasks.remove(task)'''
    
    def remove_task(self, task_number: int) -> None:
        for task in self.tasks:
            if task.number == task_number:
                self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        return self.tasks #list(self.tasks)


@dataclass
class Owner:
    name: str
    daily_time_available: int  # minutes
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks
    
    def get_all_task_by_pet(self):
        tasks_by_pet = {}
        for pet in self.pets:
            tasks_by_pet[pet.name] = pet.get_tasks()
        return tasks_by_pet
# -------------------------
# Scheduling Logic
# -------------------------

@dataclass
class Scheduler:
    def generate_plan(self, owner: Owner) -> Tuple[List[Task], List[str]]:
        """
        Returns:
        - plan: tasks selected for today
        - explanation: reasons why tasks were selected or skipped
        """
        available_minutes = owner.daily_time_available
        explanation: List[str] = []
        selected: List[Task] = []

        tasks = owner.get_all_tasks()
        #sort by priority (high to low), then by duration (short to long)
        tasks.sort(key=lambda t: (-t.priority, t.duration_minutes))

        for task in tasks:
            
            if task.completed:
                explanation.append(
                    f"Skipped '{task.description}' (already completed)."
                )
                continue
            if task.duration_minutes > available_minutes:
                explanation.append(
                    f"Skipped '{task.description}' (not enough time)."
                )
                continue
            selected.append(task)
            available_minutes -= task.duration_minutes
            explanation.append(
                f"Scheduled '{task.description}' (priority {task.priority})."
            )

        return selected, explanation
    
    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: t.time)
    
    def filter_by_completed(self, tasks: List[Task], completed: bool) -> List[Task]:
        return [t for t in tasks if t.completed == completed]
