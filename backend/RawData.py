import feedparser
import re
import json
from datetime import datetime, timedelta, timezone
from dateutil import parser as dateparser

class RawData:
    FEEDS = {
        "ABC7 Chicago": "https://abc7chicago.com/feed/?section=news/crime",
        "WGN9": "https://wgntv.com/category/news/crime/feed/",
        "FOX32 Chicago": "https://www.fox32chicago.com/category/news/crime/rss",
        "Google News Chicago Crime": "https://news.google.com/rss/search?q=Chicago+crime"
    }

    CRIME_PATTERN = re.compile(
        r"\b(shooting|homicide|murder|arrest|charged|police|robbery|assault|dui|burglary|stabbed|gun|crime|carjacking)\b",
        re.IGNORECASE
    )

    HOURS_BACK = 24

    def __init__(self):
        self.seen_links = set()
        self.articles = []

    # ----------------------
    # Helper Methods
    # ----------------------
    @staticmethod
    def is_recent(published_str):
        try:
            published_date = dateparser.parse(published_str)
            now = datetime.now(timezone.utc)
            return published_date >= now - timedelta(hours=RawData.HOURS_BACK)
        except:
            return False

    @staticmethod
    def is_crime_related(text):
        return bool(RawData.CRIME_PATTERN.search(text))

    @staticmethod
    def fetch_feed(url):
        return feedparser.parse(url)

    # ----------------------
    # Main Aggregation
    # ----------------------
    def aggregate(self):
        for source, url in self.FEEDS.items():
            print(f"Fetching from {source}...")
            feed = self.fetch_feed(url)

            for entry in feed.entries:
                title = entry.title
                summary = getattr(entry, "summary", "")
                link = entry.link
                published = getattr(entry, "published", "")

                text = f"{title} {summary}"

                if link in self.seen_links:
                    continue
                if not self.is_crime_related(text):
                    continue
                if not published or not self.is_recent(published):
                    continue

                self.seen_links.add(link)

                self.articles.append({
                    "source": source,
                    "title": title,
                    "link": link,
                    "published": published
                })

        return self.articles

    # ----------------------
    # Output Method
    # ----------------------
    def to_json(self):
        return json.dumps(self.articles, indent=2)

# ----------------------
# Entry Point
# ----------------------
if __name__ == "__main__":
    aggregator = RawData()
    aggregator.aggregate()
    print("\n========== FINAL RESULTS ==========")
    print(aggregator.to_json())