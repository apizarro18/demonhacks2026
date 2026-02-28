# Database setup and helpers (SQLite)
import sqlite3
import json
from datetime import datetime
import sqlitecloud

DB_NAME = "incidents.db"

def get_connection():
    conn = sqlitecloud.connect("sqlitecloud://ctdsjulovk.g5.sqlite.cloud:8860/incidents.db?apikey=hwbtOOtrpqCjTa1MYk4Vk05V9nlwRjGpIwsWBh6gY0M")
    return conn                       

def create_tables():
    conn = get_connection()
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

def insert_raw_news(source, raw_json):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO raw_news (source, raw_json) VALUES (?, ?)
    """, (source, json.dumps(raw_json)))
    conn.commit()
    news_id = cursor.lastrowid
    conn.close()
    return news_id

def insert_parsed_incident(raw_news_id, latitude, longitude, hour, incident_level, incident_type, description, location_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO parsed_incidents (raw_news_id, latitude, longitude, hour, incident_level, incident_type, description, location_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (raw_news_id, latitude, longitude, hour, incident_level, incident_type, description, location_name))
    conn.commit()
    conn.close()

def get_all_parsed_incidents():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parsed_incidents")
    incidents = cursor.fetchall()
    conn.close()
    return incidents

create_tables()

