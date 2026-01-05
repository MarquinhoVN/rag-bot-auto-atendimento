from app.models.database import db
from datetime import date

from app.mock.model_mock import RoomType, Room, RoomOccupancy


def load_mock_data():
    db.session.query(RoomOccupancy).delete()
    db.session.query(Room).delete()
    db.session.query(RoomType).delete()
    db.session.commit()

    rt1 = RoomType(id=1, name="Standard", description="Quarto simples para até 2 pessoas")
    rt2 = RoomType(id=2, name="Deluxe", description="Quarto confortável para 3 pessoas")
    rt3 = RoomType(id=3, name="Suite", description="Quarto grande e luxuoso")
    db.session.add_all([rt1, rt2, rt3])
    db.session.commit()

    r1 = Room(id=1, room_type_id=1, room_number="101", capacity=2, price=180)
    r2 = Room(id=2, room_type_id=1, room_number="102", capacity=2, price=180)
    r3 = Room(id=3, room_type_id=2, room_number="201", capacity=3, price=260)
    r4 = Room(id=4, room_type_id=2, room_number="202", capacity=3, price=260)
    r5 = Room(id=5, room_type_id=3, room_number="301", capacity=4, price=420)

    db.session.add_all([r1, r2, r3, r4, r5])
    db.session.commit()

    o1 = RoomOccupancy(
        id=1,
        room_id=1,
        check_in_date=date(2025, 8, 5),
        check_out_date=date(2025, 8, 8),
        guest_name="João Silva",
        source="external_system"
    )

    o2 = RoomOccupancy(
        id=2,
        room_id=4,
        check_in_date=date(2025, 8, 10),
        check_out_date=date(2025, 8, 12),
        guest_name="Maria Oliveira",
        source="phone_request"
    )

    db.session.add_all([o1, o2])
    db.session.commit()

