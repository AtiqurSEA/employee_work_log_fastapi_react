from datetime import date
from sqlalchemy.orm import Session

from backend.auth import hash_password
from backend.models import User, WorkLog


def seed_database(db: Session) -> None:
    users_data = [
        ("Admin User", "admin@example.com", "admin123", "admin"),
        ("Abbas Khan", "abbas@example.com", "password123", "regular"),
        ("James Smith", "james@example.com", "password123", "regular"),
        ("Sarah Ahmed", "sarah@example.com", "password123", "regular"),
        ("Fatima Ali", "fatima@example.com", "password123", "regular"),
        ("Yusuf Rahman", "yusuf@example.com", "password123", "regular"),
        ("Layla Begum", "layla@example.com", "password123", "regular"),
        ("Aisha Hussain", "aisha@example.com", "password123", "regular"),
        ("Omar Patel", "omar@example.com", "password123", "regular"),
        ("Maya Jones", "maya@example.com", "password123", "regular"),
    ]

    for full_name, email, password, role in users_data:
        existing_user = db.query(User).filter(User.email == email).first()
        if not existing_user:
            db.add(
                User(
                    full_name=full_name,
                    email=email,
                    password_hash=hash_password(password),
                    role=role,
                )
            )

    db.commit()

    if db.query(WorkLog).count() > 0:
        return

    users = {user.email: user for user in db.query(User).all()}

    logs = [
        WorkLog(user_id=users["abbas@example.com"].id, date=date(2026, 1, 5), task="Fixed backend login bug", hours=3.5, status="Completed", project="Web Portal", comments="Resolved validation issue"),
        WorkLog(user_id=users["james@example.com"].id, date=date(2026, 1, 6), task="Updated dashboard layout", hours=2.0, status="In Progress", project="Employee Work Log", comments="Improved table spacing"),
        WorkLog(user_id=users["sarah@example.com"].id, date=date(2026, 1, 7), task="Wrote test cases", hours=4.0, status="Completed", project="Testing", comments="Covered CRUD functions"),
        WorkLog(user_id=users["fatima@example.com"].id, date=date(2026, 1, 8), task="Created ERD draft", hours=1.5, status="Completed", project="Design", comments="Added users and work logs"),
        WorkLog(user_id=users["yusuf@example.com"].id, date=date(2026, 1, 9), task="Reviewed accessibility", hours=2.5, status="Pending", project="Frontend", comments="Colour contrast review needed"),
        WorkLog(user_id=users["layla@example.com"].id, date=date(2026, 1, 10), task="Updated API documentation", hours=2.0, status="In Progress", project="Backend", comments="Checked endpoint descriptions"),
        WorkLog(user_id=users["aisha@example.com"].id, date=date(2026, 1, 11), task="Refactored work log routes", hours=3.0, status="Completed", project="Backend", comments="Reduced duplicate code"),
        WorkLog(user_id=users["omar@example.com"].id, date=date(2026, 1, 12), task="Tested delete permissions", hours=1.0, status="Completed", project="Security", comments="Regular users blocked"),
        WorkLog(user_id=users["maya@example.com"].id, date=date(2026, 1, 13), task="Prepared screenshots", hours=2.0, status="Pending", project="Report", comments="Need final hosted screenshots"),
        WorkLog(user_id=users["admin@example.com"].id, date=date(2026, 1, 14), task="Checked seed data", hours=1.5, status="Completed", project="Database", comments="10 users and 10 logs added"),
    ]

    db.add_all(logs)
    db.commit()