"""Class stubs for PawPal+, matching diagrams/uml.mmd.

No scheduling logic yet — attributes are set up, methods are placeholders.
"""

from dataclasses import dataclass


@dataclass
class Pet:
    name: str
    species: str
    breed: str = None


@dataclass
class Task:
    title: str
    category: str
    pet: Pet
    scheduled_time: str
    duration_minutes: int
    priority: str
    is_recurring: bool = False
    is_completed: bool = False

    def mark_complete(self):
        pass


class Owner:
    def __init__(self, name):
        self.name = name
        self.pets = []

    def add_pet(self, pet):
        pass

    def get_pets(self):
        pass


class Scheduler:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        pass

    def remove_task(self, task):
        pass

    def get_tasks_for_today(self):
        pass

    def get_tasks_for_pet(self, pet):
        pass

    def build_daily_plan(self):
        pass
