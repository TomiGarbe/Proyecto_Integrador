import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../src/App';

jest.mock('../src/services/api'); 

describe('App component', () => {
  test('renderiza el Navbar y el Footer', () => {
    render(<App />);

    // Verifica que el Navbar esté
    expect(screen.getByRole('navigation')).toBeInTheDocument();

    // Verifica que el Footer esté
    expect(screen.getByText(/©/i)).toBeInTheDocument(); // Suponiendo que el footer tiene el símbolo ©
  });
});
