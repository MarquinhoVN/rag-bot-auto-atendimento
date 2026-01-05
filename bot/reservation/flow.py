from app.services.preReservationStepService import (
    get_active_pre_reservation_step,
    create_pre_reservation_step,
    update_pre_reservation_step,
    cancel_pre_reservation_step
)
from app.services.reservationService import save_reservation

from bot.reservation.llm import structured_llm
from bot.reservation.prompt import dynamic_question_prompt
from bot.reservation.extractor import extract_fields_with_llm, parse_date_or_none
from bot.reservation.validator import is_empty

from bot.reservation.findBestRoom import find_best_room

def generate_dynamic_question(field, context):
    prompt = dynamic_question_prompt(field, context)
    return structured_llm.ask(prompt)


def handle_reservation_flow(user, message):
    cleaned = message.strip().lower()

    if cleaned in ["cancelar", "cancelar reserva", "cancelar pré-reserva"]:
        cancel_pre_reservation_step(user.id)
        return "Reserva cancelada! Se quiser começar de novo, é só dizer 😊"

    step = get_active_pre_reservation_step(user.id)
    if not step:
        step = create_pre_reservation_step(user.id)
        return generate_dynamic_question("name", "Início da reserva")

    data = {
        "name": step.name,
        "contact": step.contact,
        "check_in_date": str(step.check_in_date) if step.check_in_date else None,
        "check_out_date": str(step.check_out_date) if step.check_out_date else None,
        "room_type": step.room_type,
        "quantity": step.quantity,
        "description": step.description
    }

    extracted = extract_fields_with_llm(message, data, step.step)

    if "__error__" in extracted:
        return extracted["__error__"]

    for key, val in extracted.items():
        if key in data and is_empty(getattr(step, key)):
            if "date" in key:
                val = parse_date_or_none(val)

            if key == step.step:
                setattr(step, key, val)

    needed_fields = [
        "name",
        "contact",
        "check_in_date",
        "check_out_date",
        "quantity",
        "room_type",
        "description"
    ]

    for field in needed_fields:
        if field in ["room_type", "description"]:
            if is_empty(getattr(step, field)) and field == step.step:

                if field == "room_type":
                    if step.check_in_date and step.check_out_date and step.quantity:
                        best = find_best_room(
                            step.check_in_date,
                            step.check_out_date,
                            step.quantity,
                            message
                        )

                        if not best:
                            return (
                                "Não encontrei nenhum quarto compatível com essa preferência. "
                                "Pode descrever outro tipo de quarto?"
                            )

                setattr(step, field, message)

        if is_empty(getattr(step, field)):
            update_pre_reservation_step(user.id, field, step)
            return generate_dynamic_question(field, data)


    save_reservation(
        user_id=user.id,
        name=step.name,
        contact=step.contact,
        check_in_date=step.check_in_date,
        check_out_date=step.check_out_date,
        room_type=step.room_type,
        quantity=step.quantity,
        description=step.description,
    )

    step.step = "finalizado"
    update_pre_reservation_step(user.id, "finalizado", step)

    return "Prontinho! Sua pré-reserva foi registrada com sucesso. Entraremos em contato em breve 😊"
