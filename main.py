import subprocess
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# ===============================
# 🔴 CHANGE ONLY THIS PART
# ===============================
STATIC_DESCRIPTION = """
Follow the channel and support us on the journey to 1K subscribers ❤️  
We upload short videos based on motivation and real-life mindset.

#Shorts #Motivation #Reels
"""

# ===============================
# 🔴 DO NOT CHANGE BELOW
# ===============================

# Download Instagram Reel
def download_video(insta_url):
    subprocess.run([
        "yt-dlp",
        "-f", "mp4",
        "-o", "video.mp4",
        insta_url
    ])

# Upload to YouTube
def upload_to_youtube(video_title):
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json",
        ["https://www.googleapis.com/auth/youtube.upload"]
    )
    creds = flow.run_local_server(port=0)

    youtube = build("youtube", "v3", credentials=creds)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": video_title,
                "description": STATIC_DESCRIPTION,
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload("video.mp4", resumable=True)
    )

    request.execute()

# ===============================
# MAIN PROGRAM
# ===============================
insta_link = input("Paste Instagram Reel link: ")
title = input("Enter YouTube title: ")

download_video(insta_link)
upload_to_youtube(title)

print("✅ Upload complete!")
