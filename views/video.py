import os

from flask import Blueprint, jsonify, request, send_file
from werkzeug.datastructures import MultiDict

from flask_jwt_extended import jwt_required, get_jwt_identity

from models.engine.static_storage import VideoStorage, ImageStorage
from models.video import Video
from models.user import User

from utils.exceptions import NotFound, BadRequest


bp = Blueprint("video", __name__)

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
DASH_OUTPUT_FOLDER = os.getenv("DASH_OUTPUT_FOLDER")

@bp.route("/<vid_id>/details", strict_slashes=False)
@jwt_required()
def get_video_details(vid_id):
    try:
        vid = Video.search(id=vid_id)
        if not vid: raise NotFound
        
        v_dict = vid.to_dict()
        user = User.search(id=v_dict["source_id"])
        if not user: raise NotFound
        v_dict["user"] = user.basic_info()

        return jsonify({
            "status": 200,
            "message": "Resource retrieved successfully",
            "data": {
                "video": v_dict
            }
        }), 200
    except NotFound as e:
        return jsonify({
            "status": 404,
            "message": "Resource not found",
        }), 404

@bp.route("/<video_id>/<ob_name>/<path:filename>", methods=["GET"], strict_slashes=False)
def video_get(video_id, ob_name, filename):
    """
    """
    try:
        if request.args.get("mpd"):
            object_name = ob_name.rsplit(".", 1)[0] # remove the filename extension
            dash_manifest = f"{object_name}/{object_name}.mpd"
            return send_file(os.path.join(DASH_OUTPUT_FOLDER, dash_manifest))
        else:    
            object_name = ob_name.rsplit(".", 1)[0] # remove the filename extension
            return send_file(os.path.join(DASH_OUTPUT_FOLDER, object_name, filename))
    except BadRequest as e:
        return jsonify({
            "status": 400,
            "message": "Bad request",
        }), 400
    except Exception as e:
        print(e)
        return jsonify({
            "status": 500,
            "message": "Internal Server Error",
        }), 500

@bp.route("/", methods=["POST"], strict_slashes=False)
@jwt_required()
def video_post():
    """
        Uploads a video
    """
    data = MultiDict(request.form)
    files = MultiDict(request.files)
    
    user_id = get_jwt_identity()["id"]

    if "video_file" not in request.files \
    or not request.files["video_file"]:
        return jsonify({
            "status": 400,
            "message": "Bad request",
        }), 400

    try:
        videoStorage = VideoStorage(files["video_file"])
        thumbnailStorage = ImageStorage(files["thumbnail"])
        vid_fn = videoStorage.save()
        thb_fn = thumbnailStorage.save()

        new_video = Video(
            object_name=vid_fn,
            thumbnail=thb_fn,
            source_id=user_id,
            course_id=1,
            **(data)
        )
        v_dict = new_video.to_dict()

        if not new_video.save(): raise Exception("Error saving to database")
        return jsonify({
            "status": 201,
            "message": "Record created successfully",
            "data": {
                "video": v_dict
            }
        }), 201
    except Exception as e:
        print(e)
        return jsonify({
            "status": 500,
            "message": "Internal server error",
        }), 500



@bp.route("/", methods=["PATCH"], strict_slashes=False)
@jwt_required()
def video_patch():
    params = MultiDict(request.args)
    if not params.get("video_id"):
        return jsonify({
            "status": 400,
            "message": "Bad request",
        }), 400

    vid = Video.search(id=params.get("video_id"))
    if not vid:
        return jsonify({
            "status": 404,
            "message": "Video not found"
        }), 404
    del params["video_id"]

    try:
        vid.update(**params)
        vid.save()
        vid.refresh()
        return jsonify({
            "status": 200,
            "message": "Record updated successfully",
            "data": {
                "video": vid.to_dict()
            }
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            "status": 500,
            "message": "Internal Server Error",
        }), 500


@bp.route("/", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def video_delete():
    vid_id = request.args.get("video_id")
    if not vid_id:
        return jsonify({
            "status": 400,
            "message": "Bad Request",
        }), 400

    vid = Video.search(id=vid_id)
    if not vid:
        return jsonify({
            "status": 404,
            "message": "Video not found",
        }), 404
    
    try:
        vid.delete()
        vid.save(delete=True)
        return jsonify({
            "status": 200,
            "message": "Record deleted successfully",
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            "status": 500,
            "message": "Internal Server Error",
        }), 500
