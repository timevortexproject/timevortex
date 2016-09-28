# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-09-23 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timevortex', '0007_auto_20160923_1349'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('value', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
