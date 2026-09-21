"""Demo/testing ground for the PawPal+ classes.

Creates an owner with two pets and a few tasks, then prints today's schedule.
"""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler, TaskCategory

today = date.today()
next_week = today + timedelta(days=7)

owner = Owner("Jordan")

mochi = Pet("Mochi", "dog", breed="Golden Retriever")
whiskers = Pet("Whiskers", "cat")

owner.add_pet(mochi)
owner.add_pet(whiskers)

mochi.add_task(Task(
    description="Morning walk",
    category=TaskCategory.WALK,
    date=today,
    scheduled_time="08:00",
    duration_minutes=30,
    priority="high",
    frequency="daily",
))

mochi.add_task(Task(
    description="Feeding",
    category=TaskCategory.FEEDING,
    date=today,
    scheduled_time="08:30",
    duration_minutes=10,
    priority="high",
    frequency="daily",
))

whiskers.add_task(Task(
    description="Medication",
    category=TaskCategory.MEDICATION,
    date=today,
    scheduled_time="09:00",
    duration_minutes=5,
    priority="high",
    frequency="once",
))

# Not due today, included to show that filtering actually works.
whiskers.add_task(Task(
    description="Vet appointment",
    category=TaskCategory.APPOINTMENT,
    date=next_week,
    scheduled_time="14:00",
    duration_minutes=60,
    priority="medium",
    frequency="once",
))

scheduler = Scheduler()
plan = scheduler.build_daily_plan(owner)

print(f"Daily plan for {owner.name} — {today.isoformat()}")
if not plan:
    print("  No tasks scheduled for today.")
for task in plan:
    pet_name = next(p.name for p in owner.get_pets() if task in p.get_tasks())
    print(f"  {task.scheduled_time} — {task.description} ({pet_name}) [priority: {task.priority}]")
