# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-09-23 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timevortex', '0008_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='value',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]