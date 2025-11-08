# AI Proctor — Features

This document lists the available features in the NeuroProctor (AI Proctor) application.

## Overview
A modern online exam proctoring system that combines a React frontend with a Flask backend and AI/ML components to monitor exams in real-time and generate alerts for suspicious activity.

## Key Features

### Authentication & User
- Student login (username, roll number, password).
- Simple credential verification against the `students` collection in MongoDB.

### Exam & UI
- Exam interface (MCQ-style) on the frontend (React).
- Instruction pages and exam flow components.
- Proctor Dashboard for viewing alerts and analytics (React + Recharts).
- Fullscreen enforcement and auto-submit considerations (frontend behavior).

### Webcam & Face Handling
- Face registration endpoint to register a student's face before the exam.
- Live face verification endpoint to check if the current frame matches the registered user (simple presence/registered check).
- MediaPipe-based face detection and face mesh for head-pose estimation.
- Head pose detection that computes yaw, pitch, and roll and generates alerts when thresholds are exceeded (looking away / tilting).

### Object Detection
- YOLOv5 (Ultralytics) integration for object detection.
- Detects forbidden objects (configured: `cell phone`, `laptop`) and returns `forbidden_object` if detected.
- Model auto-download on first run if weights are not present (e.g., `yolov5n.pt` / `yolov5nu.pt`).

### Audio Anomaly Detection
- Endpoint to receive audio features (volume, frequency peaks, duration) and detect anomalies such as speech or loud noises.
- If an audio anomaly is detected, it logs an alert to the database.

### Alerts & Logging
- Alert logging to MongoDB (`alerts` collection) with timestamp and details.
- Endpoints to fetch alert history for display on the proctor dashboard.

### Backend Reliability & DB
- MongoDB Atlas integration (the current code uses a pre-configured Atlas connection string).
- DB initialization logic that creates `students` and `alerts` collections and sets useful indexes.
- Test endpoint to verify DB connection and return counts of collections and documents.

### Miscellaneous
- CORS enabled for cross-origin requests from the frontend dev server.
- In-memory set for registered faces (simple, non-persistent) used by the register/verify flow.

## API Endpoints (available in `backend/app.py`)
- `GET /test-connection` — Tests MongoDB connection and returns DB status and collection counts.
- `POST /login` — Verify user credentials (username, rollNumber, password) against `students`.
- `POST /register-face` — Register a face: accepts `roll_number` and `image` (multipart form). Returns `registered`, `no_face`, or `multiple_faces`.
- `POST /verify-face` — Verify a face: accepts `roll_number` and `image` and returns `match`, `mismatch`, `no_face`, or `multiple_faces`.
- `POST /detect-head` — Head pose detection: accepts an `image` and returns `direction`, `yaw`, `pitch`, `roll`.
- `POST /detect-object` — Object detection via YOLO: accepts an `image` and returns `status: forbidden_object|clear` and object list.
- `POST /detect-audio-anomaly` — Accepts JSON audio features and returns `anomaly_detected` or `clear` with details.
- `POST /log-alert` — Generic alert logging endpoint; stores alerts in DB.
- `GET /alerts` — Fetches all alerts, sorted by alert time (descending).
- `GET /registered-faces` — Returns the in-memory list of registered faces.

## Frontend (short)
- React app created with Create React App (scripts in `frontend/package.json`).
- Uses `react-webcam` for video capture and `recharts` for visualizations on the dashboard.
- Main components: `Login`, `Instruction`, `Exam`, `ProctorDashboard`, and `NotFound`.

## Tech stack
- Frontend: React, Bootstrap, React Webcam, Recharts.
- Backend: Flask, Flask-CORS, OpenCV, MediaPipe, Ultralytics YOLO (via `ultralytics` package).
- Database: MongoDB (Atlas in current config).
- Languages: Python (backend), JavaScript (frontend).

## Notes & Recommendations
- Security: The repository currently contains a hard-coded MongoDB Atlas URI. Move secrets to environment variables and rotate credentials before production use.
- Persistence: Face registration is currently in-memory; to persist registered faces across restarts, implement persistent storage (e.g., add to `students` collection or separate collection).
- Performance: YOLO and MediaPipe initialization can be CPU and memory intensive; consider model selection and hardware acceleration for production.

## Where to look in the repo
- Backend main file: `backend/app.py` (API and ML logic).
- Backend deps: `backend/requirements.txt`.
- Frontend entry + components: `frontend/src/` and `frontend/package.json`.


_Last updated: generated automatically_
