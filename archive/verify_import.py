import sqlite3
import os

db_path = 'matriculas.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM estudiantes')
    count = cursor.fetchone()[0]
    print(f"TOTAL_STUDENTS: {count}")
    conn.close()
else:
    print(f"Error: Database {db_path} not found")
