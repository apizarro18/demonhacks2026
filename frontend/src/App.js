import { Routes, Route, Link } from 'react-router-dom';
import Map from "./pages/Map";

function App() {
  return (
      <Routes>
        <Route path="/" element={<></>} />
        <Route path="/map" element={<Map />} />
      </Routes>
  );
}

export default App;