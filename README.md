# SafeBlue API
<img width="1915" height="847" alt="image" src="https://github.com/user-attachments/assets/3ce2ca44-a95d-4187-b2ae-7bc5794df5d5" />

A real-time Chicago Loop safety database with a dashboard for Chicago University Students. The app scrapes crime news from local RSS feeds, parses articles through Google Gemini to extract structured incident data (location, severity, type), stores everything in SQLite Cloud, and displays results on an interactive map.

##Map with realtime crime incidents and heat map
<img width="1916" height="875" alt="image" src="https://github.com/user-attachments/assets/62580029-f74f-4821-971e-240122d59eaf" />
##Campus Designation
<img width="1372" height="872" alt="image" src="https://github.com/user-attachments/assets/31636a21-afcd-4409-b53c-85928874f4a9" />
##Settings
<img width="1907" height="875" alt="image" src="https://github.com/user-attachments/assets/98d6334f-2f47-4182-89aa-ba3ce5d55acf" />



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
│   ├── app.py             # Flask API server (GET /alerts)
│   ├── requirements.txt   # Python dependencies
│   └── .env.example       # Environment variable template
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── OneSignalSDKWorker.js  # Push notification service worker
│   └── src/
│       ├── App.js              # Router — splash, map, feed, settings
│       ├── pages/
│       │   ├── Map.js          # Leaflet map with campus polygons & incident markers
│       │   ├── Feed.js         # Live alert feed sidebar
│       │   ├── Settings.js     # Push notification subscription (OneSignal)
│       │   └── SplashPage.js   # Animated loading screen
│       └── css/
│           └── Map.css         # Map and campus label styles
└── README.md
```

## Getting Started

### Backend
```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` folder with:
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

## API Documentation

### `GET /alerts`

Returns all parsed safety incidents as a JSON array. Falls back to sample data if the database is unreachable or empty.

**URL:** `http://localhost:5000/alerts`

**Response:** `200 OK` — `application/json`

```json
[
  {
    "id": 1,
    "lat": 41.8781,
    "lng": -87.6298,
    "type": "Robbery",
    "severity": 3,
    "message": "Armed robbery reported near State St and Jackson Blvd.",
    "timestamp": "2026-02-28T14:30:00Z"
  }
]
```

**Response fields:**

| Field       | Type    | Description                                          |
|-------------|---------|------------------------------------------------------|
| `id`        | integer | Unique incident ID                                   |
| `lat`       | float   | Latitude                                             |
| `lng`       | float   | Longitude                                            |
| `type`      | string  | Incident category in title case (e.g. "Robbery", "Assault") |
| `severity`  | integer | 1 (Low), 3 (Medium), 5 (High)                       |
| `message`   | string  | AI-generated incident summary                        |
| `timestamp` | string  | ISO 8601 datetime (UTC)                              |

**Behavior:**
- Queries `parsed_incidents` from SQLite Cloud and transforms DB fields to the frontend schema
- If the database returns no rows or the connection fails, the endpoint returns hardcoded fallback alerts so the frontend always has data to render

---

## Deployment

### Prerequisites

- Python 3.10+
- Node.js 18+
- A [SQLite Cloud](https://sqlitecloud.io) database
- A [Google Gemini API key](https://aistudio.google.com/apikey)

### Environment Variables

**Backend** — create `backend/.env`:
```
SQL_URL=sqlitecloud://<user>:<pass>@<host>:<port>/<database>
GEMINI_KEY=<your-google-gemini-api-key>
```

**Frontend** — create `frontend/.env`:
```
REACT_APP_SQL_URL=sqlitecloud://<user>:<pass>@<host>:<port>/<database>
```

### Deploy the Backend (Render / Railway / any VPS)

1. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Initialize the database tables:
   ```bash
   python database.py
   ```

3. Run the data pipeline (fetch + parse):
   ```bash
   python main.py        # Scrape RSS feeds → raw_news table
   python aiparser.py    # Parse with Gemini → parsed_incidents table
   ```

4. Start the API server:
   ```bash
   # Development
   python app.py

   # Production (with gunicorn)
   pip install gunicorn
   gunicorn app:app --bind 0.0.0.0:5000
   ```

### Deploy the Frontend (Vercel / Netlify)

1. Build the production bundle:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. The `build/` folder contains static files ready to deploy. Point your hosting provider at this directory.

3. Set the environment variable `REACT_APP_SQL_URL` in your hosting provider's dashboard.

4. If deploying to a different domain than the backend, update the fetch URL in `Feed.js` to point to your deployed backend (e.g. `https://your-api.onrender.com/alerts`).

### Example: Render (Backend)

| Setting       | Value                          |
|---------------|--------------------------------|
| Build command | `pip install -r requirements.txt` |
| Start command | `gunicorn app:app --bind 0.0.0.0:$PORT` |
| Environment   | Set `SQL_URL` and `GEMINI_KEY` |

### Example: Vercel (Frontend)

| Setting         | Value                            |
|-----------------|----------------------------------|
| Framework       | Create React App                 |
| Build command   | `npm run build`                  |
| Output directory| `build`                          |
| Environment     | Set `REACT_APP_SQL_URL`          |

---

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
