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

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
