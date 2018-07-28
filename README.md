# Appointments Demo

This project reads the appointments.csv file for appointments and imports them to a PostgreSQL db and then calls the people whose appointment is "today".

## Requirements
* [Python 3](https://www.python.org/downloads/release/python-370/)
* [Pipenv](https://docs.pipenv.org/#install-pipenv-today)
* [PostgreSQL](https://www.postgresql.org/download/)
* [ngrok](https://ngrok.com/download)

## Running the code

Make sure you have the "praktise-demo" DB in your PostgreSQL after installing PSQL by running 
```
createdb praktise-demo
```

Install all dependencies by running
```
pipenv install
```

Run ngrok as per the instructions on your ngrok dashboard

Create a file `config.py` with the following template
```python
TWILIO_ACCOUNT_SID = <your Twilio SID>
TWILIO_ACCOUNT_TOKEN = <your Twilio token>

NGROK_URL = <your ngrok URL from your ngrok instance>
```

Run the flask app by running the following commands
```
export FLASK_APP=app.py
flask run
```