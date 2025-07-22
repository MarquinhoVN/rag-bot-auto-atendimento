from models.database import db
from datetime import datetime

class preReservation(db.Model):
    __tablename__ = 'pre_resevation'
    __table_args__ = {'schema': 'hotel'}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('hotel.user.id'), nullable=False)
    name = db.Column(db.Text)
    contact = db.Column(db.Text)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    room_type = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PreReserva {self.name} de {self.check_in_date} a {self.check_out_date}>"
