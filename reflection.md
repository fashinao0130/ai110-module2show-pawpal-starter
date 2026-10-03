# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design had four classes: `Owner`, `Pet`, `Task`, and `Scheduler`.

- **Owner** stored the owner's name and a list of `Pet` objects, with `add_pet()` and `get_pets()` methods.

- **Pet** just holds data with `name`, `species`, and `breed`.

- **Task** represented a single care activity (title, category, which pet it belonged to, scheduled time, duration, priority, whether it was recurring, and completion status) and a `mark_complete()` method.

- **Scheduler** held its own list of every `Task` in the system and was responsible for adding or removing tasks and answering questions like "what's due today" or "what's the plan for a pet."

The reasoning behind this split was to avoid two classes both trying to own the same list of tasks which is why `Pet` is just pure data. while `Scheduler` was the single source of truth for tasks across all pets.

**b. Design changes**

Yes, the design changed once I started thinking through how tasks actually connect to pets and owners. I moved task ownership from `Scheduler` to `Pet` which means each `Pet` now holds its own `tasks` list directly (`add_task()`, `get_tasks()`), `Owner` gained a `get_all_tasks()` method that gathers tasks across all of its pets, and `Scheduler` became stateless: instead of storing tasks itself, it takes an `Owner` as an argument and pulls/organizes tasks on demand (`get_tasks_for_today(owner)`, `build_daily_plan(owner)`).

I also had to add a `date` field and a `frequency` field ("once"/"daily"/"weekly") to `Task`, along with an `is_due_on()` method. Originally `Task` only tracked a time of day and completion status, but that wasn't enough to answer "is this task due today?" For example a time like "08:00" doesn't say which day it must be done, so I needed a date for one-time and weekly tasks, and a way for daily tasks to always count as due.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**


The scheduler considers three things: time, priority used to rank tasks so urgent ones surface first, and conflicts whether two tasks for the same pet land at the same time. It does not consider owner preferences for example "no tasks before 7am" or pet-specific limits for example max tasks per day" those weren't in apart of this version.

Priority was ranked above time: build_daily_plan() sorts by priority first, then by time within each priority level. The reasoning is that a pet-care app should surface urgency over chronology. Conflicts were treated as the lowest-stakes constraint: rather than blocking scheduling outright when two tasks collide, the scheduler just warns, on the assumption that a human should make the final call about overlapping care tasks rather than the program silently dropping one.

**b. Tradeoffs**


The Find conflicts function only catches tasks with the same schedule time string but it doesnt check if the actual time windows overlap


This is reasonable because r≥eal overlap detection means comparing every task's start-plus-duration against the next task's start time, which adds real complexity for an edge case (near-miss overlaps) that rarely happens with a handful of daily pet-care tasks. Catching exact same-time conflicts already handles the obvious mistake so trading full accuracy for a simpler, "good enough" check is a reasonable tradeoff for a small personal planner, even though it would need to be fixed for something higher-stakes.


---

## 3. AI Collaboration

**a. How you used AI**

I used Claude mostly for the parts that would've taken me a long time to work through alone: brainstorming what edge cases actually mattered for sorting and recurring tasks, drafting the pytest functions for those specific behaviors, updating app.py to actually use Scheduler.find_conflicts instead of just showing the sorted list, and comparing my UML diagram against the real pawpal_system.py once I was done implementing. The prompts that worked best were the specific ones, like asking what to update in the UML "based on my final implementation" instead of just asking it to redo the diagram. That forced it to actually diff my code against the diagram instead of guessing at what my classes do.

**b. Judgment and verification**

One place I didn't just take the output as-is was testing the Streamlit UI changes. After I asked for app.py to use st.success/st.warning/st.table, Claude told me it couldn't actually click through the app in a browser since there's no browser automation tool set up in this environment, it could only confirm the server started and that the data being fed into those components was correct. So I know I still need to open the app myself and click "Generate schedule" with two conflicting tasks before I can say that change actually works, not just trust that the code looks right.

---

## 4. Testing and Verification

**a. What you tested**

Besides the two tests I already had (marking a task complete, and a pet's task count going up after adding one), I added tests for the three Scheduler behaviors this assignment actually cares about: that sort_by_time returns tasks in chronological order, that completing a daily task creates a new task dated one day later, and that find_conflicts flags two tasks for the same pet at the same time. These mattered because they're the exact behaviors I'm claiming in the README demo walkthrough, so if they were wrong the "smarter scheduling" part of the app wouldn't actually hold up.

**b. Confidence**

I'm fairly confident the common cases work since all 5 tests pass, but not confident on the edges. When I asked Claude to list edge cases for a scheduler like this, it found a few real gaps I haven't fixed or tested yet: a completed task still shows up as "due today" because is_due_on and get_tasks_for_today never check is_completed, weekly tasks only check if the weekday matches rather than whether the start date has passed yet (so a weekly task starting next month would incorrectly look due right now), and find_conflicts only flags tasks with the exact same scheduled_time string, so two overlapping-but-not-identical times (9:00 for an hour vs. 9:30) slip through even though duration_minutes exists for exactly that. If I had more time I'd write tests for those and fix them.

---

## 5. Reflection

**a. What went well**

Probably the Scheduler itself. Once I split task ownership out to Pet and made Scheduler stateless, build_daily_plan, sort_by_time, and find_conflicts all came together pretty cleanly, and the tests back that up.

**b. What you would improve**

I'd go fix the gaps from section 4, the completed-task bug and the weekly recurrence date bug especially since those are actual bugs and not just missing features, and I'd make find_conflicts compare actual time windows using duration_minutes instead of just matching the exact scheduled_time string.

**c. Key takeaway**

Design docs and diagrams drift from the real code fast once you start implementing, mine did. It's better to come back and fix the UML and README after the logic exists instead of trying to get everything perfect upfront.
