import sqlite3

conn = sqlite3.connect('patterns.db')
cursor = conn.cursor()
with open('create_db.sql', 'r') as f:
    script = f.read()
cursor.executescript(script)
cursor.close()
conn.close()
