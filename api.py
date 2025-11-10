import os
from flask import Flask
from sqlalchemy import text
from models.database import db
from routes.webhook import webhook_bp

from models import messageHistory, preReservation, user, preReservationStep

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

app.register_blueprint(webhook_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
