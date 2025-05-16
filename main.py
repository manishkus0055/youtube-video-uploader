# main.py

import os
from app.auth import get_youtube_service
from app.video_manager import get_unuploaded_videos, save_uploaded, load_uploaded
from app.uploader import upload_video, wait_until_processed
from app.scheduler import random_sleep_between, get_daily_upload_limit, has_wait_time_passed, update_last_upload_time
from app.config import VIDEO_FOLDER, BASE_TITLE
from app.metadata import generate_title, get_description, get_tags

def main():
    if not has_wait_time_passed():
        print("Upload session not allowed yet. Try again later.")
        return

    youtube = get_youtube_service("default")
    unuploaded = get_unuploaded_videos()
    uploaded_log = load_uploaded()
    limit = get_daily_upload_limit()

    print(f"Uploading {limit} video(s) today...")

    if not unuploaded:
        print("No new videos to upload.")
        return

    for i in range(min(limit, len(unuploaded))):
        video_name = unuploaded[i]
        video_path = os.path.join(VIDEO_FOLDER, video_name)

        title = generate_title(BASE_TITLE, len(uploaded_log) + 1)
        description = get_description()
        tags = get_tags()

        try:
            video_id = upload_video(youtube, video_path, title, description, tags)
            wait_until_processed(youtube, video_id)
            uploaded_log.append(video_name)
            save_uploaded(uploaded_log)
        except Exception as e:
            print(f"Failed to upload {video_name}: {e}")

        if i < limit - 1:
            random_sleep_between(10, 60)

    update_last_upload_time()

if __name__ == "__main__":
    main()
