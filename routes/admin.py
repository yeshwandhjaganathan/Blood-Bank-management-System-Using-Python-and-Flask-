from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, make_response, send_file
from extensions import db         # <-- changed her
from models import User, BloodInventory, BloodRequest, Donation, DonationCamp
from datetime import datetime, date, timedelta
from sqlalchemy import func
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import pandas as pd
import io
import os

bp = Blueprint('admin', __name__, url_prefix='/admin')

def require_admin():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('auth.login'))
    return None

@bp.route('/dashboard')
def dashboard():
    auth_check = require_admin()
    if auth_check:
        return auth_check
    
    # Get statistics
    total_donors = User.query.filter_by(role='donor', is_active=True).count()
    total_patients = User.query.filter_by(role='patient', is_active=True).count()
    pending_requests = BloodRequest.query.filter_by(status='pending').count()
    total_inventory = db.session.query(func.sum(BloodInventory.units_available)).scalar() or 0
    
    # Recent donations
    recent_donations = db.session.query(Donation).join(User).order_by(Donation.created_at.desc()).limit(5).all()
    
    # Blood group inventory
    inventory = BloodInventory.query.all()
    
    return render_template('admin/dashboard.html', 
                         total_donors=total_donors,
                         total_patients=total_patients,
                         pending_requests=pending_requests,
                         total_inventory=total_inventory,
                         recent_donations=recent_donations,
                         inventory=inventory)

@bp.route('/inventory')
def inventory():
    auth_check = require_admin()
    if auth_check:
        return auth_check
    
    inventory = BloodInventory.query.all()
    return render_template('admin/inventory.html', inventory=inventory)

@bp.route('/inventory/update', methods=['POST'])
def update_inventory():
    auth_check = require_admin()
    if auth_check:
        return auth_check
    
    blood_group = request.form['blood_group']
    units = int(request.form['units'])
    
    inventory_item = BloodInventory.query.filter_by(blood_group=blood_group).first()
    if inventory_item:
        inventory_item.units_available = units
    else:
        inventory_item = BloodInventory()
        inventory_item.blood_group = blood_group
        inventory_item.units_available = units
        db.session.add(inventory_item)
    
    db.session.commit()
    flash(f'Inventory updated for blood group {blood_group}', 'success')
    return redirect(url_for('admin.inventory'))

@bp.route('/requests')
def requests():
    auth_check = require_admin()
    if auth_check:
        return auth_check
    
    requests = BloodRequest.query.order_by(BloodRequest.created_at.desc()).all()
    return render_template('admin/requests.html', requests=requests)

@bp.route('/requests/<int:request_id>/approve', methods=['POST'])
def approve_request(request_id):
    auth_check = require_admin()
    if auth_check:
        return auth_check
    
    blood_request = BloodRequest.query.get_or_404(request_id)
    
    # Check if enough blood is available
    inventory = BloodInventory.query.filter_by(blood_group=blood_request.blood_group).first()
    if inventory and inventory.units_available >= blood_request.units_required:
        blood_request.status = 'approved'
        blood_request.approved_by = session['user_id']
        blood_request.approved_date = datetime.utcnow()
        
        # Update inventory
        inventory.units_available -= blood_request.units_required
        
        db.session.commit()
        flash('Blood request approved successfully', 'success')
    else:
        flash('Insufficient blood units available', 'error')
    
    return redirect(url_for('admin.requests'))

@bp.route('/requests/<int:request_id>/reject', methods=['POST'])
def reject_request(request_id):
    auth_check = require_admin()
    if auth_check:
        return auth_check
    
    blood_request = BloodRequest.query.get_or_404(request_id)
    blood_request.status = 'rejected'
    blood_request.approved_by = session['user_id']
    blood_request.approved_date = datetime.utcnow()
    blood_request.notes = request.form.get('notes', '')
    
    db.session.commit()
    flash('Blood request rejected', 'info')
    return redirect(url_for('admin.requests'))

@bp.route('/donors')
def donors():
    auth_check = require_admin()
    if auth_check:
        return auth_check
    
    donors = User.query.filter_by(role='donor').all()
    return render_template('admin/donors.html', donors=donors)

@bp.route('/patients')
def patients():
    auth_check = require_admin()
    if auth_check:
        return auth_check
    
    patients = User.query.filter_by(role='patient').all()
    return render_template('admin/patients.html', patients=patients)

@bp.route('/reports')
def reports():
    auth_check = require_admin()
    if auth_check:
        return auth_check
    
    # Get date range from query parameters
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    
    # Donations in date range
    donations = db.session.query(
        Donation.blood_group,
        func.sum(Donation.units_donated).label('total_units'),
        func.count(Donation.id).label('total_donations')
    ).filter(
        Donation.donation_date >= start_date,
        Donation.donation_date <= end_date
    ).group_by(Donation.blood_group).all()
    
    # Requests in date range
    requests = db.session.query(
        BloodRequest.blood_group,
        func.sum(BloodRequest.units_required).label('total_units'),
        func.count(BloodRequest.id).label('total_requests')
    ).filter(
        BloodRequest.request_date >= start_date,
        BloodRequest.request_date <= end_date
    ).group_by(BloodRequest.blood_group).all()
    
    # Current inventory
    inventory = BloodInventory.query.all()
    
    return render_template('admin/reports.html', 
                         donations=donations,
                         requests=requests,
                         inventory=inventory,
                         start_date=start_date,
                         end_date=end_date)

@bp.route('/reports/export/pdf')
def export_reports_pdf():
    auth_check = require_admin()
    if auth_check:
        return auth_check
    
    # Get the same data as reports page
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    
    donations = db.session.query(
        Donation.blood_group,
        func.sum(Donation.units_donated).label('total_units'),
        func.count(Donation.id).label('total_donations')
    ).filter(
        Donation.donation_date >= start_date,
        Donation.donation_date <= end_date
    ).group_by(Donation.blood_group).all()
    
    requests = db.session.query(
        BloodRequest.blood_group,
        func.sum(BloodRequest.units_required).label('total_units'),
        func.count(BloodRequest.id).label('total_requests')
    ).filter(
        BloodRequest.request_date >= start_date,
        BloodRequest.request_date <= end_date
    ).group_by(BloodRequest.blood_group).all()
    
    inventory = BloodInventory.query.all()
    
    # Create PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.darkblue,
        alignment=1  # Center alignment
    )
    title = Paragraph(f"Blood Bank Management Report<br/>({start_date} to {end_date})", title_style)
    story.append(title)
    story.append(Spacer(1, 20))
    
    # Current Inventory Section
    inventory_title = Paragraph("Current Blood Inventory", styles['Heading2'])
    story.append(inventory_title)
    story.append(Spacer(1, 10))
    
    inventory_data = [['Blood Group', 'Units Available', 'Status']]
    for item in inventory:
        status = 'Critical' if item.units_available < 10 else 'Low' if item.units_available < 20 else 'Good'
        inventory_data.append([item.blood_group, str(item.units_available), status])
    
    inventory_table = Table(inventory_data, colWidths=[2*inch, 2*inch, 2*inch])
    inventory_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(inventory_table)
    story.append(Spacer(1, 20))
    
    # Donations Section
    donations_title = Paragraph("Donations Summary", styles['Heading2'])
    story.append(donations_title)
    story.append(Spacer(1, 10))
    
    donations_data = [['Blood Group', 'Total Donations', 'Total Units']]
    for donation in donations:
        donations_data.append([donation.blood_group, str(donation.total_donations), str(donation.total_units)])
    
    donations_table = Table(donations_data, colWidths=[2*inch, 2*inch, 2*inch])
    donations_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(donations_table)
    story.append(Spacer(1, 20))
    
    # Requests Section
    requests_title = Paragraph("Blood Requests Summary", styles['Heading2'])
    story.append(requests_title)
    story.append(Spacer(1, 10))
    
    requests_data = [['Blood Group', 'Total Requests', 'Total Units Required']]
    for req in requests:
        requests_data.append([req.blood_group, str(req.total_requests), str(req.total_units)])
    
    requests_table = Table(requests_data, colWidths=[2*inch, 2*inch, 2*inch])
    requests_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightcoral),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(requests_table)
    
    # Add footer
    story.append(Spacer(1, 30))
    footer = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
    story.append(footer)
    
    doc.build(story)
    buffer.seek(0)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=blood_bank_report_{end_date}.pdf'
    
    return response

@bp.route('/reports/export/excel')
def export_reports_excel():
    auth_check = require_admin()
    if auth_check:
        return auth_check
    
    # Get the same data as reports page
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    
    # Create a simple Excel file using pandas
    buffer = io.BytesIO()
    
    # Get inventory data
    inventory = BloodInventory.query.all()
    inventory_data = []
    for item in inventory:
        status = 'Critical' if item.units_available < 10 else 'Low' if item.units_available < 20 else 'Good'
        inventory_data.append({
            'Blood Group': item.blood_group,
            'Units Available': item.units_available,
            'Status': status
        })
    
    # Get donations summary
    donations = db.session.query(
        Donation.blood_group,
        func.sum(Donation.units_donated).label('total_units'),
        func.count(Donation.id).label('total_donations')
    ).filter(
        Donation.donation_date >= start_date,
        Donation.donation_date <= end_date
    ).group_by(Donation.blood_group).all()
    
    donations_data = []
    for donation in donations:
        donations_data.append({
            'Blood Group': donation.blood_group,
            'Total Donations': donation.total_donations,
            'Total Units': donation.total_units
        })
    
    # Get requests summary
    requests = db.session.query(
        BloodRequest.blood_group,
        func.sum(BloodRequest.units_required).label('total_units'),
        func.count(BloodRequest.id).label('total_requests')
    ).filter(
        BloodRequest.request_date >= start_date,
        BloodRequest.request_date <= end_date
    ).group_by(BloodRequest.blood_group).all()
    
    requests_data = []
    for req in requests:
        requests_data.append({
            'Blood Group': req.blood_group,
            'Total Requests': req.total_requests,
            'Total Units Required': req.total_units
        })
    
    # Create DataFrame and export to Excel
    with pd.ExcelWriter(buffer, engine='openpyxl', mode='w') as writer:
        if inventory_data:
            pd.DataFrame(inventory_data).to_excel(writer, sheet_name='Current Inventory', index=False)
        if donations_data:
            pd.DataFrame(donations_data).to_excel(writer, sheet_name='Donations Summary', index=False)
        if requests_data:
            pd.DataFrame(requests_data).to_excel(writer, sheet_name='Requests Summary', index=False)
    
    buffer.seek(0)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = f'attachment; filename=blood_bank_report_{end_date}.xlsx'
    
    return response
