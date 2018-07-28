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

@twilio_views.route('/call_answered/menu/<appointment_id>', methods=['POST'])
def menu(appointment_id):
    selected_option = request.form['Digits']
    response = VoiceResponse()
    if selected_option == '1':
        response.say('Thanks for the confirmation', voice='alice')
    elif selected_option == '2':
        response.say('"Could you please let us know the reason for not being able to attend the appointment after the beep and then hangup', voice='alice')
        response.record(action=url_for('twilio_views.delay_recording', appointment_id=appointment_id))
    else:
        response.say('Wrong digit pressed. Returning', voice='alice')
        response.redirect(url_for('twilio_views.answer_call', appointment_id=appointment_id))
    return str(response)

@twilio_views.route('/call_answered/delay_recording/<appointment_id>', methods=['POST'])
def delay_recording(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    appointment.delay_reason = request.form['RecordingUrl']
    db.session.commit()
    return Response(200)
