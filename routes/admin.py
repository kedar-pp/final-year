from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import ParkingSlot, VehicleEntry, User ,db
from datetime import datetime


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.username != 'admin':
        flash("Access denied: Admins only!")
        return redirect(url_for('dashboard'))

    slots = ParkingSlot.query.all()
    users = User.query.all()
    return render_template('admin.html', slots=slots, users=users)

@admin_bp.route('/registered_users')
@login_required
def registered_users():
    if current_user.username != 'admin':
        flash("Access denied: Admins only!")
        return redirect(url_for('dashboard'))
    users = User.query.all()
    return render_template('registered_users.html', users=users)

@admin_bp.route('/release_slot/<int:slot_id>', methods=['POST'])
@login_required
def admin_release_slot(slot_id):
    if current_user.username != 'admin':
        flash('Access denied: Admins only!')
        return redirect(url_for('dashboard'))
    
    slot = ParkingSlot.query.get(slot_id)
    if slot and slot.status == "booked":
        slot.status = "available"
        slot.booked_by = None
        slot.vehicle_id = None # Clear vehicle details
        db.session.commit()
        flash("Slot released successfully!","success")
    else:
        flash("Slot is already available!")
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/reserve_slot/<slot_id>', methods=['POST'])
@login_required
def admin_reserve_slot(slot_id):
    if current_user.username != 'admin':
        flash('Access denied: Admins only!')
        return redirect(url_for('dashboard'))

    slot = ParkingSlot.query.get(slot_id)
    if not slot or slot.status != "available":
        flash("Slot is already booked or does not exist.")
        return redirect(url_for('admin.admin_dashboard'))

    # Get form data
    owner_name = request.form.get('owner_name', '').strip()
    registration_number = request.form.get('registration_number', '').strip()
    vehicle_category = request.form.get('vehicle_category', '').strip()
    owner_contact = request.form.get('owner_contact', '').strip()
    duration = request.form.get('duration')

    # Validate input
    if not all([owner_name, registration_number, vehicle_category, owner_contact, duration]):
        flash("All fields are required!")
        return redirect(url_for('admin.admin_dashboard'))

    try:
        duration = int(duration)
    except ValueError:
        flash("Invalid duration value!")
        return redirect(url_for('admin.admin_dashboard'))

    # Create a new vehicle entry
    vehicle_entry = VehicleEntry(
        user_id=current_user.id,  # Set user_id to admin's ID
        registration_number=registration_number,
        vehicle_category=vehicle_category,
        owner_name=owner_name,
        owner_contact=owner_contact,
        duration=duration
    )
    
    db.session.add(vehicle_entry)
    db.session.commit()

    # Update the slot as booked
    slot.status = "booked"
    slot.booked_by = current_user.id  # Store admin's ID
    slot.vehicle_id = vehicle_entry.id
    db.session.commit()

    flash('Slot reserved successfully!')
    return redirect(url_for('admin.admin_dashboard'))
