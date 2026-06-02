from datetime import date
from sqlalchemy.orm import Session

from backend.auth import hash_password
from backend.models import User, WorkLog


def seed_database(db: Session) -> None:
    if db.query(User).count() > 0:
        return

    users = [
        User(full_name="Admin User", email="admin@example.com", password_hash=hash_password("admin123"), role="admin"),
        User(full_name="Abbas Khan", email="abbas@example.com", password_hash=hash_password("password123"), role="regular"),
        User(full_name="James Smith", email="james@example.com", password_hash=hash_password("password123"), role="regular"),
        User(full_name="Sarah Ahmed", email="sarah@example.com", password_hash=hash_password("password123"), role="regular"),
        User(full_name="Fatima Ali", email="fatima@example.com", password_hash=hash_password("password123"), role="regular"),
        User(full_name="Yusuf Rahman", email="yusuf@example.com", password_hash=hash_password("password123"), role="regular"),
        User(full_name="Layla Begum", email="layla@example.com", password_hash=hash_password("password123"), role="regular"),
        User(full_name="Aisha Hussain", email="aisha@example.com", password_hash=hash_password("password123"), role="regular"),
        User(full_name="Omar Patel", email="omar@example.com", password_hash=hash_password("password123"), role="regular"),
        User(full_name="Maya Jones", email="maya@example.com", password_hash=hash_password("password123"), role="regular"),
    ]
    db.add_all(users)
    db.commit()

    user_ids = [user.id for user in db.query(User).all()]
    logs = [
        WorkLog(user_id=user_ids[1], date=date(2026, 1, 5), task="Fixed backend login bug", hours=3.5, status="Completed", project="Web Portal", comments="Resolved validation issue"),
        WorkLog(user_id=user_ids[2], date=date(2026, 1, 6), task="Updated dashboard layout", hours=2.0, status="In Progress", project="Employee Work Log", comments="Improved table spacing"),
        WorkLog(user_id=user_ids[3], date=date(2026, 1, 7), task="Wrote test cases", hours=4.0, status="Completed", project="Testing", comments="Covered CRUD functions"),
        WorkLog(user_id=user_ids[4], date=date(2026, 1, 8), task="Created ERD draft", hours=1.5, status="Completed", project="Design", comments="Added users and work logs"),
        WorkLog(user_id=user_ids[5], date=date(2026, 1, 9), task="Reviewed accessibility", hours=2.5, status="Pending", project="Frontend", comments="Colour contrast review needed"),
        WorkLog(user_id=user_ids[6], date=date(2026, 1, 10), task="Updated API documentation", hours=2.0, status="In Progress", project="Backend", comments="Checked endpoint descriptions"),
        WorkLog(user_id=user_ids[7], date=date(2026, 1, 11), task="Refactored work log routes", hours=3.0, status="Completed", project="Backend", comments="Reduced duplicate code"),
        WorkLog(user_id=user_ids[8], date=date(2026, 1, 12), task="Tested delete permissions", hours=1.0, status="Completed", project="Security", comments="Regular users blocked"),
        WorkLog(user_id=user_ids[9], date=date(2026, 1, 13), task="Prepared screenshots", hours=2.0, status="Pending", project="Report", comments="Need final hosted screenshots"),
        WorkLog(user_id=user_ids[0], date=date(2026, 1, 14), task="Checked seed data", hours=1.5, status="Completed", project="Database", comments="10 users and 10 logs added"),
    ]
    db.add_all(logs)
    db.commit()
