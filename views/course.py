from flask import Blueprint, request, jsonify

from models.course import Course

bp = Blueprint("course", __name__)


@bp.route("/", methods=["GET", "POST", "PATCH", "DELETE"], strict_slashes=False)
def course():
    """
    """
    if request.method == "GET":
        course_id = request.args.get("course_id")
        if not course_id:
            return jsonify({
                "status": 400,
                "message": "Bad request",
            }), 400
        try:
            course = Course.search(id=course_id)
            if not course:
                return jsonify({
                    "status": 404,
                    "message": "Course not found",
                }), 404
            
            return jsonify({
                "status": 200,
                "message": "Record retrieved successfuly",
                "data": {
                    "course": course.to_dict()
                }
            }), 200
        except Exception as e:
            print(e)
            return jsonify({
                "status": 500, 
                "message": "Internal Server Error",
            }), 500
    if request.method == "POST":
        try:
            new_course = Course(**request.args)
            c_dict = new_course.to_dict()
            if not new_course.save(): raise Exception("Error saving to database")
            return jsonify({
                "status": 201,
                "message": "Record created successfully",
                "data": {
                    "course": c_dict
                }
            }), 201
        except Exception as e:
            print(e)
            return jsonify({
                "status": 500,
                "message": "Internal server error",
            }), 500
