from werkzeug.datastructures import MultiDict
from flask import Blueprint, request, jsonify

from models.user import User
from models.engine.static_storage import ImageStorage
from utils.exceptions import BadRequest, NotFound, Successful

bp = Blueprint("user", __name__)


@bp.route("/", methods=["GET"], strict_slashes=False)
def user_get():
    """Retrieves information about a particular user"""
    params = request.args
    level = params.get("level")
    level = level if level else "basic"
    user_id = params.get("user_id")

    if not user_id:
        return jsonify({
            "status": 400,
            "message": "Bad request"
        }), 400

    user = User.search(id=user_id)
    if not user:
        return jsonify({
            "status": 404,
            "message": "User not found"
        }), 404
    if level == "basic":
        info = user.basic_info()
    elif level == "full":
        pass
    return jsonify({
        "status": 200,
        "message": "Info retrieved successfully",
        "data": {
            "user": info,
        },
    }), 200

@bp.route("/", methods=["POST"], strict_slashes=False)
def user_post():
    """ Creates a new user
    """
    try:
        data = MultiDict(request.form)
        # Confirm that the user email does not exist in the database
        email = data.get("email")
        if email is None or email == "":
            raise BadRequest("email address not found in request")
        if User.search(email=email) is not None:
            raise BadRequest("User already exists")
        
        picture = request.files.get("picture")
        if picture:
            picture = ImageStorage(picture)
            picture = picture.save()

        new_user = User(**data, picture=picture)
        info = new_user.basic_info()
        if not new_user.save(): raise Exception("Error saving to database")
        return jsonify({
            "status": 201,
            "message": "record created successfully",
            "data": {
                "user": info,
            },
        }), 201
    except BadRequest as e:
        print(e)
        return jsonify({
            "status": 400,
            "message": "Bad request",
            "error": str(e),
        }), 400
    except ValueError as e:
        return jsonify({
            "status": 400,
            "message": "incomplete fields sent",
            "error": str(e),
        }), 400
    except Exception as e:
        return jsonify({
            "status": 500,
            "message": "Internal server error",
            "error": str(e)
        }), 500
        
@bp.route("/", methods=["PATCH"], strict_slashes=False)
def user_patch():
    """Updates the details of a single user
    """
    params = MultiDict(request.args)
    if not params.get("user_id"):
        return jsonify({
            "status": 400,
            "message": "Bad request",
        }), 400

    user = User.search(id=params.get("user_id"))
    if not user:
        return jsonify({
            "status": 404,
            "message": "User not found"
        }), 404
    del params["user_id"]
    try:
        user.update(**params)
        if not user.save(): raise Exception("Error saving to database")
        user.refresh()
        return jsonify({
            "status": 200,
            "message": "Record updated successfully",
            "data": {
                "user": user.basic_info()
            }
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            "status": 500,
            "message": "Internal server error",
        }), 500

@bp.route("/", methods=["DELETE"], strict_slashes=False)
def user_delete():
    """Deletes a user record"""
    params = request.args
    if not params.get("user_id"):
        return jsonify({
            "status": 400,
            "message": "Bad request",
        }), 400

    user = User.search(id=params.get("user_id"))
    if not user:
        return jsonify({
            "status": 404,
            "message": "User not found"
        }), 404
    try:
        user.delete()
        if not user.save(delete=True):
            raise Exception("Error saving to database")
        return jsonify({
            "status": 200,
            "message": "Record deleted successfully",
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            "status": 500,
            "message": "Internal server error",
        }), 500
