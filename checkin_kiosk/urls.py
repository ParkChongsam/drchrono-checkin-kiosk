from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import views

urlpatterns = [
    url(r'',views.CheckInView.as_view(), name="search_appointment"),
]