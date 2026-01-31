import streamlit as st
import os
import json
import subprocess
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
def download_instagram_video(insta_url):
    """Download Instagram video using yt-dlp with cookie support"""
    
    # Delete old video if exists
    if os.path.exists("video.mp4"):
        try:
            os.remove("video.mp4")
            st.info("🗑️ Removed old video...")
        except:
            pass
    
    st.info("⬇️ Downloading video from Instagram...")
    
    try:
        # Method 1: Try with Chrome cookies (works best for Instagram)
        st.info("🔄 Trying with Chrome cookies...")
        result = subprocess.run([
            "yt-dlp",
            "--cookies-from-browser", "chrome",
            "-f", "best",
            "--merge-output-format", "mp4",
            "-o", "video.mp4",
            insta_url
        ], capture_output=True, text=True, timeout=60)
        
        # Method 2: If Chrome fails, try Firefox
        if result.returncode != 0:
            st.info("🔄 Trying with Firefox cookies...")
            result = subprocess.run([
                "yt-dlp",
                "--cookies-from-browser", "firefox",
                "-f", "best",
                "--merge-output-format", "mp4",
                "-o", "video.mp4",
                insta_url
            ], capture_output=True, text=True, timeout=60)
        
        # Method 3: If both fail, try without cookies (may work for public videos)
        if result.returncode != 0:
            st.info("🔄 Trying without cookies...")
            result = subprocess.run([
                "yt-dlp",
                "--no-check-certificates",
                "-f", "best",
                "--merge-output-format", "mp4",
                "-o", "video.mp4",
                insta_url
            ], capture_output=True, text=True, timeout=60)
        
        # Check if download succeeded
        if result.returncode == 0 and os.path.exists("video.mp4"):
            file_size = os.path.getsize("video.mp4")
            if file_size > 0:
                size_mb = file_size / (1024 * 1024)
                st.success(f"✅ Video downloaded! ({size_mb:.2f} MB)")
                return True
            else:
                st.error("❌ Downloaded file is empty")
                return False
        else:
            st.error("❌ All download methods failed!")
            st.warning("⚠️ **Why this happens:**")
            st.info("• Instagram blocks downloads from cloud servers")
            st.info("• You need to be logged into Instagram in Chrome/Firefox")
            st.info("• This works when running locally, not on Streamlit Cloud")
            
            with st.expander("🔍 See error details"):
                st.code(result.stderr, language="text")
            
            return False
            
    except subprocess.TimeoutExpired:
        st.error("❌ Download timed out")
        return False
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return False

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

st.markdown("### � Paste Instagram Link")

st.info("""
**How to use:**
1. Copy Instagram Reel link
2. Paste it below
3. Enter YouTube title
4. Click "Run Automation"
""")

st.warning("⚠️ **Note:** This works best when running locally. On Streamlit Cloud, Instagram may block downloads.")

st.markdown("---")

# Instagram link input
insta_link = st.text_input(
    "🔗 Instagram Reel Link", 
    placeholder="https://www.instagram.com/reel/...",
    help="Paste the Instagram reel URL here"
)

# Title input
video_title = st.text_input(
    "📝 YouTube Title", 
    placeholder="My Awesome Short",
    help="Enter a catchy title for your Short"
)

st.markdown("---")

# Upload button
if st.button("🚀 Run Automation", type="primary", use_container_width=True):
    if insta_link and video_title:
        if "instagram.com" not in insta_link:
            st.error("❌ Please enter a valid Instagram link!")
        else:
            # Download video
            with st.spinner("Downloading from Instagram..."):
                download_success = download_instagram_video(insta_link)
            
            # Upload if download succeeded
            if download_success:
                with st.spinner("Uploading to YouTube..."):
                    upload_to_youtube(video_title)
            else:
                st.error("❌ Cannot upload - download failed!")
                st.info("💡 **Alternative:** Download the reel manually and use the file upload option below")
    else:
        st.warning("⚠️ Please fill in both fields!")

st.markdown("---")
st.markdown("### OR")
st.markdown("---")

# Alternative: File upload
st.markdown("### 📤 Upload Video File (Alternative)")
st.info("If Instagram link doesn't work, download the reel manually and upload here")

uploaded_file = st.file_uploader(
    "📁 Choose video file", 
    type=['mp4', 'mov', 'avi', 'mkv'],
    help="Upload the Instagram reel you downloaded"
)

video_title_upload = st.text_input(
    "📝 YouTube Title", 
    placeholder="My Awesome Short",
    key="title_upload",
    help="Enter a catchy title for your Short"
)

if uploaded_file:
    file_size = len(uploaded_file.getvalue()) / (1024 * 1024)
    st.success(f"✅ File ready: {uploaded_file.name} ({file_size:.2f} MB)")

if st.button("🚀 Upload File to YouTube", type="secondary", use_container_width=True):
    if uploaded_file and video_title_upload:
        # Save uploaded file
        with open("video.mp4", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Upload to YouTube
        with st.spinner("Uploading to YouTube..."):
            upload_to_youtube(video_title_upload)
    else:
        st.warning("⚠️ Please upload a video and enter a title")

st.markdown("---")

# Quick download links
st.markdown("### 📱 Manual Download Links")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("[SnapInsta](https://snapinsta.app)")
with col2:
    st.markdown("[SaveFrom](https://en.savefrom.net/)")
with col3:
    st.markdown("[InstaDownloader](https://instadownloader.net/)")

st.markdown("---")
st.caption("Made with ❤️ | Instagram to YouTube Shorts Automation")
st.caption("✨ Automatically optimized for YouTube Shorts")
st.caption("💡 For best results, run locally with: `streamlit run app.py`")
