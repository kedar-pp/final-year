from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    

class ParkingSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot_number = db.Column(db.String(10), unique=True, nullable=False)
    status = db.Column(db.String(10), nullable=False, default="available")  # 'available' or 'booked'
    booked_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle_entry.id'), nullable=True)  # Link to vehicle details

class VehicleEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    registration_number = db.Column(db.String(20), unique=True, nullable=False)
    vehicle_category = db.Column(db.String(20), nullable=False)  # 2-wheeler, 3-wheeler, 4-wheeler
    owner_name = db.Column(db.String(100), nullable=False)
    owner_contact = db.Column(db.String(15), nullable=False)
    entry_time = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Integer, nullable=False)  # Parking duration in hours
    exit_time = db.Column(db.DateTime, nullable=True)
    fee_paid = db.Column(db.Float, default=0.0)

    def exit_vehicle(self, fee):
        self.exit_time = datetime.utcnow()
        self.fee_paid = fee
        db.session.commit()
