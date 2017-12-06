from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import CheckInPageView, DemographicsFormView, SuccessPageView, DoctorPageView, CompleteSessionPageView

urlpatterns = [
    url(r'^accounts/profile/', CheckInPageView.as_view(), name='search_appointment'),
    url(
        r'^accounts/profile/update_info/(?P<patient_id>\d+)$', 
        DemographicsFormView.as_view(), 
        name='demographic_form'
    ),
    url(r'^accounts/profile/success/(?P<room_id>\d+)$', SuccessPageView.as_view(), name='success'),
    url(r'^accounts/profile/dashboard$', DoctorPageView.as_view(), name='doctor_page'),
    url(
        r'^accounts/profile/complete/(?P<appointment_id>\d+)$', 
        CompleteSessionPageView.as_view(), 
        name='complete_session'
    ),
]

urlpatterns += staticfiles_urlpatterns()