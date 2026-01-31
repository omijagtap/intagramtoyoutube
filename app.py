import streamlit as st
import os
import json
import requests
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
def download_video_from_instagram(insta_url):
    """Download Instagram video using a third-party API"""
    
    # Delete old video if it exists
    if os.path.exists("video.mp4"):
        try:
            os.remove("video.mp4")
            st.info("🗑️ Removed old video...")
        except:
            pass
    
    st.info("⬇️ Downloading video from Instagram...")
    
    try:
        # Extract Instagram post ID from URL
        post_id = None
        if "/reel/" in insta_url:
            post_id = insta_url.split("/reel/")[1].split("/")[0].split("?")[0]
        elif "/p/" in insta_url:
            post_id = insta_url.split("/p/")[1].split("/")[0].split("?")[0]
        
        if not post_id:
            st.error("❌ Invalid Instagram URL format")
            return False
        
        # Use RapidAPI Instagram Downloader (free tier available)
        # Alternative: Use instaloader or other methods
        
        # Method 1: Try using a free Instagram downloader API
        api_url = f"https://instagram-scraper-api2.p.rapidapi.com/v1/post_info?code_or_id_or_url={post_id}"
        
        # For now, use a simpler approach with instaloader library
        import subprocess
        
        # Try using instaloader (Python library)
        result = subprocess.run([
            "instaloader",
            "--no-metadata-json",
            "--no-captions",
            "--filename-pattern={shortcode}",
            f":{post_id}",
            "--dirname-pattern=."
        ], capture_output=True, text=True)
        
        # Find the downloaded video file
        for file in os.listdir("."):
            if file.endswith(".mp4") and post_id in file:
                os.rename(file, "video.mp4")
                st.success("✅ Video downloaded!")
                return True
        
        st.error("❌ Could not find downloaded video")
        return False
        
    except Exception as e:
        st.error(f"❌ Download error: {e}")
        return False

def download_video_simple(insta_url):
    """Simplified download using direct request"""
    
    # Delete old video if it exists
    if os.path.exists("video.mp4"):
        try:
            os.remove("video.mp4")
        except:
            pass
    
    st.info("⬇️ Downloading video...")
    
    try:
        # Use a free Instagram video downloader service
        # Note: This uses a third-party service which may have rate limits
        
        # Extract post ID
        post_id = None
        if "/reel/" in insta_url:
            post_id = insta_url.split("/reel/")[1].split("/")[0].split("?")[0]
        elif "/p/" in insta_url:
            post_id = insta_url.split("/p/")[1].split("/")[0].split("?")[0]
        
        if not post_id:
            st.error("❌ Invalid Instagram URL")
            return False
        
        # Use SaveFrom.net API (free)
        api_url = f"https://v3.savefrom.net/api/ajaxSearch"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        data = {
            'q': insta_url,
            'lang': 'en'
        }
        
        response = requests.post(api_url, headers=headers, data=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract video URL from response
            # This part depends on the API response structure
            # For now, show a helpful message
            
            st.warning("⚠️ Instagram download requires authentication")
            st.info("**Alternative Solution:**")
            st.info("1. Download the Instagram video manually to your phone")
            st.info("2. Use the 'Upload Video File' option below")
            
            return False
        else:
            st.error("❌ Download service unavailable")
            return False
            
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return False

def get_authenticated_service():
    # Try to load from Streamlit Secrets
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
    st.info("Please configure Google authentication in Streamlit Secrets")
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
            media_body=MediaFileUpload(video_path, resumable=True)
        )
        
        response = request.execute()
        st.balloons()
        st.success(f"✅ Upload Complete: {video_title}")
        
        video_id = response.get("id")
        if video_id:
            youtube_url = f"https://www.youtube.com/watch?v={video_id}"
            st.success(f"🎥 [Watch on YouTube]({youtube_url})")
        
        # Cleanup
        try:
            os.remove(video_path)
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

# Tab selection
tab1, tab2 = st.tabs(["📱 Upload Video File", "🔗 Instagram Link (Beta)"])

with tab1:
    st.markdown("### � Upload Video Directly")
    st.info("**Recommended:** Download Instagram video to your phone, then upload here")
    
    uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'mov', 'avi'])
    video_title_upload = st.text_input("📝 YouTube Title", key="title_upload", placeholder="My Awesome Short")
    
    if st.button("🚀 Upload to YouTube", key="upload_btn", type="primary"):
        if uploaded_file and video_title_upload:
            # Save uploaded file
            with open("video.mp4", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            # Upload to YouTube
            with st.spinner("Uploading to YouTube..."):
                upload_to_youtube(video_title_upload)
        else:
            st.warning("⚠️ Please upload a video and enter a title")

with tab2:
    st.markdown("### 🔗 Instagram Link Method")
    st.warning("⚠️ This method may not work due to Instagram restrictions")
    st.info("If this fails, please use the 'Upload Video File' tab instead")
    
    insta_link = st.text_input("🔗 Paste Instagram Reel link", placeholder="https://www.instagram.com/reel/...")
    video_title_link = st.text_input("📝 YouTube Title", key="title_link", placeholder="My Awesome Short")
    
    if st.button("🚀 Try Download & Upload", key="link_btn"):
        if insta_link and video_title_link:
            if "instagram.com" not in insta_link:
                st.error("❌ Please enter a valid Instagram link!")
            else:
                download_success = download_video_simple(insta_link)
                
                if download_success:
                    with st.spinner("Uploading to YouTube..."):
                        upload_to_youtube(video_title_link)
                else:
                    st.error("❌ Download failed. Please use 'Upload Video File' tab instead")
        else:
            st.warning("⚠️ Please fill in both fields!")

st.markdown("---")
st.caption("Made with ❤️ | Instagram to YouTube Automation")
st.caption("💡 Tip: For best results, download Instagram videos manually and use the Upload tab")
