#!/usr/bin/env python3
"""
Initialize database with sample data for Blood Bank Management System
Run this script to populate the database with test data
"""

import os
import sys
from datetime import datetime, date, timedelta
from app import app, db
from models import User, BloodInventory, Donation, BloodRequest, DonationCamp

def init_database():
    """Initialize database with sample data"""
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        print("Creating sample users...")
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@bloodbank.com',
            role='admin',
            full_name='System Administrator',
            phone='123-456-7890',
            address='Blood Bank Headquarters',
            blood_group='O+',
            date_of_birth=date(1980, 1, 1),
            gender='male'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create sample donors
        donors_data = [
            {
                'username': 'john_doe',
                'email': 'john@email.com',
                'full_name': 'John Doe',
                'phone': '555-0101',
                'blood_group': 'O+',
                'date_of_birth': date(1990, 5, 15),
                'gender': 'male',
                'address': '123 Main St, City, State'
            },
            {
                'username': 'jane_smith',
                'email': 'jane@email.com',
                'full_name': 'Jane Smith',
                'phone': '555-0102',
                'blood_group': 'A+',
                'date_of_birth': date(1985, 8, 22),
                'gender': 'female',
                'address': '456 Oak Ave, City, State'
            },
            {
                'username': 'mike_johnson',
                'email': 'mike@email.com',
                'full_name': 'Mike Johnson',
                'phone': '555-0103',
                'blood_group': 'B+',
                'date_of_birth': date(1992, 3, 10),
                'gender': 'male',
                'address': '789 Pine Rd, City, State'
            },
            {
                'username': 'sarah_wilson',
                'email': 'sarah@email.com',
                'full_name': 'Sarah Wilson',
                'phone': '555-0104',
                'blood_group': 'AB+',
                'date_of_birth': date(1988, 11, 30),
                'gender': 'female',
                'address': '321 Elm St, City, State'
            },
            {
                'username': 'david_brown',
                'email': 'david@email.com',
                'full_name': 'David Brown',
                'phone': '555-0105',
                'blood_group': 'O-',
                'date_of_birth': date(1995, 7, 8),
                'gender': 'male',
                'address': '654 Maple Dr, City, State'
            }
        ]
        
        for donor_data in donors_data:
            donor = User(
                username=donor_data['username'],
                email=donor_data['email'],
                role='donor',
                full_name=donor_data['full_name'],
                phone=donor_data['phone'],
                address=donor_data['address'],
                blood_group=donor_data['blood_group'],
                date_of_birth=donor_data['date_of_birth'],
                gender=donor_data['gender']
            )
            donor.set_password('password123')
            db.session.add(donor)
        
        # Create sample patients
        patients_data = [
            {
                'username': 'patient1',
                'email': 'patient1@email.com',
                'full_name': 'Alice Cooper',
                'phone': '555-0201',
                'blood_group': 'A+',
                'date_of_birth': date(1970, 4, 12),
                'gender': 'female',
                'address': '111 First St, City, State'
            },
            {
                'username': 'patient2',
                'email': 'patient2@email.com',
                'full_name': 'Bob Miller',
                'phone': '555-0202',
                'blood_group': 'B+',
                'date_of_birth': date(1965, 9, 25),
                'gender': 'male',
                'address': '222 Second Ave, City, State'
            },
            {
                'username': 'patient3',
                'email': 'patient3@email.com',
                'full_name': 'Carol Davis',
                'phone': '555-0203',
                'blood_group': 'O+',
                'date_of_birth': date(1975, 12, 3),
                'gender': 'female',
                'address': '333 Third Blvd, City, State'
            }
        ]
        
        for patient_data in patients_data:
            patient = User(
                username=patient_data['username'],
                email=patient_data['email'],
                role='patient',
                full_name=patient_data['full_name'],
                phone=patient_data['phone'],
                address=patient_data['address'],
                blood_group=patient_data['blood_group'],
                date_of_birth=patient_data['date_of_birth'],
                gender=patient_data['gender']
            )
            patient.set_password('password123')
            db.session.add(patient)
        
        db.session.commit()
        
        print("Creating blood inventory...")
        
        # Create blood inventory
        blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        initial_units = [25, 15, 20, 12, 8, 5, 30, 18]
        
        for bg, units in zip(blood_groups, initial_units):
            inventory = BloodInventory(
                blood_group=bg,
                units_available=units
            )
            db.session.add(inventory)
        
        db.session.commit()
        
        print("Creating sample donations...")
        
        # Create sample donations
        donors = User.query.filter_by(role='donor').all()
        
        # Create donations for the past 6 months
        for i in range(20):
            donor = donors[i % len(donors)]
            donation_date = date.today() - timedelta(days=i*7 + (i%30))
            
            donation = Donation(
                donor_id=donor.id,
                donation_date=donation_date,
                units_donated=1,
                blood_group=donor.blood_group,
                hemoglobin_level=12.5 + (i % 3) * 0.5,
                notes=f'Donation {i+1} - Regular donation'
            )
            db.session.add(donation)
        
        db.session.commit()
        
        print("Creating sample blood requests...")
        
        # Create sample blood requests
        patients = User.query.filter_by(role='patient').all()
        urgency_levels = ['urgent', 'normal', 'low']
        statuses = ['pending', 'approved', 'rejected']
        
        for i in range(15):
            patient = patients[i % len(patients)]
            request_date = date.today() - timedelta(days=i*3)
            required_by = request_date + timedelta(days=7)
            
            blood_request = BloodRequest(
                patient_id=patient.id,
                blood_group=blood_groups[i % len(blood_groups)],
                units_required=(i % 3) + 1,
                urgency=urgency_levels[i % len(urgency_levels)],
                reason=f'Medical procedure requiring blood transfusion #{i+1}',
                request_date=request_date,
                required_by=required_by,
                status=statuses[i % len(statuses)]
            )
            
            # If approved, set approval details
            if blood_request.status == 'approved':
                blood_request.approved_by = admin.id
                blood_request.approved_date = datetime.utcnow()
            elif blood_request.status == 'rejected':
                blood_request.approved_by = admin.id
                blood_request.approved_date = datetime.utcnow()
                blood_request.notes = 'Insufficient blood available at the time'
            
            db.session.add(blood_request)
        
        db.session.commit()
        
        print("Creating sample donation camps...")
        
        # Create future donation camps
        camps_data = [
            {
                'name': 'City Hospital Blood Drive',
                'location': 'City Hospital, Main Building',
                'camp_date': date.today() + timedelta(days=7),
                'start_time': datetime.strptime('09:00', '%H:%M').time(),
                'end_time': datetime.strptime('17:00', '%H:%M').time(),
                'organizer': 'City Hospital',
                'contact_phone': '555-1000',
                'description': 'Annual blood drive to support local hospital needs'
            },
            {
                'name': 'University Blood Donation Camp',
                'location': 'University Campus, Student Center',
                'camp_date': date.today() + timedelta(days=14),
                'start_time': datetime.strptime('10:00', '%H:%M').time(),
                'end_time': datetime.strptime('16:00', '%H:%M').time(),
                'organizer': 'University Health Services',
                'contact_phone': '555-2000',
                'description': 'Blood donation camp for students and faculty'
            },
            {
                'name': 'Community Center Blood Drive',
                'location': 'Downtown Community Center',
                'camp_date': date.today() + timedelta(days=21),
                'start_time': datetime.strptime('08:00', '%H:%M').time(),
                'end_time': datetime.strptime('18:00', '%H:%M').time(),
                'organizer': 'Red Cross',
                'contact_phone': '555-3000',
                'description': 'Community blood drive open to all residents'
            }
        ]
        
        for camp_data in camps_data:
            camp = DonationCamp(**camp_data)
            db.session.add(camp)
        
        db.session.commit()
        
        print("Database initialized successfully!")
        print("\nSample login credentials:")
        print("Admin: username='admin', password='admin123'")
        print("Donor: username='john_doe', password='password123'")
        print("Patient: username='patient1', password='password123'")
        print("\nOther test users follow the same pattern with password='password123'")

if __name__ == '__main__':
    init_database()
