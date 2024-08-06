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

from .decorators import bridge_required

bp = Blueprint("video", __name__)


@bp.route("/upload", methods=["POST"], strict_slashes=False)
@jwt_required()
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
    
    vid_obj = Video(
        bridge_id=kwargs["bridge_id"],
        video=video,
        title=title,
        thumbnail=thumbnail,
        description=description,
    )

    vid_obj.save()
    return jsonify({
        "status": "Success",
        "message": "Video Uploaded Successfully",
    }), 201


# int main() {

#     goto label;


#     # there is a code here

#     label:
#         # RUN TIS CODE
# }