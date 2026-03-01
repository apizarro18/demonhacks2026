import json
from database import database
from google import genai
from dotenv import load_dotenv
import os
import time

load_dotenv()

# -----------------------------
# AI Processor
# -----------------------------
class AIProcessor:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_KEY not found in .env file")
        self.client = genai.Client(api_key=self.api_key)

    def parse_article(self, article_dict):
        prompt = f"""
Extract crime incident details from this news article.

Example output:
{{"latitude": 40.7128, "longitude": -74.0060, "time": "10:30 PM", "incident_level": "High", "incident_type": "robbery", "description": "Armed robbery at corner store", "location_name": "5th Ave & 42nd St"}}

Instructions:
- if duplicate incidents are mentioned from different new sources, only create one entry for that incident, using the most specific location and time details available across all sources.
- latitude & longitude: If exact coordinates aren't mentioned, infer from location_name
- time: Extract the US Central timestamp of the reported crime from the article. If not available, use the time of the article being published. If not, infer a time.
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
    processor = AIProcessor()

    conn = db.get_connection()
    cursor = conn.cursor()

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

    batch_size = 5
    total = len(rows)

    for i in range(0, total, batch_size):
        batch = rows[i:i+batch_size]
        batch_start_time = time.time()
        print(f"Processing batch {i//batch_size + 1}\n")

        for raw_news_id, raw_json in batch:
            try:
                article = json.loads(raw_json)
            except:
                continue

            print("Processing:", article.get("title"))
            structured = processor.parse_article(article)
            if not structured:
                continue

            if isinstance(structured, list):
                if not structured:
                    continue
                structured = structured[0]

            if not isinstance(structured, dict):
                print("Invalid AI format returned. Skipping.")
                continue

            db.insert_parsed_incident(
                raw_news_id=raw_news_id,
                latitude=structured.get("latitude"),
                longitude=structured.get("longitude"),
                time=structured.get("time"),
                incident_level=structured.get("incident_level"),
                incident_type=structured.get("incident_type"),
                description=structured.get("description"),
                location_name=structured.get("location_name"),
            )
            print("Inserted.\n")

        # Prompt user for next batch if there are more
        if i + batch_size < total:
            while True:
                user_input = input("Processed 5 articles. Continue next 5? (yes/quit): ").strip().lower()
                if user_input == "yes":
                    elapsed = time.time() - batch_start_time
                    if elapsed < 60:
                        wait_time = 60 - elapsed
                        print(f"Waiting {int(wait_time)} seconds to respect rate limit...")
                        time.sleep(wait_time)
                    break
                elif user_input == "quit":
                    print("Exiting parser safely.")
                    return
                else:
                    print("Please type 'yes' to continue or 'quit' to exit.")

    print("Done.")


if __name__ == "__main__":
    run()