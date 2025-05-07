import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import Sucursales from './pages/Sucursales';
import Mantenimiento from './pages/Mantenimiento';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <Router>
      <div className="d-flex flex-column min-vh-100">
        <Navbar />
        <main className="flex-grow-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/mantenimiento" element={<Mantenimiento />} /> 
            <Route path="/sucursales" element={<Sucursales />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;