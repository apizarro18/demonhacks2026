import json
from database import database
from google import genai

# -----------------------------
# AI Processor
# -----------------------------
class AIProcessor:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def parse_article(self, article_dict):
        prompt = f"""
You are analyzing a crime news article.

ARTICLE DATA:
Title: {article_dict.get('title','')}
Link: {article_dict.get('link','')}
Published: {article_dict.get('published','')}

Your job:
1. Determine incident_type (shooting, homicide, DUI, robbery, etc.)
2. Determine incident_level (Low, Med, High)
3. Extract approximate hour (0-23) from publish time if possible
4. Extract location_name (city or neighborhood)
5. Estimate latitude and longitude if location is known
6. Write a short description (1 sentence)

Return ONLY valid JSON with these keys:
latitude,
longitude,
hour,
incident_level,
incident_type,
description,
location_name.
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
    processor = AIProcessor(api_key="AIzaSyBO9nJvsdOwaQSYDZGDKa5sKptVYzq0S14")

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