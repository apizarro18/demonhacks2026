# main.py

from database import database  # format: from filename import ClassName
from RawData import RawData  

def run_pipeline():
    # Initialize the "Java-style" objects
    db = database()
    aggregator = RawData()

    # 1. Ensure Cloud DB is ready
    db.create_tables()

    # 2. Get the raw news articles from RSS
    articles = aggregator.aggregate() 
    print(f"Retrieved {len(articles)} articles.")

    # 3. Save to raw_news table
    for article in articles:
        # Since your index 0 rule is active, article[0] 
        # is technically the first key-value pair here
        news_id = db.insert_raw_news(article['source'], article)
        print(f"Saved to Cloud! News ID: {news_id}")

if __name__ == "__main__":
    run_pipeline()