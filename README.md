# YouTube Video Auto Uploader (Python)

Automate uploading your videos to YouTube using the YouTube Data API v3.  
This project handles OAuth2 authentication, manages video metadata, schedules daily uploads, and tracks uploaded videos.

---

## 📋 Project Overview

- Upload videos automatically from a folder (`videos/`)
- Auto-increment video titles (e.g., "My Title 1", "My Title 2", ...)
- Use default descriptions and tags from config
- Keep track of uploads to avoid duplicates
- Wait 24 hours plus random delay between uploads
- Secure OAuth2 authentication with token caching

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/youtube-video-uploader.git
cd youtube-video-uploader
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Google OAuth2 Setup

You need to create OAuth credentials to authorize this app to upload videos on your behalf.

### Step-by-step:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. In **APIs & Services** → **Library**, enable **YouTube Data API v3**
4. In **APIs & Services** → **OAuth consent screen**, configure your app:

   * User type: External or Internal (as needed)
   * Add app name and your email
   * Save and continue
5. Go to **Credentials** → **Create Credentials** → **OAuth client ID**

   * Application type: **Desktop app**
   * Name it (e.g., `YouTubeUploader`)
6. Download the generated `client_secret.json`
7. Place `client_secret.json` in the root folder of this project

---

## 🛠 Initial Authentication ("Credify")

Before running the uploader, you need to authenticate your Google account and generate a `token.pickle`.

### To do this:

1. Open the `app/auth.py` file
2. Add the following function (for one-time use):

```python
def initial_credify():
    """
    Run this function once to generate token.pickle by
    performing OAuth login in the browser.
    """
    creds = None
    if os.path.exists('user_data/default/token.pickle'):
        with open('user_data/default/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('user_data/default/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    print("Authentication successful. token.pickle created.")
```

3. In `auth.py`, call this function once at the bottom:

```python
if __name__ == '__main__':
    initial_credify()
```

4. Run the auth file:

```bash
python app/auth.py
```

5. A browser window will open, log in with your Google account and grant permissions
6. After success, **delete** the `initial_credify` function and its call in `auth.py` to keep your code clean

---

## 🏃‍♂️ Running the uploader

1. Place your video files (e.g., `.mp4`) inside the `videos/` folder
2. Edit metadata (title base, description, tags) in `app/config.py` as needed
3. Run the uploader:

```bash
python main.py
```

The program will:

* Upload new videos automatically (limit daily uploads as configured)
* Skip videos that have already been uploaded
* Use auto-incremented titles and default metadata
* Log uploads to `data/video_db.json`
* Wait 24 hours + random delay between runs

---

## 📁 Folder/File Summary

| Folder/File          | Purpose                              |
| -------------------- | ------------------------------------ |
| `app/`               | Main app logic and modules           |
| `videos/`            | Put your local video files here      |
| `data/`              | Logs and database files              |
| `user_data/default/` | OAuth token storage (`token.pickle`) |
| `client_secret.json` | Google OAuth client credentials      |
| `.gitignore`         | Files/folders to exclude from git    |
| `main.py`            | Main entry point to run uploader     |
| `requirements.txt`   | Python dependencies                  |

---
