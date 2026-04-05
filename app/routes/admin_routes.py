"""
MODULE 12: ADMIN PANEL
Admin and Officer dashboard for approving/rejecting requests
"""

import logging

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models.models import ServiceRequest, User, AuditLog
from app.security.access_control import check_authentication, check_permission
from app.storage import update_application_status, sync_audit_log

bp = Blueprint('admin', __name__)
logger = logging.getLogger(__name__)


def add_log(action, details, severity='info'):
    logger.info('%s | %s', action, details)
    log = AuditLog(
        user_id=session.get('user_id'),
        action=action,
        details=details,
        ip_address=request.remote_addr,
        severity=severity
    )
    db.session.add(log)
    return log


@bp.route('/admin')
@check_authentication
@check_permission('approve_requests')
def admin_panel():
    """Admin panel - view and manage requests"""
    pending_requests = ServiceRequest.query.filter_by(status='pending').all()
    approved_requests = ServiceRequest.query.filter_by(status='approved').all()
    rejected_requests = ServiceRequest.query.filter_by(status='rejected').all()
    
    for req in pending_requests + approved_requests + rejected_requests:
        req.decrypted_description = req.get_decrypted_payload()
    
    return render_template('admin.html', 
                         pending=pending_requests,
                         approved=approved_requests,
                         rejected=rejected_requests)


@bp.route('/approve-request/<int:req_id>', methods=['POST'])
@check_authentication
@check_permission('approve_requests')
def approve_request(req_id):
    """Approve a service request with digital signature"""
    try:
        request_obj = ServiceRequest.query.get_or_404(req_id)
        
        request_obj.status = 'approved'
        request_obj.approved_by = session['user_id']
        
        request_obj.add_digital_signature(officer_remark='Approved after verification')
        
        db.session.commit()
        update_application_status(request_obj)
        
        log = add_log('APPROVE_APPLICATION', f'Approved application {request_obj.application_number}')
        db.session.commit()
        sync_audit_log(log)
        
        flash(f'Application {request_obj.application_number} approved and digitally signed!', 'success')
    
    except Exception as e:
        db.session.rollback()
        logger.exception('Failed to approve application')
        flash('Error approving application', 'error')
    
    return redirect(url_for('admin.admin_panel'))


@bp.route('/reject-request/<int:req_id>', methods=['POST'])
@check_authentication
@check_permission('approve_requests')
def reject_request(req_id):
    """Reject a service request"""
    try:
        request_obj = ServiceRequest.query.get_or_404(req_id)
        request_obj.status = 'rejected'
        request_obj.officer_remark = 'Rejected after review'
        
        db.session.commit()
        update_application_status(request_obj)
        
        log = add_log('REJECT_APPLICATION', f'Rejected application {request_obj.application_number}', severity='warning')
        db.session.commit()
        sync_audit_log(log)
        
        flash(f'Application {request_obj.application_number} rejected.', 'success')
    
    except Exception as e:
        db.session.rollback()
        logger.exception('Failed to reject application')
        flash('Error rejecting application', 'error')
    
    return redirect(url_for('admin.admin_panel'))


@bp.route('/admin-dashboard')
@check_authentication
@check_permission('manage_users')
def admin_dashboard():
    """Full admin dashboard - manage users"""
    users = User.query.all()
    
    return render_template('admin_dashboard.html', users=users)
