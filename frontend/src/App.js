import { Routes, Route, useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import Map from "./pages/Map";
import SplashPage from "./pages/SplashPage"; // Adjust path as needed

function App() {
  const navigate = useNavigate();

  useEffect(() => {
    // This logic handles the "Splash to Map" transition
    const timer = setTimeout(() => {
      navigate('/map');
    }, 3500); // 3.5 seconds

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <Routes>
      <Route path="/" element={<SplashPage />} />
      <Route path="/map" element={<Map />} />
    </Routes>
  );
}

export default App;