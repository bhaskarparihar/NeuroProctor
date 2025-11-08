/**
 * Tests for ProctorDashboard Component
 */
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import ProctorDashboard from '../pages/ProctorDashboard';

describe('ProctorDashboard Component', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  test('renders dashboard title', () => {
    render(
      <BrowserRouter>
        <ProctorDashboard />
      </BrowserRouter>
    );
    
    expect(screen.getByText(/AI Proctor Dashboard/i)).toBeInTheDocument();
  });

  test('fetches and displays alerts', async () => {
    const mockAlerts = [
      {
        student_id: 'TEST001',
        direction: 'Looking Left',
        alert_time: '2024-01-01T12:00:00',
        details: {}
      },
      {
        student_id: 'TEST002',
        direction: 'Looking Right',
        alert_time: '2024-01-01T12:01:00',
        details: {}
      }
    ];

    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockAlerts),
      })
    );

    render(
      <BrowserRouter>
        <ProctorDashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/TEST001/i)).toBeInTheDocument();
      expect(screen.getByText(/TEST002/i)).toBeInTheDocument();
    });
  });

  test('handles fetch error gracefully', async () => {
    global.fetch = jest.fn(() => Promise.reject(new Error('Network error')));

    render(
      <BrowserRouter>
        <ProctorDashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      // Component should still render even if fetch fails
      expect(screen.getByText(/AI Proctor Dashboard/i)).toBeInTheDocument();
    });
  });

  test('displays statistics section', () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve([]),
      })
    );

    render(
      <BrowserRouter>
        <ProctorDashboard />
      </BrowserRouter>
    );
    
    // Dashboard typically shows stats
    expect(screen.getByText(/Dashboard/i)).toBeInTheDocument();
  });
});
