from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from ..auth import login_required
from ..services.repository import analyze_attendance, finalize_attendance_session, get_session

attendance_bp = Blueprint("attendance", __name__, url_prefix="/attendance")


@attendance_bp.route("/", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        uploaded = request.files.get("classroom_image")
        if uploaded is None or not uploaded.filename:
            flash("Please upload a classroom image.", "error")
            return render_template("attendance_upload.html")
        title = request.form.get("title", "").strip() or "Attendance Session"
        ok, message, session_id = analyze_attendance(
            tenant_id=g.user["tenant_id"],
            user_id=g.user["id"],
            title=title,
            uploaded_bytes=uploaded.read(),
            filename=uploaded.filename,
        )
        flash(message, "success" if ok else "error")
        if ok and session_id is not None:
            return redirect(url_for("attendance.review", session_id=session_id))
    return render_template("attendance_upload.html")


@attendance_bp.route("/<int:session_id>/review", methods=["GET", "POST"])
@login_required
def review(session_id: int):
    session_data = get_session(session_id, g.user["tenant_id"])
    if session_data is None:
        flash("Attendance session not found.", "error")
        return redirect(url_for("attendance.upload"))

    if request.method == "POST":
        decisions = {}
        for detection in session_data["detections"]:
            raw_value = request.form.get(f"face_{detection['id']}", "").strip()
            decisions[int(detection["id"])] = int(raw_value) if raw_value.isdigit() else None
        ok, message = finalize_attendance_session(g.user["tenant_id"], g.user["id"], session_id, decisions)
        flash(message, "success" if ok else "error")
        if ok:
            return redirect(url_for("dashboard.reports"))

    return render_template("attendance_review.html", session=session_data)
