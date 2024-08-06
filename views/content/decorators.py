from functools import wraps

from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

from google.oauth2.credentials import Credentials

from models.bridge import Bridge
from models.user import User
from models.admin.youtube import YoutubeCredentials

def bridge_required():
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            bridge_not_found = jsonify({
                "status": "Failed",
                "message": "You need a Bridge to access this endpoint"
            }), 404
            
            identity = get_jwt_identity()
            if not identity["bridge_id"]:
                return bridge_not_found
            
            bridge = Bridge.search(id=identity["bridge_id"])
            if len(bridge) == 0:
                return bridge_not_found
            kwargs["bridge"] = bridge[0]
            return func(*args, **kwargs)
        return decorator
    return wrapper

def user_required():
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            try:
                identity = get_jwt_identity()
                id = identity['id']

                user = User.search(id=id)
                if len(user) == 0:
                    return jsonify({
                        "status": "Error",
                        "message": "User not found"
                    }), 404
                
                kwargs["user"] = user[0]
                return func(*args, **kwargs)
            except:
                return jsonify({
                    "status": "Failed",
                    "message": "Internal server error"
                }), 500
        return decorator
    return wrapper
