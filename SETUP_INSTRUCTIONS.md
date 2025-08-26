# Blood Bank Management System - Setup Instructions

## Project Overview
A comprehensive Blood Bank Management System built with Flask that manages blood donations, inventory, and requests with role-based access control for administrators, donors, and patients.

## Requirements
- Python 3.11+
- PostgreSQL or SQLite
- Flask and related packages (see package list below)

## Required Python Packages
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Werkzeug==3.0.1
SQLAlchemy==2.0.23
psycopg2-binary==2.9.9
gunicorn==21.2.0
email-validator==2.1.0
```

## Installation Steps

### 1. Clone/Download the Project
```bash
# Download all project files to your local directory
```

### 2. Install Python Dependencies
```bash
# On Replit, packages are automatically managed
# For local setup:
pip install Flask Flask-SQLAlchemy Werkzeug SQLAlchemy psycopg2-binary gunicorn email-validator
```

### 3. Environment Variables
Set the following environment variables:
```bash
# For PostgreSQL (recommended for production)
DATABASE_URL=postgresql://username:password@localhost/blood_bank_db
SESSION_SECRET=your-secret-key-here

# For SQLite (development)
DATABASE_URL=sqlite:///blood_bank.db
SESSION_SECRET=your-secret-key-here
```

### 4. Database Setup

#### Option A: Using the Python initialization script (Recommended)
```bash
python init_db.py
```

#### Option B: Using the SQL file
```bash
# For PostgreSQL
psql -d blood_bank_db -f database_schema.sql

# For SQLite
sqlite3 blood_bank.db < database_schema.sql
```

### 5. Run the Application
```bash
# Development mode
python main.py

# Production mode with Gunicorn
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## Project Structure
```
blood-bank-system/
├── app.py                  # Flask application configuration
├── main.py                 # Application entry point
├── models.py               # Database models
├── init_db.py             # Database initialization script
├── database_schema.sql     # Complete SQL schema and sample data
├── routes/                 # Application routes
│   ├── __init__.py
│   ├── auth.py            # Authentication routes
│   ├── admin.py           # Admin dashboard routes
│   ├── donor.py           # Donor portal routes
│   └── patient.py         # Patient portal routes
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── admin/            # Admin templates
│   │   ├── dashboard.html
│   │   ├── donors.html
│   │   ├── inventory.html
│   │   ├── patients.html
│   │   ├── reports.html
│   │   └── requests.html
│   ├── donor/            # Donor templates
│   │   ├── dashboard.html
│   │   ├── history.html
│   │   └── profile.html
│   └── patient/          # Patient templates
│       ├── dashboard.html
│       ├── request.html
│       └── requests.html
└── static/               # Static files
    └── js/
        └── main.js       # JavaScript functionality
```

## Default Login Credentials

### Administrator
- Username: `admin`
- Password: `admin123`
- Role: Full system access

### Sample Donor Accounts
- Username: `john_doe` / Password: `password123`
- Username: `jane_smith` / Password: `password123`
- Username: `mike_johnson` / Password: `password123`
- Username: `sarah_wilson` / Password: `password123`
- Username: `david_brown` / Password: `password123`

### Sample Patient Accounts
- Username: `patient1` / Password: `password123`
- Username: `patient2` / Password: `password123`
- Username: `patient3` / Password: `password123`

## Features

### Admin Dashboard
- View system statistics and metrics
- Manage blood inventory (add/update stock)
- Approve/reject blood requests
- View donor and patient lists
- Generate reports on donations and requests
- Monitor blood availability by group

### Donor Portal
- Personal dashboard with donation statistics
- View donation history and eligibility status
- Update personal profile information
- View upcoming donation camps
- Record new donations (with eligibility checking)

### Patient Portal
- Personal dashboard with request overview
- Submit new blood requests with urgency levels
- Track request status and approval
- View blood availability
- Update personal profile information

## System Capabilities

### Blood Management
- Real-time inventory tracking for all blood groups (A+, A-, B+, B-, AB+, AB-, O+, O-)
- Automatic inventory updates on donations and approvals
- Blood compatibility information and validation
- Expiration tracking and waste management

### User Management
- Role-based access control (Admin, Donor, Patient)
- Secure password hashing and authentication
- User profile management
- Account activation/deactivation

### Request Workflow
- Blood request submission with medical justification
- Urgency level classification (Urgent, Normal, Low)
- Admin approval workflow
- Inventory availability checking
- Status tracking and notifications

### Reporting and Analytics
- Donation statistics by blood group and time period
- Request fulfillment rates and trends
- Donor retention and engagement metrics
- Inventory status and critical level alerts
- Monthly/quarterly summary reports

## Database Schema

### Core Tables
1. **user** - All system users with role-based access
2. **blood_inventory** - Current blood stock by group
3. **donation** - Donation records and history
4. **blood_request** - Patient blood requests and status
5. **donation_camp** - Upcoming donation events

### Key Relationships
- Users can be donors (one-to-many with donations)
- Users can be patients (one-to-many with blood requests)
- Blood requests reference both patient and approving admin
- Inventory tracks current stock levels by blood group

## Security Features
- Password hashing using Werkzeug security
- Session-based authentication
- Role-based route protection
- CSRF protection through Flask's built-in security
- Input validation and sanitization

## API Endpoints

### Authentication
- `POST /login` - User authentication
- `POST /register` - New user registration
- `GET /logout` - User logout

### Admin Routes (requires admin role)
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/inventory` - Blood inventory management
- `POST /admin/inventory/update` - Update inventory levels
- `GET /admin/requests` - View all blood requests
- `POST /admin/requests/<id>/approve` - Approve blood request
- `POST /admin/requests/<id>/reject` - Reject blood request
- `GET /admin/donors` - View all donors
- `GET /admin/patients` - View all patients
- `GET /admin/reports` - Generate reports

### Donor Routes (requires donor role)
- `GET /donor/dashboard` - Donor dashboard
- `GET /donor/profile` - View/edit donor profile
- `POST /donor/profile` - Update donor profile
- `GET /donor/history` - View donation history
- `POST /donor/donate` - Record new donation

### Patient Routes (requires patient role)
- `GET /patient/dashboard` - Patient dashboard
- `GET /patient/request` - Blood request form
- `POST /patient/request` - Submit blood request
- `GET /patient/requests` - View request history
- `GET /patient/profile` - View/edit patient profile
- `POST /patient/profile` - Update patient profile

## Troubleshooting

### Common Issues
1. **Database connection errors**: Check DATABASE_URL environment variable
2. **Import errors**: Ensure all required packages are installed
3. **Session errors**: Verify SESSION_SECRET is set
4. **Permission errors**: Check user roles and authentication

### Development Tips
- Use `python init_db.py` to reset database with fresh sample data
- Check application logs for detailed error messages
- Verify all environment variables are properly set
- Test with different user roles to ensure proper access control

## Deployment Notes

### For Production
1. Use PostgreSQL instead of SQLite
2. Set strong SESSION_SECRET value
3. Enable HTTPS/SSL
4. Use proper environment variable management
5. Set up regular database backups
6. Configure proper logging and monitoring
7. Use Gunicorn with multiple workers for better performance

### Environment Variables for Production
```bash
DATABASE_URL=postgresql://user:password@host:port/database
SESSION_SECRET=your-very-secure-secret-key
FLASK_ENV=production
```

## Support and Maintenance

### Regular Tasks
- Monitor blood inventory levels
- Review and approve blood requests
- Update donation camp information
- Generate periodic reports
- Backup database regularly

### System Monitoring
- Check application logs for errors
- Monitor database performance
- Track user registration and activity
- Review security logs for suspicious activity

This system provides a complete solution for blood bank management with proper security, user experience, and data integrity features.