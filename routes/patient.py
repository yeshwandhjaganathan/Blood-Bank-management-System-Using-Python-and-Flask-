from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db         # <-- changed her
from models import User, BloodRequest, BloodInventory
from datetime import datetime, date

bp = Blueprint('patient', __name__, url_prefix='/patient')

def require_patient():
    if 'user_id' not in session or session.get('user_role') != 'patient':
        flash('Access denied. Patient privileges required.', 'error')
        return redirect(url_for('auth.login'))
    return None

@bp.route('/dashboard')
def dashboard():
    auth_check = require_patient()
    if auth_check:
        return auth_check
    
    user = User.query.get(session['user_id'])
    
    # Get request statistics
    total_requests = BloodRequest.query.filter_by(patient_id=user.id).count()
    pending_requests = BloodRequest.query.filter_by(patient_id=user.id, status='pending').count()
    approved_requests = BloodRequest.query.filter_by(patient_id=user.id, status='approved').count()
    
    # Get recent requests
    recent_requests = BloodRequest.query.filter_by(patient_id=user.id).order_by(BloodRequest.created_at.desc()).limit(5).all()
    
    # Get blood availability
    inventory = BloodInventory.query.all()
    
    return render_template('patient/dashboard.html',
                         user=user,
                         total_requests=total_requests,
                         pending_requests=pending_requests,
                         approved_requests=approved_requests,
                         recent_requests=recent_requests,
                         inventory=inventory)

@bp.route('/request', methods=['GET', 'POST'])
def request_blood():
    auth_check = require_patient()
    if auth_check:
        return auth_check
    
    if request.method == 'POST':
        blood_group = request.form['blood_group']
        units_required = int(request.form['units_required'])
        urgency = request.form['urgency']
        reason = request.form['reason']
        required_by_str = request.form['required_by']
        
        required_by = datetime.strptime(required_by_str, '%Y-%m-%d').date() if required_by_str else None
        
        # Create blood request
        blood_request = BloodRequest(
            patient_id=session['user_id'],
            blood_group=blood_group,
            units_required=units_required,
            urgency=urgency,
            reason=reason,
            request_date=date.today(),
            required_by=required_by
        )
        
        db.session.add(blood_request)
        db.session.commit()
        
        flash('Blood request submitted successfully', 'success')
        return redirect(url_for('patient.requests'))
    
    # Get available blood groups from inventory
    inventory = BloodInventory.query.filter(BloodInventory.units_available > 0).all()
    
    return render_template('patient/request.html', inventory=inventory)

@bp.route('/requests')
def requests():
    auth_check = require_patient()
    if auth_check:
        return auth_check
    
    user = User.query.get(session['user_id'])
    requests = BloodRequest.query.filter_by(patient_id=user.id).order_by(BloodRequest.created_at.desc()).all()
    
    return render_template('patient/requests.html', requests=requests)

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    auth_check = require_patient()
    if auth_check:
        return auth_check
    
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        user.full_name = request.form['full_name']
        user.email = request.form['email']
        user.phone = request.form['phone']
        user.address = request.form['address']
        user.blood_group = request.form['blood_group']
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('patient.profile'))
    
    return render_template('patient/profile.html', user=user)
