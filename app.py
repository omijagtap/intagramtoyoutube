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
    """Download Instagram video using Instaloader API"""
    
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
        
        # Use Instagram's embed API to get video URL
        embed_url = f"https://www.instagram.com/p/{shortcode}/embed/captioned/"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        # Get embed page
        response = requests.get(embed_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            html_content = response.text
            
            # Try to extract video URL from HTML
            # Look for video_url in the page
            video_url_match = re.search(r'"video_url":"([^"]+)"', html_content)
            
            if not video_url_match:
                # Try alternative pattern
                video_url_match = re.search(r'<video[^>]+src="([^"]+)"', html_content)
            
            if video_url_match:
                video_url = video_url_match.group(1)
                # Unescape URL
                video_url = video_url.replace('\\u0026', '&')
                
                # Download the video
                st.info("📥 Downloading video file...")
                video_response = requests.get(video_url, headers=headers, stream=True, timeout=30)
                
                if video_response.status_code == 200:
                    with open("video.mp4", "wb") as f:
                        for chunk in video_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    # Verify file was downloaded
                    if os.path.exists("video.mp4") and os.path.getsize("video.mp4") > 0:
                        file_size = os.path.getsize("video.mp4") / (1024 * 1024)
                        st.success(f"✅ Video downloaded! ({file_size:.2f} MB)")
                        return True
                    else:
                        st.error("❌ Downloaded file is empty")
                        return False
                else:
                    st.error(f"❌ Failed to download video (Status: {video_response.status_code})")
                    return False
            else:
                st.error("❌ Could not find video URL in Instagram page")
                st.warning("💡 This reel might be private or age-restricted")
                return False
        else:
            st.error(f"❌ Could not access Instagram (Status: {response.status_code})")
            return False
            
    except requests.exceptions.Timeout:
        st.error("❌ Request timed out. Instagram might be slow or blocking requests.")
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

insta_link = st.text_input("🔗 Paste Instagram Reel link", placeholder="https://www.instagram.com/reel/...")
video_title_input = st.text_input("📝 Enter YouTube title", placeholder="My Awesome Short")

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
                st.info("💡 **Tips:**")
                st.info("• Make sure the reel is PUBLIC (not private)")
                st.info("• Try a different Instagram link")
                st.info("• Some reels may be blocked by Instagram")
    else:
        st.warning("⚠️ Please fill in both fields!")

st.markdown("---")
st.caption("Made with ❤️ | Instagram to YouTube Automation")
