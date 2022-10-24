import { render, screen } from '@testing-library/react';
import Courses from './pages/Courses';

test('renders learn react link', () => {
    render(<Courses />);
    const linkElement = screen.getByText(/learn react/i);
    expect(linkElement).toBeInTheDocument();
});
