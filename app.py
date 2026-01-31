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
    """Download Instagram video using working API"""
    
    # Delete old video if it exists
    if os.path.exists("video.mp4"):
        try:
            os.remove("video.mp4")
            st.info("🗑️ Removed old video...")
        except:
            pass
    
    st.info("⬇️ Downloading video from Instagram...")
    
    try:
        # Method 1: Use Instagram Download API (RapidAPI alternative - free endpoint)
        st.info("🔄 Connecting to download service...")
        
        # Use a public Instagram downloader endpoint
        api_url = "https://v1.nocodeapi.com/demo/instagram/download"
        
        payload = {
            "url": insta_url
        }
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract video URL
                video_url = None
                
                if isinstance(data, dict):
                    if "video_url" in data:
                        video_url = data["video_url"]
                    elif "url" in data:
                        video_url = data["url"]
                    elif "download_url" in data:
                        video_url = data["download_url"]
                    elif "media" in data and isinstance(data["media"], list) and len(data["media"]) > 0:
                        video_url = data["media"][0].get("url")
                
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
        
        # Method 2: Try alternative free API
        st.info("🔄 Trying alternative method...")
        
        try:
            # Extract shortcode
            shortcode = None
            patterns = [
                r'instagram\.com/reel/([A-Za-z0-9_-]+)',
                r'instagram\.com/p/([A-Za-z0-9_-]+)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, insta_url)
                if match:
                    shortcode = match.group(1)
                    break
            
            if shortcode:
                # Use downloadgram.org API
                api_url = f"https://downloadgram.org/reel-downloader.php"
                
                data = {
                    'url': insta_url,
                    'submit': ''
                }
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                
                response = requests.post(api_url, data=data, headers=headers, timeout=20)
                
                if response.status_code == 200:
                    # Parse response for video URL
                    video_match = re.search(r'href="(https://[^"]+\.mp4[^"]*)"', response.text)
                    
                    if video_match:
                        video_url = video_match.group(1)
                        
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
        
        # Method 3: Direct Instagram CDN access (last resort)
        st.info("🔄 Trying direct access method...")
        
        try:
            # Get Instagram post page
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
            
            response = requests.get(insta_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                # Look for video URL in page source
                video_patterns = [
                    r'"video_url":"([^"]+)"',
                    r'<meta property="og:video" content="([^"]+)"',
                    r'"playback_url":"([^"]+)"'
                ]
                
                for pattern in video_patterns:
                    match = re.search(pattern, response.text)
                    if match:
                        video_url = match.group(1)
                        video_url = video_url.replace('\\u0026', '&')
                        
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
                        break
        except:
            pass
        
        # All methods failed
        st.error("❌ All download methods failed")
        st.warning("💡 Instagram is actively blocking downloads")
        st.info("**Possible reasons:**")
        st.info("• The reel is from a private account")
        st.info("• Instagram has rate-limited this server")
        st.info("• The link is invalid or expired")
        
        return False
            
    except Exception as e:
        st.error(f"❌ Download error: {str(e)}")
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
st.info("1. Paste Instagram Reel link (must be PUBLIC)\n2. Enter YouTube title\n3. Click 'Run Automation'")

insta_link = st.text_input("🔗 Paste Instagram Reel link", placeholder="https://www.instagram.com/reel/...")
video_title_input = st.text_input("📝 Enter YouTube title", placeholder="My Awesome Short")

if st.button("🚀 Run Automation", type="primary", use_container_width=True):
    if insta_link and video_title_input:
        if "instagram.com" not in insta_link:
            st.error("❌ Please enter a valid Instagram link!")
        else:
            # Download video
            with st.spinner("Downloading from Instagram... This may take 10-30 seconds"):
                download_success = download_instagram_video(insta_link)
            
            # Upload if download succeeded
            if download_success:
                with st.spinner("Uploading to YouTube..."):
                    upload_to_youtube(video_title_input)
            else:
                st.error("❌ Cannot upload - download failed!")
    else:
        st.warning("⚠️ Please fill in both fields!")

st.markdown("---")
st.caption("Made with ❤️ | Instagram to YouTube Automation")
st.caption("✨ Tries 3 different download methods for best success rate")
