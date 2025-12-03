"""
Reusable Streamlit components for portfolio sections
"""
import streamlit as st
import json
import os
from pathlib import Path


# Helper function to handle file uploads
def handle_file_upload(file_uploader, upload_folder):
    """
    Handle file uploads and save to appData folder
    Returns the relative path to the saved file
    """
    if file_uploader is not None:
        # Create appData directory if it doesn't exist
        appdata_path = Path("data") / upload_folder
        appdata_path.mkdir(parents=True, exist_ok=True)
        
        # Save file with original name
        file_path = appdata_path / file_uploader.name
        with open(file_path, "wb") as f:
            f.write(file_uploader.getbuffer())
        
        # Return relative path for storage
        return str(file_path).replace("\\", "/")
    return None


# Icon mapping with descriptions
SKILL_ICONS = {
    "🔧": "Tool / General",
    "💻": "Computer / Programming",
    "📚": "Language / Learning",
    "☁️": "Cloud / DevOps",
    "🎨": "Design / Creative",
    "⚙️": "Backend / Server",
    "👁️": "Frontend / UI",
    "📊": "Data / Analytics"
}


def personal_info_editor(portfolio_config):
    """Editor for personal information section"""
    st.subheader("👤 Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input(
            "Full Name",
            value=portfolio_config["personalInfo"].get("name", ""),
            key="personal_name"
        )
        email = st.text_input(
            "Email",
            value=portfolio_config["personalInfo"].get("email", ""),
            key="personal_email"
        )
    
    with col2:
        title = st.text_input(
            "Professional Title",
            value=portfolio_config["personalInfo"].get("title", ""),
            key="personal_title",
            placeholder="e.g., Hello! I'm [Name]"
        )
    
    # Profile Image Upload Section
    st.write("**Profile Image**")
    col_img1, col_img2 = st.columns(2)
    
    with col_img1:
        uploaded_image = st.file_uploader(
            "Upload Profile Image",
            type=["jpg", "jpeg", "png", "gif"],
            key="profile_image_upload",
            help="Upload your profile picture (JPG, PNG, or GIF)"
        )
        
        if uploaded_image:
            image_path = handle_file_upload(uploaded_image, "images")
            st.success(f"✅ Image saved: {uploaded_image.name}")
            profile_image = image_path
        else:
            profile_image = portfolio_config["personalInfo"].get("profileImage", "")
            if profile_image:
                st.info(f"Current image: {profile_image}")
    
    with col_img2:
        if profile_image:
            try:
                st.image(profile_image, width=150, caption="Preview")
            except:
                st.warning("Could not load image preview")
    
    summary = st.text_area(
        "Professional Summary",
        value=portfolio_config["personalInfo"].get("summary", ""),
        key="personal_summary",
        height=100
    )
    
    about = st.text_area(
        "About",
        value=portfolio_config["personalInfo"].get("about", ""),
        key="personal_about",
        height=100
    )
    
    # Update config
    portfolio_config["personalInfo"].update({
        "name": name,
        "email": email,
        "title": title,
        "profileImage": profile_image,
        "summary": summary,
        "about": about
    })
    
    return portfolio_config


def experience_editor(portfolio_config):
    """Editor for experience section"""
    st.subheader("💼 Work Experience")
    
    section_title = st.text_input(
        "Section Title",
        value=portfolio_config["experience"].get("sectionTitle", "Experience"),
        key="exp_title"
    )
    
    # Section Image Upload
    col_sec1, col_sec2 = st.columns(2)
    with col_sec1:
        uploaded_sec_image = st.file_uploader(
            "Upload Section Image",
            type=["jpg", "jpeg", "png", "gif"],
            key="exp_image_upload",
            help="Upload a cover image for experience section"
        )
        if uploaded_sec_image:
            image_path = handle_file_upload(uploaded_sec_image, "images")
            st.success(f"✅ Image saved: {uploaded_sec_image.name}")
            section_image = image_path
        else:
            section_image = portfolio_config["experience"].get("sectionImage", "")
    
    with col_sec2:
        if section_image:
            try:
                st.image(section_image, width=150)
            except:
                pass
    
    portfolio_config["experience"]["sectionTitle"] = section_title
    portfolio_config["experience"]["sectionImage"] = section_image
    
    # Experience items
    st.write("**Experience Items**")
    
    items = portfolio_config["experience"].get("items", [])
    num_items = st.number_input("Number of experience entries", min_value=0, value=len(items), key="exp_count")
    
    new_items = []
    for i in range(int(num_items)):
        with st.expander(f"Experience {i+1}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input(
                    "Job Title",
                    value=items[i].get("title", "") if i < len(items) else "",
                    key=f"exp_title_{i}"
                )
                company = st.text_input(
                    "Company",
                    value=items[i].get("company", "") if i < len(items) else "",
                    key=f"exp_company_{i}"
                )
            
            with col2:
                period = st.text_input(
                    "Period (e.g., Jan 2020 - Present)",
                    value=items[i].get("period", "") if i < len(items) else "",
                    key=f"exp_period_{i}"
                )
            
            description = st.text_area(
                "Description (one per line)",
                value="\n".join(items[i].get("description", [])) if i < len(items) else "",
                key=f"exp_desc_{i}",
                height=100
            )
            
            new_items.append({
                "title": title,
                "company": company,
                "period": period,
                "description": [line.strip() for line in description.split("\n") if line.strip()]
            })
    
    portfolio_config["experience"]["items"] = new_items
    return portfolio_config


def skills_editor(portfolio_config):
    """Editor for skills section"""
    st.subheader("🛠️ Skills")
    
    section_title = st.text_input(
        "Section Title",
        value=portfolio_config["skills"].get("sectionTitle", "Skills"),
        key="skills_title"
    )
    
    # Section Image Upload
    col_sec1, col_sec2 = st.columns(2)
    with col_sec1:
        uploaded_sec_image = st.file_uploader(
            "Upload Skills Section Image",
            type=["jpg", "jpeg", "png", "gif"],
            key="skills_image_upload",
            help="Upload a cover image for skills section"
        )
        if uploaded_sec_image:
            image_path = handle_file_upload(uploaded_sec_image, "images")
            st.success(f"✅ Image saved: {uploaded_sec_image.name}")
            section_image = image_path
        else:
            section_image = portfolio_config["skills"].get("sectionImage", "")
    
    with col_sec2:
        if section_image:
            try:
                st.image(section_image, width=150)
            except:
                pass
    
    portfolio_config["skills"]["sectionTitle"] = section_title
    portfolio_config["skills"]["sectionImage"] = section_image
    
    # Skill categories
    st.write("**Skill Categories**")
    st.info("💡 Select an icon and add comma-separated skills")
    
    categories = portfolio_config["skills"].get("categories", [])
    num_categories = st.number_input("Number of skill categories", min_value=0, value=len(categories), key="skills_count")
    
    # Create icon options with names for better UX
    icon_list = list(SKILL_ICONS.keys())
    icon_labels = [f"{icon} {SKILL_ICONS[icon]}" for icon in icon_list]
    
    new_categories = []
    for i in range(int(num_categories)):
        with st.expander(f"Category {i+1}", expanded=False):
            col1, col2 = st.columns([2, 3])
            
            with col1:
                category_title = st.text_input(
                    "Category Name",
                    value=categories[i].get("title", "") if i < len(categories) else "",
                    key=f"skills_cat_title_{i}",
                    placeholder="e.g., Languages"
                )
            
            with col2:
                current_icon = categories[i].get("icon", "🔧") if i < len(categories) else "🔧"
                icon_index = icon_list.index(current_icon) if current_icon in icon_list else 0
                
                selected_icon_label = st.selectbox(
                    "Select Icon",
                    icon_labels,
                    index=icon_index,
                    key=f"skills_icon_{i}",
                    help="Choose an icon to represent this skill category"
                )
                # Extract just the icon emoji
                selected_icon = selected_icon_label.split()[0]
            
            items = st.text_input(
                "Skills (comma-separated)",
                value=categories[i].get("items", "") if i < len(categories) else "",
                key=f"skills_items_{i}",
                placeholder="e.g., Python, JavaScript, Docker",
                help="Separate multiple skills with commas"
            )
            
            # Preview the icon with category name
            if category_title:
                st.markdown(f"**Preview:** {selected_icon} {category_title}")
            
            new_categories.append({
                "title": category_title,
                "icon": selected_icon,
                "items": items
            })
    
    portfolio_config["skills"]["categories"] = new_categories
    return portfolio_config


def projects_editor(portfolio_config):
    """Editor for projects section"""
    st.subheader("📁 Projects")
    
    section_title = st.text_input(
        "Section Title",
        value=portfolio_config["projects"].get("sectionTitle", "Projects"),
        key="projects_title"
    )
    
    portfolio_config["projects"]["sectionTitle"] = section_title
    
    # Projects items
    st.write("**Projects**")
    
    items = portfolio_config["projects"].get("items", [])
    num_items = st.number_input("Number of projects", min_value=0, value=len(items), key="projects_count")
    
    new_items = []
    for i in range(int(num_items)):
        with st.expander(f"Project {i+1}", expanded=False):
            title = st.text_input(
                "Project Name",
                value=items[i].get("title", "") if i < len(items) else "",
                key=f"proj_title_{i}"
            )
            
            url = st.text_input(
                "Project URL (optional)",
                value=items[i].get("url", "") if i < len(items) else "",
                key=f"proj_url_{i}",
                placeholder="https://..."
            )
            
            description = st.text_area(
                "Description",
                value=items[i].get("description", "") if i < len(items) else "",
                key=f"proj_desc_{i}",
                height=100
            )
            
            new_items.append({
                "title": title,
                "url": url if url else None,
                "description": description
            })
    
    portfolio_config["projects"]["items"] = new_items
    return portfolio_config


def education_editor(portfolio_config):
    """Editor for education section"""
    st.subheader("🎓 Education")
    
    section_title = st.text_input(
        "Section Title",
        value=portfolio_config["education"].get("sectionTitle", "Education"),
        key="edu_title"
    )
    
    # Section Image Upload
    col_sec1, col_sec2 = st.columns(2)
    with col_sec1:
        uploaded_sec_image = st.file_uploader(
            "Upload Education Section Image",
            type=["jpg", "jpeg", "png", "gif"],
            key="edu_image_upload",
            help="Upload a cover image for education section"
        )
        if uploaded_sec_image:
            image_path = handle_file_upload(uploaded_sec_image, "images")
            st.success(f"✅ Image saved: {uploaded_sec_image.name}")
            section_image = image_path
        else:
            section_image = portfolio_config["education"].get("sectionImage", "")
    
    with col_sec2:
        if section_image:
            try:
                st.image(section_image, width=150)
            except:
                pass
    
    portfolio_config["education"]["sectionTitle"] = section_title
    portfolio_config["education"]["sectionImage"] = section_image
    
    # Education items
    st.write("**Education Entries**")
    
    items = portfolio_config["education"].get("items", [])
    num_items = st.number_input("Number of education entries", min_value=0, value=len(items), key="edu_count")
    
    new_items = []
    for i in range(int(num_items)):
        with st.expander(f"Education {i+1}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input(
                    "Degree/Certification",
                    value=items[i].get("title", "") if i < len(items) else "",
                    key=f"edu_title_{i}"
                )
            
            with col2:
                period = st.text_input(
                    "Period (e.g., 2010-2014)",
                    value=items[i].get("period", "") if i < len(items) else "",
                    key=f"edu_period_{i}"
                )
            
            description = st.text_area(
                "Description (Institution, Field, etc.)",
                value=items[i].get("description", "") if i < len(items) else "",
                key=f"edu_desc_{i}",
                height=80
            )
            
            new_items.append({
                "title": title,
                "period": period,
                "description": description
            })
    
    portfolio_config["education"]["items"] = new_items
    return portfolio_config


def certificates_editor(portfolio_config):
    """Editor for certificates section"""
    st.subheader("🏆 Certifications")
    
    section_title = st.text_input(
        "Section Title",
        value=portfolio_config["certificates"].get("sectionTitle", "Certifications"),
        key="cert_title"
    )
    
    portfolio_config["certificates"]["sectionTitle"] = section_title
    
    # Certificates items
    st.write("**Certificates**")
    
    items = portfolio_config["certificates"].get("items", [])
    num_items = st.number_input("Number of certificates", min_value=0, value=len(items), key="cert_count")
    
    new_items = []
    for i in range(int(num_items)):
        with st.expander(f"Certificate {i+1}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input(
                    "Certificate Title",
                    value=items[i].get("title", "") if i < len(items) else "",
                    key=f"cert_title_{i}"
                )
                issuer = st.text_input(
                    "Issuing Organization",
                    value=items[i].get("issuer", "") if i < len(items) else "",
                    key=f"cert_issuer_{i}"
                )
            
            with col2:
                date = st.text_input(
                    "Date",
                    value=items[i].get("date", "") if i < len(items) else "",
                    key=f"cert_date_{i}",
                    placeholder="e.g., 2023"
                )
            
            # Certificate Image Upload
            st.write("**Certificate Image**")
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                uploaded_cert_image = st.file_uploader(
                    "Upload Certificate Image",
                    type=["jpg", "jpeg", "png", "gif"],
                    key=f"cert_image_upload_{i}",
                    help="Upload a certificate image or badge"
                )
                if uploaded_cert_image:
                    image_path = handle_file_upload(uploaded_cert_image, "certificates")
                    st.success(f"✅ Image saved: {uploaded_cert_image.name}")
                    image = image_path
                else:
                    image = items[i].get("image", "") if i < len(items) else ""
            
            with col_img2:
                if image:
                    try:
                        st.image(image, width=120, caption="Certificate Preview")
                    except:
                        pass
            
            # Certificate PDF Upload
            st.write("**Certificate PDF**")
            col_pdf1, col_pdf2 = st.columns(2)
            with col_pdf1:
                uploaded_cert_pdf = st.file_uploader(
                    "Upload Certificate PDF",
                    type=["pdf"],
                    key=f"cert_pdf_upload_{i}",
                    help="Upload the certificate PDF file"
                )
                if uploaded_cert_pdf:
                    pdf_path = handle_file_upload(uploaded_cert_pdf, "certificates")
                    st.success(f"✅ PDF saved: {uploaded_cert_pdf.name}")
                    pdf = pdf_path
                else:
                    pdf = items[i].get("pdf", "") if i < len(items) else ""
            
            with col_pdf2:
                if pdf:
                    st.info(f"📄 PDF: {pdf.split('/')[-1]}")
            
            new_items.append({
                "title": title,
                "issuer": issuer,
                "date": date,
                "image": image if image else None,
                "pdf": pdf if pdf else None
            })
    
    portfolio_config["certificates"]["items"] = new_items
    return portfolio_config


def social_links_editor(portfolio_config):
    """Editor for social links"""
    st.subheader("🔗 Social Links")
    
    links = portfolio_config.get("socialLinks", [])
    num_links = st.number_input("Number of social links", min_value=0, value=len(links), key="social_count")
    
    social_platforms = ["GitHub", "LinkedIn", "Twitter", "Portfolio", "Blog", "Instagram", "Facebook", "YouTube"]
    
    new_links = []
    for i in range(int(num_links)):
        with st.expander(f"Link {i+1}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.selectbox(
                    "Platform",
                    social_platforms,
                    index=social_platforms.index(links[i].get("name", "GitHub")) if i < len(links) else 0,
                    key=f"social_name_{i}"
                )
            
            with col2:
                url = st.text_input(
                    "URL",
                    value=links[i].get("url", "") if i < len(links) else "",
                    key=f"social_url_{i}",
                    placeholder="https://..."
                )
            
            new_links.append({
                "name": name,
                "url": url
            })
    
    portfolio_config["socialLinks"] = new_links
    return portfolio_config


def theme_editor(portfolio_config):
    """Editor for theme customization"""
    st.subheader("🎨 Theme Customization")
    
    col1, col2, col3 = st.columns(3)
    
    colors = portfolio_config.get("theme", {}).get("colors", {})
    
    with col1:
        primary = st.color_picker(
            "Primary Color",
            value=colors.get("primary", "#6366f1"),
            key="theme_primary"
        )
    
    with col2:
        secondary = st.color_picker(
            "Secondary Color",
            value=colors.get("secondary", "#8b5cf6"),
            key="theme_secondary"
        )
    
    with col3:
        accent = st.color_picker(
            "Accent Color",
            value=colors.get("accent", "#06b6d4"),
            key="theme_accent"
        )
    
    if "theme" not in portfolio_config:
        portfolio_config["theme"] = {}
    if "colors" not in portfolio_config["theme"]:
        portfolio_config["theme"]["colors"] = {}
    
    portfolio_config["theme"]["colors"].update({
        "primary": primary,
        "secondary": secondary,
        "accent": accent
    })
    # Template selection
    templates = {
        "modern": "Modern (clean, colored header)",
        "classic": "Classic (two-column, serif)",
        "compact": "Compact (dense, single-column)"
    }
    current = portfolio_config.get("theme", {}).get("template", "modern")
    template_choice = st.selectbox("Resume Template", options=list(templates.keys()), format_func=lambda k: templates[k], index=list(templates.keys()).index(current) if current in templates else 0, key="theme_template")
    portfolio_config["theme"]["template"] = template_choice
    
    return portfolio_config
