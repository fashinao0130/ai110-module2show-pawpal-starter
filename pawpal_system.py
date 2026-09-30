"""PawPal+ core classes: Task, Pet, Owner, Scheduler.

Matches diagrams/uml.mmd.
"""

from dataclasses import dataclass, field, replace
from datetime import date as date_type, timedelta
from enum import Enum

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class TaskCategory(Enum):
    """Fixed set of task types, so category can't drift into arbitrary free text."""

    FEEDING = "feeding"
    WALK = "walk"
    MEDICATION = "medication"
    APPOINTMENT = "appointment"


@dataclass
class Task:
    description: str
    category: TaskCategory
    date: date_type
    scheduled_time: str
    duration_minutes: int
    priority: str
    frequency: str = "once"  # "once", "daily", or "weekly"
    is_completed: bool = False

    def mark_complete(self):
        """Mark this task as completed and return the next occurrence, if it recurs."""
        self.is_completed = True
        return self.next_occurrence()

    def next_occurrence(self):
        """Return a fresh, incomplete Task for this task's next due date, or None if it doesn't recur."""
        if self.frequency == "daily":
            next_date = self.date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.date + timedelta(weeks=1)
        else:
            return None
        return replace(self, date=next_date, is_completed=False)

    def is_due_on(self, target_date):
        """Return True if this task is scheduled to occur on target_date."""
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
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self):
        """Return this pet's list of tasks."""
        return self.tasks

    def mark_task_complete(self, task):
        """Mark task complete and, if it recurs, add its next occurrence to this pet's tasks."""
        next_task = task.mark_complete()
        if next_task is not None:
            self.add_task(next_task)
        return next_task


class Owner:
    def __init__(self, name):
        self.name = name
        self.pets = []

    def add_pet(self, pet):
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_pets(self):
        """Return this owner's list of pets."""
        return self.pets

    def get_all_tasks(self):
        """Return every task across all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def get_tasks_for_today(self, owner, today=None):
        """Return all of owner's tasks that are due on today (defaults to the real today)."""
        today = today or date_type.today()
        return [task for task in owner.get_all_tasks() if task.is_due_on(today)]

    def get_tasks_for_pet(self, pet, today=None):
        """Return pet's tasks, optionally filtered to those due on today."""
        if today is None:
            return pet.get_tasks()
        return [task for task in pet.get_tasks() if task.is_due_on(today)]

    def sort_by_time(self, tasks):
        """Return tasks sorted chronologically by scheduled_time ("HH:MM")."""
        return sorted(
            tasks,
            key=lambda task: tuple(int(part) for part in task.scheduled_time.split(":")),
        )

    def build_daily_plan(self, owner, today=None):
        """Return owner's tasks due today, sorted by priority then scheduled time."""
        todays_tasks = self.get_tasks_for_today(owner, today)
        by_time = self.sort_by_time(todays_tasks)
        return sorted(by_time, key=lambda task: PRIORITY_ORDER.get(task.priority, 99))

    def find_conflicts(self, owner, today=None):
        """Return a warning message for each pet with two+ tasks due today at the same time.

        Lightweight by design: it groups each pet's tasks by scheduled_time and
        flags any group with more than one task, instead of raising an error.
        """
        today = today or date_type.today()
        warnings = []
        for pet in owner.get_pets():
            tasks_by_time = {}
            for task in self.get_tasks_for_pet(pet, today):
                tasks_by_time.setdefault(task.scheduled_time, []).append(task)

            for scheduled_time, tasks in tasks_by_time.items():
                if len(tasks) > 1:
                    descriptions = ", ".join(task.description for task in tasks)
                    warnings.append(
                        f"Warning: {pet.name} has {len(tasks)} tasks scheduled at "
                        f"{scheduled_time} ({descriptions})"
                    )
        return warnings
