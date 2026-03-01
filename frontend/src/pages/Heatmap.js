import { useEffect } from "react";
import { useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet.heat";

export default function Heatmap({ points }) {
  const map = useMap();
    
  useEffect(() => {
    if (!points || points.length === 0) return;

    const heatLayer = L.heatLayer(points, {
      radius: 20,  // spread of each point
      blur: 15,    // softness
      maxZoom: 15,
      gradient: {
        0.0: "orange",
        1.0: "red"
    }
    }).addTo(map);

    return () => map.removeLayer(heatLayer);
  }, [map, points]);

  return null;
}