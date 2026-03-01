from database import database
from RawData import RawData
from dotenv import load_dotenv
import os

# load environment variables stored in the `backend/env` file.  Using
# `dotenv` here means the rest of the code can simply rely on
# `os.getenv` without worrying about how the variables arrived.
load_dotenv(os.path.join(os.path.dirname(__file__), "env"))


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