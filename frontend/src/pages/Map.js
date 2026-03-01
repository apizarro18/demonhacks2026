import 'leaflet/dist/leaflet.css';
import { MapContainer, TileLayer, Marker, Popup, Polygon, useMap } from 'react-leaflet';
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

  const depaulLPBoundary = [
    [41.925201, -87.659033],
    [41.923533, -87.658982],
    [41.923595, -87.654660],
    [41.921806, -87.654591],
    [41.921809, -87.652862],
    [41.923628, -87.652947],
    [41.923710, -87.648846],
    [41.925361, -87.648936]
  ];

  const depaulLoopBoundary = [
    [41.878648, -87.627593],
    [41.878682, -87.625243],
    [41.877060, -87.625161],
    [41.877020, -87.627548]
  ];

  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/alerts")
      .then(res => res.json())
      .then(data => setAlerts(data))
      .catch(err => console.error(err));
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
        center={[41.92458, -87.650722]}
        zoom={15}
        style={{ height: "100%", width: "100%", zIndex: 1 }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {alerts.map((alert) => (
          <Marker icon={mapIcon} key={alert.id} position={[alert.lat, alert.lng]}>
            <Popup>{alert.message}</Popup>
          </Marker>
        ))}
        <Polygon
          positions={depaulLPBoundary}
          pathOptions={{
            color: 'blue',
            fillColor: 'blue',
            fillOpacity: 0.1,
            weight: 3
          }}
        ></Polygon>
        <Polygon
          positions={depaulLoopBoundary}
          pathOptions={{
            color: 'blue',
            fillColor: 'blue',
            fillOpacity: 0.1,
            weight: 3
          }}
        ></Polygon>
        <Marker
          position={[41.9239, -87.6539]} 
          icon={labelIcon("DePaul University - Lincoln Park Campus")}
        />
        <Marker
          position={[41.8778, -87.6264]} 
          icon={labelIcon("DePaul - Loop Campus")}
        />
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
        🚨 Call Public Safety: (773) 325-7777
      </a>

    </div>
  );
}

export default Map;