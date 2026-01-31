import streamlit as st
import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
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

st.set_page_config(page_title="Insta to YouTube Shorts", page_icon="🚀")

st.title("🚀 Instagram to YouTube Shorts Bot")
st.markdown("---")

# ===============================
# LOGIC
# ===============================
def get_authenticated_service():
    if "google_token" in st.secrets and "token_json" in st.secrets["google_token"]:
        try:
            token_info = json.loads(st.secrets["google_token"]["token_json"])
            creds = Credentials.from_authorized_user_info(token_info, ["https://www.googleapis.com/auth/youtube.upload"])
            
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            
            return build("youtube", "v3", credentials=creds)
        except Exception as e:
            st.error(f"❌ Authentication error: {e}")
            return None

    st.error("🔒 Authentication Required!")
    st.info("Please configure Google authentication in Streamlit Secrets")
    return None

def upload_to_youtube(video_title, video_path="video.mp4"):
    youtube = get_authenticated_service()
    if not youtube:
        return False

    st.info("⬆️ Uploading to YouTube Shorts...")
    
    # Add #Shorts to title if not already there
    if "#shorts" not in video_title.lower():
        video_title = video_title + " #Shorts"
    
    try:
        if not os.path.exists(video_path):
            st.error("❌ Video file not found!")
            return False
        
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Preparing upload...")
        progress_bar.progress(25)
        
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": video_title,
                    "description": STATIC_DESCRIPTION,
                    "categoryId": "22",
                    "tags": ["Shorts", "Short", "Vertical Video", "Instagram", "Reels"]
                },
                "status": {
                    "privacyStatus": "public",
                    "selfDeclaredMadeForKids": False
                }
            },
            media_body=MediaFileUpload(video_path, resumable=True, chunksize=1024*1024)
        )
        
        status_text.text("Uploading to YouTube...")
        progress_bar.progress(50)
        
        response = request.execute()
        
        progress_bar.progress(100)
        status_text.text("Upload complete!")
        
        st.balloons()
        st.success(f"✅ Upload Complete: {video_title}")
        
        video_id = response.get("id")
        if video_id:
            youtube_url = f"https://www.youtube.com/watch?v={video_id}"
            st.markdown(f"### 🎥 [Watch on YouTube]({youtube_url})")
            st.info(f"📱 Shorts URL: https://youtube.com/shorts/{video_id}")
        
        # Cleanup
        try:
            os.remove(video_path)
            st.caption("🧹 Video file cleaned up")
        except:
            pass
        
        return True
    except Exception as e:
        st.error(f"❌ Upload failed: {e}")
        return False

# ===============================
# UI
# ===============================

st.markdown("### 📤 Upload Instagram Reel to YouTube Shorts")

st.info("""
**How to use:**
1. Download Instagram reel using [SnapInsta](https://snapinsta.app) or [SaveFrom](https://en.savefrom.net/)
2. Upload the video file below
3. Enter YouTube title
4. Click "Upload to YouTube Shorts"
""")

st.markdown("---")

# File uploader
uploaded_file = st.file_uploader(
    "📁 Choose video file", 
    type=['mp4', 'mov', 'avi', 'mkv'],
    help="Upload the Instagram reel you downloaded"
)

# Title input
video_title = st.text_input(
    "📝 YouTube Title", 
    placeholder="My Awesome Short",
    help="Enter a catchy title for your Short"
)

# Show file info if uploaded
if uploaded_file:
    file_size = len(uploaded_file.getvalue()) / (1024 * 1024)
    st.success(f"✅ File ready: {uploaded_file.name} ({file_size:.2f} MB)")
    
    # Show video preview
    st.video(uploaded_file)

st.markdown("---")

# Upload button
if st.button("� Upload to YouTube Shorts", type="primary", use_container_width=True):
    if uploaded_file and video_title:
        # Save uploaded file
        with open("video.mp4", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Upload to YouTube
        with st.spinner("Uploading to YouTube..."):
            upload_to_youtube(video_title)
    else:
        st.warning("⚠️ Please upload a video and enter a title")

st.markdown("---")

# Quick download links
st.markdown("### 📱 Quick Download Links")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("[![SnapInsta](https://img.shields.io/badge/SnapInsta-Download-red)](https://snapinsta.app)")
with col2:
    st.markdown("[![SaveFrom](https://img.shields.io/badge/SaveFrom-Download-blue)](https://en.savefrom.net/)")
with col3:
    st.markdown("[![InstaDownloader](https://img.shields.io/badge/InstaDownloader-Download-green)](https://instadownloader.net/)")

st.markdown("---")
st.caption("Made with ❤️ | Instagram to YouTube Shorts Automation")
st.caption("✨ Automatically optimized for YouTube Shorts")
