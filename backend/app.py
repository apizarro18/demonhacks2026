from database import database
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__)
CORS(app)  # allows React (localhost:3000) to access backend

SEVERITY_MAP = {"Low": 1, "Med": 3, "High": 5}

FALLBACK_ALERTS = [
    {
        "id": 3,
        "lat": 41.9238,
        "lng": -87.6519,
        "type": "Crime",
        "severity": 4,
        "message": "Assault reported near residence hall.",
        "timestamp": "2026-02-28T03:15:00Z"
    },
    {
        "id": 4,
        "lat": 41.9271,
        "lng": -87.6492,
        "type": "Weather",
        "severity": 2,
        "message": "Heavy snowfall causing slippery sidewalks.",
        "timestamp": "2026-02-28T03:40:00Z"
    },
    {
        "id": 5,
        "lat": 41.9254,
        "lng": -87.6473,
        "type": "Crime",
        "severity": 5,
        "message": "Shots fired reported. Avoid the area.",
        "timestamp": "2026-02-28T04:05:00Z"
    },
    {
        "id": 6,
        "lat": 41.9229,
        "lng": -87.6528,
        "type": "Traffic",
        "severity": 3,
        "message": "Road closed due to construction.",
        "timestamp": "2026-02-28T04:20:00Z"
    },
    {
        "id": 7,
        "lat": 41.9282,
        "lng": -87.6465,
        "type": "Medical",
        "severity": 4,
        "message": "Medical emergency reported at campus gym.",
        "timestamp": "2026-02-28T04:45:00Z"
    },
    {
        "id": 8,
        "lat": 41.9241,
        "lng": -87.6488,
        "type": "Crime",
        "severity": 2,
        "message": "Theft reported near parking garage.",
        "timestamp": "2026-02-28T05:10:00Z"
    },
    {
        "id": 9,
        "lat": 41.9267,
        "lng": -87.6511,
        "type": "Utility",
        "severity": 3,
        "message": "Power outage affecting several buildings.",
        "timestamp": "2026-02-28T05:30:00Z"
    },
    {
        "id": 10,
        "lat": 41.9233,
        "lng": -87.6499,
        "type": "Fire",
        "severity": 4,
        "message": "Fire alarm triggered in science building.",
        "timestamp": "2026-02-28T05:55:00Z"
    }
]


def _transform_incident(row):
    ts = row.get("parsed_at", "")
    timestamp = ts.replace(" ", "T") + "Z" if isinstance(ts, str) and " " in ts else str(ts)
    return {
        "id": row.get("id"),
        "lat": row.get("latitude"),
        "lng": row.get("longitude"),
        "type": (row.get("incident_type") or "Unknown").title(),
        "severity": SEVERITY_MAP.get(row.get("incident_level"), 2),
        "message": row.get("description", ""),
        "timestamp": timestamp,
    }


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

@app.route("/subscribe", methods=["POST"])
def subscribe():
    token = request.json.get("token")

    messaging.subscribe_to_topic(token, "allUsers")

    return jsonify({"success": True})

@app.route("/alerts", methods=["GET"])
def get_alerts():
    try:
        db = database()
        rows = db.get_all_parsed_incidents()
        if not rows:
            return jsonify(FALLBACK_ALERTS)
        return jsonify([_transform_incident(row) for row in rows])
    except Exception:
        return jsonify(FALLBACK_ALERTS)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
