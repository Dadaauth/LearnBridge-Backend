from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models.video import Video
from models.user import User
from utils.exceptions import NotFound, Successful

bp = Blueprint("videos", __name__)


@bp.route("/user/<user_id>/get")
@jwt_required()
def get_user_videos(user_id):
    try:
        vdts = Video.search(source_id=user_id)
        if not vdts: raise NotFound()

        videos = []
        if isinstance(vdts, list):
            for video in vdts:
                v_dict = video.to_dict()
                user = User.search(id=video.source_id)
                if not user: raise NotFound
                v_dict["user"] = user.basic_info()
                videos.append(v_dict)
        else:
            video = vdts

            v_dict = video.to_dict()
            user = User.search(id=video.source_id)
            if not user: raise NotFound
            v_dict["user"] = user.basic_info()

            videos.append(v_dict)

        return jsonify({
            "status": 200,
            "message": "Record retrieved successfully",
            "data": {
                "videos": videos,
            }
        }), 200
    except NotFound as e:
        return jsonify({
            "status": 404,
            "message": "No videos found",
        }), 404
    except Exception as e:
        print(e)
        return jsonify({
            "status": 500,
            "message": "Internal Server Error",
        }), 500

@bp.route("/", methods=["GET"], strict_slashes=False)
@jwt_required()
def videos():
    """
    """
    try:
        all_videos = Video.all()
        if not all_videos: raise NotFound()
        
        v_list = []
        if isinstance(all_videos, list):
            for video in all_videos:
                v_dict = video.to_dict()
                user = User.search(id=video.source_id)
                if not user: raise NotFound
                v_dict["user"] = user.basic_info()

                v_list.append(v_dict)
        else:
            video = all_videos

            v_dict = video.to_dict()
            user = User.search(id=video.source_id)
            if not user: raise NotFound
            v_dict["user"] = user.basic_info()

            v_list.append(v_dict)

        return jsonify({
            "status": 200,
            "message": "Record retrieved successfully",
            "data": {
                "videos": v_list
            }
        }), 200
    except NotFound as e:
        return jsonify({
            "status": 404,
            "message": "Resource not found",
        }), 404
    except Exception as e:
        print(e)
        return jsonify({
            "status": 500,
            "message": "Internal Server Error"
        }), 500
