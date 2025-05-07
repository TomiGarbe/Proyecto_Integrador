import React from 'react';
import { Container } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { FaUsers, FaClipboardList, FaMapMarkerAlt, FaFileAlt } from 'react-icons/fa';
import '../styles/home.css';

const Home = () => {
  return (
    <Container className="home-container">
      <div className="page-content"> {/* Nuevo contenedor */}
        <div className="button-home-container">
          <Link /*to="/users"*/ className="home-button">
            <FaUsers />
            Usuarios
          </Link>

          <Link to="/mantenimiento" className="home-button">
            <FaClipboardList />
            Mantenimiento
          </Link>

          <Link /*to="/mapa"*/ className="home-button">
            <FaMapMarkerAlt />
            Mapa
          </Link>

          <Link /*to="/reportes"*/ className="home-button">
            <FaFileAlt />
            Reportes
          </Link>
        </div>
      </div>
    </Container>
  );
};

export default Home;