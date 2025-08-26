🩸 Blood Bank Management System – v1.0.0 Release

🔖 Tag: v1.0.0
📅 Release Date: 2025-06-15


---

🚀 Highlights of this Release

This is the initial public release (v1.0.0) of the Blood Bank Management System, a Flask-powered web application designed to simplify blood donation tracking, donor management, and hospital coordination.


---

🛠️ Key Features

🔐 Admin Panel
Manage donors, blood groups, hospitals, and blood requests from a secure admin interface.

🧑‍💉 Donor Registration Module
Register donors with details like name, age, blood group, contact number, and location.

🩸 Blood Group Availability Tracker
Live availability status of each blood group in stock.

🏥 Hospital Request Handling
Hospitals can request specific blood types with quantity and urgency level.

🔍 Search Functionality
Search donors/blood groups using filters such as city, blood group, and availability.

📧 Notification System (Basic Email)
Send email alerts to registered donors when a blood request is raised (extensible with Twilio/SMTP).


---

⚙️ Tech Stack

Python 3.x

Flask 2.x

SQLite3 (default, can be migrated to PostgreSQL/MySQL)

HTML/CSS + Bootstrap for frontend

Optional: Flask-Mail / SendGrid for email notifications



---

✅ Setup Instructions

# Clone repository
git clone https://github.com/yeshwandhjaganathan/blood-bank-management-flask.git

# Navigate into project
cd blood-bank-management-flask

# Install dependencies
pip install -r requirements.txt

# Initialize database
flask db init
flask db migrate
flask db upgrade

# Run application
flask run

Default Admin Login

URL: http://127.0.0.1:5000/admin

Username: admin

Password: admin@123



---

📌 Future Enhancements (Planned for v1.1.0)

📱 SMS Notification Integration (Twilio)
🔎 Advanced Search and Filters
🖥️ User Dashboard for Donors & Hospitals
📄 PDF Report Generation


---

🙏 Contribution & Feedback

Report bugs or feature requests via Issues section. Contributions via Pull Requests are welcome!

