from flask import Blueprint, request, jsonify

from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from models.bridge import Bridge
from models.static.image import ImageStatic

from .decorators import bridge_required, user_required

from errors.my_errors import MyValueError

bp = Blueprint("bridge", __name__)


@bp.route("/create/new", methods=["POST"], strict_slashes=False)
@jwt_required()
@user_required()
def create_bridge(**kwargs):
    user: User = kwargs["user"]
    if user.bridge_id is not None:
        return jsonify({
            "status": "Error",
            "message": "User already has a bridge"
        }), 400
    data = request.form
    name = data.get("name")
    description = data.get("description")
    image = request.files.get("image")

    if not name: name = f"{user.fname} {user.lname}"

    try:
        image_id = None
        if image:
            image = ImageStatic()
            image_id = image.id
        new_bridge = Bridge(
            name=name,
            description=description,
            image_id=image_id,
        )
        new_bridge.save()

        user.bridge_id = new_bridge.id
        user.save()

        new_bridge.refresh()
        user.refresh()

        bridge_dict = new_bridge.to_dict()
        user_dict = user.to_dict()
        
        return jsonify({
        "status": "successful",
        "message": "Bridge created successfully",
        "user": user_dict,
        "bridge": bridge_dict
    }), 201
    except Exception as e:
        return jsonify({
            "status": "Error",
            "message": "Internal server error"
        }), 500


@bp.route("/delete", methods=["DELETE"], strict_slashes=False)
@jwt_required()
@bridge_required()
def delete(**kwargs):
    bridge = kwargs["bridge"]
    try:
        bridge.delete()
        return jsonify({
            "status": "successful",
            "message": "Bridge deleted successfully",
        }), 200
    except:
        return jsonify({
            "status": "Error",
            "message": "Internal server error"
        }), 500
