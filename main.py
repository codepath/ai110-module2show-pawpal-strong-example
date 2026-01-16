from pawpal_system import *

# -------------------------
# TEST SETUP (Owner, 2 pets, 3+ tasks)
# -------------------------

owner = Owner("Amelia", daily_time_available=55)

pet1 = Pet("Ani", "Dog")
pet2 = Pet("Haze", "Cat")

# Add at least 3 tasks with different durations
task1 = Task("Morning walk", duration_minutes=20, priority=5, time=480, pet_name=pet1.name)
task2 = Task("Feed Haze", duration_minutes=5, priority=4, time=540, pet_name=pet1.name)
task3 = Task("Clean litter box", duration_minutes=10, priority=5, time=600, pet_name=pet2.name)
task4 = Task("Playtime with Ani", duration_minutes=15, priority=3, time=450, pet_name=pet2.name)

pet1.add_task(task1)
pet1.add_task(task2)
pet2.add_task(task3)
pet2.add_task(task4)

# Mark one task complete for filtering demo
task2.mark_complete()

owner.add_pet(pet1)
owner.add_pet(pet2)

# Generate and print today's schedule
scheduler = Scheduler()
plan, explanation = scheduler.generate_plan(owner)
print(plan, explanation)

print("=== PawPal+ Today's Schedule ===")
total = 0
for task in plan:
    print(f"[#{task.number}] {task.description} - {task.duration_minutes} min (priority {task.priority})")
    total += task.duration_minutes

print(f"\nTotal scheduled time: {total} min (out of {owner.daily_time_available} min)\n")

print("=== Reasoning ===")
for line in explanation:
    print("-", line)

print("\n=== Tasks by Pet ===")
tasks_by_pet = owner.get_all_task_by_pet()
for pet_name, tasks in tasks_by_pet.items():
    print(f"{pet_name}:")
    for task in tasks:
        print(f"  [#{task.number}] {task.description} at {task.time} min")

print("\n=== Tasks Sorted by Time ===")
sorted_by_time = scheduler.sort_by_time(owner.get_all_tasks())
for task in sorted_by_time:
    print(f"[#{task.number}] {task.description} at {task.time} min")

print("\n=== Incomplete Tasks ===")
incomplete_tasks = scheduler.filter_by_completed(owner.get_all_tasks(), completed=False)
for task in incomplete_tasks:
    print(f"[#{task.number}] {task.description} (incomplete)")

task1.mark_complete()

print("\n=== Completed Tasks ===")
completed_tasks = scheduler.filter_by_completed(owner.get_all_tasks(), completed=True)
for task in completed_tasks:
    print(f"[#{task.number}] {task.description} (completed)")