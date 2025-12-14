# API Proxy Deployment Guide

This guide explains how to deploy the `api_proxy.py` backend to enable the interactive demo on the web page.

## Why is this needed?

OpenAI's API doesn't allow direct browser calls due to CORS (Cross-Origin Resource Sharing) restrictions. The backend proxy handles API calls server-side, avoiding CORS issues.

## Quick Deployment Options

### Option 1: Render (Recommended - Free Tier Available)

1. Create a free account at [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `educational-content-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python api_proxy.py`
   - **Environment Variables**: None needed (uses user's API key)
5. Deploy!

Your API will be available at: `https://your-app-name.onrender.com`

### Option 2: Railway

1. Create account at [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Railway will auto-detect Python and deploy
5. Your API will be at: `https://your-app-name.up.railway.app`

### Option 3: Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Deploy: `git push heroku main`
5. Your API will be at: `https://your-app-name.herokuapp.com`

### Option 4: Local Testing

For local development:

```bash
pip install flask flask-cors openai
python api_proxy.py
```

The API will run at `http://localhost:5000`

## Updating the Web Page

After deploying, update the `API_ENDPOINT` variable in `docs/index.html`:

```javascript
const API_ENDPOINT = 'https://your-deployed-url.com/api/generate';
```

## Testing

Test the API endpoint:

```bash
curl -X POST https://your-api-url.com/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "sk-your-key",
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

## Security Notes

- The backend doesn't store API keys
- Each request includes the user's API key
- No persistent storage of user data
- CORS is enabled for the web page domain

## Alternative: Use Streamlit App

If you prefer not to deploy a backend, users can use the full Streamlit application which includes RAG functionality and doesn't require a separate backend.

