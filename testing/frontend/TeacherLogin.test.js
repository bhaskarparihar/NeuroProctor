/**
 * Tests for TeacherLogin Component
 */
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import TeacherLogin from '../pages/TeacherLogin';

const mockedNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedNavigate,
}));

describe('TeacherLogin Component', () => {
  beforeEach(() => {
    mockedNavigate.mockClear();
    localStorage.clear();
    global.fetch = jest.fn();
  });

  test('renders teacher login form', () => {
    render(
      <BrowserRouter>
        <TeacherLogin />
      </BrowserRouter>
    );
    
    expect(screen.getByText(/Teacher Login/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Enter your username/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Enter your password/i)).toBeInTheDocument();
  });

  test('handles successful teacher login', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({ 
          message: 'Login successful',
          username: 'admin',
          role: 'admin'
        }),
      })
    );

    render(
      <BrowserRouter>
        <TeacherLogin />
      </BrowserRouter>
    );

    fireEvent.change(screen.getByPlaceholderText(/Enter your username/i), {
      target: { value: 'admin' },
    });
    fireEvent.change(screen.getByPlaceholderText(/Enter your password/i), {
      target: { value: 'admin123' },
    });

    fireEvent.click(screen.getByRole('button', { name: /Login to Dashboard/i }));

    await waitFor(() => {
      expect(localStorage.getItem('teacherLoggedIn')).toBe('true');
      expect(localStorage.getItem('teacherUsername')).toBe('admin');
      expect(mockedNavigate).toHaveBeenCalledWith('/proctor-dashboard');
    });
  });

  test('displays error on failed teacher login', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({ message: 'Invalid credentials' }),
        status: 401
      })
    );

    render(
      <BrowserRouter>
        <TeacherLogin />
      </BrowserRouter>
    );

    fireEvent.change(screen.getByPlaceholderText(/Enter your username/i), {
      target: { value: 'wrong' },
    });
    fireEvent.change(screen.getByPlaceholderText(/Enter your password/i), {
      target: { value: 'wrong' },
    });

    fireEvent.click(screen.getByRole('button', { name: /Login to Dashboard/i }));

    await waitFor(() => {
      expect(screen.getByText(/Invalid Credentials/i)).toBeInTheDocument();
    });
  });

  test('navigates back to student login', () => {
    render(
      <BrowserRouter>
        <TeacherLogin />
      </BrowserRouter>
    );
    
    const backButton = screen.getByText(/Student Login/i);
    fireEvent.click(backButton);
    
    expect(mockedNavigate).toHaveBeenCalledWith('/');
  });
});
