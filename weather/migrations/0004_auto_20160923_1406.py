# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-09-23 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0003_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='value',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
