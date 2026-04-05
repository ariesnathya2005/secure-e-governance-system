"""
MODULE 4: DIGITAL SIGNATURE & AUTHENTICATION
Implements authentication and OTP verification
"""

import secrets
import bcrypt
from datetime import datetime, timedelta

class AuthenticationManager:
    """Handles user authentication with OTP support"""
    
    def __init__(self):
        self.otp_storage = {}
    
    def hash_password(self, password):
        """Hash password using bcrypt"""
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
        return hashed.decode()
    
    def verify_password(self, password, hashed):
        """Verify password against hash"""
        if not hashed:
            return False
        return bcrypt.checkpw(password.encode(), hashed.encode())
    
    def generate_otp(self, user_id, length=6):
        """Generate One-Time Password (OTP)"""
        otp = ''.join([str(secrets.randbelow(10)) for _ in range(length)])
        self.otp_storage[user_id] = {
            'otp': otp,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(minutes=5)
        }
        return otp
    
    def verify_otp(self, user_id, otp):
        """Verify OTP"""
        if user_id not in self.otp_storage:
            return False
        
        stored = self.otp_storage[user_id]
        
        if datetime.now() > stored['expires_at']:
            del self.otp_storage[user_id]
            return False
        
        if stored['otp'] == otp:
            del self.otp_storage[user_id]
            return True
        
        return False
    
    def create_digital_signature(self, data):
        """Create a digital signature using a strong hash"""
        return bcrypt.hashpw(data.encode(), bcrypt.gensalt(rounds=10)).decode()
    
    def verify_digital_signature(self, data, signature):
        """Verify digital signature"""
        return bcrypt.checkpw(data.encode(), signature.encode())


auth_manager = AuthenticationManager()
