# Streamlit Cloud Deployment Guide

This guide will help you deploy the Educational Content Generator to Streamlit Cloud for free.

## Prerequisites

1. A GitHub account
2. Your project pushed to GitHub (already done ✅)
3. A Streamlit Cloud account (free at https://share.streamlit.io/)
4. An OpenAI API key

## Step-by-Step Deployment

### Step 1: Sign up for Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "Sign up" and sign in with your GitHub account
3. Authorize Streamlit Cloud to access your GitHub repositories

### Step 2: Deploy Your App

1. In Streamlit Cloud dashboard, click "New app"
2. Select your repository: `TechieSingh/Final-project-ST-Prompt-eng`
3. Select the branch: `main`
4. Set the main file path: `app.py`
5. Click "Deploy"

### Step 3: Configure Secrets (API Key)

1. In your app's settings, click "Secrets"
2. Add your OpenAI API key in the following format:

```toml
OPENAI_API_KEY = "your-actual-api-key-here"
```

3. Click "Save"

### Step 4: Wait for Deployment

- Streamlit Cloud will automatically build and deploy your app
- This usually takes 1-2 minutes
- You'll see a URL like: `https://[app-name].streamlit.app`

### Step 5: Update Web Page with Live Demo URL

1. Once deployed, copy your Streamlit Cloud URL
2. Update `docs/index.html` with your actual Streamlit Cloud URL
3. Replace `https://final-project-st-prompt-eng.streamlit.app` with your actual URL

## Troubleshooting

### App won't start
- Check that `app.py` is in the root directory ✅
- Verify `requirements.txt` includes all dependencies ✅
- Check the logs in Streamlit Cloud dashboard

### API Key not working
- Verify the secret is named exactly `OPENAI_API_KEY`
- Make sure there are no extra spaces or quotes
- Check that the API key is valid and has credits

### Import errors
- Ensure all dependencies are in `requirements.txt` ✅
- Check that Python version is compatible (Streamlit Cloud uses Python 3.9+)

## Your Streamlit Cloud URL

After deployment, your app will be available at:
`https://[your-app-name].streamlit.app`

Update the link in `docs/index.html` once you have your actual URL!

## Notes

- Streamlit Cloud is free for public repositories
- Your app will automatically redeploy when you push changes to GitHub
- API keys are securely stored in Streamlit Cloud secrets
- The app will be publicly accessible (anyone with the URL can use it)

