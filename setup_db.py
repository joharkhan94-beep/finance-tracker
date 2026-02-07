import sqlite3

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

# We add 'user TEXT' to the columns
cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        date TEXT,
        category TEXT,
        item TEXT,
        cost REAL,
        type TEXT,
        user TEXT
    )
""")

conn.commit()
conn.close()
print("✅ Database with User column built!")