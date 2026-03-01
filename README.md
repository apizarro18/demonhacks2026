# SafeBlue DePaul

A real-time neighborhood safety dashboard for Chicago. The app scrapes crime news from local RSS feeds, parses articles through Google Gemini to extract structured incident data (location, severity, type), stores everything in SQLite Cloud, and displays results on an interactive map.

## How It Works

```
RSS Feeds (7 sources)
        │
        ▼
  RawData.py ── filters by keywords & recency (24h)
        │
        ▼
  raw_news table (SQLite Cloud)
        │
        ▼
  aiparser.py ── sends to Google Gemini 2.5 Flash
        │
        ▼
  parsed_incidents table (structured JSON)
        │
        ▼
  Flask API ── serves incidents as JSON
        │
        ▼
  React + Leaflet map
```

## Tech Stack

| Layer    | Tech                                  |
|----------|---------------------------------------|
| Frontend | React 19, Leaflet, React-Leaflet      |
| Backend  | Flask, Flask-CORS                     |
| Database | SQLite Cloud                          |
| AI       | Google Gemini 2.5 Flash               |
| Data     | RSS feeds via feedparser              |

## News Sources

| Source                     | Feed                                                  |
|----------------------------|-------------------------------------------------------|
| ABC7 Chicago               | `abc7chicago.com/feed/?section=news/crime`            |
| WGN9                       | `wgntv.com/category/news/crime/feed/`                 |
| FOX32 Chicago              | `fox32chicago.com/category/news/crime/rss`            |
| CWB Chicago                | `cwbchicago.com/feed/`                                |
| Block Club Chicago         | `blockclubchicago.org/feed/`                          |
| Sun-Times Crime            | `chicago.suntimes.com/rss/crime/index.xml`            |
| Google News Chicago Crime  | `news.google.com/rss/search?q=Chicago+crime`         |

Articles are filtered to the last 24 hours and must match crime-related keywords (shooting, robbery, assault, etc.).

## Database Schema

### `raw_news`
| Column     | Type      | Description               |
|------------|-----------|---------------------------|
| id         | INTEGER   | Primary key (autoincrement)|
| source     | TEXT      | News source name          |
| raw_json   | TEXT      | Full article data as JSON |
| fetched_at | TIMESTAMP | When it was fetched       |

### `parsed_incidents`
| Column         | Type      | Description                     |
|----------------|-----------|---------------------------------|
| id             | INTEGER   | Primary key (autoincrement)     |
| raw_news_id    | INTEGER   | FK -> raw_news.id               |
| latitude       | REAL      | Incident latitude               |
| longitude      | REAL      | Incident longitude              |
| hour           | INTEGER   | Hour of day (0-23)              |
| incident_level | TEXT      | Severity: Low, Med, High        |
| incident_type  | TEXT      | Category (robbery, assault, etc)|
| description    | TEXT      | LLM-generated summary           |
| location_name  | TEXT      | Neighborhood or address         |
| parsed_at      | TIMESTAMP | When the LLM parsed it          |

## Project Structure

```
demonhacks2026/
├── backend/
│   ├── main.py            # Pipeline entry point — fetches news & stores in DB
│   ├── RawData.py         # RSS feed scraper/aggregator (7 Chicago sources)
│   ├── aiparser.py        # Google Gemini parser — extracts structured incident data
│   ├── database.py        # SQLite Cloud connection & table management
│   ├── app.py             # Flask API server
│   ├── requirements.txt   # Python dependencies
│   └── .env.example       # Environment variable template
├── frontend/
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.js
│       └── components/
│           ├── Map.js           # Leaflet map with incident markers
│           ├── NewsFeed.js      # List of recent incidents
│           └── IncidentForm.js  # User-submitted reports
└── README.md
```

## Getting Started

### Backend
```bash
cd backend
pip install -r requirements.txt
```

Create a file called `env` (or `.env`) in the `backend/` folder with:
```
SQL_URL=sqlitecloud://<user>:<pass>@<host>:<port>/<database>
GEMINI_KEY=<your-google-gemini-api-key>
```

Run the pipeline:
```bash
# 1. Create database tables
python database.py

# 2. Scrape news and store raw articles
python main.py

# 3. Parse articles with Gemini (processes in batches of 5)
python aiparser.py

# 4. Start the API server
python app.py         # Flask on http://localhost:5000
```

### Frontend
```bash
cd frontend
npm install
npm start             # React on http://localhost:3000
```

## Resetting ID Counters

If you delete rows and want IDs to start fresh, clear both tables and reset the sequences:

```python
from database import database
db = database()

# delete in order (parsed_incidents first due to foreign key)
conn = db.get_connection()
cursor = conn.cursor()
cursor.execute('DELETE FROM parsed_incidents')
cursor.execute('DELETE FROM raw_news')
conn.commit()
conn.close()

db.reset_table_sequence('parsed_incidents')
db.reset_table_sequence('raw_news')
```
