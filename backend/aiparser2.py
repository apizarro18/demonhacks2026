import google.generativeai as genai
import json
from database import database # Your class

class SafetyAgent:
    def __init__(self, api_key="AIzaSyBO9nJvsdOwaQSYDZGDKa5sKptVYzq0S14"):
        genai.configure(api_key="AIzaSyBO9nJvsdOwaQSYDZGDKa5sKptVYzq0S14")
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.db = database()

    def process_pending_news(self):
        # 1. Get raw news from DB
        # You'll need a method to get news that isn't in parsed_incidents yet
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # We look for news IDs that don't exist in the parsed table yet
        cursor.execute("""
            SELECT id, raw_json FROM raw_news 
            WHERE id NOT IN (SELECT raw_news_id FROM parsed_incidents)
            ORDER BY id ASC LIMIT 5
        """)
        
        pending = cursor.fetchall()
        
        for row in pending:
            news_id = row[0]
            # row[1] is the JSON string your teammate saved
            raw_data = json.loads(row[1]) 
            text_to_analyze = f"Title: {raw_data['title']} Summary: {raw_data.get('summary', '')}"

            print(f"AI is analyzing News ID {news_id}...")
            
            # 2. Ask Gemini to structure the data
            parsed_data = self.ask_ai(text_to_analyze)

            # 3. Save to your parsed_incidents table
            if parsed_data:
                self.db.insert_parsed_incident(
                    news_id,
                    parsed_data['latitude'],
                    parsed_data['longitude'],
                    parsed_data['hour'],
                    parsed_data['incident_level'],
                    parsed_data['incident_type'],
                    parsed_data['description'],
                    parsed_data['location_name']
                )

    def ask_ai(self, text):
        prompt = f"""
        Analyze this Chicago crime report: {text}
        Return ONLY a JSON object with:
        "latitude": (float), "longitude": (float), "hour": (int 0-23),
        "incident_level": "Low" | "Medium" | "High",
        "incident_type": (short category), "description": (1 sentence),
        "location_name": (street or neighborhood)
        
        If coordinates aren't clear, provide the best estimate in Chicago.
        """
        try:
            response = self.model.generate_content(prompt)
            # Clean up the AI response in case it wraps it in markdown ```json
            clean_json = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_json)
        except Exception as e:
            print(f"AI Error: {e}")
            return None

# To run it:
# agent = SafetyAgent("YOUR_GEMINI_API_KEY")
# agent.process_pending_news()