"""
Modular Streamlit Portfolio Builder App
"""
import streamlit as st
import json
from pathlib import Path
import sys
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Add app to path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from utils.auth import AuthManager
from utils.portfolio import PortfolioManager
from components.portfolio_editors import (
    personal_info_editor, experience_editor, skills_editor,
    projects_editor, education_editor, certificates_editor,
    social_links_editor, theme_editor
)


def html_to_pdf_weasyprint(html_string):
    """Convert HTML string to PDF using WeasyPrint"""
    try:
        from weasyprint import HTML, CSS
        from io import BytesIO
        
        pdf_buffer = BytesIO()
        HTML(string=html_string).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
    except Exception as e:
        st.error(f"Error converting HTML to PDF: {str(e)}")
        return None


def generate_portfolio_html(portfolio_config):
    """Generate full HTML resume from portfolio configuration"""
    try:
        import html as html_lib
        
        def escape_html(text):
            """Escape special HTML characters and newlines"""
            if not text:
                return ""
            text = str(text)
            text = html_lib.escape(text)
            text = text.replace('\n', '<br>')
            text = text.replace('\r', '')
            return text
        
        personal_info = portfolio_config.get("personalInfo", {})
        modules = portfolio_config.get("modules", [])

        # Prepare profile image (embed as data URI so the HTML preview displays correctly)
        profile_img_tag = ""
        try:
            profile_path = personal_info.get('profileImage')
            if profile_path:
                import base64, mimetypes, pathlib
                p = pathlib.Path(profile_path)
                if p.is_file():
                    mime, _ = mimetypes.guess_type(str(p))
                    if not mime:
                        mime = 'image/png'
                    with open(p, 'rb') as imgf:
                        b = base64.b64encode(imgf.read()).decode('utf-8')
                    profile_img_tag = f'<img src="data:{mime};base64,{b}" class="profile-photo" alt="Profile photo"/>'
        except Exception:
            # non-fatal: if embedding fails, leave empty and continue
            profile_img_tag = ""
        
        # Platform icon mapping
        platform_icons = {
            "linkedin": "💼",
            "github": "🐙",
            "instagram": "📸",
            "twitter": "𝕏",
            "x": "𝕏",
            "facebook": "👍",
            "youtube": "▶️",
            "portfolio": "🌐",
            "email": "✉️",
            "website": "🌍",
            "telegram": "✈️",
            "discord": "🎮",
            "reddit": "👽",
        }
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Portfolio Resume</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                @page {{
                    size: A4;
                    margin: 0.5in;
                }}
                
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    color: #1e293b;
                    line-height: 1.6;
                    background-color: white;
                    margin: 0;
                    padding: 0.4in;
                    width: 100%;
                }}
                
                .resume-container {{
                    width: 100%;
                    background: white;
                    padding: 0;
                    margin: 0;
                    box-shadow: none;
                }}
                
                .header {{
                    text-align: center;
                    border-bottom: 3px solid #4f46e5;
                    padding-bottom: 15px;
                    margin-bottom: 20px;
                }}
                
                .name {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #4f46e5;
                    margin-bottom: 5px;
                }}
                
                .title {{
                    font-size: 16px;
                    color: #64748b;
                    margin-bottom: 8px;
                }}
                
                .contact-info {{
                    font-size: 12px;
                    color: #475569;
                    margin-bottom: 5px;
                }}
                
                .profile-photo {{
                    width: 100px;
                    height: 100px;
                    border-radius: 50%;
                    object-fit: cover;
                    border: 3px solid #4f46e5;
                    margin: 10px auto;
                    display: block;
                }}
                
                .section {{
                    margin-bottom: 20px;
                    page-break-inside: avoid;
                    break-inside: avoid;
                }}
                
                .section-title {{
                    font-size: 14px;
                    font-weight: bold;
                    color: white;
                    background-color: #4f46e5;
                    padding: 8px 12px;
                    margin-bottom: 12px;
                    border-left: 4px solid #6366f1;
                }}
                
                .item {{
                    margin-bottom: 12px;
                    padding-left: 10px;
                    border-left: 2px solid #e2e8f0;
                }}
                
                .item-title {{
                    font-weight: bold;
                    color: #1e293b;
                    font-size: 13px;
                }}
                
                .item-subtitle {{
                    font-size: 11px;
                    color: #64748b;
                    font-style: italic;
                    margin-top: 2px;
                }}
                
                .item-description {{
                    font-size: 12px;
                    color: #475569;
                    margin-top: 5px;
                }}
                
                .item-description li {{
                    margin-left: 20px;
                    margin-top: 3px;
                }}
                
                .skills-container {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                }}
                
                .skill-badge {{
                    background-color: #e0e7ff;
                    color: #4f46e5;
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-size: 12px;
                    font-weight: 500;
                    display: inline-block;
                }}
                
                .skill-category {{
                    margin-bottom: 10px;
                }}
                
                .skill-category-title {{
                    font-weight: bold;
                    color: #4f46e5;
                    font-size: 12px;
                    margin-bottom: 5px;
                }}
                
                .social-links {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 15px;
                    margin-top: 10px;
                }}
                
                .social-link {{
                    display: flex;
                    align-items: center;
                    gap: 5px;
                    font-size: 12px;
                    color: #4f46e5;
                    text-decoration: none;
                    padding: 5px 10px;
                    border-radius: 5px;
                    transition: all 0.3s ease;
                }}
                
                .social-link:hover {{
                    background-color: #e0e7ff;
                    color: #2d3a9f;
                    text-decoration: underline;
                }}
                
                .social-icon {{
                    font-size: 16px;
                }}
                
                .summary {{
                    font-size: 12px;
                    color: #475569;
                    line-height: 1.5;
                    margin-top: 10px;
                }}
                
                .footer {{
                    text-align: center;
                    font-size: 10px;
                    color: #888;
                    margin-top: 30px;
                    border-top: 1px solid #e2e8f0;
                    padding-top: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="resume-container">
                <!-- Header -->
                <div class="header">
                    {profile_img}
                    <div class="name">{name}</div>
                    <div class="title">{title}</div>
                    <div class="contact-info">{contact_info}</div>
                </div>
        """.format(
            name=escape_html(personal_info.get('name', 'Your Name')),
            title=escape_html(personal_info.get('title', 'Professional')),
            contact_info=escape_html(' | '.join([
                f"{personal_info.get('email')}" if personal_info.get('email') else '',
                f"{personal_info.get('phone')}" if personal_info.get('phone') else ''
            ]).replace(' | |', ' | ').strip(' |'))
                ,
                profile_img=profile_img_tag
        )
        
        # Summary Section
        if personal_info.get('summary') or personal_info.get('about'):
            summary = personal_info.get('summary') or personal_info.get('about')
            html += '<div class="section"><div class="summary">' + escape_html(summary) + '</div></div>'
        
        # Experience
        if "experience" in modules:
            experience = portfolio_config.get("experience", {})
            if experience.get("items"):
                html += '<div class="section">'
                html += '<div class="section-title">EXPERIENCE</div>'
                for exp in experience.get("items", []):
                    html += '<div class="item"><div class="item-title">' + escape_html(exp.get('title', 'N/A')) + ' @ ' + escape_html(exp.get('company', 'N/A')) + '</div>'
                    html += '<div class="item-subtitle">' + escape_html(exp.get('period', 'N/A')) + '</div>'
                    html += '<div class="item-description"><ul>'
                    for desc in exp.get("description", []):
                        html += '<li>' + escape_html(desc) + '</li>'
                    html += '</ul></div></div>'
                html += '</div>'
        
        # Skills
        if "skills" in modules:
            skills = portfolio_config.get("skills", {})
            if skills.get("categories"):
                html += '<div class="section">'
                html += '<div class="section-title">SKILLS</div>'
                for category in skills.get("categories", []):
                    cat_title = category.get('title', 'Skills')
                    items = category.get('items', '')
                    html += '<div class="skill-category"><div class="skill-category-title">' + escape_html(cat_title) + '</div><div class="skills-container">'
                    if items:
                        for skill in items.split(','):
                            skill = skill.strip()
                            if skill:
                                html += '<span class="skill-badge">' + escape_html(skill) + '</span>'
                    html += '</div></div>'
                html += '</div>'
        
        # Projects
        if "projects" in modules:
            projects = portfolio_config.get("projects", {})
            if projects.get("items"):
                html += '<div class="section"><div class="section-title">PROJECTS</div>'
                for project in projects.get("items", []):
                    html += '<div class="item"><div class="item-title">' + escape_html(project.get('title', 'N/A')) + '</div>'
                    if project.get('url'):
                        html += '<div class="item-subtitle">' + escape_html(project.get("url")) + '</div>'
                    if project.get('description'):
                        html += '<div class="item-description">' + escape_html(project.get("description")) + '</div>'
                    html += '</div>'
                html += '</div>'
        
        # Education
        if "education" in modules:
            education = portfolio_config.get("education", {})
            if education.get("items"):
                html += '<div class="section"><div class="section-title">EDUCATION</div>'
                for edu in education.get("items", []):
                    html += '<div class="item"><div class="item-title">' + escape_html(edu.get('title', 'N/A')) + '</div>'
                    html += '<div class="item-subtitle">' + escape_html(edu.get('period', 'N/A')) + '</div>'
                    if edu.get('description'):
                        html += '<div class="item-description">' + escape_html(edu.get("description")) + '</div>'
                    html += '</div>'
                html += '</div>'
        
        # Certificates
        if "certificates" in modules:
            certificates = portfolio_config.get("certificates", {})
            if certificates.get("items"):
                html += '<div class="section"><div class="section-title">CERTIFICATES</div>'
                for cert in certificates.get("items", []):
                    html += '<div class="item"><div class="item-title">' + escape_html(cert.get('title', 'N/A')) + '</div>'
                    html += '<div class="item-subtitle">Issuer: ' + escape_html(cert.get('issuer', 'N/A')) + '</div>'
                    if cert.get('date'):
                        html += '<div class="item-subtitle">Date: ' + escape_html(cert.get("date")) + '</div>'
                    html += '</div>'
                html += '</div>'
        
        # Social Links
        if portfolio_config.get("socialLinks"):
            html += '<div class="section">'
            html += '<div class="section-title">CONNECT</div>'
            html += '<div class="social-links">'
            for link in portfolio_config.get("socialLinks", []):
                name = link.get('name', '').lower()
                url = link.get('url', '#').strip()
                if not url or url == '#':
                    url = '#'
                icon = platform_icons.get(name, '🔗')
                html += '<a href="' + url + '" target="_blank" class="social-link"><span class="social-icon">' + icon + '</span> ' + escape_html(link.get("name")) + '</a>'
            html += '</div></div>'
        
        # Footer
        html += '<div class="footer">Generated with Streamlit Portfolio Builder</div>'
        html += '</div></body></html>'
        
        return html
    except Exception as e:
        import traceback
        error_msg = f"Error generating HTML: {str(e)}\n\n{traceback.format_exc()}"
        st.error(error_msg)
        return None


def generate_portfolio_pdf(portfolio_config):
    """Generate visually rich PDF from portfolio configuration with colors, icons, and styling"""
    try:
        from io import BytesIO
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
        
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, topMargin=0.4*inch, bottomMargin=0.4*inch)
        story = []
        
        # Define color scheme
        primary_color = colors.HexColor('#4f46e5')  # Indigo
        secondary_color = colors.HexColor('#6366f1')  # Light indigo
        text_dark = colors.HexColor('#1e293b')  # Dark slate
        text_light = colors.HexColor('#64748b')  # Light slate
        accent_color = colors.HexColor('#ec4899')  # Pink accent
        
        # Styles
        styles = getSampleStyleSheet()
        
        # Title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=32,
            textColor=primary_color,
            spaceAfter=4,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Subtitle style
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=text_light,
            spaceAfter=2,
            alignment=TA_CENTER,
            fontName='Helvetica-BoldOblique'
        )
        
        # Contact style
        contact_style = ParagraphStyle(
            'Contact',
            parent=styles['Normal'],
            fontSize=9,
            textColor=text_dark,
            spaceAfter=8,
            alignment=TA_CENTER,
            fontName='Helvetica'
        )
        
        # Section heading
        section_heading_style = ParagraphStyle(
            'SectionHeading',
            parent=styles['Heading2'],
            fontSize=13,
            textColor=colors.white,
            spaceAfter=10,
            spaceBefore=8,
            fontName='Helvetica-Bold',
            backColor=primary_color,
            leftIndent=8,
            rightIndent=8,
            topPadding=6,
            bottomPadding=6
        )
        
        # Item heading
        item_heading_style = ParagraphStyle(
            'ItemHeading',
            parent=styles['Heading3'],
            fontSize=11,
            textColor=primary_color,
            spaceAfter=2,
            spaceBefore=6,
            fontName='Helvetica-Bold'
        )
        
        # Item subheading (date/company)
        item_sub_style = ParagraphStyle(
            'ItemSub',
            parent=styles['Normal'],
            fontSize=9,
            textColor=text_light,
            spaceAfter=4,
            fontName='Helvetica-Oblique'
        )
        
        # Normal text
        normal_style = ParagraphStyle(
            'Normal',
            parent=styles['Normal'],
            fontSize=9,
            textColor=text_dark,
            spaceAfter=3,
            leading=11
        )
        
        # Skills badge style
        skills_style = ParagraphStyle(
            'Skills',
            parent=styles['Normal'],
            fontSize=9,
            textColor=secondary_color,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )
        
        # Personal Info Section
        personal_info = portfolio_config.get("personalInfo", {})
        name = personal_info.get('name', 'Your Name')
        title = personal_info.get('title', 'Professional')
        
        story.append(Paragraph(name, title_style))
        story.append(Paragraph(title, subtitle_style))
        
        # Contact Information
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(f"✉ {personal_info.get('email')}")
        if personal_info.get('phone'):
            contact_parts.append(f"☎ {personal_info.get('phone')}")
        if contact_parts:
            story.append(Paragraph(" | ".join(contact_parts), contact_style))
        
        story.append(Spacer(1, 0.15*inch))
        
        # Summary section
        if personal_info.get('summary') or personal_info.get('about'):
            summary_text = ""
            if personal_info.get('summary'):
                summary_text = personal_info.get('summary')
            elif personal_info.get('about'):
                summary_text = personal_info.get('about')
            
            story.append(Paragraph(summary_text, normal_style))
            story.append(Spacer(1, 0.15*inch))
        
        # Experience Section
        modules = portfolio_config.get("modules", [])
        if "experience" in modules:
            experience = portfolio_config.get("experience", {})
            if experience.get("items"):
                story.append(Paragraph("EXPERIENCE", section_heading_style))
                story.append(Spacer(1, 0.08*inch))
                
                for exp in experience.get("items", []):
                    # Job title and company
                    job_text = f"{exp.get('title', 'N/A')} @ {exp.get('company', 'N/A')}"
                    story.append(Paragraph(job_text, item_heading_style))
                    story.append(Paragraph(exp.get('period', 'N/A'), item_sub_style))
                    
                    # Description
                    for desc in exp.get("description", []):
                        story.append(Paragraph(f"• {desc}", normal_style))
                    story.append(Spacer(1, 0.08*inch))
        
        # Skills Section
        if "skills" in modules:
            skills = portfolio_config.get("skills", {})
            if skills.get("categories"):
                story.append(Paragraph("SKILLS", section_heading_style))
                story.append(Spacer(1, 0.08*inch))
                
                for category in skills.get("categories", []):
                    cat_title = category.get('title', 'Skills')
                    items = category.get('items', '')
                    
                    story.append(Paragraph(f"<b>{cat_title}</b>", item_heading_style))
                    
                    if items:
                        skills_list = ", ".join([s.strip() for s in items.split(',') if s.strip()])
                        story.append(Paragraph(skills_list, skills_style))
                    story.append(Spacer(1, 0.06*inch))
        
        # Projects Section
        if "projects" in modules:
            projects = portfolio_config.get("projects", {})
            if projects.get("items"):
                story.append(Paragraph("PROJECTS", section_heading_style))
                story.append(Spacer(1, 0.08*inch))
                
                for project in projects.get("items", []):
                    proj_title = project.get('title', 'N/A')
                    story.append(Paragraph(f"<b>{proj_title}</b>", item_heading_style))
                    
                    if project.get('url'):
                        story.append(Paragraph(f"<i>{project.get('url')}</i>", item_sub_style))
                    
                    if project.get('description'):
                        story.append(Paragraph(project.get('description'), normal_style))
                    story.append(Spacer(1, 0.08*inch))
        
        # Education Section
        if "education" in modules:
            education = portfolio_config.get("education", {})
            if education.get("items"):
                story.append(Paragraph("EDUCATION", section_heading_style))
                story.append(Spacer(1, 0.08*inch))
                
                for edu in education.get("items", []):
                    story.append(Paragraph(edu.get('title', 'N/A'), item_heading_style))
                    story.append(Paragraph(edu.get('period', 'N/A'), item_sub_style))
                    
                    if edu.get('description'):
                        story.append(Paragraph(edu.get('description'), normal_style))
                    story.append(Spacer(1, 0.08*inch))
        
        # Certificates Section
        if "certificates" in modules:
            certificates = portfolio_config.get("certificates", {})
            if certificates.get("items"):
                story.append(Paragraph("CERTIFICATES", section_heading_style))
                story.append(Spacer(1, 0.08*inch))
                
                for cert in certificates.get("items", []):
                    story.append(Paragraph(cert.get('title', 'N/A'), item_heading_style))
                    story.append(Paragraph(f"<b>Issuer:</b> {cert.get('issuer', 'N/A')}", normal_style))
                    
                    if cert.get('date'):
                        story.append(Paragraph(f"<b>Date:</b> {cert.get('date')}", normal_style))
                    story.append(Spacer(1, 0.08*inch))
        
        # Social Links Section
        if portfolio_config.get("socialLinks"):
            story.append(Paragraph("CONNECT", section_heading_style))
            story.append(Spacer(1, 0.08*inch))
            
            for link in portfolio_config.get("socialLinks", []):
                name = link.get('name', '')
                url = link.get('url', '')
                story.append(Paragraph(f"<b>{name}</b>: {url}", normal_style))
            story.append(Spacer(1, 0.15*inch))
        
        # Footer
        story.append(Spacer(1, 0.1*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#aaaaaa'),
            alignment=TA_CENTER
        )
        story.append(Paragraph("Generated with Streamlit Portfolio Builder", footer_style))
        
        # Build PDF
        doc.build(story)
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return None


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
    """Display portfolio preview with full HTML resume in A4 format"""
    
    with st.sidebar:
        st.subheader("Actions")
        
        if st.button("Back to Editor", use_container_width=True):
            st.session_state.show_preview = False
            st.rerun()
        
        st.divider()
        
        st.subheader("Downloads")
        
        col1, col2 = st.columns(2)
        
        with col1:
            json_str = json.dumps(st.session_state.portfolio_config, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"{st.session_state.current_user}_portfolio.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            # Generate HTML and convert to PDF
            html_resume = generate_portfolio_html(st.session_state.portfolio_config)
            if html_resume:
                pdf_data = html_to_pdf_weasyprint(html_resume)
                if pdf_data:
                    st.download_button(
                        label="Download PDF",
                        data=pdf_data,
                        file_name=f"{st.session_state.current_user}_resume.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        
        st.divider()
        
        if st.button("Logout", use_container_width=True):
            st.session_state.user_logged_in = False
            st.session_state.current_user = None
            st.session_state.portfolio_config = None
            st.rerun()
    
    # Display HTML resume in A4 format
    st.markdown("# Your Resume (A4 Format)")
    st.markdown("---")
    
    portfolio = st.session_state.portfolio_config
    html_resume = generate_portfolio_html(portfolio)
    
    if html_resume:
        # Display using Streamlit's HTML component
        st.components.v1.html(html_resume, height=1200, scrolling=True)
    else:
        st.error("Failed to generate HTML resume")
    
    # Also show traditional Streamlit preview below
    st.markdown("---")
    st.markdown("## Alternative Preview (Traditional Layout)")
    st.markdown("---")
    
    # Personal Info
    personal_info = portfolio.get("personalInfo", {})
    if personal_info:
        # Show profile image if available
        profile_image = personal_info.get('profileImage')
        if profile_image:
            try:
                st.image(profile_image, width=150)
            except Exception:
                st.warning("Could not load profile image")

        st.markdown(f"# {personal_info.get('name', 'Your Name')}")
        if personal_info.get('title'):
            st.markdown(f"## {personal_info.get('title')}")
        
        contact_items = []
        if personal_info.get('email'):
            contact_items.append(f"📧 {personal_info.get('email')}")
        if personal_info.get('phone'):
            contact_items.append(f"📱 {personal_info.get('phone')}")
        if personal_info.get('location'):
            contact_items.append(f"📍 {personal_info.get('location')}")
        
        if contact_items:
            st.markdown(" | ".join(contact_items))
        
        if personal_info.get('summary') or personal_info.get('about'):
            summary = personal_info.get('summary') or personal_info.get('about')
            st.markdown(f"**About:** {summary}")
        
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
            "linkedin": "💼",
            "github": "🐙",
            "instagram": "📸",
            "x": "𝕏",
            "twitter": "𝕏",
            "facebook": "👍",
            "youtube": "▶️",
            "portfolio": "🌐",
            "email": "✉️",
            "website": "🌍",
            "telegram": "✈️",
            "discord": "🎮",
            "reddit": "👽",
            "medium": "✍️"
            }
        
        # Create social links with icons and text
        social_links_html = ""
        for link in portfolio.get("socialLinks", []):
            name = link.get('name', '').lower()
            url = link.get('url', '#')
            
            # Get icon based on platform name
            icon = platform_icons.get(name, "🔗")
            link_text = link.get('name', 'Link')
            
            social_links_html += f'<a href="{url}" style="display: inline-block; margin: 8px 12px; padding: 8px 12px; text-decoration: none; color: #4f46e5; border: 1px solid #e0e7ff; border-radius: 6px; background-color: #f8fafc;" title="{link_text}"><span style="margin-right: 6px;">{icon}</span>{link_text}</a>'
        
        
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
