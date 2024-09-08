"""
Flask Blueprint for handling video content from creators
    :endpoints
        -   route: /upload
            function: upload_video
            description: Describe how the endpoint works

        -   route: ...
"""


from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required

from models.video import Video

from .decorators import bridge_required, user_required

bp = Blueprint("video", __name__)


@bp.route("/upload", methods=["POST"], strict_slashes=False)
@jwt_required()
@user_required()
@bridge_required()
def upload_video(**kwargs):
    """
        :params
            kwargs: a series of keyword arguments coming from the decorators
                covering the function. See the decorators implementations for
                more details.
    """
    files = request.files
    form = request.form

    video = files.get("video", None)
    thumbnail = files.get("thumbnail")

    title = form.get("title")
    description = form.get("description")

    if not video or not thumbnail:
        return jsonify({
            "status": "Bad Request",
            "message": "Video/Thumbnail resource not present in body"
        }), 400
    
    if video.filename == '' or thumbnail.filename == '':
        return jsonify({
            "status": "Bad Request",
            "message": "Video/Thumbnail resource not present in body"
        }), 400
    
    if '.' not in video.filename and '.' not in thumbnail.filename:
        return jsonify({
            "status": "Bad Request",
            "message": "Invalid Video/Thumbnail filename"
        }), 400

    video_ext = video.filename.rsplit('.', 1)[1]
    thumbnail_ext = thumbnail.filename.rsplit('.', 1)[1]
    if video_ext not in ["mp4", "webm", "ogg"] or thumbnail_ext not in ["png", "jpg", "jpeg"]:
        return jsonify({
            "status": "Bad Request",
            "message": "Invalid Video/Thumbnail file format"
        }), 400
    
    vid_obj = Video(
        bridge_id=kwargs["bridge"].id,
        video=video,
        title=title,
        thumbnail=thumbnail,
        description=description,
        video_ext=video_ext,
        thumbnail_ext=thumbnail_ext
    )

    vid_obj.save()
    return jsonify({
        "status": "Success",
        "message": "Video Uploaded Successfully",
    }), 201
