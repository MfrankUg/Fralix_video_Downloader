# Troubleshooting Vercel Deployment Error

## Error: FUNCTION_INVOCATION_FAILED (500 Internal Server Error)

If you're seeing this error, follow these steps:

### Step 1: Check Vercel Logs

1. Go to your Vercel dashboard
2. Click on your project
3. Go to the "Functions" tab
4. Click on the function that's failing
5. View the logs to see the exact error

**Common errors you might see:**
- `ModuleNotFoundError` - Missing dependency
- `ImportError` - Import issue
- `TemplateNotFound` - Template path issue
- `FileNotFoundError` - Static file path issue

### Step 2: Verify File Structure

Make sure your repository has this structure:
```
your-repo/
├── api/
│   └── index.py          ← Must exist
├── templates/
│   └── index.html        ← Must exist
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── vercel.json           ← Must exist
├── requirements.txt      ← Must exist
└── .vercelignore
```

### Step 3: Check Common Issues

#### Issue 1: Handler Not Found
**Error**: `Handler not found` or `FUNCTION_INVOCATION_FAILED`

**Solution**: 
- Verify `api/index.py` exists
- Check that it has `handler = app` at the bottom
- Ensure `vercel.json` points to `api/index.py`

#### Issue 2: Import Errors
**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
- Check `requirements.txt` is in the root directory
- Verify all dependencies are listed:
  ```
  Flask==3.0.0
  flask-cors==4.0.0
  yt-dlp>=2023.12.30
  ```
- Push updated `requirements.txt` to GitHub

#### Issue 3: Template/Static File Not Found
**Error**: `TemplateNotFound` or `FileNotFoundError`

**Solution**:
- Verify `templates/` and `static/` folders exist
- Check paths in `api/index.py` are correct
- Ensure files are committed to Git (not in `.gitignore`)

#### Issue 4: yt-dlp Issues
**Error**: `yt-dlp` related errors

**Solution**:
- yt-dlp should work on Vercel without ffmpeg for basic operations
- If you see yt-dlp errors, check the logs for specific error messages
- Try updating yt-dlp version in `requirements.txt`

### Step 4: Test Locally First

Before deploying, test locally:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test the app
cd api
python -c "from index import app; print('App loaded successfully')"
```

### Step 5: Deploy with Debugging

1. **Add a simple test route** (already added - `/health`):
   - Visit: `https://your-app.vercel.app/health`
   - Should return: `{"status": "ok", "message": "Server is running"}`

2. **Check build logs**:
   - In Vercel dashboard, go to your deployment
   - Click "View Build Logs"
   - Look for any errors during build

3. **Check function logs**:
   - Go to Functions tab
   - Click on the function
   - View real-time logs

### Step 6: Common Fixes

#### Fix 1: Update vercel.json
If static files aren't loading, ensure `vercel.json` has:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

#### Fix 2: Verify Handler Export
In `api/index.py`, ensure you have:
```python
handler = app
```
at the bottom of the file.

#### Fix 3: Check Python Version
Vercel uses Python 3.9 by default. If you need a different version, add `runtime.txt`:
```
python-3.9
```

### Step 7: Get Help

If none of these work:

1. **Share the exact error** from Vercel logs
2. **Check the build logs** for any warnings
3. **Verify all files are committed** to GitHub
4. **Try redeploying** after making fixes

### Quick Checklist

- [ ] `api/index.py` exists and has `handler = app`
- [ ] `vercel.json` is configured correctly
- [ ] `requirements.txt` is in root directory
- [ ] `templates/` and `static/` folders exist
- [ ] All files are committed to Git
- [ ] Build logs show no errors
- [ ] Function logs show the actual error

### Test Endpoints

After deployment, test these:
- `https://your-app.vercel.app/health` - Should work
- `https://your-app.vercel.app/` - Should load homepage
- `https://your-app.vercel.app/static/css/style.css` - Should load CSS

If `/health` works but `/` doesn't, it's likely a template path issue.
If nothing works, it's likely an import or handler issue.

