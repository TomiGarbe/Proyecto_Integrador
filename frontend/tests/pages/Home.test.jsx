import React from 'react';
import { render, screen } from '@testing-library/react';
import Home from '../../src/pages/Home';
import { BrowserRouter } from 'react-router-dom';

describe('Home component', () => {
  test('renderiza los botones de navegación', () => {
    render(
      <BrowserRouter>
        <Home />
      </BrowserRouter>
    );

    const buttons = [
      'Usuarios',
      'Mantenimiento',
      'Mapa',
      'Reportes',
    ];

    buttons.forEach((buttonText) => {
      expect(screen.getByText(buttonText)).toBeInTheDocument();
    });
  });
});