import { useState } from 'react';

function Feed({ alerts = [], onAlertClick }) {
  const [hoveredIndex, setHoveredIndex] = useState(null);

  const handleClick = (alert) => {
    if (alert.lat && alert.lng && onAlertClick) {
      onAlertClick({ lat: alert.lat, lng: alert.lng });
    }
  };

  const isClickable = (alert) => Boolean(alert.lat && alert.lng && onAlertClick);

  return (
    <div style={styles.container}>
      <h3 style={styles.header}> 🛡️ Blue Safety Live Alerts </h3>

      {alerts.length === 0 ? (
        <p style={styles.empty}>No active alerts</p>
      ) : (
        alerts.map((alert, index) => {
          const clickable = isClickable(alert);
          return (
            <div
              key={index}
              style={{
                ...styles.alert,
                ...(clickable ? styles.clickable : {}),
                ...(clickable && hoveredIndex === index ? styles.hovered : {}),
              }}
              onClick={() => handleClick(alert)}
              onMouseEnter={() => clickable && setHoveredIndex(index)}
              onMouseLeave={() => setHoveredIndex(null)}
            >
              <div style={styles.timestamp}>{alert.timestamp}</div>
              <div>{alert.message}</div>
            </div>
          );
        })
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
    zIndex: 1000,
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
    backgroundColor: "#cadaf2",
    borderRadius: "6px",
    fontSize: "14px",
    transition: "background-color 0.15s ease"
  },
  clickable: {
    cursor: "pointer"
  },
  hovered: {
    backgroundColor: "#e2e6ea"
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
