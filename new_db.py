from app import app,db

with app.app_context():
    db.drop_all()  # Delete all tables
    db.create_all()  # Recreate tables with updated schema
    print("Database reset successfully!")