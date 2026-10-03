# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Daily plan for Daily plan for Jordan — 2026-09-20
  08:00 — Morning walk (Mochi, dog) [priority: high]
  08:30 — Feeding (Mochi, dog) [priority: high]
  09:00 — Medication (Whiskers, cat) [priority: high]
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.13.9, pytest-8.4.2, pluggy-1.5.0 -- /opt/anaconda3/bin/python3
cachedir: .pytest_cache
rootdir: /Users/olufashina/ai110/ai110-module2show-pawpal-starter
plugins: anyio-4.10.0, Faker-40.12.0
collecting ... collected 5 items

test/test_pawpal.py::test_mark_complete_sets_is_completed_true PASSED    [ 20%]
test/test_pawpal.py::test_add_task_increases_pet_task_count PASSED       [ 40%]
test/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED [ 60%]
test/test_pawpal.py::test_mark_task_complete_creates_next_day_occurrence PASSED [ 80%]
test/test_pawpal.py::test_find_conflicts_flags_duplicate_times PASSED    [100%]

============================== 5 passed in 0.06s ===============================
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

### Main UI features

The Streamlit app (`app.py`) lets a user:

- Enter an **owner name**, persisted across reruns via `st.session_state`
- **Add a pet** (name, species, optional breed)
- **Add a task** for a selected pet — description, category (from the fixed `TaskCategory` enum), priority, date, time (`HH:MM`), duration, and frequency (`once`, `daily`, or `weekly`)
- Click **Generate schedule** to build and display that owner's plan for today

### Example workflow

1. Enter an owner name (e.g., "Jordan") and add a pet (e.g., "Mochi", species "dog").
2. Add a task for that pet — e.g., "Morning walk" at `08:00`, priority `high`, frequency `daily`.
3. Add a second task at the same time (e.g., "Nail trim" at `08:00`, priority `medium`, frequency `once`) to see conflict detection in action.
4. Click **Generate schedule**.
5. The app shows a `st.warning` for the overlapping 08:00 tasks, a `st.success` summary of how many tasks were scheduled, and a `st.table` of the sorted plan (time, task, pet, species, priority).

### Key Scheduler behaviors shown

- **Filtering** — `get_tasks_for_today` only includes tasks actually due on the selected date, via each `Task.is_due_on(...)` check (so a task dated next week, like "Vet appointment" below, is correctly excluded today).
- **Sorting** — `build_daily_plan` sorts tasks chronologically by `scheduled_time` first, then by priority (`high` → `medium` → `low`), so the busiest/most urgent tasks surface first.
- **Conflict detection** — `find_conflicts` groups each pet's tasks by `scheduled_time` and flags any pet with two or more tasks at the same time, rather than silently double-booking them.
- **Recurring tasks** — completing a `daily` or `weekly` task (`Pet.mark_task_complete`) automatically enqueues its next occurrence via `Task.next_occurrence()`.

### Sample CLI output

`main.py` seeds an owner with two pets and a deliberate same-time conflict, then prints the daily plan and any warnings:

```bash
python main.py
```

```
Daily plan for Jordan — 2026-10-01
  08:00 — Morning walk (Mochi, dog) [priority: high]
  08:30 — Feeding (Mochi, dog) [priority: high]
  09:00 — Medication (Whiskers, cat) [priority: high]
  08:00 — Nail trim (Mochi, dog) [priority: medium]

Conflicts:
  Warning: Mochi has 2 tasks scheduled at 08:00 (Morning walk, Nail trim)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
