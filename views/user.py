from werkzeug.datastructures import MultiDict
from flask import Blueprint, request, jsonify

from models.user import User
from lib.exceptions import BadRequest, NotFound, Successful

bp = Blueprint("user", __name__)


@bp.route("/", methods=["GET", "POST", "PATCH", "DELETE"], strict_slashes=False)
def user():
    if request.method == 'GET':

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

    elif request.method == 'POST':

        formData = request.form
        new_user = User(**formData)
        info = new_user.basic_info()
        try:
            if not new_user.save(): raise Exception("Error saving to database")
            return jsonify({
                "status": 201,
                "message": "record created successfully",
                "data": {
                    "user": info,
                },
            }), 201
        except Exception as e:
            return jsonify({
                "status": 500,
                "message": "Internal server error",
            }), 500
        
    elif request.method == "PATCH":
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

    elif request.method == "DELETE":
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
