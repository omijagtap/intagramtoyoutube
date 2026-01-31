import streamlit as st
import subprocess
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# ===============================
# CONFIG
# ===============================
STATIC_DESCRIPTION = """
Follow the channel and support us on the journey to 1K subscribers ❤️  
We upload short videos based on motivation and real-life mindset.

#Shorts #Motivation #Reels
"""

st.title("🚀 Insta to YouTube Shorts Bot")

# ===============================
# LOGIC
# ===============================
def download_video(insta_url):
    st.info("Downloading video...")
    subprocess.run([
        "yt-dlp",
        "-f", "mp4",
        "-o", "video.mp4",
        insta_url
    ])
    st.success("Video downloaded!")

def upload_to_youtube(video_title):
    st.info("Uploading to YouTube...")
    
    # Check if client_secret exists
    if not os.path.exists("client_secret.json"):
        st.error("❌ client_secret.json not found! Please upload it.")
        return

    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json",
        ["https://www.googleapis.com/auth/youtube.upload"]
    )
    # Note: run_local_server requires a browser, which might not work on cloud hosting easily without special config
    # For now we keep it simple for local web app usage
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
    st.balloons()
    st.success(f"✅ Upload Complete: {video_title}")

# ===============================
# UI
# ===============================
insta_link = st.text_input("🔗 Paste Instagram Reel link")
title = st.text_input("📝 Enter YouTube title")

if st.button("🚀 Run Automation"):
    if insta_link and title:
        try:
            download_video(insta_link)
            upload_to_youtube(title)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please fill in both fields!")
