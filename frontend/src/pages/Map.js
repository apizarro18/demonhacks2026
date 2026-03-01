import 'leaflet/dist/leaflet.css';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import { useEffect, useState } from 'react';
import '../css/Map.css';
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

  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
  fetch("http://localhost:5000/alerts")
    .then(res => res.json())
    .then(data => setAlerts(data))
    .catch(err => console.error(err));
}, []);

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
      </MapContainer>
    </div>
  );
}

export default Map;
