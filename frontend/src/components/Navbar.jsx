import React from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Nav, Container } from 'react-bootstrap';

const AppNavbar = () => {
  return (
    <Navbar bg="dark" variant="dark" expand="lg">
      <Container>
        <Navbar.Brand as={Link} to="/">Inversur App</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">Home</Nav.Link>
            <Nav.Link as={Link} to="/users">Usuarios</Nav.Link>
            <Nav.Link as={Link} to="/sucursales">Sucursales</Nav.Link>
            <Nav.Link as={Link} to="/cuadrillas">Cuadrillas</Nav.Link>
            <Nav.Link as={Link} to="/preventivos">Preventivos</Nav.Link>
            <Nav.Link as={Link} to="/mantenimientos-preventivos">Mantenimientos Preventivos</Nav.Link>
            <Nav.Link as={Link} to="/mantenimientos-correctivos">Mantenimientos Correctivos</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default AppNavbar;