import datetime
import requests
import urllib

from .shortcuts import Shortcuts

class API_Error(Exception):
    pass

class API_Access(object):
    main_url = 'https://drchrono.com'

    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
            'Authorization': 'Bearer %s' % self.access_token
        }
    
    def get_full_url(self, endpoint_url, **filtering_parameters):
        full_url = self.main_url + endpoint_url + '?' + urllib.urlencode(filtering_parameters)
        return full_url

    def get_patient_id(self, **kwargs):
        firstname = kwargs.pop('firstname', '')
        lastname = kwargs.pop('lastname', '')
        full_url = self.get_full_url('/api/patients', first_name=firstname, last_name=lastname)
        response = requests.get(full_url, headers=self.headers)
        data = response.json()
        patient_id = None
        if data['results']:
            patient_id = data['results'][0]['id']
        return patient_id

    def get_all_appointments_today(self):
        today_date = datetime.date.today().strftime('%Y-%m-%d')
        full_url = self.get_full_url('/api/appointments/', date=today_date)
        response = requests.get(full_url, headers=self.headers)
        data = response.json()
        return data['results']

    def get_appointments_by_appointment_id(self, appointment_id):
        full_url = self.main_url + '/api/appointments/' + str(appointment_id)
        response = requests.get(full_url, headers=self.headers)
        data = response.json()
        return data

    def get_appointments_by_patient_name(self, **kwargs):
        firstname = kwargs.pop('firstname', '')
        lastname = kwargs.pop('lastname', '')
        today_date = datetime.datetime.now().strftime('%Y-%m-%d')
        patient_id = self.get_patient_id(firstname=firstname, lastname=lastname)
        full_url = self.get_full_url('/api/appointments', date=today_date, patient=patient_id)
        print full_url
        response = requests.get(full_url, headers=self.headers)
        data = response.json()
        appointment_details = []
        if data['results']:
            for i in range(len(data['results'])):
                scheduled_time = data['results'][i]['scheduled_time']
                duration = data['results'][i]['duration']
                status = data['results'][i]['status']
                if not status:
                    status = Shortcuts.Statuses.NOT_CONFIRMED
                reason = data['results'][i]['reason']
                if not reason:
                    reason = Shortcuts.Statuses.NOT_MENTIONED
                
                appointment = {
                    'firstname': firstname,
                    'lastname': lastname,
                    'scheduled_time': scheduled_time,
                    'duration': duration,
                    'status': status,
                    'reason': reason
                }
                appointment_details.append(appointment)
                break

        return appointment_details

    def edit_appointment_information(self, appointment_id, data):
        full_url = self.main_url + '/api/appointments/' + str(appointment_id)
        response = requests.put(full_url, data=data, headers=self.headers)
        return response

    def get_patient_information(self, id):
        full_url = self.main_url + '/api/patients/' + str(id)
        response = requests.get(full_url, headers=self.headers)
        return response.json()

    def edit_patient_information(self, id, data):
        full_url = self.main_url + '/api/patients/' + str(id)
        response = requests.put(full_url, data=data, headers=self.headers)
        return response








