import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { messaging } from '../firebase';
import { getToken } from 'firebase/messaging';

export default function Settings({ heatmapVisible, setHeatmapVisible }) {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [enabled, setEnabled] = useState(false);

  useEffect(() => {
    if (Notification.permission === "granted") {
      setEnabled(true);
    }
  }, []);
  const enableNotifications = async () => {
    try {
      setLoading(true);

      const permission = await Notification.requestPermission();

      if (permission !== 'granted') {
        alert('Notification permission denied.');
        setLoading(false);
        return;
      }

      const token = await getToken(messaging, {
        vapidKey: "BGAaRzieRN5W29lRcJnGubCa08BmVmmApmXOaoZosQIzQEzIzbk0nUny0_NJ2QLG8ay7AukF-y8fd2achosxq9I"
      });

      await fetch("http://localhost:5000/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token })
      });
      
      console.log("FCM Token:", token);

      setEnabled(true);
    } catch (err) {
      console.error("Notification error:", err);
      alert("Something went wrong enabling notifications.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      {/* Top Nav */}
      <div style={styles.navbar}>
        <button
          style={styles.backButton}
          onClick={() => navigate('/map')}
        >
          ←
        </button>
        <span style={styles.navTitle}>Settings</span>
        <div style={{ width: 24 }} />
      </div>

      {/* Content Card */}
      <div style={styles.card}>
        <div style={styles.icon}>🛡️</div>

        <h1 style={styles.title}>Map Settings</h1>

        <p style={styles.description}>
          Customize how the map displays crime and safety data. 
        </p>

        {/* Heatmap Toggle Button */}
        <button
          style={{
            ...styles.button,
            backgroundColor: heatmapVisible ? "#0056B3" : "#888",
          }}
          onClick={() => setHeatmapVisible(!heatmapVisible)}
        >
          {heatmapVisible ? "Hide Heatmap" : "Show Heatmap"}
        </button>
      </div>
      {/* Content Card */}
      <div style={styles.card}>
        <div style={styles.icon}>🛡️</div>

        <h1 style={styles.title}>Stay Informed</h1>

        <p style={styles.description}>
          Enable safety alerts to receive important updates about campus
          incidents, weather warnings, and emergency notifications around DePaul.
        </p>

        <button
          style={styles.button}
          onClick={enableNotifications}
          disabled={loading || enabled}
        >
          {loading
            ? "Enabling..."
            : enabled
            ? "Alerts Enabled ✓"
            : "Enable Safety Alerts"}
        </button>
      </div>
    </div>
  );
}
const styles = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#0E2A47',
    fontFamily: 'Inter, system-ui, sans-serif',
  },
  navbar: {
    height: '60px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '0 20px',
    backgroundColor: '#0E2A47',
    color: 'white',
    borderBottom: '1px solid rgba(255,255,255,0.1)',
  },
  backButton: {
    background: 'none',
    border: 'none',
    color: 'white',
    fontSize: '22px',
    cursor: 'pointer',
  },
  navTitle: {
    fontSize: '18px',
    fontWeight: '600',
  },
  card: {
    backgroundColor: '#ffffff',
    margin: '40px auto',
    padding: '40px',
    borderRadius: '16px',
    width: '90%',
    maxWidth: '420px',
    textAlign: 'center',
    boxShadow: '0 10px 30px rgba(0,0,0,0.15)',
  },
  icon: {
    fontSize: '40px',
    marginBottom: '20px',
  },
  title: {
    fontSize: '24px',
    fontWeight: '600',
    color: '#0E2A47',
    marginBottom: '12px',
  },
  description: {
    fontSize: '15px',
    color: '#4B5563',
    lineHeight: '1.6',
    marginBottom: '28px',
  },
  button: {
    backgroundColor: '#0056B3',
    color: 'white',
    border: 'none',
    padding: '14px 20px',
    borderRadius: '10px',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer',
    width: '100%',
  },
};