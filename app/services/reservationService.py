from app.models.reservation import Reservation
from app.models.database import db
from datetime import datetime

def save_reservation(
    user_id,
    name,
    contact,
    check_in_date,
    check_out_date,
    room_type,
    quantity,
    description=None
):
    if isinstance(check_in_date, str):
        check_in_date = datetime.strptime(check_in_date, "%Y-%m-%d").date()
    if isinstance(check_out_date, str):
        check_out_date = datetime.strptime(check_out_date, "%Y-%m-%d").date()

    reservationDetail = Reservation(
        user_id=user_id,
        name=name,
        contact=contact,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        room_type=room_type,
        quantity=quantity,
        description=description
    )

    db.session.add(reservationDetail)
    db.session.commit()
    return reservationDetail
