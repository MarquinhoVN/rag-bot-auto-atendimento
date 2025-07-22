from services.preReservationStepService import (
    get_active_pre_reservation_step,
    create_pre_reservation_step,
    update_pre_reservation_step,
    cancel_pre_reservation_step
)
from services.preReservationService import save_pre_reservation
from datetime import datetime, date

def handle_reservation_flow(user, message):
    message = message.strip()

    if message.lower() in ["cancelar", "cancelar reserva", "cancelar pré-reserva"]:
        cancel_pre_reservation_step(user.id)
        return "Sua pré-reserva foi cancelada com sucesso. Se quiser começar novamente, digite *quero reservar*."

    step_obj = get_active_pre_reservation_step(user.id)

    if not step_obj:
        step_obj = create_pre_reservation_step(user.id)
        return "Vamos começar sua pré-reserva. Qual é o seu nome completo?\n\n*Você pode cancelar a qualquer momento digitando 'cancelar'.*"

    step = step_obj.step.strip().lower()
    response = ""

    if step == "aguardando_nome":
        step_obj.name = message
        step_obj.step = "aguardando_contato"
        response = "Perfeito! Agora me informe um telefone para contato."

    elif step == "aguardando_contato":
        step_obj.contact = message
        step_obj.step = "aguardando_checkin"
        response = "Qual será a data de **check-in**? (Formato: DD-MM-YYYY, DD MM YYYY ou DD/MM/YYYY)"

    elif step == "aguardando_checkin":
        try:
            msg_date = message.replace("/", "-").replace(" ", "-")
            checkin = datetime.strptime(msg_date, "%d-%m-%Y").date()
            if checkin < date.today():
                return "A data de check-in deve ser hoje ou uma data futura.\n\n*Você pode cancelar a qualquer momento digitando 'cancelar'.*"
            step_obj.check_in_date = checkin
            step_obj.step = "aguardando_checkout"
            response = "E a data de **check-out**?"
        except ValueError:
            return "Formato inválido. Por favor, informe a data de check-in no formato DD-MM-YYYY, DD MM YYYY ou DD/MM/YYYY.\n\n*Você pode cancelar a qualquer momento digitando 'cancelar'.*"

    elif step == "aguardando_checkout":
        try:
            msg_date = message.replace("/", "-").replace(" ", "-")
            checkout = datetime.strptime(msg_date, "%d-%m-%Y").date()
            if checkout < date.today():
                return "A data de check-out deve ser hoje ou uma data futura.\n\n*Você pode cancelar a qualquer momento digitando 'cancelar'.*"
            if checkout < step_obj.check_in_date:
                return "A data de check-out deve ser igual ou posterior à data de check-in.\n\n*Você pode cancelar a qualquer momento digitando 'cancelar'.*"
            step_obj.check_out_date = checkout
            step_obj.step = "aguardando_tipo_quarto"
            response = "Qual tipo de quarto você deseja? (Ex: solteiro, casal, luxo...)"
        except ValueError:
            return "Formato inválido. Por favor, informe a data de check-out no formato DD-MM-YYYY, DD MM YYYY ou DD/MM/YYYY.\n\n*Você pode cancelar a qualquer momento digitando 'cancelar'.*"

    elif step == "aguardando_tipo_quarto":
        step_obj.room_type = message
        step_obj.step = "aguardando_quantidade"
        response = "Para quantas pessoas você deseja reservar?"

    elif step == "aguardando_quantidade":
        try:
            step_obj.quantity = int(message)
            step_obj.step = "aguardando_descricao"
            response = "Deseja adicionar alguma observação ou necessidade especial? (Se não, diga 'não')"
        except ValueError:
            return "Por favor, informe a quantidade como um número inteiro (ex: 1, 2, 3...).\n\n*Você pode cancelar a qualquer momento digitando 'cancelar'.*"

    elif step == "aguardando_descricao":
        step_obj.description = message
        step_obj.step = "finalizado"

        save_pre_reservation(
            user_id=user.id,
            name=step_obj.name,
            contact=step_obj.contact,
            check_in_date=step_obj.check_in_date,
            check_out_date=step_obj.check_out_date,
            room_type=step_obj.room_type,
            quantity=step_obj.quantity,
            description=step_obj.description
        )

        update_pre_reservation_step(user.id, step_obj.step, step_obj)
        return "Sua pré-reserva foi registrada com sucesso! Entraremos em contato em breve."

    update_pre_reservation_step(user.id, step_obj.step, step_obj)

    return response + "\n\n*Você pode cancelar a qualquer momento digitando 'cancelar'.*"
