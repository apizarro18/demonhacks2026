import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Map from "./pages/Map";
import Settings from "./pages/Settings";
import Feed from "./pages/Feed";
import SplashPage from "./pages/SplashPage";

function App() {
  const navigate = useNavigate();
  const location = useLocation();

  // Splash page redirect after 3.5 seconds
  useEffect(() => {
    if (location.pathname !== '/') return;

    const timer = setTimeout(() => {
      navigate('/map');
    }, 3500);

    return () => clearTimeout(timer);
  }, [navigate, location.pathname]);

  return (
    <Routes>
      <Route path="/" element={<SplashPage />} />
      <Route path="/map" element={<Map />} />
      <Route path="/feed" element={<Feed />} />
      <Route path="/settings" element={<Settings />} />
    </Routes>
  );
}

export default App;