import React from 'react';
import { Container } from 'react-bootstrap';

const Footer = () => {
  return (
    <footer className="bg-dark text-white py-3 mt-auto">
      <Container>
        <p className="text-center mb-0">
          © {new Date().getFullYear()} Inversur App. Todos los derechos reservados.
        </p>
      </Container>
    </footer>
  );
};

export default Footer;