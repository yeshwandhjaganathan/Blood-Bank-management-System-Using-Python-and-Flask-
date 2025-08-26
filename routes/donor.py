from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db         # <-- changed her
from models import User, Donation, DonationCamp, BloodInventory
from datetime import datetime, date

bp = Blueprint('donor', __name__, url_prefix='/donor')

def require_donor():
    if 'user_id' not in session or session.get('user_role') != 'donor':
        flash('Access denied. Donor privileges required.', 'error')
        return redirect(url_for('auth.login'))
    return None

@bp.route('/dashboard')
def dashboard():
    auth_check = require_donor()
    if auth_check:
        return auth_check
    
    user = User.query.get(session['user_id'])
    
    # Get donation statistics
    total_donations = Donation.query.filter_by(donor_id=user.id).count()
    recent_donations = Donation.query.filter_by(donor_id=user.id).order_by(Donation.donation_date.desc()).limit(3).all()
    
    # Get upcoming camps
    upcoming_camps = DonationCamp.query.filter(
        DonationCamp.camp_date >= date.today(),
        DonationCamp.is_active == True
    ).order_by(DonationCamp.camp_date).limit(3).all()
    
    # Calculate next eligible donation date (56 days after last donation)
    last_donation = Donation.query.filter_by(donor_id=user.id).order_by(Donation.donation_date.desc()).first()
    next_eligible_date = None
    if last_donation:
        from datetime import timedelta
        next_eligible_date = last_donation.donation_date + timedelta(days=56)
    
    return render_template('donor/dashboard.html',
                         user=user,
                         total_donations=total_donations,
                         recent_donations=recent_donations,
                         upcoming_camps=upcoming_camps,
                         next_eligible_date=next_eligible_date,
                         date=date)

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    auth_check = require_donor()
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
        return redirect(url_for('donor.profile'))
    
    return render_template('donor/profile.html', user=user)

@bp.route('/history')
def history():
    auth_check = require_donor()
    if auth_check:
        return auth_check
    
    user = User.query.get(session['user_id'])
    donations = Donation.query.filter_by(donor_id=user.id).order_by(Donation.donation_date.desc()).all()
    
    return render_template('donor/history.html', donations=donations)

@bp.route('/donate', methods=['POST'])
def donate():
    auth_check = require_donor()
    if auth_check:
        return auth_check
    
    user = User.query.get(session['user_id'])
    
    # Check if user is eligible (last donation was at least 56 days ago)
    last_donation = Donation.query.filter_by(donor_id=user.id).order_by(Donation.donation_date.desc()).first()
    if last_donation:
        from datetime import timedelta
        days_since_last = (date.today() - last_donation.donation_date).days
        if days_since_last < 56:
            flash(f'You can donate again in {56 - days_since_last} days', 'error')
            return redirect(url_for('donor.dashboard'))
    
    # Create donation record
    donation = Donation(
        donor_id=user.id,
        donation_date=date.today(),
        units_donated=1,
        blood_group=user.blood_group,
        hemoglobin_level=float(request.form.get('hemoglobin', 12.5)),
        notes=request.form.get('notes', '')
    )
    
    db.session.add(donation)
    
    # Update blood inventory
    inventory = BloodInventory.query.filter_by(blood_group=user.blood_group).first()
    if inventory:
        inventory.units_available += 1
    else:
        inventory = BloodInventory(blood_group=user.blood_group, units_available=1)
        db.session.add(inventory)
    
    db.session.commit()
    flash('Thank you for your donation!', 'success')
    return redirect(url_for('donor.dashboard'))
