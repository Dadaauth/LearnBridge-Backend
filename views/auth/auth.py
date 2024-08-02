from flask import Blueprint, request, jsonify

from flask_jwt_extended import create_access_token
from flask_bcrypt import check_password_hash

from models.user import User
from errors.my_errors import MyValueError

bp = Blueprint("auth", __name__)


@bp.route("/user/register/new", methods=["POST"], strict_slashes=False)
def register_new_user():
    try:
        new_user = User(**(request.form))
        user_dict = new_user.to_dict()
        new_user.save()
    except (MyValueError) as e:
        if e.error_code == 1001:
            return jsonify({
                "status": "failed",
                "error": str(e),
                "code": e.error_code
            }), 409
        return {"error": "Invalid request body"}, 400
    except Exception as e:
        return {"error": "Internal server error"}, 500
    
    token = create_access_token(identity=user_dict)
    return jsonify({
        "status": "Successful",
        "message": "User created successfully",
        "user": user_dict,
        "access_token": token
    }), 201


@bp.route("/user/login", methods=["POST"], strict_slashes=False)
def login_user():
    data = request.form
    if data.get("email") is None or data.get("password") is None:
        return jsonify({"status": "failed", "message": "Bad Request"}), 400

    user = User.search(email=data.get("email"))
    if len(user) == 0:
        return jsonify({"status": "failed", "message": "User not found"}), 404
    user: User = user[0]
    if not check_password_hash(user.password, data.get("password")):
        return jsonify({"status": "failed", "message": "Invalid credentials"}), 401
    user_dict = user.to_dict()
    token = create_access_token(identity=user_dict)
    return jsonify({
        "status": "successful",
        "message": "Login successful",
        "access_token": token,
        "user": user_dict,
    }), 200