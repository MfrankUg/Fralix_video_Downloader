# 🚨 START HERE: Fix Serverless Function Crash

## The #1 Most Important Step

### ⚠️ CHECK VERCEL LOGS FIRST!

**This tells you EXACTLY what's wrong:**

1. Go to [vercel.com](https://vercel.com)
2. Click your project
3. Click **"Functions"** tab
4. Click on `api/index.py` (or the function name)
5. **Look at the logs** - You'll see the exact error!

**Don't skip this step!** The logs will show you:
- What's failing
- Which line is causing the error
- What's missing

---

## Quick Test (2 minutes)

### Test 1: Health Check
Visit: `https://your-app.vercel.app/health`

- ✅ Works → Flask is fine, problem is elsewhere
- ❌ Fails → Check Vercel logs for Flask import error

### Test 2: Debug Info
Visit: `https://your-app.vercel.app/debug`

Shows:
- What files exist
- What's loaded
- What paths are being used

---

## Most Common Fixes

### Fix #1: Missing Dependencies
**If logs show:** `ModuleNotFoundError`

**Do this:**
1. Check `requirements.txt` exists in root
2. Verify it has:
   ```
   Flask==3.0.0
   flask-cors==4.0.0
   yt-dlp>=2023.12.30
   ```
3. Push to GitHub → Vercel auto-redeploys

### Fix #2: Files Not Found
**If logs show:** `TemplateNotFound` or `FileNotFoundError`

**Do this:**
1. Verify folders exist:
   - `templates/index.html`
   - `static/css/style.css`
   - `static/js/main.js`
2. Make sure they're committed:
   ```bash
   git add templates/ static/
   git commit -m "Add files"
   git push
   ```

### Fix #3: Test Minimal Version
**If nothing works, test with minimal version:**

1. Temporarily change `vercel.json`:
   ```json
   {
     "builds": [{"src": "api/minimal.py", "use": "@vercel/python"}],
     "routes": [{"src": "/(.*)", "dest": "api/minimal.py"}]
   }
   ```
2. Deploy and test `/health`
3. If this works → Problem is in main app
4. If this fails → Problem is with Flask/Vercel setup

---

## Step-by-Step Process

1. ✅ **Check Vercel logs** (see exact error)
2. ✅ **Test `/health` endpoint** (does Flask work?)
3. ✅ **Test `/debug` endpoint** (what's missing?)
4. ✅ **Fix the specific issue** (based on logs)
5. ✅ **Redeploy and test again**

---

## Need More Help?

See these files:
- `SOLVE_CRASH_GUIDE.md` - Detailed step-by-step guide
- `QUICK_FIX_CHECKLIST.md` - Quick reference checklist
- `ROOT_CAUSE_ANALYSIS.md` - Understanding why this happens

---

## Remember

**The logs are your friend!** They tell you exactly what's wrong. Always check them first before trying random fixes.

