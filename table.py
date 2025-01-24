import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect('complaints.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            description TEXT NOT NULL,
            image BLOB,
            location TEXT NOT NULL,  -- Added location column
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
    ''')
    conn.close()

def submit_complaint(subject, description, image, location, latitude, longitude):
    conn = sqlite3.connect('complaints.db')
    conn.execute('INSERT INTO complaints (subject, description, image, location, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)',
                 (subject, description, image, location, latitude, longitude))
    conn.commit()
    conn.close()

def fetch_complaints():
    conn = sqlite3.connect('complaints.db')
    df = pd.read_sql_query('SELECT * FROM complaints', conn)
    conn.close()
    return df

def recreate_db():
    conn = sqlite3.connect('complaints.db')
    conn.execute('DROP TABLE IF EXISTS complaints;')  # Drop the table if it exists
    conn.execute('''
        CREATE TABLE complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            description TEXT NOT NULL,
            image BLOB,
            location TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
    ''')
    conn.close()