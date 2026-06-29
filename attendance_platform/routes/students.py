from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from ..auth import login_required
from ..services.repository import delete_student, get_student, list_students, save_student_with_image, update_student

students_bp = Blueprint("students", __name__, url_prefix="/students")


@students_bp.route("/")
@login_required
def index():
    return render_template("students.html", students=list_students(g.user["tenant_id"]))


@students_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        uploaded = request.files.get("image")
        if uploaded is None or not uploaded.filename:
            flash("Student image is required.", "error")
            return render_template("student_form.html")
        try:
            ok, message = save_student_with_image(
                tenant_id=g.user["tenant_id"],
                user_id=g.user["id"],
                name=request.form.get("name", "").strip(),
                roll_no=request.form.get("roll_no", "").strip(),
                department=request.form.get("department", "").strip(),
                section_name=request.form.get("section_name", "").strip(),
                uploaded_bytes=uploaded.read(),
                filename=uploaded.filename,
            )
        except Exception as exc:
            ok, message = False, f"Failed to save student: {exc}"
        flash(message, "success" if ok else "error")
        if ok:
            return redirect(url_for("students.index"))
    return render_template("student_form.html")


@students_bp.route("/<int:student_id>")
@login_required
def detail(student_id: int):
    student = get_student(student_id, g.user["tenant_id"])
    if student is None:
        flash("Student not found.", "error")
        return redirect(url_for("students.index"))
    return render_template("student_detail.html", student=student)


@students_bp.route("/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def edit(student_id: int):
    student = get_student(student_id, g.user["tenant_id"])
    if student is None:
        flash("Student not found.", "error")
        return redirect(url_for("students.index"))

    if request.method == "POST":
        ok, message = update_student(
            tenant_id=g.user["tenant_id"],
            user_id=g.user["id"],
            student_id=student_id,
            name=request.form.get("name", "").strip(),
            roll_no=request.form.get("roll_no", "").strip(),
            department=request.form.get("department", "").strip(),
            section_name=request.form.get("section_name", "").strip(),
        )
        flash(message, "success" if ok else "error")
        if ok:
            return redirect(url_for("students.index"))

    return render_template("student_edit.html", student=student)


@students_bp.route("/<int:student_id>/delete", methods=["POST"])
@login_required
def delete(student_id: int):
    try:
        ok, message = delete_student(g.user["tenant_id"], g.user["id"], student_id)
    except Exception as exc:
        ok, message = False, f"Failed to delete student: {exc}"
    flash(message, "success" if ok else "error")
    return redirect(url_for("students.index"))
