from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import hashlib
import sqlite3

app = FastAPI()

class Code(BaseModel):
    code: str

def initialize_database():
    conn = sqlite3.connect('opener.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS opener (id INTEGER PRIMARY KEY, counter INTEGER)")
    cursor.execute("SELECT counter FROM opener WHERE id = 1")
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO opener (id, counter) VALUES (1, 0)")
        conn.commit()
    conn.close()

def get_current_counter():
    conn = sqlite3.connect('opener.db')
    cursor = conn.cursor()
    cursor.execute("SELECT counter FROM opener WHERE id = 1")
    result = cursor.fetchone()
    conn.close()
    return result[0]

def update_counter(new_counter):
    conn = sqlite3.connect('opener.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE opener SET counter = ? WHERE id = 1", (new_counter,))
    conn.commit()
    conn.close()

@app.on_event("startup")
async def startup_event():
    initialize_database()

@app.post("/auth")
def open_door(code_data: Code):
    seed = os.getenv('SECRET_KEY')
    tolerance = 5
    current_counter = get_current_counter()
    for i in range(tolerance):
        expected_code = hashlib.sha256(f"{seed}{current_counter + i + 1}".encode()).hexdigest()
        if code_data.code == expected_code:
            update_counter(current_counter + i + 1)
            return {"status": "Authenticated"}

    raise HTTPException(status_code=400, detail="Invalid code")

if __name__ == "__main__":
    load_dotenv()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)