from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler, TaskCategory

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+ — a pet care planning assistant.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# --- Owner setup, persisted across reruns ---
st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)
st.session_state.owner.name = owner_name
owner = st.session_state.owner

st.divider()

# --- Add a pet ---
st.subheader("Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    breed = st.text_input("Breed (optional)", value="")

if st.button("Add pet"):
    owner.add_pet(Pet(pet_name, species, breed or None))
    st.success(f"Added {pet_name} ({species}).")

if owner.get_pets():
    st.write("Current pets:", ", ".join(p.name for p in owner.get_pets()))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a task ---
st.subheader("Add a Task")

if owner.get_pets():
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_pet_name = st.selectbox("Pet", [p.name for p in owner.get_pets()])
    with col2:
        category_label = st.selectbox("Category", [c.name.title() for c in TaskCategory])
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    description = st.text_input("Task description", value="Morning walk")

    col4, col5, col6, col7 = st.columns(4)
    with col4:
        task_date = st.date_input("Date", value=date.today())
    with col5:
        scheduled_time = st.text_input("Time (HH:MM)", value="08:00")
    with col6:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col7:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task"):
        selected_pet = next(p for p in owner.get_pets() if p.name == selected_pet_name)
        selected_pet.add_task(
            Task(
                description=description,
                category=TaskCategory[category_label.upper()],
                date=task_date,
                scheduled_time=scheduled_time,
                duration_minutes=int(duration),
                priority=priority,
                frequency=frequency,
            )
        )
        st.success(f"Added task '{description}' for {selected_pet_name}.")
else:
    st.info("Add a pet before adding tasks.")

st.divider()

# --- Build and display today's schedule ---
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler()
    plan = scheduler.build_daily_plan(owner)

    for warning in scheduler.find_conflicts(owner):
        st.warning(warning)

    if not plan:
        st.info("No tasks scheduled for today.")
    else:
        st.success(f"Built a schedule with {len(plan)} task(s), sorted by priority then time.")
        rows = []
        for task in plan:
            pet = next(p for p in owner.get_pets() if task in p.get_tasks())
            rows.append(
                {
                    "Time": task.scheduled_time,
                    "Task": task.description,
                    "Pet": pet.name,
                    "Species": pet.species,
                    "Priority": task.priority.title(),
                }
            )
        st.table(rows)
