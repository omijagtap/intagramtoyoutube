import subprocess
import os
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
    # Delete old video if exists
    if os.path.exists("video.mp4"):
        try:
            os.remove("video.mp4")
            print("🗑️ Removed old video")
        except:
            pass
    
    print("⬇️ Downloading video from Instagram...")
    
    # Try with Chrome cookies first (works best for Instagram)
    result = subprocess.run([
        "yt-dlp",
        "--cookies-from-browser", "chrome",
        "-f", "best",
        "-o", "video.mp4",
        insta_url
    ], capture_output=True, text=True)
    
    # If Chrome fails, try Firefox
    if result.returncode != 0:
        print("🔄 Trying with Firefox cookies...")
        result = subprocess.run([
            "yt-dlp",
            "--cookies-from-browser", "firefox",
            "-f", "best",
            "-o", "video.mp4",
            insta_url
        ], capture_output=True, text=True)
    
    # If both fail, try without cookies
    if result.returncode != 0:
        print("🔄 Trying without cookies...")
        result = subprocess.run([
            "yt-dlp",
            "-f", "best",
            "-o", "video.mp4",
            insta_url
        ], capture_output=True, text=True)
    
    if result.returncode == 0 and os.path.exists("video.mp4"):
        file_size = os.path.getsize("video.mp4") / (1024 * 1024)
        print(f"✅ Video downloaded! ({file_size:.2f} MB)")
        return True
    else:
        print("❌ Download failed!")
        print(result.stderr)
        return False

# Upload to YouTube
def upload_to_youtube(video_title):
    print("⬆️ Uploading to YouTube...")
    
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

    response = request.execute()
    
    video_id = response.get("id")
    if video_id:
        print(f"✅ Upload complete!")
        print(f"🎥 Watch at: https://www.youtube.com/watch?v={video_id}")
    
    # Clean up video file
    try:
        os.remove("video.mp4")
        print("🧹 Cleaned up video file")
    except:
        pass

# ===============================
# MAIN PROGRAM
# ===============================
print("=" * 50)
print("🚀 Instagram to YouTube Shorts Bot")
print("=" * 50)

insta_link = input("\n🔗 Paste Instagram Reel link: ")
title = input("📝 Enter YouTube title: ")

print("\n" + "=" * 50)

# Download
if download_video(insta_link):
    # Upload only if download succeeded
    upload_to_youtube(title)
    print("\n✅ All done!")
else:
    print("\n❌ Cannot upload - download failed!")
    print("\n💡 Make sure you're logged into Instagram in Chrome or Firefox browser")

print("=" * 50)

