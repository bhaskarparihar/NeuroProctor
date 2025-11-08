/**
 * Tests for Exam Component
 */
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Exam from '../components/Exam';

// Mock react-webcam
jest.mock('react-webcam', () => {
  return jest.fn(() => null);
});

const mockedNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedNavigate,
}));

describe('Exam Component', () => {
  beforeEach(() => {
    mockedNavigate.mockClear();
    localStorage.setItem('rollNumber', 'TEST001');
    global.fetch = jest.fn();
  });

  afterEach(() => {
    localStorage.clear();
  });

  test('redirects to login if no roll number', () => {
    localStorage.removeItem('rollNumber');
    
    render(
      <BrowserRouter>
        <Exam />
      </BrowserRouter>
    );
    
    expect(mockedNavigate).toHaveBeenCalledWith('/');
  });

  test('renders exam interface with webcam and questions', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({ direction: 'Looking Forward' }),
      })
    );

    render(
      <BrowserRouter>
        <Exam />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/AI Proctored Exam/i)).toBeInTheDocument();
    });
  });

  test('displays questions and answer options', async () => {
    render(
      <BrowserRouter>
        <Exam />
      </BrowserRouter>
    );

    await waitFor(() => {
      // Check if question is displayed (questions are hardcoded in Exam.js)
      const questionElements = screen.queryAllByText(/What is/i);
      expect(questionElements.length).toBeGreaterThan(0);
    });
  });
});
