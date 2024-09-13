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
from views.videos import bp as videos_bp

from views.article import bp as article_bp
from views.articles import bp as articles_bp

from views.course import bp as course_bp
from views.courses import bp as courses_bp

def create_app():
    app = Flask(__name__)
    load_dotenv()
    CORS(app)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=10)
    app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER")
    app.config["DASH_OUTPUT_FOLDER"] = os.getenv("DASH_OUTPUT_FOLDER")
    app.config['MAX_CONTENT_LENGTH'] = 9999999999999999999999999999999999999999999999999999999 * 1000 * 1000

    jwt = JWTManager(app)
    f_bcrypt = Bcrypt(app)

    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(users_bp, url_prefix="/api/users")

    app.register_blueprint(video_bp, url_prefix="/api/video")
    app.register_blueprint(videos_bp, url_prefix="/api/videos")

    app.register_blueprint(article_bp, url_prefix="/api/article")
    app.register_blueprint(articles_bp, url_prefix="/api/articles")

    app.register_blueprint(course_bp, url_prefix="/api/course")
    app.register_blueprint(courses_bp, url_prefix="/api/courses")

    return app