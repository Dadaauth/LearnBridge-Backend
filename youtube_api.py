from flask import Flask, redirect

app = Flask(__name__)

import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow


CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)

flow.redirect_uri = 'http://localhost:5000/auth/verify'

authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')


@app.route("/auth/login")
def hello_world():
    return redirect(authorization_url)

@app.route("/auth/verify")
def verify_youtube_data_auth():
    flow.fetch_token(authorization_response=authorization_url)
    credentials = flow.credentials
    return credentials