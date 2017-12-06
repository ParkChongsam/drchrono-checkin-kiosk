from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'', include('social_django.urls', namespace='social')),
    url(r'^checkin_kiosk/', include('checkin_kiosk.urls')),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()