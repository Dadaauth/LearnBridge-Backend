from flask import Blueprint, jsonify, request
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity, jwt_required, decode_token

bp = Blueprint('auth', __name__)

from models.user import User

from utils.exceptions import BadRequest, NotFound, Successful, NotAllowed

# @bp.route("/token/verify", methods=["POST"], strict_slashes=False)
# @jwt_required(optional=True)
# def verify_token():
#     # check if the access token is still valid
#     identity = get_jwt_identity()

#     if identity:
#         return jsonify({
#         "status": 200,
#         "message": "authenticated",
#         "data": {
#             "user": identity,
#         }
#     })
#     else:
#         # Token has expired or is invalid,
#         # Let's check for a refresh token
#         refresh_token = request.json.get("refresh_token")

#         if not refresh_token:
#             return jsonify({
#                 "status": 400,
#                 "message": "Missing refresh token",
#             }), 400
        
#         # Use refresh token to issue a new access token
#         try:
#             # refresh token validation
#             identity = decode_token(refresh_token)['sub'] # requires valid refresh token
#             access_token = create_access_token(identity=identity)
#             return jsonify({

#             }), 200
#         except Exception as e:
#             return jsonify({
#                 "status": 401,
#                 "message": "Refresh token expired or invalid",
#             }), 401

@bp.route("/check", strict_slashes=False)
@jwt_required()
def check():
    # refresh the token if it has expired
    return jsonify({
        "status": 200,
        "message": "user logged in",
        "data": {
            "user": get_jwt_identity(),
        }
    }), 200


@bp.route("/refresh", strict_slashes=False)
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({
        "status": 200,
        "message": "Token refreshed successfully",
        "data": {
            "access_token": access_token,
            "user": identity,
        }
    }), 200


@bp.route("/signin", methods=["POST"], strict_slashes=False)
def sign_in():
    try:

        data = request.get_json()
        email, password = data.get("email"), data.get("password")

        if not email or not password or email == "" or password == "":
            raise BadRequest("required fields not present in request")

        # check if user exists
        user = User.search(email=email)
        if not user: raise NotFound("User not found")
        
        if isinstance(user, list): user = user[0]
        if not check_password_hash(user.password, password):
            raise NotAllowed("Invalid credentials")
        
        user_basic_info = user.basic_info()
        access_token = create_access_token(identity=user_basic_info)
        refresh_token = create_refresh_token(identity=user_basic_info)
        raise Successful({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "basic_info": user_basic_info,
        })
    
    except NotAllowed as e:
        return jsonify({
            "status": 401,
            "message": "Invalid credentials",
            "error": str(e)
        }), 401
    except NotFound as e:
        return jsonify({
            "status": 404,
            "message": "record not found",
            "error": str(e)
        }), 404
    except BadRequest as e:
        return jsonify({
            "status": 400,
            "message": "Bad request",
            "error": str(e)
        }), 400
    except Successful as e:
        return jsonify({
            "status": 200,
            "message": "Authentication successful",
            "data": {
                "access_token": e.args[0].get("access_token"),
                "refresh_token": e.args[0].get("refresh_token"),
                "user": e.args[0].get("basic_info"),
            },
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            "status": 500,
            "message": "Internal Server Error",            
        }), 500