import json
from database import database
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
# -----------------------------
# AI Processor
# -----------------------------
class AIProcessor:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_KEY not found in .env file")

        self.client = genai.Client(api_key=api_key)

    def parse_article(self, article_dict):
        prompt = f"""
Extract crime incident details from this news article.

Example output:
{{"latitude": 40.7128, "longitude": -74.0060, "hour": 14, "incident_level": "High", "incident_type": "robbery", "description": "Armed robbery at corner store", "location_name": "5th Ave & 42nd St"}}

Instructions:
- latitude & longitude: If exact coordinates aren't mentioned, infer from location_name
- hour: Extract from timestamp if available, otherwise use 12 (noon) as default
- incident_level: Classify as "Low", "Med", or "High" based on severity
- incident_type: e.g., "robbery", "assault", "theft", "burglary", "homicide", "DUI"
- description: Concise summary of what happened (1 sentence)
- location_name: Specific city, street, building, or area name

ARTICLE DATA:
Title: {article_dict.get('title','')}
Link: {article_dict.get('link','')}
Published: {article_dict.get('published','')}

Return ONLY valid JSON with the structure shown in the example above.
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            text = response.text.strip()

            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()

            return json.loads(text)

        except Exception as e:
            print("AI parsing failed:", e)
            return None


# -----------------------------
# Main Pipeline
# -----------------------------
def run():
    db = database()
    processor = AIProcessor(self.api_key)

    conn = db.get_connection()
    cursor = conn.cursor()

    # Only fetch raw_news that have NOT been parsed yet
    cursor.execute("""
        SELECT r.id, r.raw_json
        FROM raw_news r
        LEFT JOIN parsed_incidents p
        ON r.id = p.raw_news_id
        WHERE p.raw_news_id IS NULL
    """)

    rows = cursor.fetchall()
    conn.close()

    print(f"Found {len(rows)} unparsed articles.\n")

    for raw_news_id, raw_json in rows:
        try:
            article = json.loads(raw_json)
        except:
            continue

        print("Processing:", article.get("title"))

        structured = processor.parse_article(article)
        if not structured:
            continue

        db.insert_parsed_incident(
            raw_news_id=raw_news_id,
            latitude=structured.get("latitude"),
            longitude=structured.get("longitude"),
            hour=structured.get("hour"),
            incident_level=structured.get("incident_level"),
            incident_type=structured.get("incident_type"),
            description=structured.get("description"),
            location_name=structured.get("location_name"),
        )

        print("Inserted.\n")

    print("Done.")


if __name__ == "__main__":
    run()