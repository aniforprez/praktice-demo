from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Appointment(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    provider = db.Column(db.String(50), nullable=False)
    appointment_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    delay_reason = db.Column(db.String(200))

    def __init__(self, phone_number, provider, appointment_datetime, **kwargs):
        self.phone_number = phone_number
        self.provider = provider
        self.appointment_datetime = appointment_datetime
        super(Appointment, self).__init__(**kwargs)
