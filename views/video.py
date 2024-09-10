from flask import Blueprint, jsonify



bp = Blueprint("video", __name__)

@bp.route("/", methods=["GET"])
def video_get():
    return "Haha", 302

@bp.route("/", methods=["POST"])
def video_post():
    pass

@bp.route("/", methods=["PATCH"])
def video_patch():
    pass

@bp.route("/", methods=["DELETE"])
def video_delete():
    pass
