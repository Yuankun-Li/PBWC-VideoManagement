# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-23 18:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videomanagement', '0004_auto_20170323_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]