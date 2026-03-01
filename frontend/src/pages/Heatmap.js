// Heatmap.js
import { useEffect } from "react";
import { useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet.heat";

export default function Heatmap({ points, flyAnimationActive }) {
  const map = useMap();

  useEffect(() => {
    if (!points || points.length === 0) return;

    // Create the heatmap layer
    const heatLayer = L.heatLayer(points, {
      radius: 30,       // slightly bigger for smoother edges
      blur: 30,         // more blur so new points fade in naturally
      maxZoom: 17,
      minOpacity: 0.05, // slightly more subtle base
      gradient: {
        0.2: "rgba(0,0,255,0.3)",
        0.4: "rgba(0,255,0,0.3)",
        0.6: "rgba(255,255,0,0.4)",
        0.8: "rgba(255,165,0,0.5)",
        1.0: "rgba(255,0,0,0.6)"
      },
      updateWhenIdle: false, // redraw while moving
      updateInterval: 0
    }).addTo(map);

    // Fade helpers for zoom/fly
    const fadeOut = () => {
      if (heatLayer._canvas) {
        heatLayer._canvas.style.transition = "opacity 0.3s ease";
        heatLayer._canvas.style.opacity = 0;
      }
    };
    const fadeIn = () => {
      if (heatLayer._canvas) {
        heatLayer._canvas.style.transition = "opacity 0.3s ease";
        heatLayer._canvas.style.opacity = 1;
      }
    };

    // Only fade on zoom (user zooms) and programmatic fly
    map.on("zoomstart", fadeOut);
    map.on("zoomend", fadeIn);

    if (flyAnimationActive) {
      fadeOut();
      map.once("moveend", fadeIn);
    }

    return () => {
      map.removeLayer(heatLayer);
      map.off("zoomstart", fadeOut);
      map.off("zoomend", fadeIn);
    };
  }, [map, points, flyAnimationActive]);

  return null;
}