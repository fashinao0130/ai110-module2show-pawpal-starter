from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task, TaskCategory


def make_task(
    description="Feeding",
    *,
    category=TaskCategory.FEEDING,
    task_date=None,
    scheduled_time="08:00",
    duration_minutes=10,
    priority="high",
    frequency="daily",
):
    return Task(
        description=description,
        category=category,
        date=task_date or date.today(),
        scheduled_time=scheduled_time,
        duration_minutes=duration_minutes,
        priority=priority,
        frequency=frequency,
    )


def test_mark_complete_sets_is_completed_true():
    task = make_task()
    assert task.is_completed is False

    task.mark_complete()

    assert task.is_completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Mochi", "dog")
    assert len(pet.get_tasks()) == 0

    pet.add_task(make_task("Morning walk"))

    assert len(pet.get_tasks()) == 1


def test_sort_by_time_returns_chronological_order():
    scheduler = Scheduler()
    evening = make_task("Dinner", scheduled_time="18:30")
    morning = make_task("Breakfast", scheduled_time="08:00")
    midday = make_task("Walk", scheduled_time="12:15")

    sorted_tasks = scheduler.sort_by_time([evening, morning, midday])

    assert [task.description for task in sorted_tasks] == ["Breakfast", "Walk", "Dinner"]


def test_mark_task_complete_creates_next_day_occurrence():
    pet = Pet("Mochi", "dog")
    today = date(2026, 9, 30)
    task = make_task("Morning walk", task_date=today, frequency="daily")
    pet.add_task(task)

    next_task = pet.mark_task_complete(task)

    assert task.is_completed is True
    assert next_task is not None
    assert next_task.date == today + timedelta(days=1)
    assert next_task.is_completed is False
    assert next_task.frequency == "daily"
    assert next_task in pet.get_tasks()
    assert len(pet.get_tasks()) == 2


def test_find_conflicts_flags_duplicate_times():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    today = date(2026, 9, 30)
    pet.add_task(
        make_task("Walk", task_date=today, scheduled_time="09:00", frequency="once")
    )
    pet.add_task(
        make_task("Feeding", task_date=today, scheduled_time="09:00", frequency="once")
    )
    owner.add_pet(pet)

    warnings = Scheduler().find_conflicts(owner, today=today)

    assert len(warnings) == 1
    assert "Mochi" in warnings[0]
    assert "09:00" in warnings[0]
