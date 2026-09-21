from datetime import date

from pawpal_system import Pet, Task, TaskCategory


def make_task(description="Feeding"):
    return Task(
        description=description,
        category=TaskCategory.FEEDING,
        date=date.today(),
        scheduled_time="08:00",
        duration_minutes=10,
        priority="high",
        frequency="daily",
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
