# ThreatSleuth Deployment Guide

## Architecture
- **Frontend**: Vercel (React)
- **Backend**: Railway/Render (Python Flask)

## Pre-Deployment Checklist

### 1. Prepare Git Repository
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### 2. Deploy Backend (Railway - Recommended)

#### Option A: Railway (Easiest)
1. Go to [railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your ThreatSleuth repository
5. Select the `backend` folder
6. Railway will auto-detect Python and deploy
7. Note your Railway URL (e.g., `https://threatsleuth-backend-production.up.railway.app`)

#### Option B: Render
1. Go to [render.com](https://render.com)
2. Connect GitHub repository
3. Create new "Web Service"
4. Set:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt && python model_trainer.py`
   - **Start Command**: `gunicorn app:app`
   - **Python Version**: 3.11.9

### 3. Deploy Frontend (Vercel)

1. Go to [vercel.com](https://vercel.com)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Import your ThreatSleuth repository
5. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
6. Set Environment Variable:
   - **Key**: `REACT_APP_API_URL`
   - **Value**: Your Railway/Render backend URL
7. Deploy

## Configuration Steps

### Update CORS Origins
After deployment, update `backend/app.py` line 16:
```python
"https://your-actual-frontend-domain.vercel.app"  # Replace with your Vercel URL
```

### Environment Variables
- **Frontend (Vercel)**: Set `REACT_APP_API_URL` to your backend URL
- **Backend (Railway)**: No additional variables needed

## Framework Preset for Vercel
- **Choose**: "Create React App"
- **Root Directory**: `frontend`
- **Build Command**: `npm run build` (default)
- **Output Directory**: `build` (default)

## Post-Deployment Testing
1. Visit your Vercel frontend URL
2. Try uploading a test file
3. Verify API calls work correctly
4. Check browser console for errors

## Troubleshooting
- **CORS Errors**: Update backend CORS origins
- **Build Failures**: Check Node.js/Python versions
- **API Connection**: Verify environment variables
- **File Upload Issues**: Check backend file size limits

## File Size Considerations
- Vercel has 50MB deployment limit
- Your ML model (malware_detector.joblib) should be included
- If model is too large, consider model compression or cloud storage

## Alternative: Serverless Backend
If you want everything on Vercel, you'll need to:
1. Convert Flask routes to Vercel API functions
2. Handle file uploads differently
3. Optimize ML model size
4. Use Vercel's Python runtime