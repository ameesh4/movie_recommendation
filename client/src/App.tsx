import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/home';
import Recommend from './pages/recommend'; 

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/recommendations" element={<Recommend />} />
      </Routes>
    </Router>
  );
}

