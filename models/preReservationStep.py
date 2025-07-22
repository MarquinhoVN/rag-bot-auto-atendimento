from models.database import db
from datetime import datetime

class PreReservationStep(db.Model):
    __tablename__ = 'pre_reservation_steps'
    __table_args__ = {'schema': 'hotel'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('hotel.user.id'), nullable=False)
    step = db.Column(db.String(50), nullable=False, default="aguardando_nome")
    
    name = db.Column(db.Text)
    contact = db.Column(db.Text)
    check_in_date = db.Column(db.Date)
    check_out_date = db.Column(db.Date)
    room_type = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    description = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", backref="pre_reservation_steps")

    def __repr__(self):
        return f"<PreReservationStep user_id={self.user_id} step={self.step}>"
