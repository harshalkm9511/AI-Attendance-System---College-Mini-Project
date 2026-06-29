# AI Attendance System

A Flask-based AI attendance management system that supports teacher login, student enrollment with face data, classroom image-based attendance analysis, manual review before finalization, and session-wise attendance reporting.

## Current Stack

- Backend: Python, Flask
- Frontend: Flask templates, HTML, CSS
- Database: SQLite
- Recognition: OpenCV with an optional DeepFace fallback when available
- Storage: Filesystem-backed SQLite and image storage

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

## Deployment

This repository is configured for Render deployment via `render.yaml`.

- Web start command: `gunicorn --workers 1 --threads 4 --timeout 120 run:app`
- Persistent storage: mounted at `/var/data`
- Flask entrypoint: `run:app`
- Python version: `3.12.7`
- Required environment variables:
  - `SECRET_KEY`
  - `DEFAULT_TENANT_NAME`
  - `DEFAULT_TENANT_CODE`
  - `DEFAULT_ADMIN_USERNAME`
  - `DEFAULT_ADMIN_PASSWORD`
  - `DATA_DIR`
  - `DATABASE_PATH`
  - `STORAGE_DIR`

## Default Behavior

On first startup, the application initializes the SQLite database automatically and seeds a default tenant/admin user from configuration defaults.

## Notes

- The old Streamlit prototype is intentionally ignored for deployment.
- The Flask app stores uploaded images and the SQLite database on the configured filesystem path, so a persistent disk is required in production.
