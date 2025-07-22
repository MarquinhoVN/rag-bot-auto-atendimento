
import os
from flask import Flask
from models.database import db
from routes.webhook import webhook_bp

#Instanciando Models
from models import messageHistory, preReservation, user, preReservationStep

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_CONNECTION_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(webhook_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
