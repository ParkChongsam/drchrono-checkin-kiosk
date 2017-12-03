from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin

import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'', include('social_django.urls', namespace='social')),
    url(r'^birthday_reminder/', include('birthday_reminder.urls')),
    url(r'^admin/', admin.site.urls),
]