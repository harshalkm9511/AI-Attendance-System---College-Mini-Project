import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_RUNTIME_DIR = Path(os.getenv("TEMP", os.getenv("LOCALAPPDATA", str(BASE_DIR / ".runtime")))) / "AttendanceOS"
DEFAULT_INSTANCE_DIR = DEFAULT_RUNTIME_DIR / "instance"
DEFAULT_STORAGE_DIR = DEFAULT_RUNTIME_DIR / "storage"
LEGACY_ROOTS = [
    BASE_DIR,
    BASE_DIR / "data",
    BASE_DIR / "assets",
]


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-attendance-secret")
    DATA_DIR = Path(os.getenv("DATA_DIR", str(DEFAULT_RUNTIME_DIR)))
    DATABASE_PATH = Path(os.getenv("DATABASE_PATH", str(DEFAULT_INSTANCE_DIR / "attendance.sqlite3")))
    STORAGE_DIR = Path(os.getenv("STORAGE_DIR", str(DEFAULT_STORAGE_DIR)))
    LEGACY_ROOTS = LEGACY_ROOTS
    DEFAULT_TENANT_NAME = os.getenv("DEFAULT_TENANT_NAME", "Demo Institute")
    DEFAULT_TENANT_CODE = os.getenv("DEFAULT_TENANT_CODE", "demo-institute")
    DEFAULT_ADMIN_USERNAME = os.getenv("DEFAULT_ADMIN_USERNAME", "admin")
    DEFAULT_ADMIN_PASSWORD = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123")
