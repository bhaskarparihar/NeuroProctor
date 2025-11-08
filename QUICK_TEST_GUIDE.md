# Quick Start Guide - AI Proctor

## Backend Testing

### Run All Tests
```bash
cd testing/backend
pytest
```

### Run Specific Test Files
```bash
# Authentication tests
pytest test_auth.py

# API tests
pytest test_api.py

# Detection tests
pytest test_detection.py
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in your browser
```

## Frontend Testing

### Run All Tests
```bash
cd frontend
npm test
```

### Run Tests Once (No Watch Mode)
```bash
npm test -- --watchAll=false
```

### Run with Coverage
```bash
npm test -- --coverage --watchAll=false
```

## Teacher Login Credentials

The following teacher accounts are available in MongoDB:

- **Username:** `admin` | **Password:** `admin123` | **Role:** Admin
- **Username:** `teacher1` | **Password:** `teacher123` | **Role:** Teacher
- **Username:** `proctor` | **Password:** `proctor123` | **Role:** Proctor

## Student Test Account

- **Username:** `test_student`
- **Roll Number:** `12345`
- **Password:** `password123`

## Common Issues

### Backend Tests Fail with MongoDB Connection Error
- Ensure MongoDB Atlas is accessible
- Check internet connection
- Verify MONGO_URI in `backend/app.py`

### Frontend Tests Fail with Module Not Found
```bash
cd frontend
npm install
```

### MediaPipe/OpenCV Errors in Tests
- Some detection tests may show warnings
- Tests will still pass/fail correctly
- These warnings can be ignored in test environment

## Full Test Suite

Run all tests (backend + frontend):

```bash
# Backend
cd testing/backend
pytest

# Frontend
cd frontend
npm test -- --watchAll=false
```

For detailed testing documentation, see [TESTING.md](TESTING.md)
