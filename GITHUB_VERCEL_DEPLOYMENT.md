# Deploy to Vercel via GitHub - Complete Guide

## Is This Possible?

**Yes, you can deploy this Flask app on Vercel!** However, there are some important limitations to be aware of:

### Limitations:
1. **Timeout Limits**: 
   - Free/Hobby Plan: 10 seconds per function execution
   - Pro Plan: 60 seconds per function execution
   - **Large video downloads may timeout**

2. **File Size Limits**:
   - Response payload: 4.5MB (Hobby) / 50MB (Pro)
   - **Large videos cannot be returned directly**

3. **File Persistence**:
   - Files stored in `/tmp` are temporary
   - Files may not persist between function invocations

### What Will Work:
- Video analysis (getting video info, thumbnails, formats)
- Small video downloads (under timeout limits)
- Frontend UI and all static assets

---

## Step-by-Step Deployment Guide

### Step 1: Prepare Your Code for GitHub

1. **Initialize Git** (if not already done):
   ```bash
   git init
   ```

2. **Create/Update .gitignore**:
   Make sure your `.gitignore` includes:
   ```
   downloads/
   __pycache__/
   *.pyc
   .env
   venv/
   .venv/
   ```

3. **Stage and commit your files**:
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   ```

### Step 2: Push to GitHub

1. **Create a new repository on GitHub**:
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it (e.g., "youtube-downloader")
   - **Don't** initialize with README, .gitignore, or license (you already have these)
   - Click "Create repository"

2. **Push your code**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```
   Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name.

### Step 3: Deploy on Vercel (Browser Interface)

1. **Go to Vercel**:
   - Visit [vercel.com](https://vercel.com)
   - Sign up or log in (you can use your GitHub account)

2. **Import Your Project**:
   - Click **"Add New Project"** or **"Import Project"**
   - You'll see a list of your GitHub repositories
   - Find and select your `youtube-downloader` repository
   - Click **"Import"**

3. **Configure Project Settings**:
   - **Framework Preset**: Vercel should auto-detect "Other" or "Python"
   - **Root Directory**: Leave as `.` (root)
   - **Build Command**: Leave empty (Vercel handles Python automatically)
   - **Output Directory**: Leave empty
   - **Install Command**: Leave empty (Vercel uses `requirements.txt` automatically)

4. **Environment Variables** (if needed):
   - Usually not required for this project
   - If you add any later, you can set them here

5. **Deploy**:
   - Click **"Deploy"**
   - Wait for the build to complete (usually 1-3 minutes)
   - You'll see build logs in real-time

6. **Get Your URL**:
   - Once deployed, Vercel will give you a URL like: `https://your-project.vercel.app`
   - Your site is now live! 🎉

### Step 4: Verify Deployment

1. **Visit your Vercel URL**
2. **Test the application**:
   - Try analyzing a video URL
   - Test downloading a small video
   - Check if static assets (CSS, JS) load correctly

---

##  Required Files Checklist

Make sure these files exist in your repository:

- ✅ `vercel.json` - Vercel configuration
- ✅ `api/index.py` - Serverless function entry point
- ✅ `requirements.txt` - Python dependencies
- ✅ `templates/index.html` - HTML template
- ✅ `static/css/style.css` - Styles
- ✅ `static/js/main.js` - JavaScript
- ✅ `.vercelignore` - Files to exclude

---

##  Troubleshooting Common Issues

### Issue: "Module not found" or "Import error"

**Solution**:
- Check that `requirements.txt` includes all dependencies:
  ```
  Flask==3.0.0
  flask-cors==4.0.0
  yt-dlp>=2023.12.30
  ```
- Ensure `requirements.txt` is in the root directory

### Issue: "Handler not found"

**Solution**:
- Verify `api/index.py` exists and has `handler = app` at the bottom
- Check `vercel.json` routes configuration

### Issue: "Timeout" errors

**Solution**:
- This is expected for large video downloads
- Vercel functions have execution time limits
- Consider:
  - Upgrading to Pro plan (60s timeout)
  - Implementing streaming downloads
  - Using external storage (S3, etc.)

### Issue: Static files not loading

**Solution**:
- Check `vercel.json` has the static file route:
  ```json
  {
    "src": "/static/(.*)",
    "dest": "/static/$1"
  }
  ```
- Verify `static/` folder structure is correct

### Issue: "File not found" when downloading

**Solution**:
- Files in `/tmp` are temporary and may be cleared
- This is a limitation of serverless functions
- Consider implementing direct streaming or external storage

---

##  Updating Your Deployment

After making changes:

1. **Commit and push to GitHub**:
   ```bash
   git add .
   git commit -m "Update code"
   git push
   ```

2. **Vercel will automatically redeploy**:
   - Vercel watches your GitHub repository
   - It automatically deploys on every push to `main` branch
   - You'll see a new deployment in your Vercel dashboard

---

##  Monitoring Your Deployment

1. **View Logs**:
   - Go to your project in Vercel dashboard
   - Click "Functions" tab
   - View real-time logs

2. **Check Deployment Status**:
   - Dashboard shows deployment history
   - Green = successful, Red = failed
   - Click any deployment to see details

---

##  Tips for Better Performance

1. **Optimize for Small Videos**:
   - The app works best with shorter videos
   - Large downloads may timeout

2. **Consider Pro Plan**:
   - 60-second timeout vs 10 seconds
   - Better for video downloads

3. **Future Improvements**:
   - Implement streaming downloads
   - Use external storage (AWS S3, Cloudflare R2)
   - Add queue system for large downloads

---

##  Summary

**Yes, you can deploy this on Vercel via GitHub!**

**Workflow**:
1. Push code to GitHub ✅
2. Import repository in Vercel ✅
3. Deploy with one click ✅
4. Get live URL ✅

**What works**:
- ✅ Frontend UI
- ✅ Video analysis
- ✅ Small video downloads
- ✅ All static assets

**Limitations**:
- ⚠️ Large downloads may timeout
- ⚠️ File persistence issues
- ⚠️ Response size limits

The app will work, but may have limitations with very large video downloads. For most use cases, it should work fine!

