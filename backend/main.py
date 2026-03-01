from database import database
from RawData import RawData
from dotenv import load_dotenv
import os

# load environment variables stored in the `backend/env` file.  Using
# `dotenv` here means the rest of the code can simply rely on
# `os.getenv` without worrying about how the variables arrived.
load_dotenv(os.path.join(os.path.dirname(__file__), "env"))


def run_pipeline(reset_sequences: bool = False):
    db = database()
    aggregator = RawData()

    db.create_tables()

    if reset_sequences:
        # the user might delete rows directly from the database for testing
        # or cleanup.  SQLite's integer primary keys will keep counting up
        # even when rows are gone; calling ``reset_autoincrement`` rolls the
        # counter back to 0 so the next insert will start at 1 again.
        print("resetting autoincrement counters")
        db.reset_autoincrement("raw_news")
        db.reset_autoincrement("parsed_incidents")

    articles = aggregator.aggregate()
    print(f"Retrieved {len(articles)} articles.")

    for article in articles:
        news_id = db.insert_raw_news(article['source'], article)
        print(f"Saved to Cloud! News ID: {news_id}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="run the scraping/parsing pipeline")
    parser.add_argument(
        "--reset-seq",
        action="store_true",
        help="reset table ID counters before inserting anything",
    )
    args = parser.parse_args()

    run_pipeline(reset_sequences=args.reset_seq)
