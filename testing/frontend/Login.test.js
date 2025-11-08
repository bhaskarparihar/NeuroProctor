/**
 * Tests for Login Component
 */
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Login from '../components/Login';

// Mock useNavigate
const mockedNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedNavigate,
}));

describe('Login Component', () => {
  beforeEach(() => {
    mockedNavigate.mockClear();
    global.fetch = jest.fn();
  });

  test('renders login form with all fields', () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );
    
    expect(screen.getByPlaceholderText('Enter your username')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter your roll number')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter your password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Login to Exam/i })).toBeInTheDocument();
  });

  test('displays teacher login link', () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );
    
    const teacherButton = screen.getByText(/Teacher\/Proctor Login/i);
    expect(teacherButton).toBeInTheDocument();
  });

  test('navigates to teacher login when button clicked', () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );
    
    const teacherButton = screen.getByText(/Teacher\/Proctor Login/i);
    fireEvent.click(teacherButton);
    
    expect(mockedNavigate).toHaveBeenCalledWith('/teacher/login');
  });

  test('handles successful login', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({ message: 'Login successful' }),
      })
    );

    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );

    fireEvent.change(screen.getByPlaceholderText('Enter your username'), {
      target: { value: 'test_user' },
    });
    fireEvent.change(screen.getByPlaceholderText('Enter your roll number'), {
      target: { value: '12345' },
    });
    fireEvent.change(screen.getByPlaceholderText('Enter your password'), {
      target: { value: 'password123' },
    });

    fireEvent.click(screen.getByRole('button', { name: /Login to Exam/i }));

    await waitFor(() => {
      expect(mockedNavigate).toHaveBeenCalledWith('/instruction');
    });
  });

  test('displays error message on failed login', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({ message: 'Invalid credentials' }),
      })
    );

    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );

    fireEvent.change(screen.getByPlaceholderText('Enter your username'), {
      target: { value: 'wrong_user' },
    });
    fireEvent.change(screen.getByPlaceholderText('Enter your roll number'), {
      target: { value: 'wrong' },
    });
    fireEvent.change(screen.getByPlaceholderText('Enter your password'), {
      target: { value: 'wrong' },
    });

    fireEvent.click(screen.getByRole('button', { name: /Login to Exam/i }));

    await waitFor(() => {
      expect(screen.getByText('Invalid Credentials')).toBeInTheDocument();
    });
  });

  test('displays network error on fetch failure', async () => {
    global.fetch = jest.fn(() => Promise.reject(new Error('Network error')));

    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );

    fireEvent.change(screen.getByPlaceholderText('Enter your username'), {
      target: { value: 'test' },
    });
    fireEvent.change(screen.getByPlaceholderText('Enter your roll number'), {
      target: { value: '123' },
    });
    fireEvent.change(screen.getByPlaceholderText('Enter your password'), {
      target: { value: 'test' },
    });

    fireEvent.click(screen.getByRole('button', { name: /Login to Exam/i }));

    await waitFor(() => {
      expect(screen.getByText('Network error. Please try again.')).toBeInTheDocument();
    });
  });
});
