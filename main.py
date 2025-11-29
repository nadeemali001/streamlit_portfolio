"""
Modular Streamlit Portfolio Builder App
"""
import streamlit as st
import json
from pathlib import Path
import sys

# Add app to path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from utils.auth import AuthManager
from utils.portfolio import PortfolioManager
from components.portfolio_editors import (
    personal_info_editor, experience_editor, skills_editor,
    projects_editor, education_editor, certificates_editor,
    social_links_editor, theme_editor
)


# Page configuration
st.set_page_config(
    page_title="Portfolio Builder",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "auth_manager" not in st.session_state:
    st.session_state.auth_manager = AuthManager("data")

if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "portfolio_config" not in st.session_state:
    st.session_state.portfolio_config = None


def login_page():
    """Display login/signup page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("# 🎨 Portfolio Builder")
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.subheader("Login to Your Account")
            
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", use_container_width=True, type="primary"):
                auth_manager = st.session_state.auth_manager
                success, message = auth_manager.authenticate(login_username, login_password)
                
                if success:
                    st.session_state.user_logged_in = True
                    st.session_state.current_user = login_username
                    portfolio = auth_manager.get_user_portfolio(login_username)
                    st.session_state.portfolio_config = portfolio
                    st.success("Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error(message)
        
        with tab2:
            st.subheader("Create a New Account")
            
            signup_username = st.text_input("Choose a Username", key="signup_username")
            signup_email = st.text_input("Email Address", key="signup_email")
            signup_password = st.text_input("Password (min 6 characters)", type="password", key="signup_password")
            signup_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")
            
            if st.button("Sign Up", use_container_width=True, type="primary"):
                if not signup_username or not signup_email or not signup_password:
                    st.error("Please fill all fields")
                elif signup_password != signup_confirm:
                    st.error("Passwords do not match")
                else:
                    auth_manager = st.session_state.auth_manager
                    success, message = auth_manager.register_user(
                        signup_username, signup_password, signup_email
                    )
                    
                    if success:
                        st.success(message)
                        portfolio = auth_manager.get_user_portfolio(signup_username)
                        st.session_state.portfolio_config = portfolio
                        st.session_state.user_logged_in = True
                        st.session_state.current_user = signup_username
                        st.info("Account created! Redirecting to your portfolio...")
                        st.rerun()
                    else:
                        st.error(message)


def portfolio_editor_page():
    """Display portfolio editor page"""
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.current_user}")
        st.markdown("---")
        
        st.markdown("### 📋 Portfolio Modules")
        
        available_modules = PortfolioManager.get_available_modules()
        current_modules = st.session_state.portfolio_config.get("modules", [])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Active Modules**")
            for module_key, module_info in available_modules.items():
                is_active = module_key in current_modules
                
                if module_info["required"]:
                    st.markdown(f"✅ {module_info['icon']} {module_info['name']}")
                else:
                    is_checked = st.checkbox(
                        f"{module_info['icon']} {module_info['name']}",
                        value=is_active,
                        key=f"module_{module_key}"
                    )
                    
                    if is_checked and module_key not in current_modules:
                        current_modules.append(module_key)
                    elif not is_checked and module_key in current_modules:
                        current_modules.remove(module_key)
        
        st.session_state.portfolio_config["modules"] = current_modules
        
        st.markdown("---")
        
        if st.button("💾 Save Portfolio", use_container_width=True, type="primary"):
            auth_manager = st.session_state.auth_manager
            success = auth_manager.update_user_portfolio(
                st.session_state.current_user,
                st.session_state.portfolio_config
            )
            
            if success:
                st.success("Portfolio saved successfully!")
            else:
                st.error("Failed to save portfolio")
        
        if st.button("🔗 View Public Portfolio", use_container_width=True):
            st.session_state.show_preview = True
            st.rerun()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_logged_in = False
            st.session_state.current_user = None
            st.session_state.portfolio_config = None
            st.rerun()
    
    # Main content
    st.markdown("# 🎨 Edit Your Portfolio")
    st.markdown("---")
    
    # Tab navigation for different sections
    tab_names = []
    tab_objects = []
    
    modules = st.session_state.portfolio_config.get("modules", [])
    available_modules = PortfolioManager.get_available_modules()
    
    # Always show personal info first
    if "personal_info" in modules:
        tab_names.append("👤 Personal Info")
        tab_objects.append("personal_info")
    
    # Then show other modules
    module_tab_mapping = {
        "experience": ("💼 Experience", "experience"),
        "skills": ("🛠️ Skills", "skills"),
        "projects": ("📁 Projects", "projects"),
        "education": ("🎓 Education", "education"),
        "certificates": ("🏆 Certificates", "certificates"),
        "social_links": ("🔗 Social Links", "social_links"),
    }
    
    for module_key, (tab_name, _) in module_tab_mapping.items():
        if module_key in modules:
            tab_names.append(tab_name)
            tab_objects.append(module_key)
    
    # Theme tab
    tab_names.append("🎨 Theme")
    tab_objects.append("theme")
    
    tabs = st.tabs(tab_names)
    
    for tab, module_key in zip(tabs, tab_objects):
        with tab:
            if module_key == "personal_info":
                st.session_state.portfolio_config = personal_info_editor(
                    st.session_state.portfolio_config
                )
            
            elif module_key == "experience":
                st.session_state.portfolio_config = experience_editor(
                    st.session_state.portfolio_config
                )
            
            elif module_key == "skills":
                st.session_state.portfolio_config = skills_editor(
                    st.session_state.portfolio_config
                )
            
            elif module_key == "projects":
                st.session_state.portfolio_config = projects_editor(
                    st.session_state.portfolio_config
                )
            
            elif module_key == "education":
                st.session_state.portfolio_config = education_editor(
                    st.session_state.portfolio_config
                )
            
            elif module_key == "certificates":
                st.session_state.portfolio_config = certificates_editor(
                    st.session_state.portfolio_config
                )
            
            elif module_key == "social_links":
                st.session_state.portfolio_config = social_links_editor(
                    st.session_state.portfolio_config
                )
            
            elif module_key == "theme":
                st.session_state.portfolio_config = theme_editor(
                    st.session_state.portfolio_config
                )


def portfolio_preview_page():
    """Display portfolio preview"""
    
    with st.sidebar:
        if st.button("← Back to Editor"):
            st.session_state.show_preview = False
            st.rerun()
        
        if st.button("📥 Download as JSON"):
            json_str = json.dumps(st.session_state.portfolio_config, indent=2)
            st.download_button(
                label="Download Config",
                data=json_str,
                file_name=f"{st.session_state.current_user}_portfolio.json",
                mime="application/json"
            )
        
        if st.button("🚪 Logout"):
            st.session_state.user_logged_in = False
            st.session_state.current_user = None
            st.session_state.portfolio_config = None
            st.rerun()
    
    # Portfolio preview
    portfolio = st.session_state.portfolio_config
    
    st.markdown("# 🎉 Your Portfolio Preview")
    st.markdown("---")
    
    # Get theme colors
    colors = portfolio.get("theme", {}).get("colors", {})
    primary_color = colors.get("primary", "#6366f1")
    
    # Header
    personal_info = portfolio.get("personalInfo", {})
    st.markdown(f"## {personal_info.get('title', 'Welcome')}")
    
    if personal_info.get("profileImage"):
        col1, col2 = st.columns([1, 2])
        with col1:
            try:
                st.image(personal_info.get("profileImage"), width=200, caption="Profile")
            except:
                st.info("📷 Profile image not found")
        with col2:
            st.markdown(f"### {personal_info.get('name', 'Name')}")
            if personal_info.get("email"):
                st.write(f"**📧 Email:** {personal_info.get('email')}")
            if personal_info.get("summary"):
                st.write(f"**Summary:** {personal_info.get('summary')}")
            if personal_info.get("about"):
                st.write(f"**About:** {personal_info.get('about')}")
    else:
        st.markdown(f"### {personal_info.get('name', 'Name')}")
        if personal_info.get("email"):
            st.write(f"**📧 Email:** {personal_info.get('email')}")
        if personal_info.get("summary"):
            st.write(f"**Summary:** {personal_info.get('summary')}")
        if personal_info.get("about"):
            st.write(f"**About:** {personal_info.get('about')}")
    
    st.markdown("---")
    
    modules = portfolio.get("modules", [])
    
    # Experience
    if "experience" in modules:
        experience = portfolio.get("experience", {})
        if experience.get("items"):
            st.markdown(f"## 💼 {experience.get('sectionTitle', 'Experience')}")
            for exp in experience.get("items", []):
                st.markdown(f"### {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}")
                st.write(f"*{exp.get('period', 'N/A')}*")
                for desc in exp.get("description", []):
                    st.write(f"• {desc}")
            st.markdown("---")
    
    # Skills
    if "skills" in modules:
        skills = portfolio.get("skills", {})
        if skills.get("categories"):
            st.markdown(f"## 🛠️ {skills.get('sectionTitle', 'Skills')}")
            
            for category in skills.get("categories", []):
                icon = category.get('icon', '🔧')
                title = category.get('title', 'N/A')
                items = category.get('items', '')
                
                # Display with icon and title
                st.markdown(f"### {icon} {title}")
                
                # Display skills as rounded badge boxes
                if items:
                    skills_list = [skill.strip() for skill in items.split(',')]
                    # Create HTML for badge-style skills
                    badges_html = " ".join([
                        f'<span style="display: inline-block; background-color: #e0e7ff; color: #4f46e5; padding: 4px 12px; border-radius: 20px; font-size: 13px; margin: 4px 4px; font-weight: 500;">{skill}</span>'
                        for skill in skills_list if skill
                    ])
                    st.markdown(badges_html, unsafe_allow_html=True)
            
            st.markdown("---")
    
    # Projects
    if "projects" in modules:
        projects = portfolio.get("projects", {})
        if projects.get("items"):
            st.markdown(f"## 📁 {projects.get('sectionTitle', 'Projects')}")
            for project in projects.get("items", []):
                if project.get("url"):
                    st.markdown(f"### [{project.get('title', 'N/A')}]({project.get('url')})")
                else:
                    st.markdown(f"### {project.get('title', 'N/A')}")
                st.write(project.get("description", ""))
            st.markdown("---")
    
    # Education
    if "education" in modules:
        education = portfolio.get("education", {})
        if education.get("items"):
            st.markdown(f"## 🎓 {education.get('sectionTitle', 'Education')}")
            for edu in education.get("items", []):
                st.markdown(f"### {edu.get('title', 'N/A')}")
                st.write(f"*{edu.get('period', 'N/A')}*")
                st.write(edu.get("description", ""))
            st.markdown("---")
    
    # Certificates
    if "certificates" in modules:
        certificates = portfolio.get("certificates", {})
        if certificates.get("items"):
            st.markdown(f"## 🏆 {certificates.get('sectionTitle', 'Certifications')}")
            
            for cert in certificates.get("items", []):
                with st.container(border=True):
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        # Display certificate image if available
                        if cert.get("image"):
                            try:
                                st.image(cert.get("image"), width=150, caption="Certificate Badge")
                            except:
                                st.info("📋 Certificate image")
                        else:
                            st.info("📋 No image")
                    
                    with col2:
                        # Certificate details
                        st.markdown(f"### 🏅 {cert.get('title', 'N/A')}")
                        st.write(f"**Issuer:** {cert.get('issuer', 'N/A')}")
                        
                        if cert.get("date"):
                            st.write(f"**Date:** 📅 {cert.get('date')}")
                        
                        # PDF download if available
                        if cert.get("pdf"):
                            try:
                                with open(cert.get("pdf"), "rb") as pdf_file:
                                    st.download_button(
                                        label="📥 Download Certificate PDF",
                                        data=pdf_file,
                                        file_name=f"{cert.get('title', 'certificate')}.pdf",
                                        mime="application/pdf",
                                        use_container_width=True
                                    )
                            except FileNotFoundError:
                                st.warning("PDF file not found")
            
            st.markdown("---")
    
    # Social Links
    if portfolio.get("socialLinks"):
        st.markdown("## 🔗 Connect")
        
        # Icon mapping for popular platforms with real SVG-like representations
        platform_icons = {
            "linkedin": "in",
            "github": "🐙",
            "instagram": "📸",
            "x": "𝕏",
            "facebook": "f",
            "youtube": "▶️",
            "portfolio": "🌐",
            "email": "✉️",
            "website": "🌍",
            "telegram": "📨",
            "discord": "💬",
            "reddit": "👽",
            "medium": "✍️"
            }
        
        # Create social links with icons
        social_links_html = ""
        for link in portfolio.get("socialLinks", []):
            name = link.get('name', '').lower()
            url = link.get('url', '#')
            
            # Get icon based on platform name
            icon = platform_icons.get(name, "🔗")
            
            social_links_html += f'<a href="{url}" style="display: inline-block; margin: 8px 12px; text-decoration: none; font-size: 24px;" title="{link.get("name")}">{icon}</a>'
        
        if social_links_html:
            st.markdown(f'<div style="text-align: center;">{social_links_html}</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown('<div style="text-align: center; color: #888; font-size: 14px; padding: 20px;">Built with ❤️ using Streamlit</div>', unsafe_allow_html=True)


def main():
    """Main app logic"""
    
    if not st.session_state.user_logged_in:
        login_page()
    else:
        if st.session_state.get("show_preview", False):
            portfolio_preview_page()
        else:
            portfolio_editor_page()


if __name__ == "__main__":
    main()
