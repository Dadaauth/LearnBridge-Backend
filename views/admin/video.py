
from uuid import uuid4

from flask import Blueprint, request, redirect, jsonify, url_for

import google_auth_oauthlib.flow

from models.admin.youtube import YoutubeCredentials

bp = Blueprint("admin_video", __name__)


flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "secret_client.json",
        scopes=["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.force-ssl"]
    )
flow.redirect_uri = "http://localhost:5000/admin/video/verify_youtube_callback"

authorization_url, state = flow.authorization_url(
    access_type="offline",
    include_granted_scopes="true",
    login_hint="dadaauthourity23@gmail.com",
    state=f"LearnBridge-{uuid4()}",
    prompt="consent"
)

@bp.route("/authorize_youtube", methods=["GET"], strict_slashes=False)
# @admin_required()
def authorize_youtube():
    return redirect(authorization_url)


@bp.route("/verify_youtube_callback")
def verify_youtube_auth_callback():
    data = request.args
    if data.get("error"):
        return jsonify({
            "status": "Error",
            "error": data.get("error")
        }), 401
    try:
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials

        YTcredentials = YoutubeCredentials(
            token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_uri=credentials.token_uri,
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
            scopes=credentials.scopes
        )
        YTcredentials.save()
        YTcredentials.refresh()
        return redirect(url_for("admin_home.admin_dashboard"))
    except Exception as e:
        print("\n\n\n")
        print(e)
        print("\n\n\n")
        return jsonify({
            "status": "Failed",
            "message": "Internal server error",
        }), 500
