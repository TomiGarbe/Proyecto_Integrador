import React from 'react';
import { render, screen } from '@testing-library/react';
import AppNavbar from '../../src/components/Navbar';
import { BrowserRouter } from 'react-router-dom';

describe('Navbar component', () => {
  beforeEach(() => {
    // Mock localStorage
    window.localStorage = {
      getItem: jest.fn(() => JSON.stringify({ nombre: 'Usuario' })),
    };
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('renderiza los links de navegación', () => {
    render(
      <BrowserRouter>
        <AppNavbar />
      </BrowserRouter>
    );

    const links = [
      'Usuarios',
      'Sucursales',
      'Cuadrillas',
      'Preventivos',
      'Mantenimientos Preventivos',
      'Mantenimientos Correctivos',
      'Mapa',
      'Reportes',
    ];

    links.forEach((linkText) => {
      expect(screen.getByText(linkText)).toBeInTheDocument();
    });
  });
});