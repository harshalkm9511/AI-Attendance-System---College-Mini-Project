import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
RUNTIME_DIR = Path(os.getenv("TEMP", os.getenv("LOCALAPPDATA", str(BASE_DIR)))) / "AttendanceOS"
INSTANCE_DIR = RUNTIME_DIR / "instance"
STORAGE_DIR = RUNTIME_DIR / "storage"
LEGACY_ROOTS = [
    BASE_DIR,
    BASE_DIR / "data",
    BASE_DIR / "assets",
]


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-attendance-secret")
    DATABASE_PATH = INSTANCE_DIR / "attendance.sqlite3"
    STORAGE_DIR = STORAGE_DIR
    LEGACY_ROOTS = LEGACY_ROOTS
    DEFAULT_TENANT_NAME = os.getenv("DEFAULT_TENANT_NAME", "Demo Institute")
    DEFAULT_TENANT_CODE = os.getenv("DEFAULT_TENANT_CODE", "demo-institute")
    DEFAULT_ADMIN_USERNAME = os.getenv("DEFAULT_ADMIN_USERNAME", "admin")
    DEFAULT_ADMIN_PASSWORD = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123")
