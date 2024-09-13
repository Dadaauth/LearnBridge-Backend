import os

from flask import Blueprint, jsonify, request, send_file
from werkzeug.datastructures import MultiDict

from models.engine.static_storage import VideoStorage
from models.video import Video


bp = Blueprint("video", __name__)

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
DASH_OUTPUT_FOLDER = os.getenv("DASH_OUTPUT_FOLDER")

@bp.route("/<path:filename>", methods=["GET"])
def video_get(filename):
    """
    """
    if request.args.get("mpd"):
        video_id = filename
        if not video_id:
            return jsonify({
                "status": 400,
                "message": "Bad request",
            }), 400
        vid = Video.search(id=video_id)
        if not vid:
            return jsonify({
                "status": 404,
                "message": "Video not found",
            }), 404
        object_name = vid.object_name.rsplit(".", 1)[0]
        dash_manifest = f"{object_name}/{object_name}.mpd"
        try:
            return send_file(os.path.join(DASH_OUTPUT_FOLDER, dash_manifest))
        except Exception as e:
            print(e)
            return jsonify({
                "status": 500,
                "message": "Internal Server Error",
            }), 500
    else:
        try:
            return send_file(os.path.join(DASH_OUTPUT_FOLDER, filename))
        except Exception as e:
            print(e)
            return jsonify({
                "status": 500,
                "message": "Internal Server Error",
            }), 500

@bp.route("/", methods=["POST"])
def video_post():
    data = request.form
    user_id = data.get("user_id")

    if not user_id or \
    "video_file" not in request.files \
    or not request.files["video_file"]:
        return jsonify({
            "status": 400,
            "message": "Bad request",
        }), 400

    try:
        videoStorage = VideoStorage(request.files["video_file"])
        filename = videoStorage.save()
        new_video = Video(
            object_name=filename,
            **request.form
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



@bp.route("/", methods=["PATCH"])
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


@bp.route("/", methods=["DELETE"])
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
