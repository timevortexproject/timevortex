# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-24 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('site_type', models.CharField(
                    choices=[(None, 'Pas de type particulier'), ('METEAR', 'METEAR')], default=None, max_length=2)),
            ],
        ),
    ]
