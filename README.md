# 🎨 Modular Portfolio Builder - Complete Guide

A production-ready Streamlit application that allows users to create and customize professional portfolios with modular components.

**Version**: 1.0 | **Status**: Production Ready ✅ | **Python**: 3.8+

---

## 📖 Table of Contents

1. [Quick Start](#quick-start)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Architecture](#architecture)
6. [Customization](#customization)
7. [Deployment](#deployment)
8. [Testing](#testing)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Development](#advanced-development)

---

## 🚀 Quick Start

### Get Running in 5 Minutes

```bash
# Navigate to project
cd /Users/nadeemali/Learning_Projects/Portfolio_Streamlit

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run main.py
```

Visit **http://localhost:8501** in your browser.

---

## ✨ Features

### Core Application Features
- ✅ **User Registration** - Secure account creation with email
- ✅ **User Authentication** - Login with password hashing (SHA256)
- ✅ **Session Management** - Persistent user sessions
- ✅ **Portfolio Editing** - Intuitive multi-tab interface
- ✅ **Module Management** - Enable/disable portfolio sections dynamically
- ✅ **Theme Customization** - Choose primary, secondary, and accent colors
- ✅ **Real-time Preview** - See changes instantly
- ✅ **JSON Export** - Download portfolio configuration
- ✅ **Data Persistence** - All user data saved locally
- ✅ **File Upload Support** - Upload images and PDFs directly (NEW!)
  - Profile images saved to `data/images/`
  - Section cover images saved to `data/images/`
  - Certificate images & PDFs saved to `data/certificates/`
  - **No external links needed** - Everything stored locally
- ✅ **Enhanced Skill Icons** - Visual icons with descriptive names for better clarity (NEW!)

### Portfolio Modules (7 Total)

| Module | Icon | Type | Purpose |
|--------|------|------|---------|
| Personal Information | 👤 | Required | Profile, summary, about |
| Work Experience | 💼 | Optional | Job history and achievements |
| Skills | 🛠️ | Optional | Skills organized by category |
| Projects | 📁 | Optional | Project showcase with links |
| Education | 🎓 | Optional | Educational background |
| Certifications | 🏆 | Optional | Professional certifications |
| Social Links | 🔗 | Optional | Social media profiles |

---

## � Installation

### Prerequisites
- macOS with Python 3.8+
- Homebrew (optional but recommended for Python)

### Step-by-Step Installation

1. **Install Python (if needed)**
   ```bash
   # Using Homebrew
   brew install python3
   ```

2. **Navigate to Project**
   ```bash
   cd /Users/nadeemali/Learning_Projects/Portfolio_Streamlit
   ```

3. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run Application**
   ```bash
   streamlit run main.py
   ```

### Verify Installation
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check Streamlit
streamlit --version

# Check dependencies
pip list
```

---

## � Usage

### First-Time Users

#### Step 1: Create Account
1. Go to **Sign Up** tab
2. Enter username, email, and password (min 6 characters)
3. Click **Sign Up**
4. You'll be redirected to the editor

#### Step 2: Enable Modules
1. Check the sidebar on the left
2. Enable modules you want (Personal Info is always active):
   - ☑️ Experience
   - ☑️ Skills
   - ☑️ Projects
   - ☑️ Education
   - ☑️ Certificates
   - ☑️ Social Links

#### Step 3: Fill Portfolio with Data & Media
1. Click on each tab to fill in information:
   - 👤 **Personal Info** 
     - Name, email, title, summary
     - **Upload profile image** (JPG, PNG, or GIF)
     - Image is saved to `data/images/` folder
   
   - 💼 **Experience** 
     - Job title, company, period, achievements
     - **Upload section cover image** (optional)
     - Images auto-save to `data/images/`
   
   - 🛠️ **Skills** 
     - Skill categories with **visual icon indicators**
     - **Icons now display with descriptions:**
       - 🔧 Tool / General
       - 💻 Computer / Programming
       - 📚 Language / Learning
       - ☁️ Cloud / DevOps
       - 🎨 Design / Creative
       - ⚙️ Backend / Server
       - 👁️ Frontend / UI
       - 📊 Data / Analytics
     - Add comma-separated skills (e.g., Python, JavaScript)
     - **Upload section cover image** (optional)
   
   - 📁 **Projects** - Project names, URLs, descriptions
   
   - 🎓 **Education** 
     - Degree, period, institution
     - **Upload section cover image** (optional)
   
   - 🏆 **Certifications** 
     - Certificate title, issuer, date
     - **Upload certificate image** (PNG, JPG, or GIF)
     - **Upload certificate PDF file**
     - All files saved to `data/certificates/`
   
   - 🔗 **Social Links** - LinkedIn, GitHub, etc.
   
   - 🎨 **Theme** - Customize colors

#### Step 4: File Storage & Management
- **All uploaded files are automatically saved in the `data/` folder**
- Files are organized by type:
  - `data/images/` - Profile and section images
  - `data/certificates/` - Certificate images and PDFs
- **No external links needed** - Everything is stored locally
- Files persist after logout and can be used across sessions

#### Step 5: Save & Preview
1. Click **💾 Save Portfolio** (blue button in sidebar)
2. Click **🔗 View Public Portfolio** to preview
3. Click **📥 Download as JSON** to export

### Returning Users

1. Enter username and password
2. Edit any section you want to change
3. Previously uploaded files are shown with preview
4. Upload new files to replace or add media
5. Click **💾 Save Portfolio**
6. Click **🚪 Logout** when done

### File Upload Tips

- **Profile Image**: Single image (recommended: 400x400px or square)
- **Section Images**: Cover images for each portfolio section (recommended: wide format)
- **Certificate Images**: Badge or document screenshot (any size)
- **Certificate PDFs**: Original certificate documents
- **Supported formats**: JPG, JPEG, PNG, GIF (images), PDF (documents)
- **Maximum file size**: Based on Streamlit's file upload limits (~200MB)
- **All files are private** and tied to your user account

---

## 🏗️ Architecture

### Project Structure

```
Portfolio_Streamlit/
├── main.py                              # Main Streamlit application
│   ├── login_page()                    # Authentication UI
│   ├── portfolio_editor_page()         # Editor interface
│   └── portfolio_preview_page()        # Preview & export
│
├── app/
│   ├── utils/
│   │   ├── auth.py                    # User authentication
│   │   │   ├── AuthManager class
│   │   │   ├── register_user()
│   │   │   ├── authenticate()
│   │   │   └── update_portfolio()
│   │   │
│   │   └── portfolio.py               # Portfolio management
│   │       ├── PortfolioManager class
│   │       ├── AVAILABLE_MODULES
│   │       └── Validation methods
│   │
│   └── components/
│       └── portfolio_editors.py       # UI Editors (8 functions)
│           ├── personal_info_editor()
│           ├── experience_editor()
│           ├── skills_editor()
│           ├── projects_editor()
│           ├── education_editor()
│           ├── certificates_editor()
│           ├── social_links_editor()
│           └── theme_editor()
│
├── data/
│   └── users.json                     # User database (auto-created)
│
├── .streamlit/
│   └── config.toml                    # Streamlit settings
│
├── requirements.txt                   # Python dependencies
├── .gitignore
└── README.md                          # This file
```

### Data Flow

```
User Input
    ↓
Validation
    ↓
Session State Update
    ↓
Save to users.json
    ↓
Preview/Export
```

### Session State Variables

```python
st.session_state.auth_manager        # AuthManager instance
st.session_state.user_logged_in      # Boolean: login status
st.session_state.current_user        # String: current username
st.session_state.portfolio_config    # Dict: portfolio data
st.session_state.show_preview        # Boolean: preview mode
```

---

## 🎨 Customization

### 1. File Upload Management

#### Upload Profile Image
- Go to **👤 Personal Info** tab
- Click **Upload Profile Image** button
- Select JPG, PNG, or GIF (recommended: square format, 400x400px)
- Image auto-saves to `data/images/profile_[filename]`
- Preview appears immediately after upload

#### Upload Section Images
- Each section (Experience, Skills, Education) has optional cover image
- Click **Upload Section Image** button
- Select JPG, PNG, or GIF (recommended: wide format)
- Images auto-save to `data/images/`
- Used as visual headers for portfolio sections

#### Upload Certificates
- Go to **🏆 Certifications** tab
- **Upload Certificate Image** - Badge or screenshot (JPG, PNG, GIF)
- **Upload Certificate PDF** - Original document (PDF format)
- Both files auto-save to `data/certificates/`
- View preview immediately after upload

#### File Storage Structure
```
data/
├── images/
│   ├── [profile_image_name].jpg
│   ├── [section_cover_image].jpg
│   └── ...
├── certificates/
│   ├── [certificate_image].jpg
│   ├── [certificate_document].pdf
│   └── ...
└── users.json
```

### 2. Skill Icons with Visual Descriptions

Skills section now shows **icons with descriptive names** for better clarity:

| Icon | Name | Best For |
|------|------|----------|
| 🔧 | Tool / General | General tools, utilities |
| 💻 | Computer / Programming | Languages, frameworks, coding |
| 📚 | Language / Learning | Languages, libraries, learning |
| ☁️ | Cloud / DevOps | AWS, Azure, Docker, deployment |
| 🎨 | Design / Creative | Design tools, creative software |
| ⚙️ | Backend / Server | Databases, servers, backend |
| 👁️ | Frontend / UI | Frontend frameworks, UI/UX |
| 📊 | Data / Analytics | Data science, analytics, BI |

**To use:**
1. Go to **🛠️ Skills** tab
2. Select a skill category
3. Click **Select Icon** dropdown
4. Choose from the list (shows icon + description)
5. Add comma-separated skills (e.g., Python, JavaScript, Docker)
6. See live preview with icon + category name

**Example:**
```
Category: Programming Languages
Icon: 💻 Computer / Programming
Skills: Python, JavaScript, Java, C++
Preview: 💻 Programming Languages
```

### 3. Changing Colors

Go to **🎨 Theme** tab in the editor and use color pickers to customize:
- **Primary Color** - Used for headings, buttons, links
- **Secondary Color** - Used for accents and highlights
- **Accent Color** - Used for details and emphasis

### 4. Adding Content

Each editor supports:
- **Text Input** - Names, titles, descriptions
- **Text Areas** - Long-form content (bullet points on separate lines)
- **Dropdowns** - Select from predefined options
- **Number Inputs** - Count items dynamically
- **File Upload** - Images, PDFs with preview

### 5. Editing Streamlit Theme

Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#6366f1"           # Change to your color
backgroundColor = "#f5f7fa"
secondaryBackgroundColor = "#ffffff"
textColor = "#1e293b"
font = "sans serif"
```

### 6. Extending with New Modules

#### Create Editor Function
```python
# In app/components/portfolio_editors.py
def new_module_editor(portfolio_config):
    st.subheader("🆕 New Module")
    
    value = st.text_input("Field", 
        value=portfolio_config.get("new_module", {}).get("field", ""))
    
    portfolio_config["new_module"] = {"field": value}
    return portfolio_config
```

#### Register Module
```python
# In app/utils/portfolio.py
AVAILABLE_MODULES = {
    ...
    "new_module": {
        "name": "New Module",
        "description": "Description",
        "icon": "🆕",
        "required": False
    }
}
```

#### Add to Main App
```python
# In main.py, portfolio_editor_page()
module_tab_mapping = {
    ...
    "new_module": ("🆕 New Module", "new_module"),
}

# In tabs section
elif module_key == "new_module":
    st.session_state.portfolio_config = new_module_editor(
        st.session_state.portfolio_config
    )
```

---

## 🌐 Deployment

### Option 1: Streamlit Cloud (Easiest)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Select main.py
5. Deploy - Done!

**Cost**: Free (with limitations)

### Option 2: Heroku

1. Create `Procfile`:
   ```
   web: streamlit run main.py --logger.level=debug
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

**Cost**: ~$7/month

### Option 3: DigitalOcean App Platform

1. Connect GitHub repository
2. Set runtime to Python
3. Set run command: `streamlit run main.py`
4. Deploy

**Cost**: ~$5/month

### Option 4: Docker

```bash
# Build image
docker build -t portfolio-app .

# Run container
docker run -p 8501:8501 portfolio-app
```

---

## 🧪 Testing

### Test Scenarios

#### 1. Registration Test
- Create account with valid credentials
- Try duplicate username (should fail)
- Try weak password (should fail)
- **Expected**: New account created successfully

#### 2. Login Test
- Login with correct password
- Try wrong password (should fail)
- Try non-existent user (should fail)
- **Expected**: Login succeeds with correct credentials

#### 3. Portfolio Creation
- Enable different modules
- Fill in each section
- Save portfolio
- Reload page
- **Expected**: Data persists after reload

#### 4. Module Management
- Toggle modules on/off
- Verify they appear/disappear in tabs
- Save changes
- **Expected**: Modules persist as selected

#### 5. Theme Customization
- Change color values
- Preview updates in real-time
- Save portfolio
- **Expected**: Colors saved and applied

#### 6. Data Export
- Create portfolio with data
- Click "Download as JSON"
- Verify JSON structure
- **Expected**: Valid JSON with all data

#### 7. Multi-User Support
- Create account A with portfolio
- Create account B with different portfolio
- Login as A, verify data
- Login as B, verify data
- **Expected**: Each user has separate data

#### 8. Experience Editor
- Add 3 experiences
- Fill in all fields including bullet points
- Save and verify
- **Expected**: Data saved correctly with bullets

#### 9. Skills Editor
- Add 3 skill categories
- Select different icons
- Add comma-separated skills
- **Expected**: Categories display correctly

#### 10. Export & Re-import
- Export portfolio as JSON
- Create new account
- Manually import JSON structure
- **Expected**: Portfolio displays correctly

### Running Tests Manually

```bash
# Test 1: Create new account
# Test 2: Add portfolio information
# Test 3: Toggle modules
# Test 4: Change theme colors
# Test 5: Preview portfolio
# Test 6: Download JSON
# Test 7: Logout and login
# Test 8: Verify data persisted
```

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Use different port
streamlit run main.py --server.port 8502
```

### Import Errors

```bash
# Verify virtual environment is active
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Data Not Saving

```bash
# Check data directory exists
mkdir -p data

# Check permissions
chmod 755 data

# Check users.json is valid
python3 -c "import json; json.load(open('data/users.json'))"
```

### Login Always Fails

```bash
# Delete corrupted database and restart
rm data/users.json
streamlit run main.py
# Create new account
```

### Streamlit Slow/Cache Issues

```bash
# Clear cache
rm -rf ~/.streamlit/

# Clear app cache
streamlit cache clear
```

### Module Not Appearing

1. Check module is in AVAILABLE_MODULES in portfolio.py
2. Verify module key in main.py module_tab_mapping
3. Check editor function exists in portfolio_editors.py
4. Verify module is enabled in sidebar

### Colors Not Updating

1. Check theme editor is saving changes
2. Verify color format is valid hex (#RRGGBB)
3. Check config.toml has correct settings
4. Try clearing browser cache

---

## 💡 Advanced Development

### Code Structure

#### Authentication (auth.py)
```python
from app.utils.auth import AuthManager

auth = AuthManager("data")

# Register
success, msg = auth.register_user("username", "password", "email@test.com")

# Login
success, msg = auth.authenticate("username", "password")

# Get portfolio
portfolio = auth.get_user_portfolio("username")

# Update portfolio
auth.update_user_portfolio("username", portfolio)
```

#### Portfolio Management (portfolio.py)
```python
from app.utils.portfolio import PortfolioManager

# Get available modules
modules = PortfolioManager.get_available_modules()

# Validate data
success, msg = PortfolioManager.validate_personal_info(data)

# Create default portfolio
portfolio = PortfolioManager.create_default_portfolio(username, email)
```

### Common Development Tasks

#### Add Custom Validation
```python
def validate_custom(data):
    if not data.get("field"):
        return False, "Field is required"
    if len(data["field"]) < 3:
        return False, "Field must be at least 3 characters"
    return True, "Valid"
```

#### Add Logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info("User logged in")
logger.error("Invalid credentials")
```

#### Cache Expensive Operations
```python
@st.cache_data
def load_user_data(username):
    return auth_manager.get_user_portfolio(username)
```

### Dependencies

- **streamlit==1.28.0** - Web framework
- **pandas==2.1.0** - Data processing
- **pillow==10.0.0** - Image handling
- **PyYAML==6.0.1** - YAML parsing
- **python-dotenv==1.0.0** - Environment variables

### Performance Tips

1. Use `@st.cache_data` for expensive operations
2. Minimize database calls
3. Validate input early
4. Clear cache periodically
5. Use session state efficiently

### Security Notes

1. **Current**: SHA256 password hashing
2. **For Production**: Use bcrypt instead
3. **Database**: Migrate from JSON to proper database
4. **Secrets**: Use environment variables
5. **HTTPS**: Enable for production

### Future Enhancements

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] File upload support
- [ ] Email verification
- [ ] Portfolio hosting
- [ ] Analytics dashboard
- [ ] Collaborative editing
- [ ] Dark mode
- [ ] Mobile app
- [ ] Template library
- [ ] API service

---

## 📄 File Reference

| File | Purpose | Lines |
|------|---------|-------|
| main.py | Main application | 400+ |
| auth.py | Authentication | 120 |
| portfolio.py | Portfolio management | 150 |
| portfolio_editors.py | UI components | 500+ |

**Total**: 1,115 lines of production code

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Database migration
- File upload support
- Template library
- Performance optimization
- UI/UX enhancements

---

## 📞 Support

### Getting Help

1. **Usage Questions** → Check "Usage" section above
2. **Setup Issues** → Check "Installation" and "Troubleshooting"
3. **Code Questions** → Check "Architecture" and "Advanced Development"
4. **Deployment Help** → Check "Deployment" section

### Debugging

Enable debug mode:
```bash
streamlit run main.py --logger.level=debug
```

View session state:
```python
st.write("Debug:", st.session_state)
```

---

## 📄 License

MIT License - Open source and free for personal and commercial use.

---

## ✅ Checklist for New Users

- [ ] Read this README
- [ ] Install Python 3.8+
- [ ] Create virtual environment
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Run application (`streamlit run main.py`)
- [ ] Create test account
- [ ] Add portfolio information
- [ ] Try each module
- [ ] Customize theme colors
- [ ] Export portfolio as JSON
- [ ] Preview final portfolio

---

## 🎉 You're Ready!

Everything you need is here. Start building amazing portfolios!

**Questions?** Check this README or the code comments.

**Ready to deploy?** See Deployment section.

**Want to extend?** See Advanced Development section.

---

**Version**: 1.0  
**Last Updated**: January 2024  
**Status**: Production Ready ✅

Built with ❤️ using Streamlit

## 🎯 Future Enhancements

- [ ] Database integration (SQLite, PostgreSQL)
- [ ] Direct HTML portfolio export
- [ ] Template library
- [ ] File upload for images and documents
- [ ] Analytics dashboard
- [ ] Portfolio sharing with custom URLs
- [ ] Collaborative editing
- [ ] Dark mode
- [ ] Multi-language support
- [ ] Email notifications

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements!

## 📝 License

This project is open source and available under the MIT License.

## 🙋 Support

For issues or questions, please open an issue in the repository.

---

**Built with ❤️ using Streamlit**
