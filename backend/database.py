# Database setup and helpers (SQLite)
import sqlite3
import json
from datetime import datetime
import sqlitecloud

DB_NAME = "incidents.db"

class database():
    def __init__(self):
        self.connection_string = "sqlitecloud://ctdsjulovk.g5.sqlite.cloud:8860/incidents.db?apikey=hwbtOOtrpqCjTa1MYk4Vk05V9nlwRjGpIwsWBh6gY0M"

    def get_connection(self):
        return sqlitecloud.connect(self.connection_string)             

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS raw_news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                raw_json TEXT,
                fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS parsed_incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                raw_news_id INTEGER,
                latitude REAL,
                longitude REAL,
                hour INTEGER,
                incident_level TEXT,
                incident_type TEXT,
                description TEXT,
                location_name TEXT,
                parsed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (raw_news_id) REFERENCES raw_news(id)
            )
        """)
        # sqlitecloud usually auto-commits, but this ensures it's saved
        conn.commit() 
        conn.close()

    def insert_raw_news(self, source, raw_json):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Wrapping in a list of tuples: [(val1, val2)]
        params = [(source, json.dumps(raw_json))]
        
        cursor.execute("INSERT INTO raw_news (source, raw_json) VALUES (?, ?)", params)
        
        news_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return news_id

    def insert_parsed_incident(self, raw_news_id, latitude, longitude, hour, incident_level, incident_type, description, location_name):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # The 8 parameters for your incident
        params = [(raw_news_id, latitude, longitude, hour, incident_level, incident_type, description, location_name)]
        
        cursor.execute("""
            INSERT INTO parsed_incidents (raw_news_id, latitude, longitude, hour, incident_level, incident_type, description, location_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, params)
        
        conn.commit()
        conn.close()

    def get_all_parsed_incidents(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM parsed_incidents")
        
        # Mapping to dictionaries so your team doesn't struggle with index numbers
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results