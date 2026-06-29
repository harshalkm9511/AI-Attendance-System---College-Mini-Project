from __future__ import annotations

import shutil
from pathlib import Path

import cv2
import pandas as pd
from flask import current_app

from ..db import query_one, transaction, utcnow
from .recognition import RecognitionEngine


def to_storage_ref(path: Path) -> str:
    return path.as_posix()


def resolve_legacy_path(raw_path: str) -> Path | None:
    if not raw_path:
        return None
    candidate = Path(raw_path)
    if candidate.is_absolute() and candidate.exists():
        return candidate
    for root in current_app.config["LEGACY_ROOTS"]:
        joined = Path(root) / raw_path
        if joined.exists():
            return joined
    return None


def migrate_if_needed() -> None:
    tenant = query_one("SELECT * FROM tenants WHERE code = ?", (current_app.config["DEFAULT_TENANT_CODE"],))
    student_count = query_one("SELECT COUNT(*) AS count FROM students WHERE tenant_id = ?", (tenant["id"],))
    if student_count["count"] > 0:
        return

    engine = RecognitionEngine(current_app.config["STORAGE_DIR"])
    candidate_csvs = [
        current_app.config["LEGACY_ROOTS"][0] / "students.csv",
        current_app.config["LEGACY_ROOTS"][1] / "students.csv",
    ]

    imported_rolls = set()
    for csv_path in candidate_csvs:
        if not csv_path.exists():
            continue
        try:
            df = pd.read_csv(csv_path)
        except Exception:
            continue

        for _, row in df.iterrows():
            roll_no = str(row.get("Roll No", "")).strip()
            name = str(row.get("Name", "")).strip()
            if not roll_no or not name or roll_no in imported_rolls:
                continue

            image_path = resolve_legacy_path(str(row.get("Image Path", "")).strip())
            if image_path is None or not image_path.exists():
                continue

            image_bgr = cv2.imread(str(image_path))
            if image_bgr is None:
                continue

            report = engine.assess_enrollment_image(image_bgr)
            if not report.is_usable:
                continue

            box = engine.detect_faces(image_bgr, min_size=(40, 40))[0]
            face_bgr = engine.crop_face(image_bgr, box)
            embedding, provider = engine.build_embedding(face_bgr)
            imported_rolls.add(roll_no)

            with transaction() as db:
                now = utcnow()
                student_cursor = db.execute(
                    """
                    INSERT INTO students (tenant_id, name, roll_no, department, section_name, is_active, created_at, updated_at)
                    VALUES (?, ?, ?, '', '', 1, ?, ?)
                    """,
                    (tenant["id"], name, roll_no, now, now),
                )
                student_id = student_cursor.lastrowid

                student_dir = current_app.config["STORAGE_DIR"] / "tenants" / str(tenant["id"]) / "students" / str(student_id)
                student_dir.mkdir(parents=True, exist_ok=True)
                original_copy = student_dir / f"legacy_{image_path.name}"
                face_copy = student_dir / f"legacy_face_{image_path.name}"
                shutil.copy2(image_path, original_copy)
                cv2.imwrite(str(face_copy), face_bgr)

                db.execute(
                    """
                    INSERT INTO student_images (student_id, file_path, face_path, embedding_json, embedding_provider, quality_score, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        student_id,
                        to_storage_ref(original_copy.relative_to(current_app.config["STORAGE_DIR"])),
                        to_storage_ref(face_copy.relative_to(current_app.config["STORAGE_DIR"])),
                        engine.dumps_embedding(embedding),
                        provider,
                        report.score,
                        now,
                    ),
                )
