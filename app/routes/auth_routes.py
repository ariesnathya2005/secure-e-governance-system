"""
MODULE 4: AUTHENTICATION & MODULE 6: WEB SECURITY
Login and Authentication Routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models.models import User, AuditLog
from app.storage import sync_user, sync_audit_log
from markupsafe import escape

bp = Blueprint('auth', __name__)

SAMPLE_USERS = [
    {
        'username': 'citizen1',
        'password': 'citizen123',
        'email': 'citizen@example.com',
        'role': 'citizen',
        'full_name': 'Anita Sharma',
        'aadhaar_id': '123456789012',
        'address': '12 Civil Lines, Jaipur'
    },
    {
        'username': 'officer1',
        'password': 'officer123',
        'email': 'officer@example.com',
        'role': 'officer',
        'full_name': 'Rahul Mehta',
        'aadhaar_id': '234567890123',
        'address': 'District Office, Jaipur'
    },
    {
        'username': 'admin1',
        'password': 'admin123',
        'email': 'admin@example.com',
        'role': 'admin',
        'full_name': 'System Admin',
        'aadhaar_id': '345678901234',
        'address': 'State e-Governance Center'
    }
]

@bp.route('/')
def index():
    """Home page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login endpoint"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return redirect(url_for('auth.login'))
        
        if len(username) > 80 or len(password) > 255:
            flash('Invalid input length', 'error')
            return redirect(url_for('auth.login'))
        
        try:
            user = User.query.filter_by(username=escape(username)).first()
            
            if user and user.check_password(password):
                session.clear()
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                
                log = AuditLog(user_id=user.id, action='LOGIN', 
                             details=f'User {username} logged in',
                             ip_address=request.remote_addr)
                db.session.add(log)
                db.session.commit()
                sync_audit_log(log)
                
                flash(f'Welcome {username}!', 'success')
                return redirect(url_for('dashboard.dashboard'))
            else:
                flash('Invalid username or password', 'error')
                log = AuditLog(action='LOGIN_FAILED', 
                             details=f'Failed login attempt for {username}',
                             ip_address=request.remote_addr)
                db.session.add(log)
                db.session.commit()
                sync_audit_log(log)
        
        except Exception as e:
            flash('An error occurred during login', 'error')
            print(f"Login error: {e}")
    
    return render_template('login.html')


@bp.route('/logout')
def logout():
    """Logout endpoint"""
    if 'user_id' in session:
        user_id = session['user_id']
        log = AuditLog(user_id=user_id, action='LOGOUT',
                     details=f'User logged out',
                     ip_address=request.remote_addr)
        db.session.add(log)
        db.session.commit()
        sync_audit_log(log)
    
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))


@bp.route('/setup')
def setup():
    """Setup endpoint - Create sample users"""
    try:
        if User.query.first():
            return "Database already initialized!", 200
        
        for user_data in SAMPLE_USERS:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                role=user_data['role'],
                full_name=user_data['full_name'],
                aadhaar_id=user_data['aadhaar_id'],
                address=user_data['address']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
        
        db.session.commit()

        for user in User.query.all():
            sync_user(user)

        return "Sample users created! Login with any sample user.", 200
    
    except Exception as e:
        db.session.rollback()
        return f"Error: {str(e)}", 500
