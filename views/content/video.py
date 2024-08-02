from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required

from googleapiclient.discovery import build

from models.admin.youtube import YoutubeCredentials
from .decorators import bridge_required, youtube_credentials_required

bp = Blueprint("video", __name__)


@bp.route("/upload", methods=["POST"], strict_slashes=False)
@jwt_required()
@bridge_required()
@youtube_credentials_required()
def upload_video(**kwargs):
    YTcredentials = kwargs['YTcredentials']

    if "video" not in request.files:
        return jsonify({
            "status": "Failed",
            "message": "Video not present in request"
        }), 400
    video = request.files["video"]

    if video.filename == '':
        abort(400, "no selected file")

    mime_type = video.content_type
    if not mime_type.startswith('video/') and mime_type != 'application/octet-stream':
        abort(400, 'Invalid file type')

    with build("youtube", "v3", credentials=YTcredentials) as youtube:
        
        channel = youtube.channels().list(mine=True, part='snippet').execute()

    return jsonify(channel)

