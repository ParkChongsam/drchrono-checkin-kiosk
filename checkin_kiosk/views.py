# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, TemplateView, FormView
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, get_user_model, login, logout

from .forms import PatientSignInForm, PatientDemographicsForm
from .models import AppointmentHistory, AverageWaitTime
from .api_access import API_Access
from .shortcuts import Shortcuts
from .helper_functions import (
    get_user_access_token, 
    get_current_appointment,
    get_correct_time, 
    split_appointments, 
    get_wait_time, 
    get_average_wait_time
)

from dateutil import parser
import datetime

# Views
class CheckInPageView(View):
    form_class = PatientSignInForm
    template_name = 'checkin_kiosk/check_in.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        api_request = API_Access(get_user_access_token(request.user))
        form = self.form_class(request.POST)
        if form.is_valid():
            clean = form.cleaned_data
            firstname = clean['firstname']
            lastname = clean['lastname']
            patient_id = api_request.get_patient_id(firstname=firstname, lastname=lastname)
            if patient_id is None:
                context = {
                    'form': form,
                    'cred': Shortcuts.Validations.INVALID_CREDENTIALS
                }
                return render(request, self.template_name, context)

            else:
                response = api_request.get_appointments_by_patient_name(
                    firstname=firstname, 
                    lastname=lastname,
                    form_filled=False
                )
                context = {
                    'form': form,
                    'appointment_details': response,
                    'patient_id': patient_id
                }
                return render(request, self.template_name, context)

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

class DemographicsFormView(FormView):
    form_class = PatientDemographicsForm
    template_name = 'checkin_kiosk/demographics.html'

    def dispatch(self, request, *args, **kwargs):
        self.api_access = API_Access(get_user_access_token(request.user))
        self.patient_id = int(self.kwargs['patient_id'])
        self.patient_info = self.api_access.get_patient_information(self.patient_id)
        return super(DemographicsFormView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DemographicsFormView, self).get_context_data(**kwargs)
        context['patient_info'] = self.patient_info
        return context

    def get_initial(self):
        return self.patient_info

    def form_valid(self, form):
        data = form.cleaned_data
        patient_id = self.patient_id
        doctor_id = self.patient_info['doctor']
        data.update({
            'doctor': doctor_id
        })
        self.patient_updated_info = self.api_access.edit_patient_information(patient_id, data)
        name = data['first_name'] + ' ' + data['last_name']
        if self.patient_updated_info.status_code != Shortcuts.ErrorCodes.SUCCESS:
            print 'Error updating patient info'
            return HttpResponseRedirect(reverse('demographic_form', args=[patient_id]))

        else:
            self.appointment = self.api_access.get_appointments_by_patient_name(
                firstname = data['first_name'],
                lastname = data['last_name'],
                form_filled = True
            )
            appointment_id = self.appointment['id']
            self.appointment['status'] = Shortcuts.Statuses.ARRIVED 
            response = self.api_access.edit_appointment_information(appointment_id, self.appointment)
            if response.status_code != Shortcuts.ErrorCodes.SUCCESS:
                return HttpResponseRedirect(reverse('demographic_form', args=[patient_id]))

            else:
                appointment_obj, created = AppointmentHistory.objects.get_or_create(
                    name=name,
                    appointment_id=appointment_id,
                    patient_id=patient_id,
                    status=Shortcuts.Statuses.ARRIVED,
                    appointment_start_time=parser.parse(self.appointment['scheduled_time']),
                    appointment_duration=self.appointment['duration']
                )
                if created:
                    try:
                        appointment_obj.save()
                    except Exception as e:
                        return HttpResponseRedirect(reverse('demographic_form', args=[patient_id]))
                else:
                    appointment_obj.status = Shortcuts.Statuses.ARRIVED
                    appointment_obj.appointment_start_time = parser.parse(self.appointment['scheduled_time'])
                    appointment_obj.appointment_duration = self.appointment['duration']
                    appointment_obj.status_time = datetime.datetime.now()
                    appointment_obj.save()
            
                return HttpResponseRedirect(reverse('success', args=[self.appointment['exam_room']]))

class SuccessPageView(FormView):
    template_name = 'checkin_kiosk/success.html'
    
    def get(self, request, *args, **kwargs):
        room_id = kwargs['room_id']
        context = {
            'room_id': room_id
        }
        return render(request, self.template_name, context)

class DoctorPageView(FormView):
    template_name = 'checkin_kiosk/doctor_page.html'

    def get(self, request, *args, **kwargs):
        AppointmentHistory.objects.all().delete()
        current_appointment, appointments = split_appointments(request)
        context = {
            'current_appointment': current_appointment,
            'appointments': appointments,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'refresh' in request.POST:
            AppointmentHistory.objects.all().delete()
            current_appointment, appointments = split_appointments(request)
            context = {
                'current_appointment': current_appointment,
                'appointments': appointments,
            }
            return render(request, self.template_name, context)

        elif 'begin' in request.POST:
            appointment_id = request.POST.get('appointment_id')
            patient_id = request.POST.get('patient_id')
            appointment, created = AppointmentHistory.objects.get_or_create(
                appointment_id=appointment_id, 
                patient_id=patient_id
            )
            print appointment.status_time
            check_in_time = appointment.status_time
            appointment.status = Shortcuts.Statuses.IN_SESSION
            appointment.session_start_time = datetime.datetime.now()
            appointment.status_time = appointment.session_start_time
            appointment.save()
            app_id = appointment.appointment_id
            start_time = appointment.status_time
            wait_time = get_wait_time(check_in_time, start_time)[0]
            wait_time_obj, created = AverageWaitTime.objects.get_or_create(
                appointment_id=app_id,
                wait_time=wait_time
            )
            return HttpResponseRedirect(reverse('complete_session', args=[appointment_id]))

class CompleteSessionPageView(FormView):
    template_name = 'checkin_kiosk/complete_session.html'

    def get(self, request, *args, **kwargs):
        appointment_id = kwargs['appointment_id']
        current_appointment = AppointmentHistory.objects.get(appointment_id=appointment_id)
        context = {
            'current_appointment': current_appointment,
            'completed_appointment': None
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        appointment_id = kwargs['appointment_id']
        appointment = AppointmentHistory.objects.get(appointment_id=appointment_id)
        curr_appointment = appointment
        appointment.status = Shortcuts.Statuses.COMPLETE
        appointment.session_end_time = datetime.datetime.now()
        appointment.status_time = appointment.session_end_time
        appointment.save()
        comp_appointment = AppointmentHistory.objects.get(appointment_id=appointment_id)
        context = {
            'current_appointment': curr_appointment,
            'completed_appointment': comp_appointment
        }
        return render(request, self.template_name, context)

def AverageWaitTimeView(request):
    template_name = 'checkin_kiosk/wait_time.html'
    wait_time_objects = AverageWaitTime.objects.all()
    print wait_time_objects
    if not wait_time_objects:
        average_wait_time = 0
    else:
        wait_times = []
        for wait_time_obj in wait_time_objects:
            wait_times.append(wait_time_obj.wait_time)
        average_wait_time = get_average_wait_time(wait_times)[0]
    context = {
        'average_wait_time': average_wait_time
    }
    return render(request, template_name, context)

    








        
        

