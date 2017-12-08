# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class AppointmentHistory(models.Model):
    name = models.CharField(max_length=100, null=True)
    appointment_id = models.IntegerField()
    patient_id = models.IntegerField(null=True)
    status_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    appointment_start_time = models.DateTimeField(null=True)
    appointment_duration = models.IntegerField(null=True)
    session_start_time = models.DateTimeField(null=True)
    session_end_time = models.DateTimeField(null=True)
    check = models.BooleanField(default=False)

    class Meta:
        unique_together = ('appointment_id', 'appointment_start_time')
        ordering = ['-status_time']

class AverageWaitTime(models.Model):
    appointment_id = models.IntegerField(null=True)
    wait_time = models.IntegerField(null=True)

    def __unicode__(self):
        return str(self.wait_time)