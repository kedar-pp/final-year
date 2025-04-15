from flask import Flask, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, User, ParkingSlot, VehicleEntry
from routes.auth import auth_bp
from routes.booking import booking_bp
from routes.admin import admin_bp
from flask_login import LoginManager, login_required, current_user
from datetime import datetime




app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(booking_bp, url_prefix='/booking')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def index():
    if current_user.is_authenticated:
        # Redirect logged in users to the landing page or their dashboard.
        return redirect(url_for('landing'))
    else:
        # Show the public home page with animations for non-logged in users.
        return render_template('home.html')


# Landing Page shown right after login for all users.
@app.route('/landing')
@login_required
def landing():
    return render_template('landing.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Example logic: redirect admin users to the admin dashboard
    if current_user.username == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    
    # For regular users, fetch available parking slots and render dashboard template
    db.session.expire_all()
    slots = ParkingSlot.query.all()
    vehicle_entries = VehicleEntry.query.all()
    now = datetime.utcnow()  # For time remaining calculation
    return render_template('dashboard.html', slots=slots, vehicle_entries=vehicle_entries, now=now)

# New Reserve Slot Route
@app.route('/reserve')
@login_required
def reserve():
    # Only show slots that are available.
    available_slots = ParkingSlot.query.filter_by(status='available').all()
    return render_template('reserve.html', slots=available_slots)

@app.route('/profile')
@login_required
def profile():
    # Render a profile page; you can include more details as needed.
    return render_template('profile.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates tables in MySQL
    app.run(debug=True)
