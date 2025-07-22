from flask import Blueprint, request, jsonify
from libs.evo import EvoAPI
from bot.aiBot import AIBot
from bot.intencao import IntencaoDetector
from bot.reservationFlow import handle_reservation_flow
from services.userService import get_user_by_contact, create_user
from services.messageHistoryService import get_last_messages_by_user, save_message
from services.preReservationStepService import get_active_pre_reservation_step

evo = EvoAPI()
ai_bot = AIBot()
intencao = IntencaoDetector()


webhook_bp = Blueprint('webhook', __name__)


@webhook_bp.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json

    received_message = data.get('data', {}).get('message', {}).get('conversation')
    instance = data.get('instance', {})
    apikey = data.get('apikey', {})
    remotejid =  data.get('data', {}).get('key', {}).get('remoteJid')
    received_number = remotejid.split("@")[0]
    sender_type = remotejid.split("@")[1]

    if sender_type in ['@g.us', 'status@broadcast']:
        return jsonify({'status': 'success', 'message': 'Mensagem de grupo/status ignorada.'}), 200

    user = get_user_by_contact(received_number)
        
    
    if not user:
        user = create_user(name = data.get('data', {}).get('pushName', {}), contact = received_number, language='pt')
        history_messages = []

    step = get_active_pre_reservation_step(user.id)
    intencao_tipo = intencao.detectar(received_message)

    if step or intencao_tipo == "pre_reserva":
        message = handle_reservation_flow(user, received_message)
        language = user.language or "pt"
    else:
        history_messages = get_last_messages_by_user(user.id)
        message, language = ai_bot.invoke(
            history_messages=history_messages,
            question=received_message
        )

    evo.enviar_mensagem(instance=instance,
                         apikey=apikey, 
                         sender_number=received_number, 
                         message=message)
    

    save_message(user_id = user.id, message=received_message, response = message, language=language )

    return jsonify({'status': 'success'}), 200