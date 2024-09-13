from flask import Blueprint, request, jsonify

from models.course import Course

bp = Blueprint("courses", __name__)


@bp.route("/", strict_slashes=False)
def courses_get():
    courses = Course.all()
    c_list = []
    for course in courses:
        c_list.append(course.to_dict())

    return jsonify({
        "status": 200,
        "message": "Record retrieved successfully",
        "data": {
            "courses": c_list
        }
    }), 200