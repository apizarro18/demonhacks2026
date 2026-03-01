import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import Map from "./pages/Map";
import Feed from "./pages/Feed";
import SplashPage from "./pages/SplashPage"; // Adjust path as needed

function App() {
    const navigate = useNavigate();
    const location = useLocation();
  
    useEffect(() => {
      if (location.pathname !== '/') return; // only run when actually on the splash route
      const timer = setTimeout(() => {
        navigate('/map');
      }, 3500); // 3.5 seconds
  
      return () => clearTimeout(timer);
    }, [navigate, location.pathname]);

  return (
    <Routes>
      <Route path="/" element={<SplashPage />} />
      <Route path="/map" element={<Map />} />
      <Route path="/feed" element={<Feed />} />
    </Routes>
  );
}

export default App;