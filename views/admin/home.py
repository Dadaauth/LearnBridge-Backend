
from flask import Blueprint, jsonify

bp = Blueprint("admin_home", __name__)


@bp.route("/dashboard", methods=["GET"], strict_slashes=False)
def admin_dashboard():
    return jsonify({"status": "Success", "message": "Welcome to your dashboard"})