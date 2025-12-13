# Render Deployment - Quick Start

## ✅ Files Created

1. **`wsgi.py`** - WSGI entry point for gunicorn
2. **`requirements.txt`** - Updated with gunicorn
3. **`render.yaml`** - Render configuration (optional)

## 🚀 Start Command for Render

```
gunicorn wsgi:application
```

**What this means:**
- `gunicorn` - The WSGI server
- `wsgi` - The module (wsgi.py file)
- `application` - The Flask app variable in wsgi.py

## 📋 Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Add Render deployment files"
git push
```

### 2. Deploy on Render

1. Go to [render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub and select your repo
4. Configure:
   - **Name**: `youtube-downloader`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:application`
5. Click **"Create Web Service"**
6. Wait 2-5 minutes
7. Your app is live! 🎉

## ✅ That's It!

Your app will be available at: `https://your-app.onrender.com`

**No more serverless crashes!** Render runs a traditional server, perfect for video downloads.

## 📖 Full Guide

See `RENDER_DEPLOYMENT.md` for detailed instructions and troubleshooting.

