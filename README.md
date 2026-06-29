# AI Attendance System

A Flask-based AI attendance management system that supports teacher login, student enrollment with face data, classroom image-based attendance analysis, manual review before finalization, and session-wise attendance reporting.

## Current Stack

- Backend: Python, Flask
- Frontend: Flask templates, HTML, CSS
- Database: SQLite
- Recognition: OpenCV, optional DeepFace/FaceNet embeddings, cosine similarity
- Storage: Local filesystem for uploaded/student/session images

## Main Features

- Teacher authentication
- Student enrollment with face image quality validation
- Student management: create, view, edit, delete
- Attendance session creation from classroom image
- Face detection and recognition workflow
- Match classification: matched, uncertain, unknown
- Manual review before final attendance save
- Dashboard metrics and attendance reports
- Session-wise attendance history

## Project Structure

```text
attendance_platform/
  app.py
  auth.py
  config.py
  db.py
  routes/
  services/
  static/
  templates/
run.py
requirements.txt
tests/
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python run.py
```

4. Open the app in your browser:

```text
http://127.0.0.1:5000
```

## Default Behavior

On first startup, the application initializes the SQLite database automatically and seeds a default tenant/admin user from configuration defaults.

## Notes

- This repository contains only the current Flask-based attendance platform.
- Older prototype files are intentionally excluded from the GitHub upload.



cd "C:\Users\Lenovo\OneDrive\Desktop\Coding\projects\attendence system\frontend"
>> npm install
>> npm run dev

 cd "C:\Users\Lenovo\OneDrive\Desktop\Coding\projects\attendence system\backend"
>> .\venv\Scripts\Activate.ps1
>> uvicorn main:app --reload
