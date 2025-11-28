#!/bin/bash

# ---- Start Backend ----
cd backend
python3 app.py &    # runs backend in background

# ---- Start Frontend ----
cd ../frontend
npm install         # install frontend dependencies
npm start           # start frontend
