import sqlitecloud
import json
from datetime import datetime
import os

class database():
    def __init__(self):
        self.connection_string = os.getenv("SQL_URL")

    def get_connection(self):
        if not self.connection_string:
            raise ValueError("SQLITE_CLOUD_URL not found in .env")
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

        conn.commit() 
        conn.close()

    def insert_raw_news(self, source, raw_json):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Pass a single tuple, not a list
        params = (source, json.dumps(raw_json))
        cursor.execute("INSERT INTO raw_news (source, raw_json) VALUES (?, ?)", params)
        
        news_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return news_id

    def insert_parsed_incident(self, raw_news_id, latitude, longitude, hour, incident_level, incident_type, description, location_name):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        params = (raw_news_id, latitude, longitude, hour, incident_level, incident_type, description, location_name)
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
        
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results

    def get_unparsed_news(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT rn.id, rn.source, rn.raw_json, rn.fetched_at
            FROM raw_news rn
            WHERE rn.id NOT IN (
                SELECT DISTINCT raw_news_id FROM parsed_incidents
            )
        """)
        
        results = cursor.fetchall()
        conn.close()
        return results