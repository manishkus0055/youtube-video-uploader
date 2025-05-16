# backend/scheduler.py

import os
import time
import random
from datetime import datetime, timedelta
from app.config import RANDOM_EXTRA_DELAY_HOURS, VIDEO_LIMIT_PER_DAY, VIDEO_MIN_PER_DAY

LAST_UPLOAD_FILE = "data/last_upload_time.txt"

# Minimum wait between upload sessions
BASE_WAIT_HOURS = 24

def has_wait_time_passed():
    """Check if 24h + random delay has passed since last upload"""
    if not os.path.exists(LAST_UPLOAD_FILE):
        return True

    try:
        with open(LAST_UPLOAD_FILE, "r") as f:
            parts = f.read().strip().split("|")
            if len(parts) != 2:
                return True
            last_time_str, random_delay_str = parts
            last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")
            random_delay = int(random_delay_str)

            next_upload_time = last_time + timedelta(hours=BASE_WAIT_HOURS + random_delay)
            return datetime.now() >= next_upload_time
    except Exception:
        return True

def update_last_upload_time():
    """Update last upload time and generate new random delay"""
    random_delay = random.randint(0, RANDOM_EXTRA_DELAY_HOURS)
    now = datetime.now()
    with open(LAST_UPLOAD_FILE, "w") as f:
        f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')}|{random_delay}")
    print(f"✅ Next upload will be scheduled after {BASE_WAIT_HOURS + random_delay} hours.")

def get_daily_upload_limit():
    """Return a random number of videos to upload today within defined range"""
    return random.randint(VIDEO_MIN_PER_DAY, VIDEO_LIMIT_PER_DAY)

def random_sleep_between(min_minutes=10, max_minutes=60):
    """Sleep between videos to simulate natural upload intervals"""
    seconds = random.randint(min_minutes * 60, max_minutes * 60)
    print(f"🕒 Sleeping for {seconds // 60} minutes before next upload...")
    time.sleep(seconds)
