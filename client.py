import hashlib
import requests
import sqlite3
import os
from dotenv import load_dotenv

def get_current_counter():
    conn = sqlite3.connect('remote.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS remote (id INTEGER PRIMARY KEY, counter INTEGER)")
    cursor.execute("SELECT counter FROM remote WHERE id = 1")
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO remote (id, counter) VALUES (1, 0)")
        conn.commit()
        return 0
    conn.close()
    return result[0]

def update_counter(new_counter):
    conn = sqlite3.connect('remote.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE remote SET counter = ? WHERE id = 1", (new_counter,))
    conn.commit()
    conn.close()

def generate_code():
    seed = os.getenv('SECRET_KEY')
    counter = get_current_counter()
    counter += 1
    update_counter(counter)
    return hashlib.sha256(f"{seed}{counter}".encode()).hexdigest()

def authenticate():
    code = generate_code()
    response = requests.post("http://localhost:8000/auth", json={"code": code})
    if response.status_code == 200:
        print("Successfully authenticated")
    else:
        print("Authentication Failed", response.status_code, response.text)

if __name__ == "__main__":
    load_dotenv()
    authenticate()
