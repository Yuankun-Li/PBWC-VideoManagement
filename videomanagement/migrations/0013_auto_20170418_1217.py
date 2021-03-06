# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-18 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videomanagement', '0012_merge_20170416_2148'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meetingrequest',
            old_name='reasoning',
            new_name='description',
        ),
        migrations.AddField(
            model_name='meetingrequest',
            name='reason_for_request',
            field=models.CharField(default='foobar', max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='request',
            name='type',
            field=models.CharField(choices=[('extend_retention', 'extend_retention'), ('privatize_video', 'privatize_video'), ('register_complaint', 'register_complaint')], default='extend_retention', max_length=50),
        ),
    ]
