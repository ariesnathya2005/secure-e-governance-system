"""
Database Models for Secure Digital Governance System
MODULE 1: Confidentiality & Integrity
"""

from app import db
from datetime import datetime
from app.security.authentication import auth_manager
from app.security.encryption import encrypt_sensitive_data, decrypt_sensitive_data

class User(db.Model):
    """User model - stores citizen, officer, and admin data"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    full_name = db.Column(db.String(120), nullable=True)
    aadhaar_id = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    requests = db.relationship('Application', backref='requestor', lazy=True, foreign_keys='Application.user_id')
    approvals = db.relationship('Application', backref='approver', lazy=True, foreign_keys='Application.approved_by')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = auth_manager.hash_password(password)
    
    def check_password(self, password):
        """Verify password"""
        return auth_manager.verify_password(password, self.password_hash)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Application(db.Model):
    """Application model - stores citizen applications"""
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    application_type = db.Column(db.String(50), nullable=False)
    application_number = db.Column(db.String(40), unique=True, nullable=False)
    purpose = db.Column(db.Text, nullable=False)
    original_payload = db.Column(db.Text, nullable=False)
    encrypted_payload = db.Column(db.Text, nullable=False)
    
    status = db.Column(db.String(20), default='pending')
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    officer_remark = db.Column(db.Text, nullable=True)
    
    digital_signature = db.Column(db.String(255), nullable=True)
    signature_timestamp = db.Column(db.DateTime, nullable=True)
    signature_verification_hash = db.Column(db.String(255), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_payload(self, payload):
        """Store a plain preview and encrypted payload for demonstration"""
        self.original_payload = payload
        self.encrypted_payload = encrypt_sensitive_data(payload)
    
    def get_decrypted_payload(self):
        """Decrypt payload when retrieving"""
        try:
            return decrypt_sensitive_data(self.encrypted_payload)
        except:
            return self.original_payload

    def add_digital_signature(self, officer_remark='Approved by officer'):
        """Add digital signature when approved"""
        signature_data = f"{self.application_number}|{self.user_id}|{self.application_type}|{self.status}|{datetime.utcnow()}"
        self.digital_signature = auth_manager.create_digital_signature(signature_data)
        self.signature_verification_hash = auth_manager.create_digital_signature(self.encrypted_payload)
        self.signature_timestamp = datetime.utcnow()
        self.officer_remark = officer_remark
    
    def __repr__(self):
        return f'<Application {self.id}>'


class AuditLog(db.Model):
    """Audit Log - for security tracking"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    severity = db.Column(db.String(20), default='info')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AuditLog {self.action}>'


# Backward-compatible alias used by older code paths and templates.
ServiceRequest = Application
