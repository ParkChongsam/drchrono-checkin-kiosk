# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('appointment_id', models.IntegerField()),
                ('patient_id', models.IntegerField(null=True)),
                ('status_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=20)),
                ('appointment_start_time', models.DateTimeField(null=True)),
                ('appointment_duration', models.IntegerField(null=True)),
                ('session_start_time', models.DateTimeField(null=True)),
                ('session_end_time', models.DateTimeField(null=True)),
                ('check', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-status_time'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together=set([('appointment_id', 'appointment_start_time')]),
        ),
    ]
