
import sqlite3

conn = sqlite3.connect("annotation_database.db")
cursor = conn.cursor()

for table in ["datasets", "annotations"]:
    print(f"\nTable: {table}")

    cursor.execute(f"PRAGMA table_info({table})")

    columns = cursor.fetchall()

    for column in columns:
        print("Column:", column[1], "| Type:", column[2])

conn.close()


