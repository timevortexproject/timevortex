# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-04 11:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('energy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentcostsetting',
            name='tty_port',
            field=models.CharField(default='/dev/currentcost', max_length=200),
            preserve_default=False,
        ),
    ]
