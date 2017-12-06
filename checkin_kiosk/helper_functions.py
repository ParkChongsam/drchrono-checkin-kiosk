from .models import Appointment
from .api_access import API_Access

import datetime


def get_user_access_token(user):
    return user.social_auth.get(provider='drchrono').extra_data['access_token']

'''
def checkin(request):
    template_name = 'checkin_kiosk/checkin_page.html'
    context = {
        'user': request.user
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))
'''

def get_current_appointment(appointments):
    time_now = datetime.datetime.now()
    for appointment in appointments:
        start_time = appointment['appointment_start_time']
        if (
            start_time.day == time_now.day and 
            start_time.hour == time_now.hour and 
            time_now.minute in range(start_time.minute, start_time.minute+61)
        ):
            return appointment

def split_appointments(request):
    api_access = API_Access(get_user_access_token(request.user))
    appointments = Appointment.objects.values()
    current_appointment = get_current_appointment(appointments)
    appointment_ids = [appointment['id'] for appointment in appointments]
    if not current_appointment or not current_appointment['check']:
        all_appointments = api_access.get_all_appointments_today()
        for appointment in all_appointments:
            if int(appointment['id']) not in appointment_ids:
                data = api_access.get_patient_information(appointment['id'])
                name = data['first_name'] + ' ' + data['last_name']
                appointment_obj = Appointment(
                    name=name,
                    appointment_id=appointment['id'],
                    patient_id=appointment['patient'],
                    status=appointment['status'],
                    appointment_start_time=parser.parse(appointment['scheduled_time']),
                    duration=appointment['duration']
                )
                appointment_obj.save()
    appointments = Appointment.objects.values()
    return current_appointment, appointments