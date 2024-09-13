from flask import Blueprint, request, jsonify

from models.video import Video

bp = Blueprint("videos", __name__)

@bp.route("/", methods=["GET"], strict_slashes=False)
def videos():
    """
    """
    try:
        all_videos = Video.all()
        v_list = []
        for video in all_videos:
            v_list.append(video.to_dict())

        return jsonify({
            "status": 200,
            "message": "Record retrieved successfully",
            "data": {
                "videos": v_list
            }
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            "status": 500,
            "message": "Internal Server Error"
        }), 500