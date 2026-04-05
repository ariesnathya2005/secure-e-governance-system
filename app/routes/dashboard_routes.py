"""
MODULE 8: USER DASHBOARD
Citizen dashboard for viewing and submitting applications
"""

import json
import logging
from uuid import uuid4

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models.models import ServiceRequest, User, AuditLog
from app.security.access_control import check_authentication, check_permission
from app.storage import sync_application, sync_audit_log

bp = Blueprint('dashboard', __name__)
logger = logging.getLogger(__name__)


def log_event(user_id, action, details, severity='info'):
    logger.info('%s | user=%s | %s', action, user_id, details)
    log = AuditLog(
        user_id=user_id,
        action=action,
        details=details,
        ip_address=request.remote_addr,
        severity=severity
    )
    db.session.add(log)
    return log


@bp.route('/dashboard')
@check_authentication
def dashboard():
    """User dashboard - view and submit applications"""
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    requests = ServiceRequest.query.filter_by(user_id=user_id).order_by(ServiceRequest.created_at.desc()).all()
    
    for req in requests:
        req.decrypted_description = req.get_decrypted_payload()
    
    return render_template('dashboard.html', user=user, requests=requests)


@bp.route('/submit-request', methods=['GET', 'POST'])
@check_authentication
@check_permission('submit_request')
def submit_request():
    """Submit a government service application"""
    if request.method == 'POST':
        user_id = session['user_id']
        
        application_type = request.form.get('application_type', '').strip()
        aadhaar_id = request.form.get('aadhaar_id', '').strip()
        address = request.form.get('address', '').strip()
        purpose = request.form.get('purpose', '').strip()
        remarks = request.form.get('remarks', '').strip()
        
        if not application_type or not aadhaar_id or not address or not purpose:
            flash('All fields are required', 'error')
            return redirect(url_for('dashboard.submit_request'))
        
        if len(application_type) > 50 or len(aadhaar_id) > 20 or len(address) > 250 or len(purpose) > 5000:
            flash('Input exceeds maximum length', 'error')
            return redirect(url_for('dashboard.submit_request'))
        
        valid_types = ['birth_certificate', 'income_certificate', 'residence_certificate', 'public_grievance']
        if application_type not in valid_types:
            flash('Invalid request type', 'error')
            return redirect(url_for('dashboard.submit_request'))
        
        if not aadhaar_id.isdigit() or len(aadhaar_id) != 12:
            flash('Aadhaar ID must be a 12-digit number', 'error')
            return redirect(url_for('dashboard.submit_request'))
        
        try:
            application_number = f"APP-{uuid4().hex[:10].upper()}"
            payload = json.dumps({
                'application_number': application_number,
                'application_type': application_type,
                'aadhaar_id': aadhaar_id,
                'address': address,
                'purpose': purpose,
                'remarks': remarks,
                'submitted_by': session.get('username')
            }, ensure_ascii=False)

            new_request = ServiceRequest(
                user_id=user_id,
                application_type=application_type,
                application_number=application_number,
                purpose=purpose
            )
            
            new_request.set_payload(payload)
            
            db.session.add(new_request)
            db.session.commit()
            sync_application(new_request)
            
            log = log_event(user_id, 'SUBMIT_APPLICATION', f'Submitted {application_type} as {application_number}')
            db.session.commit()
            sync_audit_log(log)
            
            flash(f'Application submitted successfully! Application No: {application_number}', 'success')
            return redirect(url_for('dashboard.dashboard'))
        
        except Exception as e:
            db.session.rollback()
            logger.exception('Failed to submit application')
            flash('Error submitting application', 'error')
            return redirect(url_for('dashboard.submit_request'))
    
    return render_template('submit_request.html')


@bp.route('/view-request/<int:req_id>')
@check_authentication
def view_request(req_id):
    """View detailed application"""
    request_obj = ServiceRequest.query.get_or_404(req_id)
    
    if session['role'] != 'admin' and request_obj.user_id != session['user_id']:
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    request_obj.decrypted_description = request_obj.get_decrypted_payload()
    
    return render_template('view_request.html', request=request_obj)
