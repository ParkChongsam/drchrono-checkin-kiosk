from .models import AppointmentHistory, AverageWaitTime
from .api_access import API_Access

from dateutil import parser, tz
import datetime


def get_user_access_token(user):
    return user.social_auth.get(provider='drchrono').extra_data['access_token']

def get_current_appointment(appointments):
    time_now = datetime.datetime.now()
    for appointment in appointments:
        start_time = appointment['appointment_start_time']
        if (
            start_time.year == time_now.year and
            start_time.month == time_now.month and
            start_time.day == time_now.day and 
            start_time.hour == time_now.hour and 
            time_now.minute in range(start_time.minute, start_time.minute+31)
        ):
            return appointment

def get_correct_time(time):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    time = time.replace(tzinfo=from_zone)
    return time.astimezone(to_zone)

def split_appointments(request):
    api_access = API_Access(get_user_access_token(request.user))
    appointments = AppointmentHistory.objects.all().values()
    current_appointment = get_current_appointment(appointments)
    print current_appointment
    appointment_ids = [appointment['id'] for appointment in appointments]
    if not current_appointment or not current_appointment['check']:
        all_appointments = api_access.get_all_appointments_today()
        for appointment in all_appointments:
            if int(appointment['id']) not in appointment_ids:
                data = api_access.get_patient_information(appointment['patient'])
                name = data['first_name'] + ' ' + data['last_name']
                appointment_obj, created = AppointmentHistory.objects.get_or_create(
                    name=name,
                    appointment_id=appointment['id'],
                    patient_id=appointment['patient'],
                    status=appointment['status'],
                    appointment_start_time=parser.parse(appointment['scheduled_time']),
                    appointment_duration=appointment['duration']
                )
                appointment_obj.save()
    appointments = AppointmentHistory.objects.all().values()
    return current_appointment, appointments

def get_wait_time(start_time, status_time):
    time_diff = status_time - start_time
    return divmod(time_diff.days*86400+time_diff.seconds, 1)

def get_average_wait_time(wait_times):
    total_wait_time = 0.0
    count = 0
    for wait_time in wait_times:
        total_wait_time += wait_time
        count += 1
    return (total_wait_time/count, 0)
