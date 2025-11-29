# Streamlit Cloud Deployment Guide

## Quick Deploy to Streamlit Cloud

This project is ready to be deployed to [Streamlit Cloud](https://streamlit.io/cloud).

### Deployment Steps:

1. **Push to GitHub** ✅ (Already done!)
   - Your code is in: `https://github.com/nadeemali001/streamlit_portfolio`
   - On the `main` branch

2. **Create Streamlit Cloud Account**
   - Go to https://streamlit.io/cloud
   - Sign in with GitHub account
   - Click "New app"

3. **Configure New App**
   - **Repository:** `nadeemali001/streamlit_portfolio`
   - **Branch:** `main`
   - **Main file path:** `main.py`
   - Click "Deploy"

4. **App Configuration** (Optional)
   - After deployment, click "⚙️ Settings" in top-right
   - Go to "Secrets" tab
   - Add any sensitive data if needed (future use)
   - Click "Save"

### What Gets Deployed:

✅ **Application Files:**
- `main.py` - Main Streamlit app (entry point)
- `app/utils/auth.py` - Authentication module
- `app/utils/portfolio.py` - Portfolio manager
- `app/components/portfolio_editors.py` - Editor components

✅ **Configuration Files:**
- `.streamlit/config.toml` - Theme and display settings
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules
- `README.md` - Documentation

✅ **Data Storage:**
- `data/` directory - Created automatically on first run
- `data/users.json` - User credentials (persisted)
- `data/images/` - Profile/section images (persisted)
- `data/certificates/` - Certificate files (persisted)

### Data Persistence on Streamlit Cloud:

> ⚠️ **Important:** Streamlit Cloud has limitations on file persistence. For production use, consider:
> - Using a cloud database (Firebase, MongoDB, etc.)
> - Using cloud storage (AWS S3, Google Cloud Storage, etc.)
> - Currently, files uploaded will be stored locally but may be lost on app restart

### Troubleshooting:

**Issue: "Module not found" error**
- Solution: Ensure all imports in `main.py` use relative paths with `sys.path` setup

**Issue: "Port already in use" locally**
- Solution: Run `streamlit run main.py --logger.level=debug` with a different port

**Issue: Files not persisting**
- Solution: Upgrade to a cloud-backed storage solution for production

### Local Testing Before Deploy:

```bash
cd /Users/nadeemali/Learning_Projects/Portfolio_Streamlit
source .venv/bin/activate
streamlit run main.py
```

Visit: http://localhost:8501

### Project Structure:

```
Portfolio_Streamlit/
├── main.py                           # Entry point
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git configuration
├── .streamlit/
│   ├── config.toml                  # Theme settings
│   └── secrets.toml.example         # Secrets template
├── app/
│   ├── __init__.py
│   ├── utils/
│   │   ├── auth.py                  # Auth manager
│   │   └── portfolio.py             # Portfolio manager
│   └── components/
│       └── portfolio_editors.py      # Editor components
├── data/                            # Auto-created
│   ├── users.json
│   ├── images/
│   └── certificates/
├── README.md                        # Documentation
└── FEATURES_GUIDE.md               # Features guide
```

### Next Steps:

1. Go to https://streamlit.io/cloud
2. Click "New app"
3. Select your repository: `streamlit_portfolio`
4. Select branch: `main`
5. Set main file: `main.py`
6. Click "Deploy"

Your app will be live in a few minutes! 🚀

### Support:

- Streamlit Cloud Docs: https://docs.streamlit.io/streamlit-cloud/deploy-your-app
- Streamlit Community: https://discuss.streamlit.io
