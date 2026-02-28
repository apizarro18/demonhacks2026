# main.py

from database import database  
from RawData import RawData  

def run_pipeline():
    db = database()
    aggregator = RawData()

    db.create_tables()

    articles = aggregator.aggregate() 
    print(f"Retrieved {len(articles)} articles.")

    for article in articles:
        news_id = db.insert_raw_news(article['source'], article)
        print(f"Saved to Cloud! News ID: {news_id}")

if __name__ == "__main__":
    run_pipeline()