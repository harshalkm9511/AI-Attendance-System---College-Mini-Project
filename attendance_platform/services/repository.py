from __future__ import annotations

import json
import shutil
from pathlib import Path

import cv2
import numpy as np
from flask import current_app

from ..db import get_db, log_action, query_all, query_one, transaction, utcnow
from .recognition import RecognitionEngine


def to_storage_ref(path: Path) -> str:
    return path.as_posix()


def tenant_storage_root(tenant_id: int) -> Path:
    root = Path(current_app.config["STORAGE_DIR"]) / "tenants" / str(tenant_id)
    root.mkdir(parents=True, exist_ok=True)
    return root


def list_students(tenant_id: int) -> list[dict]:
    students = query_all(
        """
        SELECT students.*, COUNT(student_images.id) AS image_count
        FROM students
        LEFT JOIN student_images ON student_images.student_id = students.id
        WHERE students.tenant_id = ? AND students.is_active = 1
        GROUP BY students.id
        ORDER BY students.name
        """,
        (tenant_id,),
    )
    for student in students:
        student["latest_face_path"] = query_one(
            "SELECT face_path FROM student_images WHERE student_id = ? ORDER BY id DESC LIMIT 1",
            (student["id"],),
        )
    return students


def get_student(student_id: int, tenant_id: int) -> dict | None:
    student = query_one("SELECT * FROM students WHERE id = ? AND tenant_id = ?", (student_id, tenant_id))
    if student is None:
        return None
    student["images"] = query_all("SELECT * FROM student_images WHERE student_id = ? ORDER BY id DESC", (student_id,))
    return student


def update_student(
    tenant_id: int,
    user_id: int | None,
    student_id: int,
    name: str,
    roll_no: str,
    department: str,
    section_name: str,
) -> tuple[bool, str]:
    student = get_student(student_id, tenant_id)
    if student is None:
        return False, "Student not found."
    if not name or not roll_no:
        return False, "Name and roll number are required."

    existing = query_one(
        "SELECT id FROM students WHERE tenant_id = ? AND roll_no = ? AND is_active = 1 AND id != ?",
        (tenant_id, roll_no, student_id),
    )
    if existing is not None:
        return False, "Roll number already exists in this tenant."

    db = get_db()
    db.execute(
        """
        UPDATE students
        SET name = ?, roll_no = ?, department = ?, section_name = ?, updated_at = ?
        WHERE id = ? AND tenant_id = ?
        """,
        (name, roll_no, department, section_name, utcnow(), student_id, tenant_id),
    )
    db.commit()
    log_action(tenant_id, user_id, "student.updated", "student", student_id, {"name": name, "roll_no": roll_no})
    return True, "Student updated successfully."


def save_student_with_image(
    tenant_id: int,
    user_id: int | None,
    name: str,
    roll_no: str,
    department: str,
    section_name: str,
    uploaded_bytes: bytes,
    filename: str,
) -> tuple[bool, str]:
    if not name or not roll_no:
        return False, "Name and roll number are required."

    existing = query_one("SELECT id FROM students WHERE tenant_id = ? AND roll_no = ? AND is_active = 1", (tenant_id, roll_no))
    if existing is not None:
        return False, "Roll number already exists in this tenant."

    temp_image = cv2.imdecode(np.frombuffer(uploaded_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
    if temp_image is None:
        return False, "Unable to read the uploaded image."

    engine = RecognitionEngine(current_app.config["STORAGE_DIR"])
    report = engine.assess_enrollment_image(temp_image)
    if not report.is_usable:
        return False, report.message

    box = engine.detect_faces(temp_image, min_size=(40, 40))[0]
    face_bgr = engine.crop_face(temp_image, box)
    embedding, provider = engine.build_embedding(face_bgr)

    with transaction() as db:
        now = utcnow()
        student_cursor = db.execute(
            """
            INSERT INTO students (tenant_id, name, roll_no, department, section_name, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 1, ?, ?)
            """,
            (tenant_id, name, roll_no, department, section_name, now, now),
        )
        student_id = student_cursor.lastrowid

        student_dir = tenant_storage_root(tenant_id) / "students" / str(student_id)
        student_dir.mkdir(parents=True, exist_ok=True)
        safe_name = Path(filename).name or f"student_{student_id}.jpg"
        original_path = student_dir / f"original_{safe_name}"
        face_path = student_dir / f"face_{safe_name}"
        original_path.write_bytes(uploaded_bytes)
        cv2.imwrite(str(face_path), face_bgr)

        db.execute(
            """
            INSERT INTO student_images (student_id, file_path, face_path, embedding_json, embedding_provider, quality_score, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student_id,
                to_storage_ref(original_path.relative_to(current_app.config["STORAGE_DIR"])),
                to_storage_ref(face_path.relative_to(current_app.config["STORAGE_DIR"])),
                engine.dumps_embedding(embedding),
                provider,
                report.score,
                now,
            ),
        )

    log_action(tenant_id, user_id, "student.created", "student", student_id, {"name": name, "roll_no": roll_no})
    return True, "Student enrolled successfully."


def archive_student(tenant_id: int, user_id: int | None, student_id: int) -> None:
    db = get_db()
    db.execute(
        "UPDATE students SET is_active = 0, updated_at = ? WHERE id = ? AND tenant_id = ?",
        (utcnow(), student_id, tenant_id),
    )
    db.commit()
    log_action(tenant_id, user_id, "student.archived", "student", student_id, {})


def delete_student(tenant_id: int, user_id: int | None, student_id: int) -> tuple[bool, str]:
    student = get_student(student_id, tenant_id)
    if student is None:
        return False, "Student not found."

    student_dir = tenant_storage_root(tenant_id) / "students" / str(student_id)
    with transaction() as db:
        db.execute("DELETE FROM attendance_records WHERE student_id = ?", (student_id,))
        db.execute("DELETE FROM detected_faces WHERE best_student_id = ? OR reviewed_student_id = ?", (student_id, student_id))
        db.execute("DELETE FROM student_images WHERE student_id = ?", (student_id,))
        db.execute("DELETE FROM students WHERE id = ? AND tenant_id = ?", (student_id, tenant_id))

    if student_dir.exists():
        shutil.rmtree(student_dir, ignore_errors=True)

    log_action(tenant_id, user_id, "student.deleted", "student", student_id, {"name": student["name"], "roll_no": student["roll_no"]})
    return True, "Student deleted successfully."


def analyze_attendance(tenant_id: int, user_id: int | None, title: str, uploaded_bytes: bytes, filename: str) -> tuple[bool, str, int | None]:
    image_bgr = cv2.imdecode(np.frombuffer(uploaded_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
    if image_bgr is None:
        return False, "Unable to read the uploaded classroom image.", None

    engine = RecognitionEngine(current_app.config["STORAGE_DIR"])
    boxes = engine.detect_faces(image_bgr)
    if not boxes:
        return False, "No faces were detected in the classroom image.", None

    students = query_all(
        """
        SELECT students.id, students.name, students.roll_no, student_images.embedding_json, student_images.embedding_provider
        FROM students
        JOIN student_images ON student_images.student_id = students.id
        WHERE students.tenant_id = ? AND students.is_active = 1
        ORDER BY students.name, student_images.id DESC
        """,
        (tenant_id,),
    )
    embeddings_by_student: dict[int, list[dict]] = {}
    for row in students:
        embeddings_by_student.setdefault(row["id"], []).append(row)

    tenant_root = tenant_storage_root(tenant_id)
    now = utcnow()
    session_dir = tenant_root / "sessions" / now.replace(":", "-")
    session_dir.mkdir(parents=True, exist_ok=True)
    classroom_path = session_dir / f"classroom_{Path(filename).name}"
    classroom_path.write_bytes(uploaded_bytes)

    annotated = engine.annotate_image(image_bgr, boxes)
    annotated_path = session_dir / f"annotated_{Path(filename).name}"
    cv2.imwrite(str(annotated_path), annotated)

    detections = []
    for index, box in enumerate(boxes, start=1):
        face_bgr = engine.crop_face(image_bgr, box)
        face_path = session_dir / f"face_{index}.jpg"
        cv2.imwrite(str(face_path), face_bgr)
        embedding, provider = engine.build_embedding(face_bgr)
        best_student_id = None
        best_score = 0.0
        best_status = "unknown"

        for student_id, variants in embeddings_by_student.items():
            for variant in variants:
                ref_embedding = engine.loads_embedding(variant["embedding_json"])
                score = engine.similarity(embedding, ref_embedding)
                if score > best_score:
                    best_score = score
                    best_student_id = student_id
                    best_status = engine.classify_similarity(score, provider)

        detections.append(
            {
                "face_index": index,
                "bbox_json": json.dumps({"x": box[0], "y": box[1], "w": box[2], "h": box[3]}),
                "face_path": to_storage_ref(face_path.relative_to(current_app.config["STORAGE_DIR"])),
                "embedding_json": engine.dumps_embedding(embedding),
                "embedding_provider": provider,
                "best_student_id": best_student_id if best_status != "unknown" else None,
                "match_score": best_score,
                "status": best_status,
            }
        )

    matched_candidates = sorted(
        [d for d in detections if d["best_student_id"] is not None],
        key=lambda item: item["match_score"],
        reverse=True,
    )
    claimed_students = set()
    for detection in matched_candidates:
        if detection["best_student_id"] in claimed_students:
            detection["status"] = "uncertain"
        elif detection["status"] == "matched":
            claimed_students.add(detection["best_student_id"])

    with transaction() as db:
        session_cursor = db.execute(
            """
            INSERT INTO attendance_sessions (
                tenant_id, title, classroom_image_path, annotated_image_path, status,
                faces_detected, matched_count, uncertain_count, unknown_count, created_by, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tenant_id,
                title,
                to_storage_ref(classroom_path.relative_to(current_app.config["STORAGE_DIR"])),
                to_storage_ref(annotated_path.relative_to(current_app.config["STORAGE_DIR"])),
                "draft",
                len(detections),
                sum(1 for d in detections if d["status"] == "matched"),
                sum(1 for d in detections if d["status"] == "uncertain"),
                sum(1 for d in detections if d["status"] == "unknown"),
                user_id,
                now,
            ),
        )
        session_id = session_cursor.lastrowid
        for detection in detections:
            db.execute(
                """
                INSERT INTO detected_faces (
                    session_id, face_index, bbox_json, face_path, embedding_json, embedding_provider,
                    best_student_id, match_score, status, reviewed_student_id, review_notes, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '', ?)
                """,
                (
                    session_id,
                    detection["face_index"],
                    detection["bbox_json"],
                    detection["face_path"],
                    detection["embedding_json"],
                    detection["embedding_provider"],
                    detection["best_student_id"],
                    detection["match_score"],
                    detection["status"],
                    detection["best_student_id"] if detection["status"] == "matched" else None,
                    now,
                ),
            )

    log_action(tenant_id, user_id, "attendance.analyzed", "attendance_session", session_id, {"title": title, "faces": len(detections)})
    return True, "Attendance analysis completed.", session_id


def get_session(session_id: int, tenant_id: int) -> dict | None:
    session_row = query_one("SELECT * FROM attendance_sessions WHERE id = ? AND tenant_id = ?", (session_id, tenant_id))
    if session_row is None:
        return None
    detections = query_all(
        """
        SELECT detected_faces.*,
               students.name AS best_student_name,
               students.roll_no AS best_student_roll,
               reviewed_students.name AS reviewed_student_name,
               reviewed_students.roll_no AS reviewed_student_roll
        FROM detected_faces
        LEFT JOIN students ON students.id = detected_faces.best_student_id
        LEFT JOIN students AS reviewed_students ON reviewed_students.id = detected_faces.reviewed_student_id
        WHERE detected_faces.session_id = ?
        ORDER BY detected_faces.face_index
        """,
        (session_id,),
    )
    session_row["detections"] = detections
    session_row["students"] = query_all(
        "SELECT id, name, roll_no FROM students WHERE tenant_id = ? AND is_active = 1 ORDER BY name",
        (tenant_id,),
    )
    return session_row


def finalize_attendance_session(tenant_id: int, user_id: int | None, session_id: int, decisions: dict[int, int | None]) -> tuple[bool, str]:
    session_row = get_session(session_id, tenant_id)
    if session_row is None:
        return False, "Attendance session not found."
    if session_row["status"] == "finalized":
        return False, "Attendance session is already finalized."

    detection_ids = {int(detection["id"]) for detection in session_row["detections"]}
    invalid_keys = set(decisions.keys()) - detection_ids
    if invalid_keys:
        return False, "Invalid face review selection submitted."

    used_students = set()
    for student_id in decisions.values():
        if student_id is None:
            continue
        if student_id in used_students:
            return False, "A student cannot be assigned to multiple faces in the same session."
        used_students.add(student_id)

    with transaction() as db:
        db.execute("DELETE FROM attendance_records WHERE session_id = ?", (session_id,))
        for detection in session_row["detections"]:
            chosen_student = decisions.get(int(detection["id"]))
            status = "unknown"
            notes = ""
            confidence = 0.0
            if chosen_student is not None:
                confidence = float(detection["match_score"])
                if detection["best_student_id"] == chosen_student and detection["status"] == "matched":
                    status = "matched"
                else:
                    status = "manual_override"
                    notes = "Reviewed by operator before finalization."
                db.execute(
                    """
                    INSERT INTO attendance_records (session_id, student_id, status, confidence, marked_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (session_id, chosen_student, "present", confidence, utcnow()),
                )

            db.execute(
                "UPDATE detected_faces SET reviewed_student_id = ?, status = ?, review_notes = ? WHERE id = ?",
                (chosen_student, status, notes, detection["id"]),
            )

        present_ids = [student_id for student_id in decisions.values() if student_id is not None]
        all_students = query_all("SELECT id FROM students WHERE tenant_id = ? AND is_active = 1", (tenant_id,))
        for student in all_students:
            if student["id"] not in present_ids:
                db.execute(
                    """
                    INSERT INTO attendance_records (session_id, student_id, status, confidence, marked_at)
                    VALUES (?, ?, 'absent', 0, ?)
                    """,
                    (session_id, student["id"], utcnow()),
                )

        db.execute(
            """
            UPDATE attendance_sessions
            SET status = 'finalized', finalized_at = ?, matched_count = ?, uncertain_count = ?, unknown_count = ?
            WHERE id = ?
            """,
            (
                utcnow(),
                len(present_ids),
                sum(1 for detection in session_row["detections"] if decisions.get(int(detection["id"])) is None),
                0,
                session_id,
            ),
        )

    log_action(tenant_id, user_id, "attendance.finalized", "attendance_session", session_id, {"present_ids": present_ids})
    return True, "Attendance session finalized successfully."


def list_sessions(tenant_id: int) -> list[dict]:
    return query_all(
        "SELECT * FROM attendance_sessions WHERE tenant_id = ? ORDER BY datetime(created_at) DESC",
        (tenant_id,),
    )


def dashboard_metrics(tenant_id: int) -> dict:
    total_students = query_one("SELECT COUNT(*) AS count FROM students WHERE tenant_id = ? AND is_active = 1", (tenant_id,))["count"]
    sessions = query_one("SELECT COUNT(*) AS count FROM attendance_sessions WHERE tenant_id = ?", (tenant_id,))["count"]
    pending_reviews = query_one("SELECT COUNT(*) AS count FROM attendance_sessions WHERE tenant_id = ? AND status != 'finalized'", (tenant_id,))["count"]
    avg_attendance = query_one(
        """
        SELECT COALESCE(ROUND(AVG(percent_present), 2), 0) AS value
        FROM (
            SELECT attendance_records.session_id,
                   AVG(CASE WHEN attendance_records.status = 'present' THEN 100.0 ELSE 0 END) AS percent_present
            FROM attendance_records
            JOIN attendance_sessions ON attendance_sessions.id = attendance_records.session_id
            WHERE attendance_sessions.tenant_id = ?
            GROUP BY attendance_records.session_id
        )
        """,
        (tenant_id,),
    )["value"]
    return {
        "total_students": total_students,
        "sessions": sessions,
        "pending_reviews": pending_reviews,
        "avg_attendance": avg_attendance,
    }


def attendance_summary_rows(tenant_id: int) -> list[dict]:
    return query_all(
        """
        SELECT students.name, students.roll_no,
               SUM(CASE WHEN attendance_records.status = 'present' THEN 1 ELSE 0 END) AS present_count,
               COUNT(attendance_records.id) AS total_sessions,
               ROUND(
                   CASE
                     WHEN COUNT(attendance_records.id) = 0 THEN 0
                     ELSE (SUM(CASE WHEN attendance_records.status = 'present' THEN 1 ELSE 0 END) * 100.0) / COUNT(attendance_records.id)
                   END,
                   2
               ) AS attendance_percent
        FROM students
        LEFT JOIN attendance_records ON attendance_records.student_id = students.id
        WHERE students.tenant_id = ? AND students.is_active = 1
        GROUP BY students.id
        ORDER BY attendance_percent DESC, students.name
        """,
        (tenant_id,),
    )
