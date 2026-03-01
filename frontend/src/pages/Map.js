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
  iconRetinaUrl: customMapIcon, // Optional, for high-res screens
  iconSize: [48, 65], // Size of the icon
  iconAnchor: [24,65], // Point of the icon which will correspond to the marker's location
  popupAnchor: [0, -65], // Point from which the popup should open relative to the iconAnchor
  shadowUrl: customShadowIcon, // Optional, default shadow
  shadowSize: [48, 48], // Size of the shadow
  shadowAnchor: [24, 40] // Point of the shadow which will correspond to the marker's location
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
  ]

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
    iconSize: [220, null],   // width fixed, height auto
    iconAnchor: [110, 0],    // center horizontally
  });
  return (
    <div style={{ height: "100vh", width: "100vw" }}> {/* Critical for rendering */}
      <MapContainer
        center={[41.92458, -87.650722]}
        zoom={15}
        style={{ height: "100%", width: "100%" }}
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
          position={[41.9239, -87.6539]} // center of Lincoln Park boundary
          icon={labelIcon("DePaul University - Lincoln Park Campus")}
        />
        <Marker
          position={[41.8778, -87.6264]} // center of Loop boundary
          icon={labelIcon("DePaul University - Loop Campus")}
        />
      </MapContainer>
      <Feed />
    </div>
  );
}

export default Map;
