from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import views

urlpatterns = [
    url(r'^search/',views.CheckInView.as_view(), name="search_appointment"),
    url(r'^search/update_info/(?P<patient_id>\d+)$', views.DemographicsFormView.as_view(), name='demographic_form'),
    url(r'^search/success/(?P<room_id>\d+)$', views.SuccessView.as_view(), name='success'),
]

urlpatterns += staticfiles_urlpatterns()