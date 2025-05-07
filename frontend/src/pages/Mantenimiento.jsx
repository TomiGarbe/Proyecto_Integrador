import React from 'react';
import { Container } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { FaTruck, FaHome, FaCalendarAlt, FaWrench, FaTools } from 'react-icons/fa';
import '../styles/mantenimiento.css'; 

const Mantenimiento = () => {
  return (
    <Container className="home-container">
      <div className="page-content">
        <div className="button-obras-container">
          <Link /*to="/cuadrillas"*/ className="obras-button">
            <FaTruck />
            Cuadrillas
          </Link>
          <Link to="/sucursales" className="obras-button">
            <FaHome />
            Sucursales
          </Link>
          <Link /*to="/preventivos"*/ className="obras-button">
            <FaCalendarAlt />
            Preventivos
          </Link>
          <Link /*to="/mantenimientos-correctivos"*/ className="obras-button">
            <FaWrench />
            Mantenimiento Correctivo
          </Link>
          <Link /*to="/mantenimientos-preventivos"*/ className="obras-button">
            <FaTools />
            Mantenimiento Preventivo
          </Link>
        </div>
      </div>
    </Container>
  );
};

export default Mantenimiento;