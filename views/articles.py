from flask import Blueprint, request, jsonify

from models.article import Article

bp = Blueprint("articles", __name__)

@bp.route("/", strict_slashes=False)
def articles_get():
    articles = Article.all()
    art_list = []
    for art in articles:
        art_list.append(art.to_dict())

    return jsonify({
        "status": 200,
        "message": "Record retrieved successfully",
        "data": {
            "articles": art_list
        }
    }), 200