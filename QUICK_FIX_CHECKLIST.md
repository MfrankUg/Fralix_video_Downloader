# Quick Fix Checklist for Serverless Function Crash

## 🚨 Immediate Actions

### 1. Check Vercel Logs (2 minutes)
- [ ] Go to Vercel Dashboard → Your Project
- [ ] Click "Functions" tab
- [ ] Click on the function
- [ ] **Copy the exact error message**
- [ ] Note: What line/file is mentioned?

### 2. Test Minimal Version (5 minutes)
- [ ] Use `api/minimal.py` (already created)
- [ ] Temporarily update `vercel.json` to use `api/minimal.py`
- [ ] Deploy and test `https://your-app.vercel.app/health`
- [ ] Result: Works = Flask is fine | Fails = Check logs

### 3. Check File Structure (1 minute)
```bash
# Verify these exist:
templates/index.html
static/css/style.css
static/js/main.js
requirements.txt
vercel.json
api/index.py
```

### 4. Verify Requirements (1 minute)
- [ ] `requirements.txt` is in root directory
- [ ] Contains: Flask, flask-cors, yt-dlp
- [ ] No syntax errors

### 5. Test Debug Endpoint (1 minute)
- [ ] Visit: `https://your-app.vercel.app/debug`
- [ ] Check what's `false` or missing
- [ ] Fix those items

---

## 🔍 Common Errors & Quick Fixes

| Error | Quick Fix |
|-------|-----------|
| `ModuleNotFoundError: No module named 'flask'` | Check `requirements.txt` exists and has Flask |
| `TemplateNotFound` | Check `templates/` folder exists and is committed |
| `FileNotFoundError` | Check `static/` folder exists and paths are correct |
| `Handler not found` | Verify `handler = app` at bottom of `api/index.py` |
| `ImportError: yt-dlp` | Already fixed with lazy loading, check logs for specific error |

---

## ✅ Success Indicators

You'll know it's working when:
- ✅ `/health` returns `{"status": "ok"}`
- ✅ `/debug` shows all paths exist
- ✅ Homepage loads without errors
- ✅ Vercel logs show "Module loaded successfully"

---

## 🆘 Still Not Working?

1. **Share the exact error** from Vercel logs (not just "FUNCTION_INVOCATION_FAILED")
2. **Test `/health`** - Does it work?
3. **Test `/debug`** - What does it show?
4. **Check build logs** - Any errors during build?

---

## 📞 What to Share When Asking for Help

```
Error from logs: [paste exact error]
/health endpoint: [works/fails]
/debug endpoint: [paste output]
vercel.json: [paste content]
requirements.txt: [paste content]
```

