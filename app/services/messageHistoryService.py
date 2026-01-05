from app.models.messageHistory import MessageHistory
from app.models.database import db
from datetime import datetime

def get_last_messages_by_user(user_id, limit=20):
    return (
        MessageHistory.query
        .with_entities(MessageHistory.message, MessageHistory.response)
        .filter_by(user_id=user_id)
        .order_by(MessageHistory.created_at.desc())
        .limit(limit)
        .all()
    )

def save_message(user_id, message, response=None):
    history = MessageHistory(
        user_id=user_id,
        message=message,
        response=response,
        created_at=datetime.utcnow()
    )
    db.session.add(history)
    db.session.commit()
    return history
