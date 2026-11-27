
import sqlite3

conn = sqlite3.connect("annotation_database.db")
cursor = conn.cursor()

try:
    # CREATE: Insert a test annotation
    cursor.execute("""
        INSERT INTO annotations
        (input_text, annotation, confidence)
        VALUES (?, ?, ?)
    """, ("Database testing sample", "POSITIVE", 0.98))

    annotation_id = cursor.lastrowid
    conn.commit()

    print("CREATE: Record inserted successfully!")

    # READ: Retrieve the inserted record
    cursor.execute(
        "SELECT * FROM annotations WHERE id = ?",
        (annotation_id,)
    )

    record = cursor.fetchone()
    print("READ:", record)

    # UPDATE: Change the annotation
    cursor.execute("""
        UPDATE annotations
        SET annotation = ?
        WHERE id = ?
    """, ("NEGATIVE", annotation_id))

    conn.commit()
    print("UPDATE: Record updated successfully!")

    # DELETE: Remove the test record
    cursor.execute(
        "DELETE FROM annotations WHERE id = ?",
        (annotation_id,)
    )

    conn.commit()
    print("DELETE: Record deleted successfully!")

except Exception as e:
    conn.rollback()
    print("Database testing error:", e)

finally:
    conn.close()
