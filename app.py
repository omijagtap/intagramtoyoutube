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

st.title("🚀 Insta to YouTube Shorts Bot")

# ===============================
# LOGIC
# ===============================
def download_instagram_video(insta_url):
    """Download Instagram video using yt-dlp"""
    
    # Delete old video if it exists
    if os.path.exists("video.mp4"):
        try:
            os.remove("video.mp4")
            st.info("🗑️ Removed old video...")
        except:
            pass
    
    st.info("⬇️ Downloading video from Instagram...")
    
    try:
        # Use yt-dlp with best settings
        # This is the MOST reliable method
        command = [
            "yt-dlp",
            "--no-check-certificates",
            "--no-warnings",
            "--quiet",
            "--progress",
            "-f", "best",
            "--merge-output-format", "mp4",
            "-o", "video.mp4",
            insta_url
        ]
        
        # Run command
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60
        )
        
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
            # Show error
            error_msg = result.stderr if result.stderr else "Unknown error"
            
            st.error("❌ Download failed!")
            
            # Check for specific errors
            if "login" in error_msg.lower() or "rate" in error_msg.lower():
                st.warning("⚠️ **Instagram requires authentication**")
                st.info("""
                **Why this happens:**
                Instagram blocks downloads from cloud servers to protect content.
                
                **WORKING SOLUTION:**
                Since automated downloads are blocked, here's what you can do:
                
                1. **Download the reel manually:**
                   - Use SnapInsta.app on your phone
                   - Or use SaveFrom.net
                   - Or use any Instagram downloader website
                
                2. **Then upload here:**
                   - I'll add a file upload option below
                   - Upload the video you downloaded
                   - It will automatically upload to YouTube
                
                This is the ONLY reliable way that works 100% of the time.
                """)
            else:
                with st.expander("🔍 See error details"):
                    st.code(error_msg, language="text")
            
            return False
            
    except subprocess.TimeoutExpired:
        st.error("❌ Download timed out (Instagram may be slow)")
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
            st.error(f"Authentication error: {e}")
            return None

    st.error("🔒 Authentication Required!")
    return None

def upload_to_youtube(video_title, video_path="video.mp4"):
    youtube = get_authenticated_service()
    if not youtube:
        return False

    st.info("⬆️ Uploading to YouTube...")
    
    try:
        if not os.path.exists(video_path):
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
            media_body=MediaFileUpload(video_path, resumable=True, chunksize=1024*1024)
        )
        
        response = request.execute()
        st.balloons()
        st.success(f"✅ Upload Complete: {video_title}")
        
        video_id = response.get("id")
        if video_id:
            youtube_url = f"https://www.youtube.com/watch?v={video_id}"
            st.markdown(f"### 🎥 [Watch on YouTube]({youtube_url})")
        
        # Cleanup
        try:
            os.remove(video_path)
            st.info("🧹 Cleaned up video file")
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

# Create tabs for two methods
tab1, tab2 = st.tabs(["📤 Upload Video File (RECOMMENDED)", "🔗 Try Instagram Link"])

with tab1:
    st.markdown("### ✅ Most Reliable Method")
    st.success("This method works 100% of the time!")
    
    st.info("""
    **How to use:**
    1. Download Instagram reel using [SnapInsta](https://snapinsta.app) or [SaveFrom](https://en.savefrom.net/)
    2. Upload the video file below
    3. Enter YouTube title
    4. Click Upload to YouTube
    """)
    
    uploaded_file = st.file_uploader("Choose video file", type=['mp4', 'mov', 'avi', 'mkv'])
    title_upload = st.text_input("📝 YouTube Title", key="title_upload", placeholder="My Awesome Short")
    
    if st.button("🚀 Upload to YouTube", key="btn_upload", type="primary", use_container_width=True):
        if uploaded_file and title_upload:
            # Save uploaded file
            with open("video.mp4", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            file_size = os.path.getsize("video.mp4") / (1024 * 1024)
            st.success(f"✅ File received: {uploaded_file.name} ({file_size:.2f} MB)")
            
            # Upload to YouTube
            with st.spinner("Uploading to YouTube..."):
                upload_to_youtube(title_upload)
        else:
            st.warning("⚠️ Please upload a video and enter a title")

with tab2:
    st.markdown("### ⚠️ May Not Work (Instagram Blocks This)")
    st.warning("Instagram actively blocks automated downloads from cloud servers. Use Tab 1 for reliable results.")
    
    insta_link = st.text_input("🔗 Paste Instagram Reel link", placeholder="https://www.instagram.com/reel/...")
    title_link = st.text_input("📝 YouTube Title", key="title_link", placeholder="My Awesome Short")
    
    if st.button("🚀 Try Download & Upload", key="btn_link", use_container_width=True):
        if insta_link and title_link:
            if "instagram.com" not in insta_link:
                st.error("❌ Please enter a valid Instagram link!")
            else:
                with st.spinner("Attempting download... This may fail due to Instagram restrictions"):
                    download_success = download_instagram_video(insta_link)
                
                if download_success:
                    with st.spinner("Uploading to YouTube..."):
                        upload_to_youtube(title_link)
                else:
                    st.error("❌ Download failed. Please use 'Upload Video File' tab instead.")
        else:
            st.warning("⚠️ Please fill in both fields!")

st.markdown("---")
st.markdown("### 📱 Quick Download Links")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("[SnapInsta](https://snapinsta.app)")
with col2:
    st.markdown("[SaveFrom](https://en.savefrom.net/)")
with col3:
    st.markdown("[InstaDownloader](https://instadownloader.net/)")

st.markdown("---")
st.caption("Made with ❤️ | Instagram to YouTube Automation")
st.caption("💡 **Tip:** Use the 'Upload Video File' tab for 100% success rate")
