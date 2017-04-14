# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-09 03:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videomanagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='content_type',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(blank=True, upload_to='videos'),
        ),
    ]