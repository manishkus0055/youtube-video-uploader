# video_manager.py

import os
import json
from app.config import VIDEO_FOLDER, DATABASE_FILE, ALLOWED_EXTENSIONS

def load_uploaded():
    if not os.path.exists(DATABASE_FILE):
        return []
    with open(DATABASE_FILE, "r") as f:
        return json.load(f)

def save_uploaded(uploaded_videos):
    with open(DATABASE_FILE, "w") as f:
        json.dump(uploaded_videos, f, indent=2)

def get_unuploaded_videos():
    uploaded = set(load_uploaded())
    all_files = os.listdir(VIDEO_FOLDER)
    videos = [f for f in all_files if os.path.splitext(f)[1].lower() in ALLOWED_EXTENSIONS]
    return [v for v in videos if v not in uploaded]