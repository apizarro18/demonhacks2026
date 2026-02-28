import feedparser
import re
import json
from datetime import datetime, timedelta, timezone
from dateutil import parser as dateparser

# ==============================
# CONFIG
# ==============================

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

# ==============================
# HELPERS
# ==============================

def is_recent(published_str):
    try:
        published_date = dateparser.parse(published_str)
        now = datetime.now(timezone.utc)
        return published_date >= now - timedelta(hours=HOURS_BACK)
    except:
        return False

def is_crime_related(text):
    return bool(CRIME_PATTERN.search(text))

def fetch_feed(url):
    return feedparser.parse(url)

# ==============================
# MAIN AGGREGATOR
# ==============================

def aggregate_crime_news():
    seen_links = set()
    results = []

    for source, url in FEEDS.items():
        print(f"Fetching from {source}...")

        feed = fetch_feed(url)

        for entry in feed.entries:

            title = entry.title
            summary = getattr(entry, "summary", "")
            link = entry.link
            published = getattr(entry, "published", "")

            text = f"{title} {summary}"

            if link in seen_links:
                continue

            if not is_crime_related(text):
                continue

            if not published or not is_recent(published):
                continue

            seen_links.add(link)

            results.append({
                "source": source,
                "title": title,
                "link": link,
                "published": published
            })

    return results

# ==============================
# ENTRY POINT
# ==============================

def main():
    articles = aggregate_crime_news()

    print("\n========== FINAL RESULTS ==========")
    print(json.dumps(articles, indent=2))

if __name__ == "__main__":
    main()