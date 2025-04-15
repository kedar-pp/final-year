from app import app, db
from models import ParkingSlot

with app.app_context():
    # Only add slots if there are none
    current_count = ParkingSlot.query.count()
    desired_total = 25
    if current_count < desired_total:
        for i in range(current_count + 1, desired_total + 1):
            slot = ParkingSlot(slot_number=f"S{i:02d}", status="available")
            db.session.add(slot)
        db.session.commit()
        print(f"Seeded additional slots. Total slots: {desired_total}")
    else:
        print("Slots already meet or exceed the desired total.")