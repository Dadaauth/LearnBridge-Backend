from flask import Blueprint, request, jsonify
from werkzeug.datastructures import MultiDict

from models.article import Article
from lib.exceptions import BadRequest, NotFound, Successful

bp = Blueprint("article", __name__)

@bp.route("/", methods=["GET"], strict_slashes=False)
def article_get():
    try:
        article_id = request.args.get("article_id")
    
        if not article_id: raise BadRequest()
        article= Article.search(id=article_id)
    
        if not article: raise NotFound()
        raise Successful()
    
    except BadRequest as e:
        return jsonify({
            "status": 400,
            "message": "Bad request",
        }), 400
    except NotFound as e:
        return jsonify({
            "status": 404,
            "message": "Article not found",
        }), 404
    except Successful as e:
        return jsonify({
            "status": 200,
            "message": "Record retrieved successfully",
            "data": {
                "article": article.to_dict()
            }
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            "status": 500,
            "message": "Internal Server Error",
        }), 500

    

@bp.route("/", methods=["POST"], strict_slashes=False)
def article_post():
    try:
        data = request.get_json()
        
        if not data.get("source_id") or not data.get("course_id") \
            or not data.get("title") or not data.get("content"):
            raise BadRequest()

        article = Article(**data)
        if not article.save(): raise Exception("Error saving to database")
        
        raise Successful()
    
    except BadRequest as e:
        return jsonify({
            "status": 400,
            "message": "Bad request",
        }), 400
    except Successful:
        article.refresh()
        return jsonify({
            "status": 201,
            "message": "Record created successfully",
            "data": {
                "article": article.to_dict()
            }
        }), 201
    except Exception as e:
        print(e)
        return jsonify({
            "status": 500,
            "message": "Internal Server Error",
        }), 500
            

@bp.route("/", methods=["PATCH"], strict_slashes=False)
def article_patch():
    try:
        data = MultiDict(request.get_json())
        if not data.get("article_id"): raise BadRequest()

        article = Article.search(id=data.get("article_id"))
        if not article: raise NotFound()
        del data["article_id"]

        article.update(**data)
        if not article.save(): raise Exception("Error saving to database")        
        raise Successful()

    except BadRequest:
        return jsonify({
            "status": 400,
            "message": "Bad request",
        }), 400
    except NotFound:
        return jsonify({
            "status": 404,
            "message": "Article not found",
        }), 404
    except Successful:
        article.refresh()
        return jsonify({
            "status": 200,
            "message": "Record updated successfully",
            "data": {
                "article": article.to_dict()
            }
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            "status": 500,
            "message": "Internal Server Error",
        }), 500


@bp.route("/", methods=["DELETE"], strict_slashes=False)
def article_delete():
    try:
        params = request.args
        if not params.get("article_id"): raise BadRequest()

        article = Article.search(id=params.get("article_id"))
        if not article: raise NotFound()

        article.delete()
        if not article.save(delete=True):
            raise Exception("Error saving to database")

        raise Successful()

    except BadRequest:
        return jsonify({
            "status": 400,
            "message": "Bad request",
        }), 400
    except NotFound:
        return jsonify({
            "status": 404,
            "message": "Article not found"
        }), 404
    except Successful:
        return jsonify({
            "status": 200,
            "message": "Record deleted successfully",
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            "status": 500,
            "message": "Internal server error",
        }), 500
