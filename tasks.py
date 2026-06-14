import sqlite3

DB = "tasks.db"

def show_tasks():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks WHERE status='Pending'")
    rows = cur.fetchall()

    print("\n=== PENDING TASKS ===")

    if not rows:
        print("No pending tasks")

    for row in rows:
        print(f"{row[0]}. {row[1]} | Due: {row[3]}")

    conn.close()


def add_task():
    name = input("Task Name: ")
    recurrence = input("Recurrence (Daily/Weekly/Monthly): ")
    due = input("Due Date (YYYY-MM-DD): ")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO tasks(name, recurrence, due_date, status)
    VALUES(?,?,?,?)
    """, (name, recurrence, due, "Pending"))

    conn.commit()
    conn.close()

    print("Task Added Successfully!")


def complete_task():
    task_id = input("Enter Task ID: ")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    UPDATE tasks
    SET status='Completed'
    WHERE id=?
    """, (task_id,))

    conn.commit()
    conn.close()

    print("Task Completed!")


while True:

    print("\n===== TASK MANAGER =====")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Complete Task")
    print("4. Exit")

    choice = input("Choose: ")

    if choice == "1":
        show_tasks()

    elif choice == "2":
        add_task()

    elif choice == "3":
        complete_task()

    elif choice == "4":
        break