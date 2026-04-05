"""
MODULE 2: SECURITY INVESTIGATIONS - ACCESS CONTROL MATRIX
Implements role-based access control (RBAC)
"""

from functools import wraps
from flask import session, redirect, url_for, abort

ACCESS_MATRIX = {
    'citizen': {
        'view_own_data': True,
        'submit_request': True,
        'view_dashboard': True,
        'approve_requests': False,
        'view_admin': False,
        'manage_users': False
    },
    'officer': {
        'view_own_data': True,
        'submit_request': False,
        'view_dashboard': True,
        'approve_requests': True,
        'view_admin': True,
        'manage_users': False
    },
    'admin': {
        'view_own_data': True,
        'submit_request': False,
        'view_dashboard': True,
        'approve_requests': True,
        'view_admin': True,
        'manage_users': True
    }
}

def check_permission(permission):
    """Decorator to check if user has required permission"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('auth.login'))
            
            user_role = session.get('role', 'citizen')
            
            if user_role not in ACCESS_MATRIX:
                abort(403)
            
            if not ACCESS_MATRIX[user_role].get(permission, False):
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def check_authentication(f):
    """Decorator to check if user is authenticated"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
