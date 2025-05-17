import sqlite3

# Connect to the new database file (it will create the file if it doesn't exist)
conn = sqlite3.connect('taskmanager.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the 'tasks' table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0,
    due_date TEXT NOT NULL
);
''')

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Database and tasks table created successfully!")  