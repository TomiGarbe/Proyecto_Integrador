import { render, screen } from '@testing-library/react';
import Dashboard from '../src/pages/Dashboard';

test('renders dashboard', () => {
    render(<Dashboard />);
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
});
