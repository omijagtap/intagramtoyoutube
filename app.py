import streamlit as st
import subprocess
import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

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

def get_authenticated_service():
    # 1. Try to load from existing token.json (local usage)
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/youtube.upload"])
    
    # 2. If valid, return it
    if creds and creds.valid:
        return build("youtube", "v3", credentials=creds)
        
    # 3. If expired, try to refresh
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            # Save refreshed token
            with open("token.json", "w") as token:
                token.write(creds.to_json())
            return build("youtube", "v3", credentials=creds)
        except:
            st.warning("Token expired and refresh failed. Please re-authenticate.")

    # 4. If no token, we need to authenticate
    st.info("Authentication Required")
    
    # Load client config from Secrets or File
    client_config = None
    if os.path.exists("client_secret.json"):
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json",
            ["https://www.googleapis.com/auth/youtube.upload"]
        )
    elif "google_auth" in st.secrets:
        client_config = {"installed": dict(st.secrets["google_auth"])}
        flow = InstalledAppFlow.from_client_config(
            client_config,
            ["https://www.googleapis.com/auth/youtube.upload"]
        )
    else:
        st.error("❌ No secrets found! Please add [google_auth] to Streamlit Secrets.")
        return None

    # Use run_local_server if likely local, else use manual code input
    # Since we can't easily detect "Cloud" vs "Local" reliably, we can offer the manual link method in the UI
    
    flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob" 
    auth_url, _ = flow.authorization_url(prompt='consent')
    
    st.markdown(f"**[Click this link to authorize]({auth_url})**")
    auth_code = st.text_input("Paste the authorization code here:")
    
    if auth_code:
        try:
            flow.fetch_token(code=auth_code)
            creds = flow.credentials
            # Save for next time (persistence is tricky on cloud, but helps for session)
            # On Streamlit Cloud, file writes are ephemeral, but this works for the current session.
            with open("token.json", "w") as token:
                token.write(creds.to_json())
            return build("youtube", "v3", credentials=creds)
        except Exception as e:
            st.error(f"Authentication failed: {e}")
            return None
    else:
        st.warning("Waiting for authentication code...")
        return None

def upload_to_youtube(video_title):
    youtube = get_authenticated_service()
    if not youtube:
        return

    st.info("Uploading to YouTube...")
    try:
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
        st.balloons()
        st.success(f"✅ Upload Complete: {video_title}")
        st.json(response)
    except Exception as e:
        st.error(f"Upload failed: {e}")

# ===============================
# UI
# ===============================
insta_link = st.text_input("🔗 Paste Instagram Reel link")
video_title_input = st.text_input("📝 Enter YouTube title")

if st.button("🚀 Run Automation"):
    if insta_link and video_title_input:
        download_video(insta_link)
        upload_to_youtube(video_title_input)
    else:
        st.warning("Please fill in both fields!")
