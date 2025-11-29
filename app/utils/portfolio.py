"""
Portfolio data management module
"""
import json
import os
from pathlib import Path
from datetime import datetime


class PortfolioManager:
    """Manages portfolio data and modules"""
    
    # Available portfolio modules
    AVAILABLE_MODULES = {
        "personal_info": {
            "name": "Personal Information",
            "description": "Your profile, summary, and about section",
            "icon": "👤",
            "required": True
        },
        "experience": {
            "name": "Work Experience",
            "description": "Your professional work history",
            "icon": "💼",
            "required": False
        },
        "skills": {
            "name": "Skills",
            "description": "Technical and professional skills",
            "icon": "🛠️",
            "required": False
        },
        "projects": {
            "name": "Projects",
            "description": "Showcase your projects and work",
            "icon": "📁",
            "required": False
        },
        "education": {
            "name": "Education",
            "description": "Educational background",
            "icon": "🎓",
            "required": False
        },
        "certificates": {
            "name": "Certifications",
            "description": "Professional certifications and awards",
            "icon": "🏆",
            "required": False
        },
        "social_links": {
            "name": "Social Links",
            "description": "Connect with your social profiles",
            "icon": "🔗",
            "required": False
        }
    }
    
    @staticmethod
    def get_available_modules():
        """Get all available modules"""
        return PortfolioManager.AVAILABLE_MODULES
    
    @staticmethod
    def validate_personal_info(data):
        """Validate personal info data"""
        required_fields = ["name", "email"]
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Missing required field: {field}"
        return True, "Valid"
    
    @staticmethod
    def validate_experience(items):
        """Validate experience items"""
        required_fields = ["title", "company", "period"]
        for item in items:
            for field in required_fields:
                if field not in item or not item[field]:
                    return False, f"Missing required field in experience: {field}"
        return True, "Valid"
    
    @staticmethod
    def validate_skills(categories):
        """Validate skills categories"""
        for category in categories:
            if "title" not in category or not category["title"]:
                return False, "Missing title in skill category"
            if "items" not in category or not category["items"]:
                return False, "Missing items in skill category"
        return True, "Valid"
    
    @staticmethod
    def validate_projects(items):
        """Validate projects data"""
        for item in items:
            if "title" not in item or not item["title"]:
                return False, "Missing title in project"
        return True, "Valid"
    
    @staticmethod
    def validate_education(items):
        """Validate education items"""
        required_fields = ["title", "period"]
        for item in items:
            for field in required_fields:
                if field not in item or not item[field]:
                    return False, f"Missing required field in education: {field}"
        return True, "Valid"
    
    @staticmethod
    def create_default_portfolio(username, email):
        """Create default portfolio structure"""
        return {
            "personalInfo": {
                "name": username,
                "title": f"Hello! I'm {username}",
                "email": email,
                "profileImage": "",
                "summary": "Welcome to my professional portfolio",
                "about": ""
            },
            "modules": ["personal_info"],
            "experience": {
                "sectionTitle": "Experience",
                "sectionImage": "",
                "items": []
            },
            "skills": {
                "sectionTitle": "Skills",
                "sectionImage": "",
                "categories": []
            },
            "projects": {
                "sectionTitle": "Projects",
                "items": []
            },
            "education": {
                "sectionTitle": "Education",
                "sectionImage": "",
                "items": []
            },
            "certificates": {
                "sectionTitle": "Certifications",
                "items": []
            },
            "socialLinks": [],
            "resume": {
                "sectionTitle": "Download Resume",
                "files": []
            },
            "theme": {
                "colors": {
                    "primary": "#6366f1",
                    "primaryDark": "#4f46e5",
                    "secondary": "#8b5cf6",
                    "accent": "#06b6d4",
                    "textDark": "#1e293b",
                    "textLight": "#64748b",
                    "bgLight": "#f8fafc",
                    "bgWhite": "#ffffff"
                }
            }
        }
