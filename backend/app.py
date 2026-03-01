from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows React (localhost:3000) to access backend

@app.route("/alerts", methods=["GET"])
def get_alerts():
    return jsonify([
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
    ])

if __name__ == "__main__":
    app.run(debug=True, port=5000)