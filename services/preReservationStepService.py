from models.preReservationStep import PreReservationStep
from models.database import db


def get_active_pre_reservation_step(user_id):
    return (
        PreReservationStep.query
        .filter_by(user_id=user_id)
        .filter(PreReservationStep.step.notin_(["finalizado", "cancelado"]))
        .order_by(PreReservationStep.created_at.desc())
        .first()
    )

def create_pre_reservation_step(user_id):
    step = PreReservationStep(
        user_id=user_id,
        step="aguardando_nome"
    )
    db.session.add(step)
    db.session.commit()
    return step

def update_pre_reservation_step(user_id, new_step, step_obj=None):
    if not step_obj:
        step_obj = get_active_pre_reservation_step(user_id)
    if step_obj:
        step_obj.step = new_step
        db.session.commit()
    return step_obj


def cancel_pre_reservation_step(user_id):
    step = get_active_pre_reservation_step(user_id)
    if step:
        step.step = "cancelado"
        db.session.commit()
    return step
