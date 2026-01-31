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
    # Delete old video if it exists
    if os.path.exists("video.mp4"):
        try:
            os.remove("video.mp4")
            st.info("🗑️ Removed old video...")
        except:
            pass
    
    st.info("⬇️ Downloading video from Instagram...")
    
    # Use yt-dlp with best settings for Instagram
    result = subprocess.run([
        "yt-dlp",
        "--no-check-certificates",
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "-f", "best",
        "--merge-output-format", "mp4",
        "-o", "video.mp4",
        insta_url
    ], capture_output=True, text=True)
    
    # Check if download succeeded
    if result.returncode == 0 and os.path.exists("video.mp4"):
        file_size = os.path.getsize("video.mp4")
        if file_size > 0:
            st.success(f"✅ Video downloaded! ({file_size / (1024*1024):.2f} MB)")
            return True
        else:
            st.error("❌ Downloaded file is empty")
            return False
    else:
        st.error("❌ Download failed!")
        
        # Show helpful error message
        if "login" in result.stderr.lower() or "rate" in result.stderr.lower():
            st.warning("⚠️ Instagram is blocking the download. Try:")
            st.info("1. Make sure the Instagram reel is PUBLIC (not private)")
            st.info("2. Try a different Instagram link")
            st.info("3. Wait a few minutes and try again (rate limit)")
        
        with st.expander("🔍 See error details"):
            st.code(result.stderr, language="text")
        
        return False

def get_authenticated_service():
    # 1. Try to load from Streamlit Secrets (Best for Cloud)
    if "google_token" in st.secrets and "token_json" in st.secrets["google_token"]:
        try:
            token_info = json.loads(st.secrets["google_token"]["token_json"])
            creds = Credentials.from_authorized_user_info(token_info, ["https://www.googleapis.com/auth/youtube.upload"])
            
            # Refresh if needed
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            
            return build("youtube", "v3", credentials=creds)
        except Exception as e:
            st.warning(f"Secret token failed: {e}")

    # 2. Try to load from existing token.json (local usage)
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/youtube.upload"])
    
    # 3. If valid, return it
    if creds and creds.valid:
        return build("youtube", "v3", credentials=creds)
        
    # 4. If expired, try to refresh
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            # Save refreshed token
            with open("token.json", "w") as token:
                token.write(creds.to_json())
            return build("youtube", "v3", credentials=creds)
        except:
            st.warning("Token expired and refresh failed. Please re-authenticate.")

    # 5. Fail gracefully with instructions
    st.error("🔒 Authentication Required!")
    st.info("""
    **Google prevents logging in directly from this cloud app.**
    
    1. Run `python generate_token.py` on your computer.
    2. Login and copy the generated Code.
    3. Paste it into your Streamlit Secrets.
    """)
    return None

def upload_to_youtube(video_title):
    youtube = get_authenticated_service()
    if not youtube:
        return False

    st.info("⬆️ Uploading to YouTube...")
    
    try:
        # Check if video file exists
        if not os.path.exists("video.mp4"):
            st.error("❌ Video file not found!")
            return False
        
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
        
        # Show YouTube link
        video_id = response.get("id")
        if video_id:
            youtube_url = f"https://www.youtube.com/watch?v={video_id}"
            st.success(f"🎥 [Watch on YouTube]({youtube_url})")
        
        with st.expander("📊 See upload details"):
            st.json(response)
        
        # Clean up the video file after successful upload
        try:
            os.remove("video.mp4")
            st.info("🧹 Cleaned up video file.")
        except:
            pass
        
        return True
    except Exception as e:
        st.error(f"❌ Upload failed: {e}")
        return False

# ===============================
# UI
# ===============================
st.markdown("---")
st.markdown("### 📝 Instructions")
st.info("1. Paste Instagram Reel link\n2. Enter YouTube title\n3. Click 'Run Automation'")

insta_link = st.text_input("🔗 Paste Instagram Reel link", placeholder="https://www.instagram.com/reel/...")
video_title_input = st.text_input("📝 Enter YouTube title", placeholder="My Awesome Short")

if st.button("🚀 Run Automation", type="primary"):
    if insta_link and video_title_input:
        # Validate Instagram URL
        if "instagram.com" not in insta_link:
            st.error("❌ Please enter a valid Instagram link!")
        else:
            # Download video first
            with st.spinner("Downloading..."):
                download_success = download_video(insta_link)
            
            # Only upload if download was successful
            if download_success:
                with st.spinner("Uploading to YouTube..."):
                    upload_to_youtube(video_title_input)
            else:
                st.error("❌ Cannot upload - download failed!")
    else:
        st.warning("⚠️ Please fill in both fields!")

st.markdown("---")
st.caption("Made with ❤️ | Instagram to YouTube Automation")
