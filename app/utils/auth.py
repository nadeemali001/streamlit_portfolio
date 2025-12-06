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

    def _user_file(self, username):
        """Return Path for the per-user JSON file: {username}_data.json"""
        safe_name = str(username)
        return self.data_dir / f"{safe_name}_data.json"

    def _load_user_file_into_users(self, username):
        """If per-user file exists, load its portfolio_config into self.users entry.

        This keeps per-user files as the single source of truth for portfolio data while
        keeping credentials in users.json.
        """
        if not self.user_exists(username):
            return
        user_file = self._user_file(username)
        if user_file.exists():
            try:
                with open(user_file, 'r') as f:
                    data = json.load(f)
                # Per-user file may contain the full user record or just portfolio_config
                if isinstance(data, dict):
                    if 'portfolio_config' in data:
                        self.users[username]['portfolio_config'] = data.get('portfolio_config')
                    else:
                        # assume entire file is the portfolio_config
                        self.users[username]['portfolio_config'] = data
            except Exception:
                # ignore per-user file load errors; keep users.json data
                pass
    
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
        # Also write per-user data file for easier export/import and separate storage
        try:
            user_file = self._user_file(username)
            with open(user_file, 'w') as f:
                json.dump(self.users[username].get('portfolio_config', {}), f, indent=2)
        except Exception:
            # non-fatal
            pass
        return True, "User registered successfully"
    
    def authenticate(self, username, password):
        """Authenticate user"""
        if not self.user_exists(username):
            return False, "Username not found"
        
        if self.users[username]["password"] != self.hash_password(password):
            return False, "Incorrect password"
        
        # After authentication, attempt to refresh portfolio_config from per-user file
        try:
            self._load_user_file_into_users(username)
        except Exception:
            pass

        return True, "Authentication successful"
    
    def get_user_portfolio(self, username):
        """Get user's portfolio configuration"""
        if not self.user_exists(username):
            return None
        # Prefer per-user file as source of truth if present
        self._load_user_file_into_users(username)
        return self.users[username].get("portfolio_config", {})
    
    def update_user_portfolio(self, username, portfolio_config):
        """Update user's portfolio configuration"""
        if self.user_exists(username):
            self.users[username]["portfolio_config"] = portfolio_config
            # Save into central users.json and also into per-user file
            try:
                self._save_users()
            except Exception:
                pass

            try:
                user_file = self._user_file(username)
                with open(user_file, 'w') as f:
                    json.dump(portfolio_config, f, indent=2)
            except Exception:
                pass

            return True
        return False
        return False
    
    def get_user_info(self, username):
        """Get user information (without password)"""
        if not self.user_exists(username):
            return None
        user = self.users[username].copy()
        del user["password"]
        return user
