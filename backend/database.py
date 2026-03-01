import sqlitecloud
import json
from datetime import datetime
import os

class database():
    def __init__(self):
        # Attempt to load configuration from a dotenv file if present. The
        # repository ships with a simple `env` file that contains the
        # connection string, so we try to load it here. This keeps callers
        # like `main.py` relatively clean, but the file can also be loaded
        # from the entrypoint if preferred.
        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(__file__), "env"))

        # The code used to reference `SQLITE_CLOUD_URL` but the environment
        # we actually populate in `backend/env` uses `SQL_URL`.  Keep the
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

    def get_parsed_incidents_json(self):
        """Return all parsed incidents as a JSON-formatted string.

        Useful for APIs or frontend endpoints that need a serialized version
        of the data. This method simply calls :meth:`get_all_parsed_incidents`
        and dumps the resulting list of dictionaries.
        """
        data = self.get_all_parsed_incidents()
        return json.dumps(data)

    # ------------------------------------------------------------------
    # utility methods
    # ------------------------------------------------------------------
    def reset_autoincrement(self, table_name: str, vacuum: bool = False) -> None:
        """Reset the autoincrement counter for ``table_name``.

        SQLite keeps the last ROWID it issued in the internal
        ``sqlite_sequence`` table.  this method deletes that entry so the next
        ``INSERT`` will start at ``1`` (or ``MAX(id)+1`` if there are still
        rows present).

        :param table_name: name of the table whose sequence should be reset
        :param vacuum: if ``True`` run ``VACUUM`` after deleting the sequence.
                       ``VACUUM`` rebuilds the database file and also resets
                       the sequence, but it is a heavier operation and may
                       lock the file for a short time.
        :raises ValueError: if ``table_name`` is empty
        """
        if not table_name:
            raise ValueError("table_name must be provided")

        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM sqlite_sequence WHERE name = ?", (table_name,))
        conn.commit()
        if vacuum:
            # vacuum must be executed on a fresh connection in some versions of
            # sqlite; reuse the existing one to keep things simple.
            conn.execute("VACUUM")
            conn.commit()
        conn.close()

    def vacuum(self) -> None:
        """Run ``VACUUM`` on the current database.

        This is useful after large deletes to reclaim space and reset
        autoincrement sequences.  It locks the database while running, so it
        should only be used during maintenance windows or when the app is not
        under load.
        """
        conn = self.get_connection()
        conn.execute("VACUUM")
        conn.commit()
        conn.close()
