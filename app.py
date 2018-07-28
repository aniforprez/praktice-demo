import csv
import os
from datetime import datetime
from flask import Flask
from models import Appointment, db
app = Flask(__name__)
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://localhost/praktise-demo')
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
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
with app.app_context():
    import_csv()
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
