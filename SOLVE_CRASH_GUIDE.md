# How to Solve Serverless Function Crashing - Step by Step

## 🔍 Step 1: Check Vercel Logs (Most Important!)

**This tells you EXACTLY what's failing:**

1. Go to [vercel.com](https://vercel.com) → Your Project
2. Click **"Functions"** tab (or "Deployments" → Latest deployment)
3. Click on the function name (usually `api/index.py`)
4. **Look for error messages** - You should see:
   - Red error messages
   - Stack traces
   - Import errors
   - Path errors

**What to look for:**
- `ModuleNotFoundError` → Missing dependency
- `ImportError` → Import issue
- `TemplateNotFound` → Template path wrong
- `FileNotFoundError` → Static file path wrong
- Any Python traceback

**Copy the exact error message** - This is the key to fixing it!

---

## 🧪 Step 2: Test with Minimal Version

Let's create a minimal version that definitely works, then add features:

### Create `api/minimal.py`:

```python
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

try:
    from flask import Flask, jsonify
    logger.info("Flask imported")
    
    app = Flask(__name__)
    logger.info("Flask app created")
    
    @app.route('/')
    def home():
        return jsonify({'status': 'ok', 'message': 'Minimal version works!'})
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'})
    
    handler = app
    logger.info("Handler set")
    
except Exception as e:
    logger.error(f"Error: {str(e)}")
    raise
```

### Update `vercel.json` temporarily:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/minimal.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/minimal.py"
    }
  ]
}
```

**Test this first:**
- Deploy and visit `https://your-app.vercel.app/health`
- If this works → Flask is fine, problem is elsewhere
- If this fails → Check logs for Flask import issues

---

## 🔧 Step 3: Common Crash Causes & Fixes

### Crash Cause #1: Missing Dependencies

**Error in logs:** `ModuleNotFoundError: No module named 'flask'`

**Fix:**
1. Check `requirements.txt` is in root directory
2. Verify it has:
   ```
   Flask==3.0.0
   flask-cors==4.0.0
   yt-dlp>=2023.12.30
   ```
3. Push to GitHub
4. Vercel will reinstall dependencies

### Crash Cause #2: Template/Static Files Not Found

**Error in logs:** `TemplateNotFound` or `FileNotFoundError`

**Fix:**
1. Verify folders exist:
   ```
   templates/
     └── index.html
   static/
     ├── css/
     │   └── style.css
     └── js/
         └── main.js
   ```

2. Check they're committed to Git:
   ```bash
   git add templates/ static/
   git commit -m "Add templates and static files"
   git push
   ```

3. Verify paths in `api/index.py`:
   ```python
   BASE_DIR = os.path.dirname(os.path.abspath(__file__))
   PROJECT_ROOT = os.path.dirname(BASE_DIR)
   static_path = os.path.join(PROJECT_ROOT, 'static')
   template_path = os.path.join(PROJECT_ROOT, 'templates')
   ```

### Crash Cause #3: Handler Not Found

**Error in logs:** `Handler not found` or function doesn't execute

**Fix:**
1. Ensure `api/index.py` has at the bottom:
   ```python
   handler = app
   ```

2. Check `vercel.json` points to correct file:
   ```json
   {
     "src": "api/index.py",
     "use": "@vercel/python"
   }
   ```

### Crash Cause #4: yt-dlp Initialization

**Error in logs:** yt-dlp related errors during import

**Fix:** (Already done - lazy loading)
- yt-dlp is now loaded only when needed
- If still fails, check logs for specific yt-dlp error

### Crash Cause #5: Python Version Mismatch

**Error in logs:** Syntax errors or version-specific issues

**Fix:**
1. Add `runtime.txt` in root:
   ```
   python-3.9
   ```
2. Push and redeploy

---

## 🐛 Step 4: Add Debug Endpoint

Add this to `api/index.py` to see what's working:

```python
@app.route('/debug')
def debug():
    """Debug endpoint to check system status"""
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(BASE_DIR)
    
    return jsonify({
        'status': 'ok',
        'base_dir': BASE_DIR,
        'project_root': PROJECT_ROOT,
        'static_exists': os.path.exists(os.path.join(PROJECT_ROOT, 'static')),
        'template_exists': os.path.exists(os.path.join(PROJECT_ROOT, 'templates')),
        'yt_dlp_loaded': yt_dlp is not None,
        'flask_version': Flask.__version__ if 'Flask' in globals() else 'not loaded'
    })
```

**Test:** Visit `https://your-app.vercel.app/debug`
- Shows what's working
- Shows what's missing
- Helps identify the problem

---

## 📋 Step 5: Systematic Debugging Checklist

### ✅ Checklist:

1. **Can you see Vercel logs?**
   - [ ] Yes → Go to step 2
   - [ ] No → Check Vercel dashboard access

2. **What does `/health` endpoint return?**
   - [ ] Works → Flask is fine, check other features
   - [ ] 500 error → Check logs for Flask import error
   - [ ] 404 error → Check `vercel.json` routes

3. **What does `/debug` endpoint show?**
   - [ ] All true → Everything loaded correctly
   - [ ] Some false → Fix the false items

4. **Are templates/static files found?**
   - [ ] Yes → Paths are correct
   - [ ] No → Check folder structure and paths

5. **Does homepage (`/`) load?**
   - [ ] Yes → Basic functionality works
   - [ ] No → Check template rendering in logs

---

## 🚀 Step 6: Quick Fix Commands

If you just want to try the most common fixes:

```bash
# 1. Make sure all files are committed
git add .
git commit -m "Fix serverless function"
git push

# 2. Check requirements.txt exists and is correct
cat requirements.txt

# 3. Verify file structure
ls -la templates/
ls -la static/

# 4. Check vercel.json
cat vercel.json
```

---

## 🎯 Step 7: If Still Crashing

### Get the Exact Error:

1. **Go to Vercel Dashboard**
2. **Functions tab** → Click function
3. **Copy the FULL error message** (not just "FUNCTION_INVOCATION_FAILED")
4. **Look for:**
   - First line of traceback
   - File name and line number
   - Error type (ImportError, FileNotFoundError, etc.)

### Share for Help:

When asking for help, provide:
- ✅ Exact error message from logs
- ✅ What endpoint you're testing (`/`, `/health`, etc.)
- ✅ What `/debug` endpoint shows
- ✅ Your `vercel.json` content
- ✅ Your `requirements.txt` content

---

## 💡 Pro Tips

1. **Always check logs first** - They tell you exactly what's wrong
2. **Test incrementally** - Start with minimal version, add features one by one
3. **Use `/health` and `/debug`** - Quick way to test what's working
4. **Commit and push** - Vercel auto-redeploys, so you can test quickly
5. **Check build logs too** - Sometimes issues happen during build, not runtime

---

## 🔄 Quick Restart Process

If nothing works, try this clean restart:

1. **Create minimal `api/test.py`** (see Step 2)
2. **Update `vercel.json`** to use `api/test.py`
3. **Deploy and test** - Should work
4. **Gradually add back features:**
   - Add templates
   - Add static files
   - Add yt-dlp (lazy loaded)
5. **Test after each addition**

This isolates exactly where the problem is!

