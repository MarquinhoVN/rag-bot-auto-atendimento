from app.models.database import db
from datetime import date


class RoomType(db.Model):
    __tablename__ = "room_type"
    __table_args__ = {"schema": "hotel"}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    rooms = db.relationship("Room", backref="room_type", lazy=True)

class Room(db.Model):
    __tablename__ = "room"
    __table_args__ = {"schema": "hotel"}

    id = db.Column(db.Integer, primary_key=True)
    room_type_id = db.Column(
        db.Integer,
        db.ForeignKey("hotel.room_type.id"),
        nullable=False
    )
    room_number = db.Column(db.String(20), nullable=False, unique=True)
    capacity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    occupancies = db.relationship("RoomOccupancy", backref="room", lazy=True)

class RoomOccupancy(db.Model):
    __tablename__ = "room_occupancy"
    __table_args__ = {"schema": "hotel"}

    id = db.Column(db.Integer, primary_key=True)

    room_id = db.Column(
        db.Integer,
        db.ForeignKey("hotel.room.id"),
        nullable=False
    )

    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)

    guest_name = db.Column(db.String(200))
    source = db.Column(db.String(50))
