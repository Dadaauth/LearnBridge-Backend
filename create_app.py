import os
from datetime import timedelta

from flask import Flask
from dotenv import load_dotenv

from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from views.auth.auth import bp as auth_bp
from views.content.bridge import bp as bridge_bp
from views.content.video import bp as video_bp

from views.admin.video import bp as admin_video_bp
from views.admin.home import bp as admin_home_bp

def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=10)

    jwt = JWTManager(app)
    f_bcrypt = Bcrypt(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(bridge_bp, url_prefix="/bridge")
    app.register_blueprint(video_bp, url_prefix="/bridge/video")

    app.register_blueprint(admin_video_bp, url_prefix="/admin/video")
    app.register_blueprint(admin_home_bp, url_prefix="/admin/home")

    return app