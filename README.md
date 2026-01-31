# 🚀 Instagram to YouTube Shorts Bot

Automatically download Instagram Reels and upload them to YouTube as Shorts with proper optimization.

---

## ✨ Features

- ✅ Download Instagram Reels automatically
- ✅ Upload to YouTube as Shorts (with #Shorts tag)
- ✅ Auto-cleanup of video files
- ✅ Progress tracking
- ✅ Web interface (Streamlit) + Console version
- ✅ Optimized for YouTube Shorts algorithm

---

## 📋 Prerequisites

- Python 3.8 or higher
- Google account
- Instagram account (logged in Chrome or Firefox)

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

---

## 🔑 Setup Your Own YouTube API Credentials

**IMPORTANT:** You need to create your own Google Cloud credentials. This is FREE and takes 5 minutes.

### Step-by-Step Guide:

#### 1. Go to Google Cloud Console

Visit: [https://console.cloud.google.com/](https://console.cloud.google.com/)

#### 2. Create a New Project

- Click "Select a project" at the top
- Click "New Project"
- Enter project name: `Instagram-to-YouTube`
- Click "Create"

#### 3. Enable YouTube Data API v3

- In the search bar, type: `YouTube Data API v3`
- Click on it
- Click "Enable"
- Wait for it to activate

#### 4. Create OAuth Credentials

- Go to "Credentials" (left sidebar)
- Click "Create Credentials" → "OAuth client ID"
- If asked, configure consent screen:
  - User Type: **External**
  - App name: `Instagram to YouTube Bot`
  - User support email: Your email
  - Developer email: Your email
  - Click "Save and Continue"
  - Scopes: Skip (click "Save and Continue")
  - Test users: Add your email
  - Click "Save and Continue"

#### 5. Create OAuth Client ID

- Application type: **Desktop app**
- Name: `Instagram to YouTube Desktop`
- Click "Create"

#### 6. Download Credentials

- Click the **Download** icon (⬇️) next to your newly created credential
- Save the file as `client_secret.json`
- Move it to the project folder

#### 7. Verify Setup

Your project folder should now have:
```
insta_to_youtube/
├── main.py
├── app.py
├── client_secret.json  ← YOU JUST ADDED THIS
├── requirements.txt
└── README.md
```

---

## 🎯 Usage

### **Option 1: Console Version (Easiest)**

```bash
python main.py
```

**What happens:**
1. First time: Opens browser for Google login
2. Asks for Instagram Reel link
3. Asks for YouTube title
4. Downloads and uploads automatically
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

### **Option 2: Web Interface (Streamlit)**

```bash
streamlit run app.py
```

Then open: **http://localhost:8501**

**Features:**
- 🔗 Paste Instagram links
- 📤 Upload video files
- 📊 Progress bars
- 🎥 Video preview

---

## � First-Time Authentication

When you run the tool for the first time:

1. **Browser opens automatically**
2. **Select your Google account**
3. **Click "Continue"** (you may see a warning - this is normal for test apps)
4. **Click "Continue"** again
5. **Allow access** to YouTube
6. **Done!** The tool is now authorized

The credentials are saved locally, so you only do this once.

---

## � Troubleshooting

### "client_secret.json not found"

**Problem:** You haven't created Google credentials yet

**Solution:** Follow the "Setup Your Own YouTube API Credentials" section above

---

### "Download failed" Error

**Problem:** Instagram is blocking the download

**Solutions:**
1. Make sure you're logged into Instagram in Chrome or Firefox
2. Try a different Instagram link
3. Download manually from [SnapInsta.app](https://snapinsta.app) and use file upload

---

### "This app isn't verified" Warning

**Problem:** Google shows a warning during first login

**Solution:** This is normal for personal projects. Click:
1. "Advanced"
2. "Go to [Your App Name] (unsafe)"
3. "Allow"

This is YOUR app, so it's safe.

---

### "yt-dlp not found" Error

**Problem:** yt-dlp not installed

**Solution:**
```bash
pip install yt-dlp
```

---

## 📱 How to Use (Step by Step)

### For Beginners:

1. **Install Python** from [python.org](https://python.org)

2. **Download this project:**
   ```bash
   git clone https://github.com/omijagtap/intagramtoyoutube.git
   cd intagramtoyoutube
   ```

3. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create Google credentials:**
   - Follow the "Setup Your Own YouTube API Credentials" section
   - Download `client_secret.json` to this folder

5. **Run the tool:**
   ```bash
   python main.py
   ```

6. **First time:** Browser opens for Google login

7. **Paste Instagram link and title**

8. **Done!** Video uploads to YouTube

---

## 🎨 Customization

### Change Video Description

Edit `STATIC_DESCRIPTION` in `main.py` or `app.py`:

```python
STATIC_DESCRIPTION = """
Your custom description here!

#YourHashtags
"""
```

### Change Privacy Setting

```python
"privacyStatus": "public"  # Options: public, private, unlisted
```

---

## 📊 Which Version to Use?

| Feature | Console (`main.py`) | Streamlit (`app.py`) |
|---------|---------------------|----------------------|
| Instagram Links | ✅ Yes | ✅ Yes (local only) |
| File Upload | ❌ No | ✅ Yes |
| Web Interface | ❌ No | ✅ Yes |
| Ease of Use | ⭐⭐⭐ Easy | ⭐⭐⭐⭐ Very Easy |

---

## ⚠️ Important Notes

1. **Your Credentials:** Each user must create their own `client_secret.json`. Don't share yours!

2. **Instagram Terms:** Only download content you have rights to use.

3. **YouTube Guidelines:** Make sure you have permission to upload the content.

4. **Rate Limits:** YouTube API has daily quotas. For personal use, this is plenty.

---

## 🆘 Need Help?

### Common Issues:

**Q: Where do I get `client_secret.json`?**  
A: Follow the "Setup Your Own YouTube API Credentials" section. You create it yourself from Google Cloud Console.

**Q: Can I use someone else's credentials?**  
A: No, each person needs their own. It's free and takes 5 minutes to set up.

**Q: Instagram download fails?**  
A: Make sure you're logged into Instagram in your browser (Chrome or Firefox).

**Q: "This app isn't verified" warning?**  
A: Normal for personal projects. Click "Advanced" → "Go to app (unsafe)" → "Allow"

---

## 💡 Tips for Success

1. **Use vertical videos** - Instagram Reels are already vertical ✅
2. **Keep under 60 seconds** - YouTube Shorts requirement
3. **Add engaging titles** - Include keywords
4. **Use #Shorts tag** - Auto-added by this tool
5. **Upload consistently** - Algorithm loves consistency

---

## � You're Ready!

Once you have `client_secret.json` in the folder:

```bash
python main.py
```

That's it! Start uploading Instagram Reels to YouTube Shorts! 🚀

---

## 📝 Project Structure

```
insta_to_youtube/
├── main.py                 # Console version
├── app.py                  # Streamlit web app
├── generate_token.py       # For Streamlit Cloud deployment
├── requirements.txt        # Dependencies
├── client_secret.json      # YOUR Google credentials (create this)
├── .gitignore             # Excludes sensitive files
└── README.md              # This file
```

---

## � Deploy to Streamlit Cloud (Optional)

If you want to access from anywhere:

1. **Generate token locally:**
   ```bash
   python generate_token.py
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repo
   - Add the token to Secrets

3. **Note:** Instagram links won't work on cloud (use file upload)

---

Made with ❤️ | Free to use and modify
