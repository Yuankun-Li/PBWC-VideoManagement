# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-13 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videomanagement', '0009_auto_20170413_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='location',
            field=models.CharField(choices=[('Gates Center for Computer Science', 'Gates Center for Computer Science'), ('Cyert Hall', 'Cyert Hall'), ('Cohon University Center', 'Cohon University Center'), ('Hunt Library', 'Hunt Library'), ('Other place', 'Other place')], default='Gates Center for Computer Science', max_length=128),
        ),
    ]
