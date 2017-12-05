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
from .models import Appointment
from .api_access import API_Access
from .shortcuts import Shortcuts

#from dateutil import parser
import datetime

def get_user_access_token(user):
    return user.social_auth.get(provider='drchrono').extra_data['access_token']

# Create your views here.
class CheckInView(View):
    form_class = PatientSignInForm
    template_name = 'checkin_kiosk/checkin_page.html'

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
            first_name = clean['patient_first_name']
            last_name = clean['patient_last_name']
            patient_id = api_request.get_patient_id(firstname=first_name, lastname=last_name)
            if patient_id is None:
                context = {
                    'form': form,
                    'cred': Shortcuts.Validations.INVALID_CREDENTIALS
                }
                return render(request, self.template_name, context)

            else:
                response = api_request.get_appointments_by_patient_name(
                    firstname=first_name, 
                    lastname=last_name
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



        
        

