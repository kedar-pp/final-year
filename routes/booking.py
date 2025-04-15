from flask import Blueprint, render_template, request, redirect, flash, url_for 
from flask_login import login_required, current_user
from models import db, ParkingSlot, VehicleEntry

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/book_slot/<slot_id>', methods=['POST'])
@login_required
def book_slot(slot_id):
    # slot = ParkingSlot.query.get(slot_id)
    
    # if slot and slot.status == "available":
    #     slot.status = "booked"
    #     slot.booked_by = current_user.id
    #     db.session.commit()
    #     flash('Parking slot reserved successfully!')
    # else:
    #     flash('Slot is not available!')

    # return redirect(url_for('dashboard'))

    slot = ParkingSlot.query.get(slot_id)

    if not slot:
        flash("Invalid slot!", "error")
        return redirect(url_for('dashboard'))

    if slot.status != "available":
        flash("Slot is already booked!", "warning")
        return redirect(url_for('dashboard'))

    # Get form data
    owner_name = request.form.get('owner_name')
    registration_number = request.form.get('registration_number')
    vehicle_category = request.form.get('vehicle_category')
    owner_contact = request.form.get('owner_contact')
    duration = request.form.get('duration', type=int)

    # Ensure required fields are filled
    if not (owner_name and registration_number and vehicle_category and owner_contact and duration):
        flash("All fields are required!", "error")
        return redirect(url_for('dashboard'))

    # Update slot status
    slot.status = "booked"
    slot.booked_by = current_user.id

    # ✅ Create a new VehicleEntry record
    new_entry = VehicleEntry(
        user_id=current_user.id,
        registration_number=registration_number,
        vehicle_category=vehicle_category,
        owner_name=owner_name,
        owner_contact=owner_contact,
        duration=duration
    )

    # Save to database
    db.session.add(new_entry)  # ✅ Add new vehicle entry
    db.session.commit()  # ✅ Commit changes

    flash("Parking slot reserved successfully!", "success")
    return redirect(url_for('dashboard'))

@booking_bp.route('/release_slot/<int:slot_id>', methods=['POST'])
@login_required
def release_slot(slot_id):
    slot = ParkingSlot.query.get(slot_id)

    if slot and slot.booked_by == current_user.id:
        slot.status = "available"
        slot.booked_by = None
        db.session.commit()
        flash('Slot released successfully!', "success")
    # else:
    #     flash("Failed to release slot!", "danger")

    return redirect('/dashboard')
