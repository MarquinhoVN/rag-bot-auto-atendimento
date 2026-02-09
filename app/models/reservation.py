from app.models.database import db
from datetime import datetime
import enum

class ReservationStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class Reservation(db.Model):
    __tablename__ = 'reservation'
    __table_args__ = {'schema': 'hotel'}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('hotel.user.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    contact = db.Column(db.String(50), nullable=True)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    room_type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(ReservationStatus), nullable=False, default=ReservationStatus.pending)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<PreReserva {self.name} de {self.check_in_date} a {self.check_out_date}>"
