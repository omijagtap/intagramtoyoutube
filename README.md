# 🚀 Instagram to YouTube Shorts Bot

Automatically download Instagram Reels and upload them to YouTube as Shorts with proper optimization.

---

## ✨ Features

- ✅ Download Instagram Reels automatically
- ✅ Upload to YouTube as Shorts (with #Shorts tag)
- ✅ Auto-cleanup of video files
- ✅ Progress tracking
- ✅ Multiple download methods (Chrome/Firefox cookies)
- ✅ Web interface (Streamlit) + Console version
- ✅ Optimized for YouTube Shorts algorithm

---

## 📋 Prerequisites

Before you start, make sure you have:

1. **Python 3.8+** installed
2. **Google Cloud Project** with YouTube Data API v3 enabled
3. **Instagram account** (logged in Chrome or Firefox)
4. **yt-dlp** installed

---

## 🛠️ Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/omijagtap/intagramtoyoutube.git
cd intagramtoyoutube
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Install yt-dlp

**Windows:**
```bash
pip install yt-dlp
```

**Mac/Linux:**
```bash
pip install yt-dlp
```

### Step 4: Set Up Google Cloud Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable **YouTube Data API v3**
4. Create **OAuth 2.0 credentials** (Desktop app)
5. Download the credentials as `client_secret.json`
6. Place `client_secret.json` in the project folder

---

## 🎯 Usage

You have **3 ways** to use this tool:

### **Option 1: Console Version (Recommended for Instagram Links)**

Simple command-line interface:

```bash
python main.py
```

**What it does:**
1. Asks for Instagram Reel link
2. Asks for YouTube title
3. Downloads video (using your browser cookies)
4. Uploads to YouTube as Short
5. Shows YouTube link

**Example:**
```
🔗 Paste Instagram Reel link: https://www.instagram.com/reel/ABC123/
📝 Enter YouTube title: Amazing Nature Video

⬇️ Downloading video from Instagram...
✅ Video downloaded! (5.23 MB)
⬆️ Uploading to YouTube...
✅ Upload complete!
🎥 Watch at: https://www.youtube.com/watch?v=xyz123
```

---

### **Option 2: Streamlit Web App (Local)**

Beautiful web interface with Instagram link support:

```bash
streamlit run app.py
```

Then open your browser to: **http://localhost:8501**

**Features:**
- 🔗 Paste Instagram links directly
- 📤 Or upload video files
- 📊 Progress bars
- 🎥 Video preview
- 📱 Mobile-friendly

**Best for:** When you want a nice UI and Instagram links

---

### **Option 3: Streamlit Cloud (File Upload Only)**

Deploy to Streamlit Cloud for access from anywhere:

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy from your repository
4. Add `google_token` to Secrets (see below)

**Note:** Instagram links don't work on cloud (use file upload instead)

---

## 🔐 Authentication Setup

### For Local Use (main.py and local Streamlit):

Just run the script - it will open a browser for Google login on first use.

### For Streamlit Cloud:

1. **Generate token locally:**
   ```bash
   python generate_token.py
   ```

2. **Copy the output** (it will look like this):
   ```
   token_json = '{"token": "...", "refresh_token": "...", ...}'
   ```

3. **Add to Streamlit Secrets:**
   - Go to your app settings on Streamlit Cloud
   - Click "Secrets"
   - Add:
   ```toml
   [google_token]
   token_json = '{"token": "...", "refresh_token": "...", ...}'
   ```

---

## 📁 Project Structure

```
insta_to_youtube/
├── main.py                 # Console version (Instagram links work)
├── app.py                  # Streamlit web app
├── generate_token.py       # Generate auth token for cloud
├── requirements.txt        # Python dependencies
├── client_secret.json      # Google OAuth credentials (YOU ADD THIS)
├── .gitignore             # Excludes sensitive files
└── README.md              # This file
```

---

## 🎬 How It Works

### Download Process:
1. **Tries Chrome cookies** - Uses your Instagram login from Chrome
2. **Tries Firefox cookies** - Falls back to Firefox if Chrome fails
3. **Tries without cookies** - Last resort for public videos

### Upload Process:
1. **Adds #Shorts tag** - Automatically appends if not in title
2. **Sets metadata** - Category: People & Blogs, Tags: Shorts, etc.
3. **Marks as Short** - Proper settings for YouTube Shorts
4. **Uploads video** - With progress tracking
5. **Returns link** - Direct YouTube and Shorts URLs

---

## 🔧 Troubleshooting

### "Download failed" Error

**Problem:** Instagram is blocking the download

**Solutions:**
1. Make sure you're logged into Instagram in Chrome or Firefox
2. Try running locally (not on cloud)
3. Use file upload instead of Instagram link
4. Download manually from [SnapInsta.app](https://snapinsta.app)

### "Authentication Required" Error

**Problem:** Google credentials not set up

**Solutions:**
1. Make sure `client_secret.json` is in the project folder
2. For cloud: Add `google_token` to Streamlit Secrets
3. Run `python generate_token.py` to generate token

### "yt-dlp not found" Error

**Problem:** yt-dlp not installed

**Solution:**
```bash
pip install yt-dlp
```

### Video Not Appearing as Short

**Problem:** Video doesn't show in Shorts feed

**Reasons:**
- Video must be vertical (9:16 ratio) ✅ Instagram reels are
- Video must be under 60 seconds ✅ Most reels are
- Must have #Shorts tag ✅ Auto-added
- May take a few hours to appear in Shorts feed

---

## 📱 Quick Start Guide

### For Beginners:

1. **Install Python** from [python.org](https://python.org)

2. **Download this project:**
   - Click "Code" → "Download ZIP"
   - Extract to a folder

3. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Get Google credentials:**
   - Follow "Step 4" in Installation section
   - Save as `client_secret.json`

5. **Run the tool:**
   ```bash
   python main.py
   ```

6. **Paste Instagram link and title**

7. **Done!** Video uploads to YouTube

---

## 🌐 Deployment to Streamlit Cloud

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Deploy!

3. **Add Secrets:**
   - Run `python generate_token.py` locally
   - Copy the output
   - Add to Streamlit Secrets

4. **Use the app:**
   - Upload video files (Instagram links won't work on cloud)
   - Enter title
   - Upload to YouTube

---

## 🎨 Customization

### Change Video Description:

Edit `STATIC_DESCRIPTION` in `main.py` or `app.py`:

```python
STATIC_DESCRIPTION = """
Your custom description here!

#YourHashtags
"""
```

### Change Privacy Setting:

In the upload function, change:
```python
"privacyStatus": "public"  # Options: public, private, unlisted
```

### Change Category:

```python
"categoryId": "22"  # 22 = People & Blogs
# Other options: 10 = Music, 24 = Entertainment, etc.
```

---

## 📊 Comparison: Which Version to Use?

| Feature | Console (`main.py`) | Local Streamlit | Cloud Streamlit |
|---------|---------------------|-----------------|-----------------|
| Instagram Links | ✅ Yes | ✅ Yes | ❌ No |
| File Upload | ❌ No | ✅ Yes | ✅ Yes |
| Web Interface | ❌ No | ✅ Yes | ✅ Yes |
| Access from Phone | ❌ No | ⚠️ Same WiFi | ✅ Anywhere |
| Setup Difficulty | ⭐ Easy | ⭐⭐ Medium | ⭐⭐⭐ Hard |
| Best For | Quick uploads | Best UI | Remote access |

---

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

## ⚠️ Important Notes

1. **Instagram Terms:** Respect Instagram's terms of service. Only download content you have rights to.

2. **YouTube Guidelines:** Make sure you have rights to upload the content to YouTube.

3. **Rate Limits:** Instagram may rate-limit downloads. If blocked, wait a few minutes.

4. **Copyright:** Only upload content you own or have permission to use.

---

## 📝 License

This project is for educational purposes. Use responsibly and respect platform terms of service.

---

## 💡 Tips for Best Results

1. **Use vertical videos** - Instagram Reels are already vertical ✅
2. **Keep under 60 seconds** - YouTube Shorts requirement
3. **Add engaging titles** - Include keywords and emojis
4. **Use #Shorts tag** - Auto-added by this tool
5. **Upload consistently** - YouTube algorithm loves consistency

---

## 🆘 Support

If you encounter issues:

1. Check the Troubleshooting section above
2. Make sure all dependencies are installed
3. Verify you're logged into Instagram (for link downloads)
4. Check that `client_secret.json` is in the folder

---

## 🎉 Success!

Once everything is set up, you can:
- Upload Instagram Reels to YouTube in seconds
- Automate your content workflow
- Grow your YouTube Shorts channel

**Happy uploading!** 🚀

---

Made with ❤️ by Omkar Jagtap
