from models.database import db
from datetime import datetime

class MessageHistory(db.Model):
    __tablename__ = 'message_history' 
    __table_args__ = {'schema': 'hotel'} 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('hotel.user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)  
    response = db.Column(db.Text)  
    language = db.Column(db.Text)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 

    def __repr__(self):
        return f"<MessageHistory {self.user_id} - {self.created_at}>"
