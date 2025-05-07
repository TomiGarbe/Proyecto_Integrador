import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Navbar as BootstrapNavbar, Nav, Container, NavDropdown, Image, Modal, Button } from 'react-bootstrap';
import logoInversur from '../assets/logo_inversur.png';
import { FaUser, FaBell } from 'react-icons/fa'; // Importamos íconos de usuario y campanita
import '../styles/navbar.css'; 

const Navbar = () => {
  const user = JSON.parse(localStorage.getItem('user')) || {};
  const [showNotifications, setShowNotifications] = useState(false); // Estado para el modal de notificaciones

  const handleShowNotifications = () => setShowNotifications(true);
  const handleCloseNotifications = () => setShowNotifications(false);

  // Ejemplo de notificaciones (puedes reemplazar esto con datos de una API)
  const notifications = [
    { id: 1, message: 'Nueva obra asignada a Cuadrilla #1', time: 'Hace 5 minutos' },
    { id: 2, message: 'Mantenimiento preventivo programado', time: 'Hace 1 hora' },
    { id: 3, message: 'Usuario Juan Pérez actualizó su perfil', time: 'Hace 2 horas' },
  ];

  return (
    <>
      <BootstrapNavbar bg="dark" variant="dark" expand="lg" style={{ paddingLeft: '0' }}>
        <Container fluid>
          <BootstrapNavbar.Brand as={Link} to="/" className="d-flex align-items-center" style={{ marginLeft: '1rem' }}>
            <Image
              src={logoInversur} // Usamos el logo importado
              height="65"
              alt="Inversur Logo"
              style={{ objectFit: 'contain' }}
            />
          </BootstrapNavbar.Brand>
          <BootstrapNavbar.Toggle aria-controls="basic-navbar-nav" />
          <BootstrapNavbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto" style={{ gap: '2rem', marginLeft: '2rem' }}>
              <Nav.Link /*as={Link} to="/users"*/>Usuarios</Nav.Link>
              <Nav.Link as={Link} to="/sucursales">Sucursales</Nav.Link>
              <Nav.Link /*as={Link} to="/cuadrillas"*/>Cuadrillas</Nav.Link>
              <Nav.Link /*as={Link} to="/preventivos"*/>Preventivos</Nav.Link>
              <Nav.Link /*as={Link} to="/mantenimientos-preventivos"*/>Mantenimientos Preventivos</Nav.Link>
              <Nav.Link /*as={Link} to="/mantenimientos-correctivos"*/>Mantenimientos Correctivos</Nav.Link>
              <Nav.Link /*as={Link} to="/mapas"*/>Mapa</Nav.Link>
              <Nav.Link /*as={Link} to="/reportes"*/>Reportes</Nav.Link>
            </Nav>
            <Nav className="nav-right">
              {/* Botón de notificaciones */}
              <Nav.Link onClick={handleShowNotifications}>
                <FaBell size={20} style={{ color: 'white' }} />
              </Nav.Link>
              {/* Dropdown de usuario */}
              <NavDropdown 
                title={
                  <div className="d-flex align-items-center">
                    <FaUser size={24} style={{ marginRight: '0.8rem', color: 'white' }} />
                    <span>{user.nombre || 'Usuario'}</span>
                  </div>
                }
                id="user-nav-dropdown"
                align="end"
              >
                <NavDropdown.Item /*as={Link} to="/profile"*/>Mi Perfil</NavDropdown.Item>
                <NavDropdown.Item /*as={Link} to="/settings"*/>Configuración</NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item>Cerrar Sesión</NavDropdown.Item>
              </NavDropdown>
            </Nav>
          </BootstrapNavbar.Collapse>
        </Container>
      </BootstrapNavbar>

      {/* Modal de Notificaciones */}
      <Modal show={showNotifications} onHide={handleCloseNotifications} centered>
        <Modal.Header closeButton>
          <Modal.Title>Notificaciones</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {notifications.length > 0 ? (
            notifications.map((notification) => (
              <div key={notification.id} className="mb-3 p-2 border-bottom">
                <p className="mb-1">{notification.message}</p>
                <small className="text-muted">{notification.time}</small>
              </div>
            ))
          ) : (
            <p>No tienes notificaciones.</p>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseNotifications}>
            Cerrar
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default Navbar;