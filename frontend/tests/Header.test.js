import { render, screen } from '@testing-library/react';
import Header from '../src/components/Header';

test('renders header title', () => {
    render(<Header />);
    expect(screen.getByText('Gestión de Cuadrillas')).toBeInTheDocument();
});
