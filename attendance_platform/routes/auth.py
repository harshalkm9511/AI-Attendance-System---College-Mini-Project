from flask import Blueprint, flash, redirect, render_template, request, url_for

from ..auth import login_user, logout_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if login_user(request.form.get("username", "").strip(), request.form.get("password", "")):
            flash("Welcome back.", "success")
            return redirect(url_for("dashboard.home"))
        flash("Invalid username or password.", "error")
    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    flash("Signed out successfully.", "success")
    return redirect(url_for("auth.login"))
