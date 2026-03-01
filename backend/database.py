import sqlitecloud
import json
from datetime import datetime
import os

class database():
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()

        # The code used to reference `SQLITE_CLOUD_URL` but the environment
        # we actually populate in `backend/.env` uses `SQL_URL`.  Keep the
        # variable name consistent for clarity.
        self.connection_string = os.getenv("SQL_URL")

    def get_connection(self):
        if not self.connection_string:
            raise ValueError("SQL_URL not found in environment")
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

    #----------------------------------------------------------------------
    # utility helpers
    #----------------------------------------------------------------------
    def reset_table_sequence(self, table_name: str) -> None:
        """Reset the AUTOINCREMENT counter for *table_name*.

        SQLite keeps the last used integer key in the hidden
        ``sqlite_sequence`` table; deleting rows does not change that value,
        which is why gaps appear after manual deletions.  This helper removes
        the entry for the named table so that the next ``INSERT`` will start
        again at ``1`` (or ``MAX(rowid)+1`` if rows remain).

        Usage::

            db = database()
            db.reset_table_sequence('raw_news')
            # optionally call `VACUUM` afterwards to reclaim space

        The method is idempotent and safe to call even if the table has never
        been populated.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM sqlite_sequence WHERE name = ?",
            (table_name,),
        )
        conn.commit()
        conn.close()

    def insert_raw_news(self, source, raw_json):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Pass a single tuple, not a list
        params = (source, json.dumps(raw_json))
        cursor.execute("INSERT INTO raw_news (source, raw_json) VALUES (?, ?) RETURNING id", params)
        news_id = cursor.fetchone()[0]
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

    def get_parsed_incidents_json(self):
        """Return all parsed incidents as a JSON-formatted string.

        Useful for APIs or frontend endpoints that need a serialized version
        of the data. This method simply calls :meth:`get_all_parsed_incidents`
        and dumps the resulting list of dictionaries.
        """
        data = self.get_all_parsed_incidents()
        return json.dumps(data)
