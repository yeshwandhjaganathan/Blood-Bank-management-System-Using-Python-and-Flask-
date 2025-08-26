import os
import logging
from flask import Flask, session, redirect, url_for, request
from werkzeug.middleware.proxy_fix import ProxyFix
from extensions import db

# Initialize Flask app
app = Flask(__name__)

# Set secret key from environment or fallback to default (use a secure key in production!)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")

# Fix proxy headers if behind a reverse proxy (e.g., nginx)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure SQLAlchemy database URI and engine options
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///blood_bank.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Import models and register blueprints inside the application context
with app.app_context():
    import models
    from routes import auth, admin, donor, patient
    
    # Register blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(donor.bp)
    app.register_blueprint(patient.bp)
    
    # Create all tables (if not exist)
    db.create_all()

@app.route('/')
def index():
    if 'user_id' in session:
        user = models.User.query.get(session['user_id'])
        if user:
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'donor':
                return redirect(url_for('donor.dashboard'))
            elif user.role == 'patient':
                return redirect(url_for('patient.dashboard'))
    return redirect(url_for('auth.login'))

@app.context_processor
def inject_user():
    if 'user_id' in session:
        user = models.User.query.get(session['user_id'])
        return {'current_user': user}
    return {'current_user': None}

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

