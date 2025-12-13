# Quick Deploy Guide - GitHub → Vercel

## 🚀 Quick Steps

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Ready for Vercel"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Deploy on Vercel (Browser)

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"Add New Project"**
3. Select your GitHub repository
4. Click **"Import"**
5. Leave settings as default (auto-detected)
6. Click **"Deploy"**
7. Wait 1-3 minutes
8. Get your live URL! 🎉

## ✅ Files Required (Already Created)

- ✅ `vercel.json` - Configuration
- ✅ `api/index.py` - Serverless function
- ✅ `requirements.txt` - Dependencies
- ✅ `.vercelignore` - Excluded files

## ⚠️ Important Notes

- **Works**: Video analysis, small downloads, UI
- **May timeout**: Large video downloads (>10s on free plan)
- **Auto-deploys**: Every push to GitHub main branch

## 📖 Full Guide

See `GITHUB_VERCEL_DEPLOYMENT.md` for detailed instructions and troubleshooting.

