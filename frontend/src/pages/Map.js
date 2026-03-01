import 'leaflet/dist/leaflet.css';
import { MapContainer, TileLayer, Marker, Popup, Polygon } from 'react-leaflet';
import { useEffect, useState } from 'react';
import '../css/Map.css';
import Feed from './Feed';
import L from 'leaflet';
import customMapIcon from '../components/mapIcon.png';
import customShadowIcon from '../components/shadowIcon.png';

function Map() {
  const mapIcon = L.icon({
    iconUrl: customMapIcon,
    iconRetinaUrl: customMapIcon, 
    iconSize: [48, 65], 
    iconAnchor: [24,65], 
    popupAnchor: [0, -65], 
    shadowUrl: customShadowIcon, 
    shadowSize: [48, 48], 
    shadowAnchor: [24, 40] 
  });

  // 1. University of Chicago (UChicago) — 24 points
  const uchicagoBoundary = [
    [41.7943, -87.5988], [41.7943, -87.6013], [41.7960, -87.6013], [41.7960, -87.5990],
    [41.7978, -87.5990], [41.7978, -87.5876], [41.7943, -87.5876], [41.7943, -87.5862],
    [41.7925, -87.5862], [41.7925, -87.5864], [41.7907, -87.5864], [41.7878, -87.5864],
    [41.7853, -87.5864], [41.7853, -87.6058], [41.7835, -87.6058], [41.7835, -87.6013],
    [41.7853, -87.6013], [41.7853, -87.5988], [41.7871, -87.5988], [41.7871, -87.5966],
    [41.7889, -87.5966], [41.7907, -87.5966], [41.7907, -87.5988], [41.7925, -87.5988],
  ];

  // 2. University of Illinois Chicago (UIC) — 18 points
  const uicBoundary = [
    [41.8743, -87.6514], [41.8743, -87.6467], [41.8716, -87.6467], [41.8716, -87.6514],
    [41.8693, -87.6514], [41.8693, -87.6586], [41.8672, -87.6586], [41.8672, -87.6540],
    [41.8636, -87.6540], [41.8636, -87.6586], [41.8600, -87.6586], [41.8600, -87.6467],
    [41.8618, -87.6467], [41.8618, -87.6514], [41.8672, -87.6514], [41.8672, -87.6467],
    [41.8764, -87.6467], [41.8764, -87.6514],
  ];

  // 3. DePaul University – Lincoln Park — 14 points
  const depaulLPBoundary = [
    [41.9217, -87.6585], [41.9217, -87.6536], [41.9254, -87.6536], [41.9254, -87.6487],
    [41.9254, -87.6487], [41.9236, -87.6487], [41.9236, -87.6570], [41.9217, -87.6570],
    [41.9217, -87.6559], [41.9254, -87.6559], [41.9254, -87.6585], [41.9245, -87.6585],
    [41.9245, -87.6536], [41.9254, -87.6585],
  ];

  // 4. Illinois Institute of Technology (IIT) — 15 points
  const iitBoundary = [
    [41.8381, -87.6317], [41.8381, -87.6236], [41.8363, -87.6236], [41.8363, -87.6254],
    [41.8345, -87.6254], [41.8345, -87.6236], [41.8312, -87.6236], [41.8312, -87.6254],
    [41.8312, -87.6280], [41.8312, -87.6317], [41.8328, -87.6317], [41.8328, -87.6280],
    [41.8345, -87.6280], [41.8345, -87.6317], [41.8363, -87.6317],
  ];

  // 5. Loyola University – Lake Shore — 13 points
  const loyolaBoundary = [
    [41.9984, -87.6577], [41.9984, -87.6548], [41.9997, -87.6548], [41.9997, -87.6594],
    [41.9983, -87.6601], [41.9983, -87.6577], [41.9939, -87.6594], [41.9939, -87.6601],
    [41.9952, -87.6601], [41.9952, -87.6594], [41.9952, -87.6548], [41.9968, -87.6548],
    [41.9968, -87.6594],
  ];

  // 6. Northwestern – Chicago (Feinberg/Lurie) — 13 points
  const northwesternBoundary = [
    [41.8967, -87.6206], [41.8967, -87.6234], [41.8960, -87.6234], [41.8960, -87.6272],
    [41.8944, -87.6272], [41.8944, -87.6234], [41.8935, -87.6234], [41.8935, -87.6206],
    [41.8920, -87.6206], [41.8920, -87.6179], [41.8928, -87.6179], [41.8928, -87.6206],
    [41.8944, -87.6206],
  ];

  // 7. Columbia College Chicago — 12 points
  const columbiaBoundary = [
    [41.8726, -87.6247], [41.8726, -87.6261], [41.8715, -87.6261], [41.8715, -87.6278],
    [41.8707, -87.6278], [41.8707, -87.6261], [41.8684, -87.6261], [41.8684, -87.6247],
    [41.8740, -87.6247], [41.8740, -87.6261], [41.8755, -87.6261], [41.8755, -87.6247],
  ];

  // 8. Roosevelt University — 10 points
  const rooseveltBoundary = [
    [41.8755, -87.6247], [41.8755, -87.6261], [41.8755, -87.6278], [41.8764, -87.6278],
    [41.8764, -87.6261], [41.8764, -87.6247], [41.8781, -87.6247], [41.8781, -87.6261],
    [41.8793, -87.6261], [41.8793, -87.6247],
  ];

  // 9. Chicago State University (CSU) — 14 points
  const csuBoundary = [
    [41.7214, -87.6126], [41.7214, -87.6098], [41.7214, -87.6065], [41.7196, -87.6065],
    [41.7196, -87.6082], [41.7179, -87.6082], [41.7179, -87.6065], [41.7149, -87.6065],
    [41.7149, -87.6126], [41.7163, -87.6126], [41.7163, -87.6098], [41.7179, -87.6098],
    [41.7179, -87.6126], [41.7196, -87.6126],
  ];

  // 10. DePaul University – Loop Campus — 15 points
  const depaulLoopBoundary = [
    [41.8781, -87.6278], [41.8781, -87.6261], [41.8764, -87.6261], [41.8764, -87.6278],
    [41.8764, -87.6295], [41.8755, -87.6295], [41.8755, -87.6314], [41.8740, -87.6314],
    [41.8740, -87.6308], [41.8716, -87.6308], [41.8716, -87.6278], [41.8740, -87.6278],
    [41.8740, -87.6261], [41.8755, -87.6261], [41.8755, -87.6278],
  ];

  // Campus polygon config: [boundary, color, label, labelPosition]
  const campuses = [
    { boundary: uchicagoBoundary, color: '#800000', label: 'University of Chicago', position: [41.7900, -87.5950] },
    { boundary: uicBoundary, color: '#CC0000', label: 'UIC', position: [41.8682, -87.6527] },
    { boundary: depaulLPBoundary, color: '#0033A0', label: 'DePaul University - Lincoln Park', position: [41.9239, -87.6539] },
    { boundary: iitBoundary, color: '#C41E3A', label: 'Illinois Institute of Technology', position: [41.8345, -87.6277] },
    { boundary: loyolaBoundary, color: '#8B0000', label: 'Loyola University', position: [41.9968, -87.6575] },
    { boundary: northwesternBoundary, color: '#4E2A84', label: 'Northwestern - Chicago', position: [41.8945, -87.6225] },
    { boundary: columbiaBoundary, color: '#D4A017', label: 'Columbia College Chicago', position: [41.8710, -87.6254] },
    { boundary: rooseveltBoundary, color: '#006400', label: 'Roosevelt University', position: [41.8774, -87.6254] },
    { boundary: csuBoundary, color: '#2E8B57', label: 'Chicago State University', position: [41.7182, -87.6096] },
    { boundary: depaulLoopBoundary, color: '#0033A0', label: 'DePaul University - Loop', position: [41.8748, -87.6287] },
  ];

  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/alerts")
      .then(res => res.json())
      .then(data => setAlerts(data))
      .catch(err => console.error("Failed to fetch alerts:", err));
  }, []);

  const labelIcon = (text) =>
    L.divIcon({
      className: "campus-label",
      html: `<div class="label-text">${text}</div>`,
      iconSize: [220, null],   
      iconAnchor: [110, 0],    
    });

  return (
    <div style={{ height: "100vh", width: "100vw", position: "relative" }}> 
      
      {/* 1. The Map */}
      <MapContainer
        center={[41.8700, -87.6350]}
        zoom={12}
        style={{ height: "100%", width: "100%", zIndex: 1 }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {alerts
          .filter(alert => alert.lat && alert.lng)
          .map((alert, index) => (
            <Marker
              icon={mapIcon}
              key={alert.id || index}
              position={[alert.lat, alert.lng]}
            >
              <Popup>
                <strong>{alert.type}</strong><br/>
                {alert.message}
              </Popup>
            </Marker>
        ))}
        {campuses.map((campus, idx) => (
          <Polygon
            key={`poly-${idx}`}
            positions={campus.boundary}
            pathOptions={{
              color: campus.color,
              fillColor: campus.color,
              fillOpacity: 0.1,
              weight: 3,
            }}
          />
        ))}
        {campuses.map((campus, idx) => (
          <Marker
            key={`label-${idx}`}
            position={campus.position}
            icon={labelIcon(campus.label)}
          />
        ))}
      </MapContainer> 

      {/* 2. The Live Feed */}
      <Feed />
      
      {/* 3. The Public Safety Button (Fixed to screen) */}
      <a 
        href="tel:7733257777" 
        style={{
          position: "fixed",
          bottom: "30px",
          right: "20px",
          zIndex: 99999, /* Maximum z-index to guarantee visibility */
          backgroundColor: "#001a4d",
          color: "white",
          padding: "12px 18px",
          borderRadius: "8px",
          textDecoration: "none",
          fontWeight: "bold",
          fontSize: "16px",
          boxShadow: "0 4px 6px rgba(0,0,0,0.3)",
          display: "block",
          fontFamily: "Arial, sans-serif"
        }}
      >
        🚓 Call Public Safety: (773) 325-7777
      </a>
<a 
        href="tel:911"  /* Removed the space here */
        style={{
          position: "fixed",
          bottom: "100px", /* Sits right at the bottom */
          right: "20px",
          zIndex: 99999, 
          backgroundColor: "#c8102e",
          color: "white",
          padding: "12px 18px",
          borderRadius: "8px",
          textDecoration: "none",
          fontWeight: "bold",
          fontSize: "16px",
          boxShadow: "0 4px 6px rgba(0,0,0,0.3)",
          display: "block",
          fontFamily: "Arial, sans-serif"
        }}
      >
        🚨 Emergency Number: 911
      </a>
      <a 
        href="settings.html" 
        style={{
          position: "fixed",
          bottom: "170px",
          right: "20px",
          zIndex: 99999, /* Maximum z-index to guarantee visibility */
          backgroundColor: "#7e5a5a",
          color: "white",
          padding: "12px 18px",
          borderRadius: "8px",
          textDecoration: "none",
          fontWeight: "bold",
          fontSize: "16px",
          boxShadow: "0 4px 6px rgba(0,0,0,0.3)",
          display: "block",
          fontFamily: "Arial, sans-serif"
        }}
      >
        ⚙️ Settings:
      </a>

    </div>
  );
}

export default Map;