# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design had four classes: `Owner`, `Pet`, `Task`, and `Scheduler`.

- **Owner** stored the owner's name and a list of `Pet` objects, with `add_pet()` and `get_pets()` methods.
- **Pet** was a simple data holder with just `name`, `species`, and `breed` — no behavior.
- **Task** represented a single care activity (title, category, which pet it belonged to, scheduled time, duration, priority, whether it was recurring, and completion status), plus a `mark_complete()` method.
- **Scheduler** held its own list of every `Task` in the system and was responsible for adding/removing tasks and answering questions like "what's due today" or "what's the plan for a pet."

The reasoning behind this split was to avoid two classes both trying to own the same list of tasks: `Pet` stayed "dumb" (pure data), while `Scheduler` was the single source of truth for tasks across all pets.

**b. Design changes**

Yes, the design changed once I started thinking through how tasks actually connect to pets and owners. I moved task ownership from `Scheduler` to `Pet` — each `Pet` now holds its own `tasks` list directly (`add_task()`, `get_tasks()`), `Owner` gained a `get_all_tasks()` method that gathers tasks across all of its pets, and `Scheduler` became stateless: instead of storing tasks itself, it takes an `Owner` as an argument and pulls/organizes tasks on demand (`get_tasks_for_today(owner)`, `build_daily_plan(owner)`).

I also had to add a `date` field and a `frequency` field ("once"/"daily"/"weekly") to `Task`, along with an `is_due_on()` method. Originally `Task` only tracked a time of day and completion status, but that wasn't enough to answer "is this task due today?" — a time like "08:00" doesn't say *which* day, so I needed a date to anchor one-time and weekly tasks against, and a way for daily tasks to always count as due.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
