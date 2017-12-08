from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import CheckInPageView, DemographicsFormView, SuccessPageView, DoctorPageView, CompleteSessionPageView, AverageWaitTimeView

urlpatterns = [
    url(r'^app/$', CheckInPageView.as_view(), name='search_appointment'),
    url(
        r'^app/update_info/(?P<patient_id>\d+)$', 
        DemographicsFormView.as_view(), 
        name='demographic_form'
    ),
    url(r'^app/success/(?P<room_id>\d+)$', SuccessPageView.as_view(), name='success'),
    url(r'^app/dashboard$', DoctorPageView.as_view(), name='doctor_page'),
    url(
        r'^app/complete/(?P<appointment_id>\d+)$', 
        CompleteSessionPageView.as_view(), 
        name='complete_session'
    ),
    url(r'^app/wait_time/$', AverageWaitTimeView, name='wait_time'),
]

urlpatterns += staticfiles_urlpatterns()