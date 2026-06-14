import sqlite3

conn = sqlite3.connect("tasks.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    recurrence TEXT,
    due_date TEXT,
    status TEXT,
    streak INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()

print("Database created successfully!")