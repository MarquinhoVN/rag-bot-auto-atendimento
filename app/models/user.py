from app.models.database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'hotel'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    contact = db.Column(db.Text, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('MessageHistory', backref='user', lazy=True)
    reservations = db.relationship('Reservation', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.name or self.external_id}>"
