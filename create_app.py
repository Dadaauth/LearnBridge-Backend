import os
from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from views.user import bp as user_bp
from views.users import bp as users_bp

from views.video import bp as video_bp

def create_app():
    app = Flask(__name__)
    load_dotenv()
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=10)
    app.config["UPLOAD_FOLDER"] = "static"

    jwt = JWTManager(app)
    f_bcrypt = Bcrypt(app)

    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(video_bp, url_prefix="/api/video")

    return app