from app import app, db
from models import User

# Create an application context
with app.app_context():
    # Insert test user
    new_user = User(username="admin", password="adminpass", role="admin")
    db.session.add(new_user)
    db.session.commit()

    # Fetch and print the user
    user = User.query.first()
    print(f"User created: {user.username}, Role: {user.role}")
