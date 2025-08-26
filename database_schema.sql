-- Blood Bank Management System Database Schema
-- Complete SQL file for database creation and sample data

-- Create database (PostgreSQL/SQLite compatible)
-- For PostgreSQL: CREATE DATABASE blood_bank_db;
-- For SQLite: Database file will be created automatically

-- User table for all system users (admin, donor, patient)
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(20) NOT NULL, -- 'admin', 'donor', 'patient'
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    blood_group VARCHAR(5), -- 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'
    date_of_birth DATE,
    gender VARCHAR(10),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Blood inventory table
CREATE TABLE IF NOT EXISTS blood_inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    blood_group VARCHAR(5) NOT NULL,
    units_available INTEGER DEFAULT 0,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Donation records table
CREATE TABLE IF NOT EXISTS donation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_id INTEGER NOT NULL,
    donation_date DATE NOT NULL,
    units_donated INTEGER DEFAULT 1,
    blood_group VARCHAR(5) NOT NULL,
    status VARCHAR(20) DEFAULT 'completed', -- 'completed', 'cancelled'
    hemoglobin_level REAL,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (donor_id) REFERENCES user(id)
);

-- Blood request table
CREATE TABLE IF NOT EXISTS blood_request (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    blood_group VARCHAR(5) NOT NULL,
    units_required INTEGER NOT NULL,
    urgency VARCHAR(20) DEFAULT 'normal', -- 'urgent', 'normal', 'low'
    reason TEXT,
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'approved', 'rejected', 'fulfilled'
    request_date DATE NOT NULL,
    required_by DATE,
    approved_by INTEGER,
    approved_date DATETIME,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES user(id),
    FOREIGN KEY (approved_by) REFERENCES user(id)
);

-- Donation camp table
CREATE TABLE IF NOT EXISTS donation_camp (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(200) NOT NULL,
    camp_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    organizer VARCHAR(100),
    contact_phone VARCHAR(20),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_role ON user(role);
CREATE INDEX IF NOT EXISTS idx_user_blood_group ON user(blood_group);
CREATE INDEX IF NOT EXISTS idx_donation_donor_id ON donation(donor_id);
CREATE INDEX IF NOT EXISTS idx_donation_date ON donation(donation_date);
CREATE INDEX IF NOT EXISTS idx_blood_request_patient_id ON blood_request(patient_id);
CREATE INDEX IF NOT EXISTS idx_blood_request_status ON blood_request(status);
CREATE INDEX IF NOT EXISTS idx_blood_request_urgency ON blood_request(urgency);
CREATE INDEX IF NOT EXISTS idx_blood_inventory_group ON blood_inventory(blood_group);
CREATE INDEX IF NOT EXISTS idx_donation_camp_date ON donation_camp(camp_date);

-- Insert sample data

-- Insert admin user
INSERT INTO user (username, email, password_hash, role, full_name, phone, address, blood_group, date_of_birth, gender) VALUES
('admin', 'admin@bloodbank.com', 'scrypt:32768:8:1$2b2LoQPSxz5aGRaT$46d1c78c1c52e1c8a9e8b9f0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f', 'admin', 'System Administrator', '123-456-7890', 'Blood Bank Headquarters', 'O+', '1980-01-01', 'male');

-- Insert sample donors
INSERT INTO user (username, email, password_hash, role, full_name, phone, address, blood_group, date_of_birth, gender) VALUES
('john_doe', 'john@email.com', 'scrypt:32768:8:1$2b2LoQPSxz5aGRaT$46d1c78c1c52e1c8a9e8b9f0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f', 'donor', 'John Doe', '555-0101', '123 Main St, City, State', 'O+', '1990-05-15', 'male'),
('jane_smith', 'jane@email.com', 'scrypt:32768:8:1$2b2LoQPSxz5aGRaT$46d1c78c1c52e1c8a9e8b9f0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f', 'donor', 'Jane Smith', '555-0102', '456 Oak Ave, City, State', 'A+', '1985-08-22', 'female'),
('mike_johnson', 'mike@email.com', 'scrypt:32768:8:1$2b2LoQPSxz5aGRaT$46d1c78c1c52e1c8a9e8b9f0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f', 'donor', 'Mike Johnson', '555-0103', '789 Pine Rd, City, State', 'B+', '1992-03-10', 'male'),
('sarah_wilson', 'sarah@email.com', 'scrypt:32768:8:1$2b2LoQPSxz5aGRaT$46d1c78c1c52e1c8a9e8b9f0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f', 'donor', 'Sarah Wilson', '555-0104', '321 Elm St, City, State', 'AB+', '1988-11-30', 'female'),
('david_brown', 'david@email.com', 'scrypt:32768:8:1$2b2LoQPSxz5aGRaT$46d1c78c1c52e1c8a9e8b9f0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f', 'donor', 'David Brown', '555-0105', '654 Maple Dr, City, State', 'O-', '1995-07-08', 'male');

-- Insert sample patients
INSERT INTO user (username, email, password_hash, role, full_name, phone, address, blood_group, date_of_birth, gender) VALUES
('patient1', 'patient1@email.com', 'scrypt:32768:8:1$2b2LoQPSxz5aGRaT$46d1c78c1c52e1c8a9e8b9f0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f', 'patient', 'Alice Cooper', '555-0201', '111 First St, City, State', 'A+', '1970-04-12', 'female'),
('patient2', 'patient2@email.com', 'scrypt:32768:8:1$2b2LoQPSxz5aGRaT$46d1c78c1c52e1c8a9e8b9f0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f', 'patient', 'Bob Miller', '555-0202', '222 Second Ave, City, State', 'B+', '1965-09-25', 'male'),
('patient3', 'patient3@email.com', 'scrypt:32768:8:1$2b2LoQPSxz5aGRaT$46d1c78c1c52e1c8a9e8b9f0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f', 'patient', 'Carol Davis', '555-0203', '333 Third Blvd, City, State', 'O+', '1975-12-03', 'female');

-- Insert blood inventory
INSERT INTO blood_inventory (blood_group, units_available) VALUES
('A+', 25), ('A-', 15), ('B+', 20), ('B-', 12),
('AB+', 8), ('AB-', 5), ('O+', 30), ('O-', 18);

-- Insert sample donations
INSERT INTO donation (donor_id, donation_date, units_donated, blood_group, hemoglobin_level, notes) VALUES
(2, '2024-07-15', 1, 'O+', 13.2, 'Regular donation - good health'),
(3, '2024-07-18', 1, 'A+', 12.8, 'First time donor'),
(4, '2024-07-20', 1, 'B+', 13.5, 'Regular donor'),
(5, '2024-07-22', 1, 'AB+', 13.0, 'Quarterly donation'),
(6, '2024-07-25', 1, 'O-', 12.9, 'Universal donor'),
(2, '2024-06-10', 1, 'O+', 13.1, 'Previous donation'),
(3, '2024-06-15', 1, 'A+', 13.3, 'Regular check-up passed'),
(4, '2024-06-20', 1, 'B+', 13.4, 'Healthy donor'),
(5, '2024-06-25', 1, 'AB+', 12.7, 'Monthly donation'),
(6, '2024-06-30', 1, 'O-', 13.6, 'Emergency response donor');

-- Insert sample blood requests
INSERT INTO blood_request (patient_id, blood_group, units_required, urgency, reason, request_date, required_by, status) VALUES
(7, 'A+', 2, 'urgent', 'Surgery scheduled for heart procedure', '2024-08-15', '2024-08-18', 'pending'),
(8, 'B+', 1, 'normal', 'Planned surgical procedure', '2024-08-14', '2024-08-20', 'approved'),
(9, 'O+', 3, 'urgent', 'Emergency surgery after accident', '2024-08-13', '2024-08-16', 'pending'),
(7, 'A+', 1, 'low', 'Routine blood transfusion', '2024-08-10', '2024-08-25', 'approved'),
(8, 'B+', 2, 'normal', 'Cancer treatment support', '2024-08-12', '2024-08-22', 'pending'),
(9, 'O+', 1, 'normal', 'Anemia treatment', '2024-08-11', '2024-08-20', 'rejected'),
(7, 'A+', 2, 'urgent', 'Trauma case blood loss', '2024-08-09', '2024-08-12', 'approved'),
(8, 'B+', 1, 'low', 'Elective surgery preparation', '2024-08-08', '2024-08-30', 'pending');

-- Insert sample donation camps
INSERT INTO donation_camp (name, location, camp_date, start_time, end_time, organizer, contact_phone, description) VALUES
('City Hospital Blood Drive', 'City Hospital, Main Building', '2024-08-25', '09:00', '17:00', 'City Hospital', '555-1000', 'Annual blood drive to support local hospital needs'),
('University Blood Donation Camp', 'University Campus, Student Center', '2024-09-01', '10:00', '16:00', 'University Health Services', '555-2000', 'Blood donation camp for students and faculty'),
('Community Center Blood Drive', 'Downtown Community Center', '2024-09-08', '08:00', '18:00', 'Red Cross', '555-3000', 'Community blood drive open to all residents'),
('Corporate Blood Drive', 'Tech Park Conference Center', '2024-09-15', '09:00', '15:00', 'Corporate Wellness', '555-4000', 'Blood donation drive for corporate employees'),
('Mall Blood Drive', 'Central Shopping Mall', '2024-09-22', '10:00', '20:00', 'Health Alliance', '555-5000', 'Public blood drive at shopping center');

-- Useful queries for the Blood Bank Management System

-- 1. Get current blood inventory status
SELECT 
    blood_group,
    units_available,
    CASE 
        WHEN units_available < 10 THEN 'Critical'
        WHEN units_available < 20 THEN 'Low'
        ELSE 'Good'
    END as stock_status
FROM blood_inventory 
ORDER BY units_available ASC;

-- 2. Get pending blood requests with patient details
SELECT 
    br.id,
    u.full_name as patient_name,
    u.phone,
    br.blood_group,
    br.units_required,
    br.urgency,
    br.request_date,
    br.required_by,
    br.reason
FROM blood_request br
JOIN user u ON br.patient_id = u.id
WHERE br.status = 'pending'
ORDER BY 
    CASE br.urgency 
        WHEN 'urgent' THEN 1 
        WHEN 'normal' THEN 2 
        WHEN 'low' THEN 3 
    END,
    br.request_date ASC;

-- 3. Get donor statistics and eligibility
SELECT 
    u.id,
    u.full_name,
    u.blood_group,
    COUNT(d.id) as total_donations,
    MAX(d.donation_date) as last_donation_date,
    CASE 
        WHEN MAX(d.donation_date) IS NULL THEN 'Eligible'
        WHEN DATE('now') - MAX(d.donation_date) >= 56 THEN 'Eligible'
        ELSE 'Not Eligible'
    END as eligibility_status
FROM user u
LEFT JOIN donation d ON u.id = d.donor_id
WHERE u.role = 'donor' AND u.is_active = 1
GROUP BY u.id
ORDER BY total_donations DESC;

-- 4. Blood compatibility matrix query
-- Universal donors (O-) and recipients (AB+)
SELECT 
    'Universal Donors (O-)' as category,
    COUNT(*) as count
FROM user 
WHERE role = 'donor' AND blood_group = 'O-' AND is_active = 1
UNION ALL
SELECT 
    'Universal Recipients (AB+)' as category,
    COUNT(*) as count
FROM user 
WHERE role = 'patient' AND blood_group = 'AB+' AND is_active = 1;

-- 5. Monthly donation summary
SELECT 
    strftime('%Y-%m', donation_date) as month,
    blood_group,
    COUNT(*) as donations_count,
    SUM(units_donated) as total_units
FROM donation
WHERE donation_date >= date('now', '-12 months')
GROUP BY month, blood_group
ORDER BY month DESC, blood_group;

-- 6. Upcoming donation camps
SELECT 
    name,
    location,
    camp_date,
    start_time,
    end_time,
    organizer,
    contact_phone
FROM donation_camp
WHERE camp_date >= date('now') AND is_active = 1
ORDER BY camp_date ASC;

-- 7. Emergency blood request alert
SELECT 
    br.id,
    u.full_name as patient_name,
    br.blood_group,
    br.units_required,
    br.request_date,
    br.required_by,
    bi.units_available,
    CASE 
        WHEN bi.units_available >= br.units_required THEN 'Available'
        ELSE 'Insufficient Stock'
    END as availability_status
FROM blood_request br
JOIN user u ON br.patient_id = u.id
LEFT JOIN blood_inventory bi ON br.blood_group = bi.blood_group
WHERE br.urgency = 'urgent' AND br.status = 'pending'
ORDER BY br.request_date ASC;

-- 8. Donor retention analysis
SELECT 
    CASE 
        WHEN COUNT(d.id) = 1 THEN 'First Time'
        WHEN COUNT(d.id) BETWEEN 2 AND 5 THEN 'Regular'
        WHEN COUNT(d.id) > 5 THEN 'Frequent'
    END as donor_category,
    COUNT(DISTINCT u.id) as donor_count,
    AVG(COUNT(d.id)) as avg_donations
FROM user u
LEFT JOIN donation d ON u.id = d.donor_id
WHERE u.role = 'donor' AND u.is_active = 1
GROUP BY donor_category;

-- 9. Blood waste tracking (expired inventory)
-- Note: This would require an expiration_date field in blood_inventory
-- For now, showing theoretical query structure
/*
SELECT 
    blood_group,
    SUM(units_available) as expired_units,
    COUNT(*) as expired_batches
FROM blood_inventory 
WHERE expiration_date < date('now')
GROUP BY blood_group;
*/

-- 10. System usage statistics
SELECT 
    'Total Users' as metric, COUNT(*) as value FROM user WHERE is_active = 1
UNION ALL
SELECT 
    'Active Donors' as metric, COUNT(*) as value FROM user WHERE role = 'donor' AND is_active = 1
UNION ALL
SELECT 
    'Active Patients' as metric, COUNT(*) as value FROM user WHERE role = 'patient' AND is_active = 1
UNION ALL
SELECT 
    'Total Donations' as metric, COUNT(*) as value FROM donation
UNION ALL
SELECT 
    'Pending Requests' as metric, COUNT(*) as value FROM blood_request WHERE status = 'pending'
UNION ALL
SELECT 
    'Total Blood Units' as metric, SUM(units_available) as value FROM blood_inventory;