# backend/auth.py

import os
import pickle
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly"]
CLIENT_SECRETS_FILE = "client_secret.json"

def get_flow(user_id):
    return Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=f"http://localhost:5000/oauth2callback/{user_id}"
    )

def save_token(user_id, credentials):
    path = f"user_data/{user_id}/token.pickle"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as token_file:
        pickle.dump(credentials, token_file)

def load_token(user_id):
    path = f"user_data/{user_id}/token.pickle"
    if not os.path.exists(path):
        return None
    with open(path, "rb") as token_file:
        return pickle.load(token_file)

def get_youtube_service(user_id):
    creds = load_token(user_id)
    if not creds:
        raise Exception("User not authenticated")
    return build("youtube", "v3", credentials=creds)

def run_local_oauth(user_id="default"):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri="urn:ietf:wg:oauth:2.0:oob"
    )
    auth_url, _ = flow.authorization_url(prompt="consent")
    print(f"🔗 Go to this URL:\n{auth_url}")

    code = input("🔑 Enter the authorization code: ")
    flow.fetch_token(code=code)

    creds = flow.credentials
    save_token(user_id, creds)
    print("✅ Token saved successfully.")

# Soon replace the run_local_oauth() function with a Flask route like:
"""
@app.route('/login/<user_id>')
def login(user_id):
    flow = get_flow(user_id)
    auth_url, _ = flow.authorization_url(prompt="consent")
    return redirect(auth_url)
"""
# And handle the token with:
"""
@app.route('/oauth2callback/<user_id>')
def oauth2callback(user_id):
    code = request.args.get("code")
    flow = get_flow(user_id)
    flow.fetch_token(code=code)
    save_token(user_id, flow.credentials)
    return "Login successful!"
"""
# get_flow() and save_token() are perfectly modular.