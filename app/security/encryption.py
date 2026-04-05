"""
MODULE 3: ENCRYPTION & KEY MANAGEMENT
Implements AES encryption for data protection
"""

from cryptography.fernet import Fernet
import json

class EncryptionManager:
    """
    Handles AES encryption/decryption of sensitive data
    Ensures CONFIDENTIALITY (CIA Triad - Module 1)
    """
    
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
    
    def encrypt(self, data):
        """Encrypt data using Fernet (symmetric encryption based on AES)"""
        if isinstance(data, dict):
            data = json.dumps(data)
        if isinstance(data, str):
            data = data.encode()
        
        encrypted = self.cipher.encrypt(data)
        return encrypted.decode()
    
    def decrypt(self, encrypted_data):
        """Decrypt data"""
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
        
        decrypted = self.cipher.decrypt(encrypted_data)
        return decrypted.decode()
    
    def get_key(self):
        """Get encryption key (for demonstration)"""
        return self.key.decode()


encryption_manager = EncryptionManager()

def encrypt_sensitive_data(data):
    """Utility function to encrypt data"""
    return encryption_manager.encrypt(data)

def decrypt_sensitive_data(encrypted_data):
    """Utility function to decrypt data"""
    return encryption_manager.decrypt(encrypted_data)
