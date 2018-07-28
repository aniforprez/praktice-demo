import csv
import os
from datetime import datetime

from flask import Flask
from twilio.rest import Client

from models import Appointment, db
from config import NGROK_URL, TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN
from twilio_views import twilio_views

app = Flask(__name__)
app.register_blueprint(twilio_views)

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://localhost/praktise-demo')
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)
    db.create_all()

def import_csv():
    filename = os.path.join(SITE_ROOT, 'appointments.csv')
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        csvlist = list(csvreader)
        try:
            for row in csvlist:
                datetime_string = row[1] + ' ' + row[2]
                appointment_datetime = datetime.strptime(datetime_string, '%d-%m-%Y %H:%M')
                appointment = Appointment(row[0], row[3], appointment_datetime)
                db.session.add(appointment)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)

def make_twilio_call(phone_number, appointment_id):
    call = twilio_client.calls.create(
                        url=NGROK_URL + '/call_answered/' + str(appointment_id),
                        to=phone_number,
                        from_='+15594713206'
                    )
    print(call.sid)

def make_appointment_calls():
    appointments = Appointment.query.all()
    for appointment in appointments:
        if appointment.appointment_datetime.date() == datetime.today().date():
            appointment_id = appointment.id
            phone_number = appointment.phone_number
            provider = appointment.provider

            if provider == 'twilio':
                make_twilio_call(phone_number, appointment_id)

with app.app_context():
    import_csv()
    make_appointment_calls()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
