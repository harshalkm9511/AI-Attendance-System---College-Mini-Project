import tempfile
import unittest
from pathlib import Path

from attendance_platform.db import get_db
from attendance_platform.app import create_app


class AttendanceAppTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.app = create_app(
            {
                "TESTING": True,
                "DATABASE_PATH": Path(self.temp_dir.name) / "test.sqlite3",
                "STORAGE_DIR": Path(self.temp_dir.name) / "storage",
            }
        )
        self.app.config.update(
            TESTING=True,
            DATABASE_PATH=Path(self.temp_dir.name) / "test.sqlite3",
            STORAGE_DIR=Path(self.temp_dir.name) / "storage",
        )
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

    def test_dashboard_loads_without_login(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dashboard", response.data)

    def test_local_mode_uses_default_user_context(self):
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student Attendance Analysis", response.data)
        self.assertIn(b"Local Mode", response.data)

    def test_delete_student_route_removes_student(self):
        with self.app.app_context():
            db = get_db()
            db.execute(
                """
                INSERT INTO students (tenant_id, name, roll_no, department, section_name, is_active, created_at, updated_at)
                VALUES (1, 'Test User', 'T1', '', '', 1, '2026-01-01T00:00:00', '2026-01-01T00:00:00')
                """
            )
            db.commit()
            student_id = db.execute("SELECT id FROM students WHERE roll_no = 'T1'").fetchone()[0]

        response = self.client.post(f"/students/{student_id}/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student deleted successfully.", response.data)

        with self.app.app_context():
            db = get_db()
            remaining = db.execute("SELECT COUNT(*) FROM students WHERE roll_no = 'T1'").fetchone()[0]
            self.assertEqual(remaining, 0)

    def test_create_student_route_accepts_valid_image(self):
        import io
        sample_path = Path("students") / "33_Harshal_Mahajan.jpg"
        self.assertTrue(sample_path.exists())
        response = self.client.post(
            "/students/new",
            data={
                "name": "Route Student",
                "roll_no": "R100",
                "department": "Test",
                "section_name": "A",
                "image": (io.BytesIO(sample_path.read_bytes()), "student.jpg"),
            },
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student enrolled successfully.", response.data)


if __name__ == "__main__":
    unittest.main()
