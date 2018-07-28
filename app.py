import csv
import os
from datetime import datetime
from flask import Flask
app = Flask(__name__)
def import_csv():
    filename = os.path.join(SITE_ROOT, 'appointments.csv')
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        csvlist = list(csvreader)
        try:
            for row in csvlist:
                datetime_string = row[1] + ' ' + row[2]
                appointment_datetime = datetime.strptime(datetime_string, '%d-%m-%Y %H:%M')
        except Exception as e:
            print(e)
with app.app_context():
    import_csv()
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
