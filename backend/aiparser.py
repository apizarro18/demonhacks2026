import json
from database import database # Your class from earlier

# You'll need an LLM library (e.g., 'google-generativeai' or 'openai')
import google.generativeai as genai 

class AIProcessor:
    def __init__(self, api_key):
        genai.configure(api_key=AIzaSyBO9nJvsdOwaQSYDZGDKa5sKptVYzq0S14)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def parse_article(self, raw_text):
        prompt = f"""
        Extract the following crime incident details from this text:
        {raw_text}
        
        Return ONLY a JSON object with these keys: 
        latitude, longitude, hour (0-23), incident_level (Low/Med/High), 
        incident_type, description, location_name.
        """
        response = self.model.generate_content(prompt)
        # Convert AI string response back to a Python Dictionary
        return json.loads(response.text.strip('`json\n '))

# --- THE WORKFLOW ---
db = database()
processor = AIProcessor(api_key="AIzaSyBO9nJvsdOwaQSYDZGDKa5sKptVYzq0S14")

# 1. Get a raw article that hasn't been parsed yet
# (You might need to add a 'SELECT' method to your database class)
raw_articles = db.get_unparsed_news() 

for news in raw_articles:
    # news[0] is ID, news[2] is the raw_json text
    data = processor.parse_article(news[2])
    
    # 2. Fill the parsed_incidents table
    db.insert_parsed_incident(
        raw_news_id=news[0],
        latitude=data['latitude'],
        longitude=data['longitude'],
        hour=data['hour'],
        incident_level=data['incident_level'],
        incident_type=data['incident_type'],
        description=data['description'],
        location_name=data['location_name']
    )