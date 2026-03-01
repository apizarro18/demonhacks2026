import { useEffect, useState } from 'react';

function Feed() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/alerts")
      .then(res => res.json())
      .then(data => setAlerts(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={styles.container}>
      <h3 style={styles.header}>Live Alerts</h3>

      {alerts.length === 0 ? (
        <p style={styles.empty}>No active alerts</p>
      ) : (
        alerts.map((alert, index) => (
          <div key={index} style={styles.alert}>
            <div style={styles.timestamp}>{alert.timestamp}</div>
            <div>{alert.message}</div>
          </div>
        ))
      )}
    </div>
  );
}

const styles = {
  container: {
    position: "absolute",
    top: "20px",
    right: "20px",
    width: "25%",
    maxHeight: "50%",
    overflowY: "auto",
    backgroundColor: "rgba(255, 255, 255, 0.95)",
    backdropFilter: "blur(6px)",
    borderRadius: "10px",
    padding: "12px",
    boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
    zIndex: 1000, // Important: above Leaflet tiles
    fontFamily: "Arial, sans-serif"
  },
  header: {
    margin: "0 0 10px 0",
    borderBottom: "1px solid #ddd",
    paddingBottom: "6px"
  },
  alert: {
    marginBottom: "8px",
    padding: "8px",
    backgroundColor: "#f8f8f8",
    borderRadius: "6px",
    fontSize: "14px"
  },
  timestamp: {
    fontSize: "12px",
    color: "#666",
    marginBottom: "4px"
  },
  empty: {
    fontStyle: "italic",
    color: "#888"
  }
};

export default Feed;
