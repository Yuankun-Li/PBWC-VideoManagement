# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-19 02:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('videomanagement', '0013_auto_20170418_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommitteeAction',
            fields=[
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.CharField(choices=[('meeting', 'meeting'), ('make_public', 'make_public'), ('inspect_video', 'inspect_video'), ('extend_retention', 'extend_retention'), ('privatize_video', 'privatize_video')], default='meeting', max_length=20)),
                ('request_date', models.DateTimeField()),
                ('policy_justification', models.CharField(max_length=1000)),
                ('committee_text_reason', models.CharField(max_length=1000)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videomanagement.Video')),
            ],
        ),
    ]
