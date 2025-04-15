from app import app, db
from models import ParkingSlot

with app.app_context():
    slots = ParkingSlot.query.all()
    
    # Remove extra slots (assuming slots are added sequentially)
    for slot in slots[20:]:  
        db.session.delete(slot)
    
    db.session.commit()
    print("Database updated: Now only 20 slots exist.")
