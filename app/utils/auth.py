"""
Authentication module for user login/signup
"""
import json
import os
import hashlib
from datetime import datetime
from pathlib import Path


class AuthManager:
    """Manages user authentication and session"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.users_file = self.data_dir / "users.json"
        self._load_users()
    
    def _load_users(self):
        """Load users from JSON file"""
        if self.users_file.exists():
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
    
    def _save_users(self):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def user_exists(self, username):
        """Check if user exists"""
        return username in self.users
    
    def register_user(self, username, password, email):
        """Register a new user"""
        if self.user_exists(username):
            return False, "Username already exists"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        self.users[username] = {
            "password": self.hash_password(password),
            "email": email,
            "created_at": datetime.now().isoformat(),
            "portfolio_config": {
                "personalInfo": {
                    "name": username,
                    "title": f"Hello! I'm {username}",
                    "email": email,
                    "summary": "Welcome to my portfolio",
                    "about": ""
                },
                "modules": ["personal_info"],
                "experience": {"items": []},
                "skills": {"categories": []},
                "projects": {"items": []},
                "education": {"items": []},
                "certificates": {"items": []},
                "theme": {
                    "colors": {
                        "primary": "#6366f1",
                        "secondary": "#8b5cf6",
                        "accent": "#06b6d4"
                    }
                }
            }
        }
        self._save_users()
        return True, "User registered successfully"
    
    def authenticate(self, username, password):
        """Authenticate user"""
        if not self.user_exists(username):
            return False, "Username not found"
        
        if self.users[username]["password"] != self.hash_password(password):
            return False, "Incorrect password"
        
        return True, "Authentication successful"
    
    def get_user_portfolio(self, username):
        """Get user's portfolio configuration"""
        if not self.user_exists(username):
            return None
        return self.users[username].get("portfolio_config", {})
    
    def update_user_portfolio(self, username, portfolio_config):
        """Update user's portfolio configuration"""
        if self.user_exists(username):
            self.users[username]["portfolio_config"] = portfolio_config
            self._save_users()
            return True
        return False
    
    def get_user_info(self, username):
        """Get user information (without password)"""
        if not self.user_exists(username):
            return None
        user = self.users[username].copy()
        del user["password"]
        return user
