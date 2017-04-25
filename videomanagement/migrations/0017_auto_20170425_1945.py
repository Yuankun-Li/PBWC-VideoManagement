# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-25 19:45
from __future__ import unicode_literals

from django.db import migrations, models
import django_encrypted_filefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('videomanagement', '0016_auto_20170422_0317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingrequest',
            name='location',
            field=models.CharField(choices=[('Gates Center for Computer Science', 'Gates Center for Computer Science'), ('Cyert Hall', 'Cyert Hall'), ('Cohon University Center', 'Cohon University Center'), ('Hunt Library', 'Hunt Library'), ('Other place', 'Other place'), ('Morewood Apartments', 'Morewood Apartments')], default='Gates Center for Computer Science', max_length=128),
        ),
        migrations.AlterField(
            model_name='video',
            name='location',
            field=models.CharField(choices=[('Gates Center for Computer Science', 'Gates Center for Computer Science'), ('Cyert Hall', 'Cyert Hall'), ('Cohon University Center', 'Cohon University Center'), ('Hunt Library', 'Hunt Library'), ('Other place', 'Other place'), ('Morewood Apartments', 'Morewood Apartments')], default='Gates Center for Computer Science', max_length=128),
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=django_encrypted_filefield.fields.EncryptedFileField(blank=True, upload_to='videos'),
        ),
    ]
