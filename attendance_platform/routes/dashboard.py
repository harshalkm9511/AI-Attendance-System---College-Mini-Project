from flask import Blueprint, g, render_template

from ..auth import login_required
from ..services.repository import attendance_summary_rows, dashboard_metrics, list_sessions

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def home():
    metrics = dashboard_metrics(g.user["tenant_id"])
    rows = attendance_summary_rows(g.user["tenant_id"])
    sessions = list_sessions(g.user["tenant_id"])[:5]
    return render_template("dashboard.html", metrics=metrics, rows=rows, sessions=sessions)


@dashboard_bp.route("/reports")
@login_required
def reports():
    return render_template(
        "reports.html",
        rows=attendance_summary_rows(g.user["tenant_id"]),
        sessions=list_sessions(g.user["tenant_id"]),
    )
