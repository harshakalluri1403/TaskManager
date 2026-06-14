import sqlite3
import subprocess
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "tasks.db")

DB = "tasks.db"


def github_sync():
    try:
        subprocess.run(
            ["git", "add", "."],
            check=True,
            capture_output=True,
            text=True
        )

        subprocess.run(
            ["git", "commit", "-m", "Task Update"],
            check=False,
            capture_output=True,
            text=True
        )

        subprocess.run(
            ["git", "push"],
            check=True,
            capture_output=True,
            text=True
        )

        print("\n✓ GitHub Synced Successfully!")

    except Exception as e:
        print(f"\n✗ GitHub Sync Failed: {e}")


def show_tasks():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, recurrence, due_date, status
        FROM tasks
        ORDER BY id
    """)

    rows = cur.fetchall()

    print("\n==============================")
    print("CURRENT TASKS")
    print("==============================")

    if not rows:
        print("No tasks found.")
    else:
        for row in rows:
            print(
                f"{row[0]}. {row[1]} | "
                f"{row[2]} | Due: {row[3]} | "
                f"Status: {row[4]}"
            )

    conn.close()


def add_task():
    print("\n=== ADD TASK ===")

    name = input("Task Name: ").strip()

    print("\nRecurrence:")
    print("1. Daily")
    print("2. Weekly")
    print("3. Monthly")
    print("4. One-Time")

    rec_choice = input("Choose: ")

    recurrence_map = {
        "1": "Daily",
        "2": "Weekly",
        "3": "Monthly",
        "4": "One-Time"
    }

    recurrence = recurrence_map.get(rec_choice, "One-Time")

    due = input("Due Date (YYYY-MM-DD): ")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tasks
        (name, recurrence, due_date, status)
        VALUES (?, ?, ?, ?)
    """, (name, recurrence, due, "Pending"))

    conn.commit()
    conn.close()

    print("\n✓ Task Added Successfully!")

    github_sync()


def complete_task():
    show_tasks()

    task_id = input("\nEnter Task ID to complete: ")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET status='Completed'
        WHERE id=?
    """, (task_id,))

    conn.commit()

    if cur.rowcount > 0:
        print("\n✓ Task Completed!")
    else:
        print("\n✗ Task ID not found.")

    conn.close()

    github_sync()


def delete_task():
    show_tasks()

    task_id = input("\nEnter Task ID to delete: ")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM tasks
        WHERE id=?
    """, (task_id,))

    conn.commit()

    if cur.rowcount > 0:
        print("\n✓ Task Deleted!")
    else:
        print("\n✗ Task ID not found.")

    conn.close()

    github_sync()


def main():
    while True:

        print("\n=================================")
        print("      PERSONAL TASK MANAGER")
        print("=================================")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")
        print("=================================")

        choice = input("Choose: ")

        if choice == "1":
            show_tasks()

        elif choice == "2":
            add_task()

        elif choice == "3":
            complete_task()

        elif choice == "4":
            delete_task()

        elif choice == "5":
            github_sync()
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid Choice. Try Again.")


if __name__ == "__main__":
    main()
