from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.User import User


def create():
    # List of users to add
    db = SessionLocal()


    users = [
        User(email="user1@example.com", password="password1", status=True),
        User(email="user2@example.com", password="password2", status=True),
        User(email="user3@example.com", password="password3", status=True),
        User(email="user4@example.com", password="password4", status=True),
        User(email="user5@example.com", password="password5", status=False),  # Example of a user with status=False
    ]

    # Add users to the session and commit to the database
    db.add_all(users)
    db.commit()

    print("5 users have been inserted into the database.")

