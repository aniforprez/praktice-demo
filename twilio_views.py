from datetime import datetime

from flask import Blueprint, Response, request, url_for
from twilio.twiml.voice_response import VoiceResponse

from models import Appointment, db

twilio_views = Blueprint('twilio_views', __name__)

@twilio_views.route("/call_answered/<appointment_id>", methods=['GET', 'POST'])
def answer_call(appointment_id):
    response = VoiceResponse()

    appointment = Appointment.query.get(appointment_id)
    appointment_time = datetime.strftime(appointment.appointment_datetime, '%I:%M %p')

    tts_string = 'You have an appointment today with Dr. Anirudh at {}. Would you be attending? Please press 1 if you are attending and 2 if you are not attending.'.format(appointment_time)

    with response.gather(
        num_digits=1, action=url_for('twilio_views.menu', appointment_id=appointment_id), method="POST"
    ) as g:
        g.say(tts_string, voice='alice')

    return str(response)

