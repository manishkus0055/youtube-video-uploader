# uploader.py

import time
import os
from googleapiclient.http import MediaFileUpload

def upload_video(youtube, video_path, title, description, tags, category="22", privacy="public"):
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category,
            },
            "status": {
                "privacyStatus": privacy
            }
        },
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploading {os.path.basename(video_path)}: {int(status.progress() * 100)}%")

    print(f"✅ Upload Complete: {response['id']}")
    return response['id']

def wait_until_processed(youtube, video_id):
    while True:
        resp = youtube.videos().list(
            part="processingDetails,status",
            id=video_id
        ).execute()

        status = resp['items'][0]['processingDetails']['processingStatus']
        print(f"Processing: {status}")
        if status == "succeeded":
            break
        elif status == "failed":
            raise Exception("Processing failed.")
        time.sleep(10)
