import 'leaflet/dist/leaflet.css';
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMap
} from 'react-leaflet';
import { useEffect } from 'react';

function MapCompnent() {
  const map = useMap();
  return null;
}

function App() {
  return (
    <MapContainer
      center={[41.92458, -87.650722]}
      zoom={15}
      style={{ height: "100vh", width: "100%" }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={[41.92458, -87.650722]}>
        <Popup>Hello</Popup>
      </Marker>
    </MapContainer>
  );
}

export default App;