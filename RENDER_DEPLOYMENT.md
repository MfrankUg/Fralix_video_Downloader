# Deploy to Render - Complete Guide

## ✅ Why Render is Better for This App

**Render advantages over Vercel:**
- ✅ **No timeout limits** - Can handle long video downloads
- ✅ **Traditional server** - No serverless function constraints
- ✅ **Persistent storage** - Files persist between requests
- ✅ **Better for heavy operations** - Video downloads work better
- ✅ **Simpler deployment** - Standard Flask + gunicorn

---

## 🚀 Quick Deployment Steps

### Step 1: Prepare Your Code

1. **Make sure these files exist:**
   - ✅ `app.py` - Your Flask application
   - ✅ `wsgi.py` - WSGI entry point (already created)
   - ✅ `requirements.txt` - With gunicorn (already updated)
   - ✅ `render.yaml` - Render configuration (already created)
   - ✅ `templates/` - HTML templates
   - ✅ `static/` - CSS, JS, images

2. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push
   ```

### Step 2: Deploy on Render

1. **Go to Render:**
   - Visit [render.com](https://render.com)
   - Sign up or log in (you can use GitHub)

2. **Create New Web Service:**
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub account if not already connected
   - Select your repository

3. **Configure the Service:**
   - **Name**: `youtube-downloader` (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty (or `.` if needed)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:application`
   - **Plan**: Free tier works, but Pro is better for video downloads

4. **Environment Variables** (Optional):
   - Usually not needed for this app
   - Can add later if needed

5. **Deploy:**
   - Click **"Create Web Service"**
   - Wait for build to complete (2-5 minutes)
   - Your app will be live at `https://your-app.onrender.com`

---

## 📋 Configuration Details

### Start Command
```
gunicorn wsgi:application
```

**What this means:**
- `gunicorn` - The WSGI HTTP server
- `wsgi` - The module name (wsgi.py file)
- `application` - The variable name in wsgi.py (your Flask app)

### Build Command
```
pip install -r requirements.txt
```

This installs all dependencies including:
- Flask
- flask-cors
- yt-dlp
- gunicorn

---

## 🔧 File Structure

Your project should look like this:
```
youtube-downloader/
├── app.py              # Flask application
├── wsgi.py             # WSGI entry point (for gunicorn)
├── requirements.txt    # Python dependencies
├── render.yaml         # Render configuration (optional)
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── downloads/          # Created automatically
```

---

## ⚙️ Advanced Configuration

### Custom Port (if needed)
Render automatically sets the PORT environment variable. Your app should use:
```python
import os
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

But with gunicorn, this is handled automatically.

### Gunicorn Workers
You can customize gunicorn workers in the start command:
```
gunicorn --workers 2 --threads 2 wsgi:application
```

**Default is usually fine**, but for video downloads, you might want:
```
gunicorn --workers 1 --threads 4 --timeout 300 wsgi:application
```

This gives:
- 1 worker (process)
- 4 threads per worker
- 300 second timeout (for long downloads)

### Using render.yaml
If you created `render.yaml`, Render will use it automatically. You can also configure:
- Environment variables
- Health check paths
- Auto-deploy settings

---

## 🐛 Troubleshooting

### Issue: Build Fails
**Error**: `ModuleNotFoundError` or build errors

**Solution:**
- Check `requirements.txt` has all dependencies
- Verify Python version (3.9+)
- Check build logs in Render dashboard

### Issue: App Crashes on Start
**Error**: Application won't start

**Solution:**
- Verify start command: `gunicorn wsgi:application`
- Check `wsgi.py` exists and has `application = app`
- Check logs in Render dashboard

### Issue: Timeout Errors
**Error**: Request timeout

**Solution:**
- Increase timeout in start command:
  ```
  gunicorn --timeout 300 wsgi:application
  ```
- Or upgrade to Pro plan for longer timeouts

### Issue: Static Files Not Loading
**Error**: CSS/JS not loading

**Solution:**
- Verify `static/` folder structure
- Check Flask static folder configuration in `app.py`
- Ensure files are committed to Git

### Issue: Downloads Not Working
**Error**: Files not persisting

**Solution:**
- Render's free tier has ephemeral storage
- Files in `downloads/` folder may be cleared
- Consider using external storage (S3, etc.) for production

---

## 📊 Monitoring

1. **View Logs:**
   - Render Dashboard → Your Service → Logs
   - Real-time logs of your application

2. **Metrics:**
   - CPU usage
   - Memory usage
   - Request count
   - Response times

3. **Health Checks:**
   - Render automatically checks if your app is running
   - Can add custom health check endpoint

---

## 🔄 Updating Your App

1. **Make changes** to your code
2. **Commit and push** to GitHub:
   ```bash
   git add .
   git commit -m "Update app"
   git push
   ```
3. **Render auto-deploys** (if auto-deploy is enabled)
4. **Or manually deploy** from Render dashboard

---

## 💰 Pricing Considerations

### Free Tier:
- ✅ 750 hours/month
- ✅ Sleeps after 15 minutes of inactivity
- ⚠️ Ephemeral storage (files may be cleared)
- ⚠️ Limited resources

### Pro Tier ($7/month):
- ✅ Always on (no sleeping)
- ✅ More resources
- ✅ Better for production
- ✅ Persistent storage

**For video downloads, Pro tier is recommended.**

---

## ✅ Success Checklist

After deployment, verify:
- [ ] App loads at `https://your-app.onrender.com`
- [ ] Homepage displays correctly
- [ ] Static files (CSS, JS) load
- [ ] `/api/analyze` endpoint works
- [ ] Video downloads work (may be slow on free tier)

---

## 🎯 Next Steps

1. **Deploy to Render** (follow steps above)
2. **Test all features**
3. **Monitor logs** for any issues
4. **Consider Pro tier** if you need:
   - Always-on service
   - Better performance
   - Persistent storage

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Gunicorn Documentation](https://gunicorn.org/)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)

---

## 🆘 Need Help?

If you encounter issues:
1. Check Render logs (most important!)
2. Verify all files are committed to Git
3. Test locally first: `gunicorn wsgi:application`
4. Check Render status page for service issues

**Render is much better suited for this app than Vercel!** No more serverless function crashes! 🎉

