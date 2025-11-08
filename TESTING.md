# Testing Documentation - AI Proctor

This document provides comprehensive information about testing the AI Proctor application, including both backend and frontend tests.

## Table of Contents
- [Overview](#overview)
- [Backend Testing](#backend-testing)
- [Frontend Testing](#frontend-testing)
- [Test Coverage](#test-coverage)
- [Continuous Integration](#continuous-integration)

---

## Overview

The AI Proctor application has comprehensive test suites for both backend (Python/Flask) and frontend (React) components. Tests ensure reliability, catch regressions early, and validate all critical features including authentication, AI detection systems, and user interfaces.

### Testing Stack

**Backend:**
- **pytest** - Testing framework
- **pytest-flask** - Flask-specific testing utilities
- **pytest-cov** - Code coverage reporting

**Frontend:**
- **Jest** - JavaScript testing framework
- **React Testing Library** - React component testing
- **@testing-library/jest-dom** - Custom DOM matchers

---

## Backend Testing

### Setup

1. **Install Testing Dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

   This installs:
   - `pytest==7.4.3`
   - `pytest-flask==1.3.0`
   - `pytest-cov==4.1.0`

2. **Verify Installation:**
   ```bash
   pytest --version
   ```

### Running Backend Tests

#### Run All Tests
```bash
cd testing/backend
pytest
```

#### Run Specific Test Files
```bash
# Authentication tests only
pytest test_auth.py

# API endpoint tests only
pytest test_api.py

# Detection system tests only
pytest test_detection.py
```

#### Run Tests with Verbose Output
```bash
pytest -v
```

#### Run Tests with Coverage Report
```bash
pytest --cov=app --cov-report=html
```

This generates an HTML coverage report in `htmlcov/index.html`.

#### Run Specific Test Classes or Functions
```bash
# Run specific test class
pytest test_auth.py::TestStudentAuth

# Run specific test function
pytest test_auth.py::TestStudentAuth::test_student_login_success
```

### Backend Test Structure

```
testing/
├── backend/
│   ├── __init__.py          # Test module initialization
│   ├── conftest.py          # Pytest fixtures and configuration
│   ├── pytest.ini           # Pytest configuration
│   ├── test_auth.py         # Authentication tests
│   ├── test_api.py          # API endpoint tests
│   └── test_detection.py    # AI detection system tests
└── app.py                   # Main application
```

### Backend Test Coverage

#### 1. Authentication Tests (`test_auth.py`)

**Student Authentication:**
- ✅ Successful login with valid credentials
- ✅ Failed login with invalid credentials
- ✅ Missing required fields handling
- ✅ Database connection error handling

**Teacher Authentication:**
- ✅ Successful teacher login with MongoDB credentials
- ✅ Failed login with invalid teacher credentials
- ✅ Missing username or password handling
- ✅ Non-JSON request handling
- ✅ Password hashing verification

#### 2. API Endpoint Tests (`test_api.py`)

**Alerts API:**
- ✅ GET `/alerts` - Retrieve all alerts
- ✅ POST `/log-alert` - Log new alert with all required fields
- ✅ POST `/log-alert` - Handle missing data
- ✅ Validate alert data structure

**Connection & Status:**
- ✅ GET `/test-connection` - MongoDB connection test
- ✅ GET `/registered-faces` - Retrieve registered faces list
- ✅ Database status reporting

#### 3. Detection System Tests (`test_detection.py`)

**Head Pose Detection:**
- ✅ POST `/detect-head` - Endpoint exists and responds
- ✅ Detect head pose with face in image
- ✅ Handle images with no face detected
- ✅ Return yaw, pitch, roll values

**Face Registration & Verification:**
- ✅ POST `/register-face` - Register new face
- ✅ POST `/verify-face` - Verify existing face
- ✅ Handle images with no faces
- ✅ Handle images with multiple faces

**Object Detection:**
- ✅ POST `/detect-object` - Detect forbidden objects
- ✅ Clear status for allowed items
- ✅ Alert for cell phones, laptops
- ✅ Return confidence scores

**Audio Anomaly Detection:**
- ✅ POST `/detect-audio-anomaly` - Normal audio (clear status)
- ✅ Detect suspicious audio patterns
- ✅ High volume level detection
- ✅ Speech pattern recognition
- ✅ Handle missing audio data

### Backend Test Fixtures

Defined in `conftest.py`:

```python
@pytest.fixture
def app()        # Flask app instance for testing

@pytest.fixture
def client(app)  # Test client for making requests

@pytest.fixture
def runner(app)  # CLI test runner

@pytest.fixture
def db()         # MongoDB connection for test data
```

---

## Frontend Testing

### Setup

1. **Install Testing Dependencies:**
   ```bash
   cd frontend
   npm install
   ```

   Testing libraries are already in `package.json`:
   - `@testing-library/react`
   - `@testing-library/jest-dom`
   - `@testing-library/user-event`

2. **Verify Setup:**
   ```bash
   npm test -- --version
   ```

### Running Frontend Tests

#### Run All Tests
```bash
cd frontend
npm test
```

#### Run Tests in CI Mode (Non-Interactive)
```bash
npm test -- --watchAll=false
```

#### Run Tests with Coverage
```bash
npm test -- --coverage --watchAll=false
```

#### Run Specific Test File
```bash
npm test -- Login.test.js
```

#### Update Snapshots
```bash
npm test -- -u
```

### Frontend Test Structure

```
testing/
├── frontend/
│   ├── Login.test.js            # Student login tests
│   ├── TeacherLogin.test.js     # Teacher login tests
│   ├── Exam.test.js             # Exam component tests
│   ├── ProctorDashboard.test.js # Dashboard tests
│   └── setupTests.js            # Jest configuration
│   └── components/                  # Components being tested
└── package.json
```

### Frontend Test Coverage

#### 1. Login Component Tests (`Login.test.js`)

- ✅ Renders all form fields (username, roll number, password)
- ✅ Displays submit button
- ✅ Shows teacher login link
- ✅ Navigates to teacher login on link click
- ✅ Successful login navigates to `/instruction`
- ✅ Failed login displays error message
- ✅ Network error handling with error display
- ✅ Form validation
- ✅ Loading state during submission

#### 2. Teacher Login Component Tests (`TeacherLogin.test.js`)

- ✅ Renders teacher login form
- ✅ Shows username and password fields
- ✅ Successful login stores credentials in localStorage
- ✅ Successful login navigates to `/proctor-dashboard`
- ✅ Failed login displays error message
- ✅ Navigation back to student login
- ✅ Form submission handling
- ✅ Loading state management

#### 3. Exam Component Tests (`Exam.test.js`)

- ✅ Redirects to login if no roll number in localStorage
- ✅ Renders exam interface with webcam
- ✅ Displays questions and answer options
- ✅ Handles multiple choice selection
- ✅ Webcam mock functionality
- ✅ Navigation between questions
- ✅ Exam submission

#### 4. Proctor Dashboard Tests (`ProctorDashboard.test.js`)

- ✅ Renders dashboard title
- ✅ Fetches and displays alerts from API
- ✅ Shows student IDs and alert details
- ✅ Handles fetch errors gracefully
- ✅ Displays statistics section
- ✅ Real-time data updates
- ✅ Alert filtering and sorting

### Test Utilities

#### Setup Tests (`setupTests.js`)

Configures the testing environment:
- Imports `@testing-library/jest-dom` for custom matchers
- Mocks `localStorage` for testing
- Mocks `window.matchMedia` for responsive tests
- Suppresses console errors in test output

#### Common Test Patterns

**Mocking Navigation:**
```javascript
const mockedNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedNavigate,
}));
```

**Mocking Fetch:**
```javascript
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({ message: 'Success' }),
  })
);
```

**Testing User Interactions:**
```javascript
fireEvent.change(input, { target: { value: 'test' } });
fireEvent.click(button);
await waitFor(() => {
  expect(mockFunction).toHaveBeenCalled();
});
```

---

## Test Coverage

### Current Coverage Goals

**Backend:**
- Authentication: 95%+ coverage
- API endpoints: 90%+ coverage
- Detection systems: 85%+ coverage

**Frontend:**
- Components: 80%+ coverage
- User interactions: 85%+ coverage
- Navigation: 90%+ coverage

### Viewing Coverage Reports

**Backend:**
```bash
cd backend
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

**Frontend:**
```bash
cd frontend
npm test -- --coverage --watchAll=false
# Coverage summary displayed in terminal
# HTML report in coverage/lcov-report/index.html
```

---

## Continuous Integration

### Recommended CI Pipeline

```yaml
# Example GitHub Actions workflow

name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run tests
        run: |
          cd frontend
          npm test -- --coverage --watchAll=false
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## Writing New Tests

### Backend Test Template

```python
"""
Test description
"""
import pytest
import json

class TestNewFeature:
    """Test cases for new feature"""
    
    def test_feature_success(self, client):
        """Test successful feature execution"""
        response = client.post('/endpoint',
            data=json.dumps({"key": "value"}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
    
    def test_feature_failure(self, client):
        """Test feature error handling"""
        response = client.post('/endpoint',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
```

### Frontend Test Template

```javascript
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import NewComponent from '../components/NewComponent';

describe('NewComponent', () => {
  test('renders component', () => {
    render(
      <BrowserRouter>
        <NewComponent />
      </BrowserRouter>
    );
    
    expect(screen.getByText(/Expected Text/i)).toBeInTheDocument();
  });
  
  test('handles user interaction', async () => {
    render(
      <BrowserRouter>
        <NewComponent />
      </BrowserRouter>
    );
    
    const button = screen.getByRole('button');
    fireEvent.click(button);
    
    await waitFor(() => {
      expect(screen.getByText(/Result/i)).toBeInTheDocument();
    });
  });
});
```

---

## Troubleshooting

### Common Issues

**Backend:**

1. **Import errors:**
   ```bash
   # Ensure you're in the backend directory
   cd backend
   pytest
   ```

2. **Database connection errors:**
   - Tests use the same MongoDB connection as the app
   - Ensure MongoDB is accessible
   - Check `MONGO_URI` in `app.py`

3. **MediaPipe/OpenCV errors:**
   - Some detection tests may fail without proper video drivers
   - Run with `-v` flag to see detailed errors

**Frontend:**

1. **Module not found:**
   ```bash
   # Reinstall dependencies
   rm -rf node_modules package-lock.json
   npm install
   ```

2. **React version compatibility:**
   - Tests are configured for React 19
   - Check `setupTests.js` for compatibility settings

3. **Webcam mock errors:**
   - Tests mock `react-webcam` component
   - Ensure mock is properly configured in test files

---

## Test Maintenance

### Best Practices

1. **Keep tests isolated** - Each test should be independent
2. **Use descriptive names** - Test names should explain what they test
3. **Test one thing** - Each test should validate a single behavior
4. **Clean up** - Use fixtures and cleanup functions
5. **Update tests** - When features change, update corresponding tests
6. **Monitor coverage** - Aim for high coverage but prioritize critical paths

### Regular Maintenance Tasks

- [ ] Run full test suite before major releases
- [ ] Update snapshots when UI intentionally changes
- [ ] Review and update test data (mock users, sample alerts)
- [ ] Check for deprecated testing libraries
- [ ] Update test documentation when adding features

---

## Quick Reference

### Backend Commands
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_auth.py::TestTeacherAuth::test_teacher_login_success

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

### Frontend Commands
```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage --watchAll=false

# Run specific test
npm test -- Login.test.js

# Update snapshots
npm test -- -u

# CI mode
npm test -- --watchAll=false
```

---

## Contact & Support

For questions about testing:
- Review this documentation
- Check test files for examples
- Consult pytest/Jest documentation
- Review GitHub issues for similar problems

---

**Last Updated:** November 2025
**Maintained By:** AI Proctor Development Team
