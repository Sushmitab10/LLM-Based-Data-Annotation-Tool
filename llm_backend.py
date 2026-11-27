import sqlite3
import os
import pandas as pd

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(
    title="LLM Based Data Annotation Tool",
    version="1.0"
)

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
)

def get_db():
    conn = sqlite3.connect("annotation_database.db")
    print("DATABASE PATH:", os.path.abspath("annotation_database.db"))

    conn.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            total_records INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS annotations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT,
            annotation TEXT,
            confidence REAL,
            dataset_id INTEGER
        )
    """)

    # Support an existing annotations table
    columns = [
        row[1] for row in
        conn.execute("PRAGMA table_info(annotations)")
    ]

    if "dataset_id" not in columns:
        conn.execute(
            "ALTER TABLE annotations ADD COLUMN dataset_id INTEGER"
        )

    conn.commit()
    return conn

class TextInput(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Backend is Running!"}

@app.post("/annotate")
def annotate(data: TextInput):
    result = classifier(data.text)[0]

    conn = get_db()
    conn.execute(
        "INSERT INTO annotations (input_text, annotation, confidence) VALUES (?, ?, ?)",
        (data.text, result["label"], float(result["score"]))
    )
    conn.commit()
    conn.close()

    return {
        "input_text": data.text,
        "annotation": result["label"],
        "confidence": result["score"]
    }

@app.get("/history")
def history():
    conn = get_db()
    rows = conn.execute("SELECT * FROM annotations").fetchall()
    conn.close()
    return {"total_records": len(rows), "history": rows}

@app.get("/statistics")
def statistics():
    conn = get_db()
    rows = conn.execute(
        "SELECT annotation, COUNT(*) FROM annotations GROUP BY annotation"
    ).fetchall()
    conn.close()
    return {"statistics": dict(rows)}

@app.put("/update/{annotation_id}")
def update(annotation_id: int, new_label: str):
    if new_label not in ["POSITIVE", "NEGATIVE"]:
        raise HTTPException(status_code=400, detail="Invalid label")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE annotations SET annotation = ? WHERE id = ?",
        (new_label, annotation_id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="ID not found")

    result = conn.execute(
        "SELECT annotation FROM annotations WHERE id = ?",
        (annotation_id,)
    ).fetchone()

    conn.close()

    return {
        "message": "Annotation updated successfully",
        "id": annotation_id,
        "updated_label": result[0]
    }
@app.delete("/delete/{annotation_id}")
def delete(annotation_id: int):
    conn = get_db()
    cursor = conn.execute(
        "DELETE FROM annotations WHERE id=?",
        (annotation_id,)
    )
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="ID not found")

    return {"message": "Annotation Deleted Successfully"}

@app.post("/annotate-csv")
async def annotate_csv(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid CSV file"
        )

    if "text" not in df.columns:
        raise HTTPException(
            status_code=400,
            detail="CSV needs a text column"
        )

    texts = df["text"].dropna().astype(str)

    conn = get_db()

    try:
        # Save dataset information
        cursor = conn.execute(
            """INSERT INTO datasets
            (filename, total_records)
            VALUES (?, ?)""",
            (file.filename, len(texts))
        )

        dataset_id = cursor.lastrowid

        results = []

        # Annotate each record
        for text in texts:
            result = classifier(text)[0]

            label = result["label"]
            score = float(result["score"])

            conn.execute(
                """INSERT INTO annotations
                (input_text, annotation, confidence, dataset_id)
                VALUES (?, ?, ?, ?)""",
                (text, label, score, dataset_id)
            )

            results.append({
                "text": text,
                "annotation": label,
                "confidence": score
            })

        conn.commit()

    except Exception:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail="Annotation failed"
        )

    finally:
        conn.close()

    return {
        "dataset_id": dataset_id,
        "filename": file.filename,
        "total_records": len(results),
        "results": results
    }


@app.get("/datasets")
def get_datasets():
    conn = get_db()

    rows = conn.execute("""
        SELECT
            d.id,
            d.filename,
            d.total_records,
            d.created_at,
            COUNT(a.id) AS annotated_records
        FROM datasets d
        LEFT JOIN annotations a
        ON d.id = a.dataset_id
        GROUP BY d.id
        ORDER BY d.id DESC
    """).fetchall()

    conn.close()

    return {
        "datasets": [
            {
                "id": row[0],
                "filename": row[1],
                "total_records": row[2],
                "created_at": row[3],
                "annotated_records": row[4],
                "pending_records": row[2] - row[4]
            }
            for row in rows
        ]
    }
if __name__ == "__main__":
    conn = get_db()
    conn.close()
    print("Project database initialized successfully!")