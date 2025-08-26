# Blood Bank Management System

## Overview

This is a comprehensive Blood Bank Management System built with Flask that manages blood donations, inventory, and requests. The system serves three types of users: administrators who oversee operations, donors who contribute blood, and patients who request blood. It tracks blood inventory across different blood groups, manages donation records, processes blood requests, and provides reporting capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Web Framework
- **Flask**: Core web framework with SQLAlchemy for database operations
- **Blueprint Architecture**: Modular routing system with separate blueprints for authentication, admin, donor, and patient functionalities
- **Session-based Authentication**: Uses Flask sessions for user authentication and role-based access control

### Database Design
- **SQLAlchemy ORM**: Database abstraction layer with models for User, BloodInventory, Donation, BloodRequest, and DonationCamp
- **Multi-role User System**: Single User model with role field (admin/donor/patient) for different access levels
- **Relational Structure**: Foreign key relationships between donations and donors, requests and patients

### Frontend Architecture
- **Server-side Rendering**: Jinja2 templates with Bootstrap for responsive UI
- **Role-based Templates**: Separate template directories for admin, donor, and patient interfaces
- **Component Reuse**: Base template with role-specific navigation and content blocks

### Security Features
- **Password Hashing**: Werkzeug security for password encryption
- **Role-based Access Control**: Function decorators to restrict access based on user roles
- **Session Management**: Secure session handling with configurable secret keys

### Data Management
- **Blood Inventory Tracking**: Real-time inventory management for all blood groups (A+, A-, B+, B-, AB+, AB-, O+, O-)
- **Donation Records**: Complete donation history with hemoglobin levels and medical notes
- **Request Processing**: Blood request workflow with urgency levels and approval status

### Administrative Features
- **Dashboard Analytics**: Statistical overview of donors, patients, requests, and inventory
- **User Management**: Admin oversight of donor and patient registrations
- **Inventory Control**: Manual inventory updates and automated tracking
- **Reporting System**: Date-range reports for donations and requests by blood group

## External Dependencies

### Core Framework
- **Flask**: Web application framework
- **Flask-SQLAlchemy**: Database ORM integration
- **Werkzeug**: WSGI utilities and security functions

### Database
- **SQLite**: Default database (configurable via DATABASE_URL environment variable)
- **PostgreSQL**: Production database support through configuration

### Frontend Libraries
- **Bootstrap**: CSS framework for responsive design
- **Font Awesome**: Icon library for UI elements
- **JavaScript**: Client-side validation and interactivity

### Development Tools
- **Python 3**: Runtime environment
- **Database Initialization Script**: Automated setup with sample data for testing

### Environment Configuration
- **SESSION_SECRET**: Session encryption key
- **DATABASE_URL**: Database connection string
- **ProxyFix**: WSGI middleware for proper header handling in production