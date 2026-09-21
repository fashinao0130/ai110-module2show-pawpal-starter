"""PawPal+ core classes: Task, Pet, Owner, Scheduler.

Matches diagrams/uml.mmd.
"""

from dataclasses import dataclass, field
from datetime import date as date_type

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    description: str
    category: str
    date: date_type
    scheduled_time: str
    duration_minutes: int
    priority: str
    frequency: str = "once"  # "once", "daily", or "weekly"
    is_completed: bool = False

    def mark_complete(self):
        self.is_completed = True

    def is_due_on(self, target_date):
        if self.frequency == "daily":
            return True
        if self.frequency == "weekly":
            return self.date.weekday() == target_date.weekday()
        return self.date == target_date


@dataclass
class Pet:
    name: str
    species: str
    breed: str = None
    tasks: list = field(default_factory=list)

    def add_task(self, task):
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks


class Owner:
    def __init__(self, name):
        self.name = name
        self.pets = []

    def add_pet(self, pet):
        self.pets.append(pet)

    def get_pets(self):
        return self.pets

    def get_all_tasks(self):
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def get_tasks_for_today(self, owner, today=None):
        today = today or date_type.today()
        return [task for task in owner.get_all_tasks() if task.is_due_on(today)]

    def get_tasks_for_pet(self, pet, today=None):
        if today is None:
            return pet.get_tasks()
        return [task for task in pet.get_tasks() if task.is_due_on(today)]

    def build_daily_plan(self, owner, today=None):
        todays_tasks = self.get_tasks_for_today(owner, today)
        return sorted(
            todays_tasks,
            key=lambda task: (PRIORITY_ORDER.get(task.priority, 99), task.scheduled_time),
        )
