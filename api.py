import os
from flask import Flask
from sqlalchemy import text
from app.models.database import db
from routes.webhook import webhook_bp

from app.models import messageHistory, reservation, user, preReservationStep
from app.mock.model_mock import RoomType, RoomOccupancy, Room ##PARA MOCK
from app.mock.data_mock import load_mock_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_CONNECTION_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    engine = db.get_engine()
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS hotel"))
        conn.commit()

    db.create_all()
    load_mock_data() ## Mock dos Dados

app.register_blueprint(webhook_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
