from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Pet care planner")


if "owners" not in st.session_state:
    st.session_state.owners = {}
if "active_owner" not in st.session_state:
    st.session_state.active_owner = None
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()


def to_minutes(t: time) -> int:
    return t.hour * 60 + t.minute


def to_hhmm(minutes: int) -> str:
    h = minutes // 60
    m = minutes % 60
    return f"{h:02d}:{m:02d}"


def get_active_owner_record():
    owner_name = st.session_state.active_owner
    if not owner_name:
        return None
    return st.session_state.owners.get(owner_name)


def build_owner_model(owner_name: str, owner_record: dict) -> Owner:
    owner = Owner(owner_name, int(owner_record["daily_time_available"]))
    for pet in owner_record["pets"].values():
        owner.add_pet(pet)
    return owner


st.subheader("Owners")
owner_col1, owner_col2, owner_col3 = st.columns([2, 2, 1])
with owner_col1:
    new_owner_name = st.text_input("Owner name", value="Jordan", key="owner_name_input")
with owner_col2:
    new_owner_daily_time = st.number_input(
        "Daily time available (minutes)",
        min_value=0,
        max_value=1440,
        value=120,
        key="owner_daily_time_input",
    )
with owner_col3:
    st.write("")
    st.write("")
    if st.button("Add owner"):
        cleaned_owner = new_owner_name.strip()
        if not cleaned_owner:
            st.error("Owner name is required.")
        elif cleaned_owner in st.session_state.owners:
            st.warning(f"Owner '{cleaned_owner}' already exists.")
        else:
            st.session_state.owners[cleaned_owner] = {
                "daily_time_available": int(new_owner_daily_time),
                "pets": {},
            }
            st.session_state.active_owner = cleaned_owner
            st.success(f"Added owner '{cleaned_owner}'.")

if st.session_state.owners:
    st.write("Current owners:")
    st.table(
        [
            {
                "owner": name,
                "daily_time_available": data["daily_time_available"],
                "pets": len(data["pets"]),
            }
            for name, data in st.session_state.owners.items()
        ]
    )

    st.session_state.active_owner = st.selectbox(
        "Active owner",
        options=list(st.session_state.owners.keys()),
        index=(
            list(st.session_state.owners.keys()).index(st.session_state.active_owner)
            if st.session_state.active_owner in st.session_state.owners
            else 0
        ),
        key="active_owner_select",
    )

    active_record = get_active_owner_record()
    if active_record is not None:
        updated_daily_time = st.number_input(
            "Update active owner daily minutes",
            min_value=0,
            max_value=1440,
            value=int(active_record["daily_time_available"]),
            key="active_owner_daily_minutes",
        )
        if st.button("Save owner settings"):
            active_record["daily_time_available"] = int(updated_daily_time)
            st.success(f"Updated settings for '{st.session_state.active_owner}'.")
else:
    st.info("No owners yet. Add an owner to continue.")

st.divider()

active_record = get_active_owner_record()
st.subheader("Pets")
if active_record is None:
    st.caption("Add and select an owner first.")
else:
    pet_col1, pet_col2, pet_col3 = st.columns([2, 2, 1])
    with pet_col1:
        new_pet_name = st.text_input("Pet name", value="Mochi", key="pet_name_input")
    with pet_col2:
        new_pet_species = st.selectbox(
            "Species", ["Dog", "Cat", "Other"], key="pet_species_input"
        )
    with pet_col3:
        st.write("")
        st.write("")
        if st.button("Add pet"):
            cleaned_pet = new_pet_name.strip()
            if not cleaned_pet:
                st.error("Pet name is required.")
            elif cleaned_pet in active_record["pets"]:
                st.warning(
                    f"Pet '{cleaned_pet}' already exists for owner '{st.session_state.active_owner}'."
                )
            else:
                active_record["pets"][cleaned_pet] = Pet(cleaned_pet, new_pet_species)
                st.success(
                    f"Added pet '{cleaned_pet}' to owner '{st.session_state.active_owner}'."
                )

    if active_record["pets"]:
        st.write(f"Current pets for {st.session_state.active_owner}:")
        st.table(
            [
                {"name": p.name, "species": p.species}
                for p in active_record["pets"].values()
            ]
        )
    else:
        st.info("No pets yet for this owner.")

st.divider()

st.subheader("Tasks")
if active_record is None or not active_record["pets"]:
    st.caption("Select an owner with at least one pet first.")
else:
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        task_pet = st.selectbox("Pet", list(active_record["pets"].keys()), key="task_pet")
        task_title = st.text_input(
            "Task description", value="Morning walk", key="task_description"
        )
        task_duration = st.number_input(
            "Duration (minutes)",
            min_value=1,
            max_value=240,
            value=20,
            key="task_duration",
        )
        priority_label = st.selectbox(
            "Priority", ["1", "2", "3", "4", "5"], index=4, key="task_priority"
        )
    with t_col2:
        task_time = st.time_input("Start time", value=time(8, 0), step=300, key="task_time")
        frequency = st.selectbox(
            "Frequency", ["daily", "weekly", "monthly"], index=0, key="task_frequency"
        )
        due = st.date_input("Due date", value=date.today(), key="task_due_date")
        completed = st.checkbox("Mark as completed", key="task_completed")

    if st.button("Add task"):
        desc = task_title.strip()
        if not desc:
            st.error("Task description is required.")
        else:
            task = Task(
                description=desc,
                duration_minutes=int(task_duration),
                priority=int(priority_label),
                time=to_minutes(task_time),
                pet_name=task_pet,
                frequency=frequency,
                completed=completed,
                due_date=due,
            )
            active_record["pets"][task_pet].add_task(task)
            st.success(
                f"Added task #{task.number} for {task_pet} (owner: {st.session_state.active_owner})."
            )

    all_tasks = []
    for pet in active_record["pets"].values():
        for t in pet.get_tasks():
            all_tasks.append(
                {
                    "#": t.number,
                    "pet": t.pet_name,
                    "description": t.description,
                    "duration": t.duration_minutes,
                    "priority": t.priority,
                    "time": to_hhmm(t.time),
                    "frequency": t.frequency,
                    "due_date": t.due_date.isoformat(),
                    "completed": t.completed,
                }
            )

    if all_tasks:
        st.write(f"Current tasks for {st.session_state.active_owner}:")
        st.table(all_tasks)
    else:
        st.info("No tasks yet for this owner.")

st.divider()

st.subheader("Scheduler")
if active_record is None:
    st.caption("Select an owner first.")
elif st.button("Generate schedule"):
    owner = build_owner_model(st.session_state.active_owner, active_record)
    scheduler = st.session_state.scheduler
    plan, explanation = scheduler.generate_plan(owner)

    st.markdown(f"### Plan for {st.session_state.active_owner}")
    if not plan:
        st.warning("No tasks scheduled with current time constraints.")
    else:
        st.table(
            [
                {
                    "#": t.number,
                    "pet": t.pet_name,
                    "description": t.description,
                    "time": to_hhmm(t.time),
                    "duration": t.duration_minutes,
                    "priority": t.priority,
                }
                for t in scheduler.sort_by_time(plan)
            ]
        )

    st.markdown("### Why")
    for line in explanation:
        st.write(f"- {line}")

    conflicts = scheduler.detect_conflicts(owner.get_all_tasks())
    st.markdown("### Conflict check")
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
    else:
        st.success("No time conflicts detected.")

    st.markdown("### Completion filters")
    incomplete = scheduler.filter_by_completed(owner.get_all_tasks(), completed=False)
    complete = scheduler.filter_by_completed(owner.get_all_tasks(), completed=True)
    st.write(f"Incomplete tasks: {len(incomplete)}")
    st.write(f"Completed tasks: {len(complete)}")

st.divider()

st.subheader("Mark Task Complete")
if active_record is None:
    st.caption("Select an owner first.")
else:
    owner_for_completion = build_owner_model(st.session_state.active_owner, active_record)
    tasks_for_picker = sorted(owner_for_completion.get_all_tasks(), key=lambda t: t.number)

    if tasks_for_picker:
        option_map = {
            f"#{t.number} | {t.pet_name} | {t.description} | due {t.due_date}": t.number
            for t in tasks_for_picker
        }
        selected_label = st.selectbox(
            "Choose task", list(option_map.keys()), key="complete_task_select"
        )

        if st.button("Mark selected task complete"):
            ok = st.session_state.scheduler.mark_task_complete(
                owner_for_completion, option_map[selected_label]
            )
            if ok:
                st.success(
                    "Task marked complete. If frequency is daily/weekly, next occurrence was created."
                )
            else:
                st.error("Task not found.")
    else:
        st.caption("No tasks available for this owner.")
