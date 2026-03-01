# SafeBlue DePaul

A real-time neighborhood safety dashboard for DePaul. The app scrapes crime and incident data from news websites, converts it to structured JSON, feeds it through an LLM to extract key details (location, severity, type, etc), stores the results in a database, and displays them on an interactive map.

## How It Works

```
News Websites ──> Scrape/Fetch raw articles ──> Store in raw_news table
                                                       │
                                                       ▼
                                              Send to SQLite-AI for parsing (LLM runs inside DB via SQL)
                                                       │
                                                       ▼
                                              LLM extracts structured data:
                                              - lat/lng coordinates
                                              - incident type
                                              - severity level
                                              - description
                                                       │
                                                       ▼
                                              Store in parsed_incidents table
                                                       │
                                                       ▼
                                              Frontend fetches via API
                                                       │
                                                       ▼
                                              Display on Leaflet map
```

## Tech Stack

| Layer    | Tech                             |
|----------|----------------------------------|
| Frontend | React 19, Leaflet, React-Leaflet |
| Backend  | Flask                |
| Database | SQLite (`incidents.db`)          |
| Data     | news scraping          |

## Database Schema

### `raw_news` — raw scraped/fetched articles
| Column     | Type      | Description                      |
|------------|-----------|----------------------------------|
| id         | INTEGER   | Primary key                      |
| source     | TEXT      | News source name                 |
| raw_json   | TEXT      | Full article data as JSON        |
| fetched_at | TIMESTAMP | When it was fetched              |

### `parsed_incidents` — LLM-extracted structured data
| Column         | Type      | Description                        |
|----------------|-----------|------------------------------------|
| id             | INTEGER   | Primary key                        |
| raw_news_id    | INTEGER   | FK → raw_news                      |
| latitude       | REAL      | Incident latitude                  |
| longitude      | REAL      | Incident longitude                 |
| hour           | INTEGER   | Hour of day (0-23)                 |
| incident_level | TEXT      | Severity (low, medium, high)       |
| incident_type  | TEXT      | Category (theft, assault, etc.)    |
| description    | TEXT      | LLM-generated summary              |
| location_name  | TEXT      | Neighborhood or address            |
| parsed_at      | TIMESTAMP | When the LLM parsed it             |

## Project Structure

```
demonhacks2026/
├── backend/
│   ├── app.py              # Flask API server
│   ├── database.py         # SQLite tables & helper functions
│   ├── news.py             # News fetching logic
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── components/
│   │       ├── Map.js           # Leaflet map with incident markers
│   │       ├── NewsFeed.js      # List of recent incidents
│   │       └── IncidentForm.js  # User-submitted reports
└── README.md
```

## Getting Started

### Backend
```bash
cd backend
pip install -r requirements.txt

# The connection string is read from the environment variable
# `SQL_URL`. A sample value is stored in the `backend/env` file, and the
# code automatically loads it using `python-dotenv`. You can instead set
# the variable yourself or rename `env` to `.env` if you prefer.

python database.py    # creates incidents.db (will load `SQL_URL`)

# the scraper script understands a `--reset-seq` flag that wipes the
# autoincrement counters for both tables.  run this if you deleted rows by
# hand and want new IDs to start back at 1:
#
#     python main.py --reset-seq

python app.py         # starts Flask on http://localhost:5000
```
### Frontend
```bash
cd frontend
npm install
npm start             # starts React on http://localhost:3000
```
