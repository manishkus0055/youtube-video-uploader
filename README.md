# 📺 YouTube Video Auto Uploader

Automate your YouTube uploads using Python and the YouTube Data API.  
Perfect for scheduled uploading, personal backups, and creator workflows.

---

## 🔧 Features

- 📁 Uploads videos from a folder, one per day
- 🏷️ Auto-incrementing titles: `t 1`, `t 2`, `t 3`, ...
- 📝 One-time setup for description and tags (reused every upload)
- 🧠 Keeps track of uploaded videos (won’t upload twice)
- ⏱️ Enforces a 24+ hour wait between uploads (configurable)
- 🔐 OAuth2-based login with your own Google account

---

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/youtube-video-uploader.git
cd youtube-video-uploader
pip install -r requirements.txt
