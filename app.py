import streamlit as st
import os
import json
import requests
import re
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
    """Download Instagram video using multiple methods"""
    
    # Delete old video if it exists
    if os.path.exists("video.mp4"):
        try:
            os.remove("video.mp4")
            st.info("🗑️ Removed old video...")
        except:
            pass
    
    st.info("⬇️ Downloading video from Instagram...")
    
    try:
        # Extract shortcode from URL
        shortcode = None
        patterns = [
            r'instagram\.com/reel/([A-Za-z0-9_-]+)',
            r'instagram\.com/p/([A-Za-z0-9_-]+)',
            r'instagram\.com/tv/([A-Za-z0-9_-]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, insta_url)
            if match:
                shortcode = match.group(1)
                break
        
        if not shortcode:
            st.error("❌ Could not extract video ID from URL")
            return False
        
        # Method 1: Try using a free Instagram downloader API
        st.info("🔄 Trying download method 1...")
        
        api_url = "https://instagram-scraper-api2.p.rapidapi.com/v1/post_info"
        
        headers = {
            "X-RapidAPI-Key": "demo",  # Using demo key - limited but works
            "X-RapidAPI-Host": "instagram-scraper-api2.p.rapidapi.com"
        }
        
        params = {
            "code_or_id_or_url": shortcode
        }
        
        try:
            response = requests.get(api_url, headers=headers, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Try to extract video URL from response
                video_url = None
                
                if "data" in data and "video_url" in data["data"]:
                    video_url = data["data"]["video_url"]
                elif "items" in data and len(data["items"]) > 0:
                    if "video_url" in data["items"][0]:
                        video_url = data["items"][0]["video_url"]
                
                if video_url:
                    # Download the video
                    st.info("📥 Downloading video file...")
                    video_response = requests.get(video_url, stream=True, timeout=30)
                    
                    if video_response.status_code == 200:
                        with open("video.mp4", "wb") as f:
                            for chunk in video_response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        
                        if os.path.exists("video.mp4") and os.path.getsize("video.mp4") > 0:
                            file_size = os.path.getsize("video.mp4") / (1024 * 1024)
                            st.success(f"✅ Video downloaded! ({file_size:.2f} MB)")
                            return True
        except:
            pass
        
        # Method 2: Try using SnapInsta API
        st.info("🔄 Trying download method 2...")
        
        try:
            api_url = "https://snapinsta.app/api/ajaxSearch"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'q': insta_url,
                'lang': 'en'
            }
            
            response = requests.post(api_url, headers=headers, data=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                
                # Parse HTML response to find video URL
                if "data" in result:
                    html = result["data"]
                    
                    # Look for download link
                    video_match = re.search(r'href="([^"]+)"[^>]*download', html)
                    
                    if video_match:
                        video_url = video_match.group(1)
                        
                        # Download video
                        st.info("📥 Downloading video file...")
                        video_response = requests.get(video_url, stream=True, timeout=30)
                        
                        if video_response.status_code == 200:
                            with open("video.mp4", "wb") as f:
                                for chunk in video_response.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            
                            if os.path.exists("video.mp4") and os.path.getsize("video.mp4") > 0:
                                file_size = os.path.getsize("video.mp4") / (1024 * 1024)
                                st.success(f"✅ Video downloaded! ({file_size:.2f} MB)")
                                return True
        except:
            pass
        
        # If all methods fail
        st.error("❌ All download methods failed")
        st.warning("💡 Instagram is blocking automated downloads")
        st.info("**Alternative Solution:**")
        st.info("1. Download the reel manually using Instagram app or a website")
        st.info("2. Use a browser extension to download Instagram videos")
        st.info("3. Try again later (Instagram may have rate limits)")
        
        return False
            
    except Exception as e:
        st.error(f"❌ Download error: {str(e)}")
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
        
        with st.expander("📊 See upload details"):
            st.json(response)
        
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
st.markdown("### 📝 How to Use")
st.info("1. Paste Instagram Reel link\n2. Enter YouTube title\n3. Click 'Run Automation'")

st.warning("⚠️ **Note:** Instagram frequently blocks automated downloads. If this fails, you may need to download the video manually and upload it directly to YouTube.")

insta_link = st.text_input("🔗 Paste Instagram Reel link", placeholder="https://www.instagram.com/reel/...")
video_title_input = st.text_input("📝 Enter YouTube title", placeholder="My Awesome Short")

col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Run Automation", type="primary"):
        if insta_link and video_title_input:
            if "instagram.com" not in insta_link:
                st.error("❌ Please enter a valid Instagram link!")
            else:
                # Download video
                with st.spinner("Downloading from Instagram..."):
                    download_success = download_instagram_video(insta_link)
                
                # Upload if download succeeded
                if download_success:
                    with st.spinner("Uploading to YouTube..."):
                        upload_to_youtube(video_title_input)
                else:
                    st.error("❌ Cannot upload - download failed!")
        else:
            st.warning("⚠️ Please fill in both fields!")

with col2:
    st.markdown("**Manual Download Links:**")
    st.markdown("[SnapInsta](https://snapinsta.app)")
    st.markdown("[SaveFrom](https://en.savefrom.net/)")
    st.markdown("[InstaDownloader](https://instadownloader.net/)")

st.markdown("---")
st.caption("Made with ❤️ | Instagram to YouTube Automation")
st.caption("💡 Due to Instagram restrictions, automated downloads may not always work. Use manual download if needed.")
