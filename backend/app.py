from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows React (localhost:3000) to access backend

@app.route("/alerts", methods=["GET"])
def get_alerts():
    return jsonify([
        {
            "id": 1,
            "lat": 41.92458,
            "lng": -87.650722,
            "type": "Crime",
            "severity": 3,
            "message": "Armed robbery reported near campus.",
            "timestamp": "2026-02-28T02:00:00Z"
        },
        {
            "id": 2,
            "lat": 41.926,
            "lng": -87.648,
            "type": "Traffic",
            "severity": 2,
            "message": "Minor accident blocking lane.",
            "timestamp": "2026-02-28T01:30:00Z"
        }
    ])

if __name__ == "__main__":
    app.run(debug=True, port=5000)