import 'leaflet/dist/leaflet.css';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import { useEffect } from 'react';
import '../css/Map.css';

// 1. This child component can safely use useMap()
function MapController() {
  const map = useMap();
  
  useEffect(() => {
    // Example: Center the map manually after load
    map.setView([41.92458, -87.650722], 15);
  }, [map]);

  return null;
}

function Map() {
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
        <Marker position={[41.92458, -87.650722]}>
          <Popup>Hello from the /map route!</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}


export default Map;
