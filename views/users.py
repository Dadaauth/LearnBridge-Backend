from flask import Blueprint, jsonify

from models.user import User

bp = Blueprint("users", __name__)

@bp.route("/", strict_slashes=False)
def users():
    users = []
    for user in User.all():
        users.append(user.basic_info())

    return jsonify({
        "status": 200,
        "message": "Records retrieved successfully",
        "data": {
            "users": users
        }
    }), 200