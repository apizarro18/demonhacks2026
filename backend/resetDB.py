import sqlite3
import os

def create_local_db():
    db_filename = "incidents.db"
    
    # If the file already exists, delete it so we start fresh
    if os.path.exists(db_filename):
        os.remove(db_filename)
        print(f"Removed old {db_filename}")

    # This creates the physical file in your Explorer
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    print(f"Creating tables in {db_filename}...")

    # 1. Create raw_news table
    cursor.execute("""
        CREATE TABLE raw_news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            raw_json TEXT,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. Create parsed_incidents table (with time as TEXT)
    cursor.execute("""
        CREATE TABLE parsed_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_news_id INTEGER,
            latitude REAL,
            longitude REAL,
            time TEXT,
            incident_level TEXT,
            incident_type TEXT,
            description TEXT,
            location_name TEXT,
            parsed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (raw_news_id) REFERENCES raw_news(id)
        )
    """)

    conn.commit()
    conn.close()
    print(f"Success! '{db_filename}' is now in your folder. You can upload this to SQLite Cloud.")

if __name__ == "__main__":
    create_local_db()