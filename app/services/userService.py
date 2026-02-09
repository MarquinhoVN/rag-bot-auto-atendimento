from app.models.user import User
from app.models.database import db

def get_user_by_contact(contact):
    return User.query.filter_by(contact=contact).first()

def create_user(name=None, contact=None):
    user = User(
        name=name,
        contact=contact
    )
    db.session.add(user)
    db.session.commit()
    return user
