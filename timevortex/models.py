#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

from django.db import models


class Sites(models.Model):
    """Sites model.
    """
    NO_TYPE = None
    METEAR_TYPE = 'METEAR'
    SITE_TYPE_CHOICES = (
        (NO_TYPE, 'Pas de type particulier'),
        (METEAR_TYPE, 'METEAR'),
    )

    label = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    site_type = models.CharField(
        max_length=2,
        choices=SITE_TYPE_CHOICES,
        default=NO_TYPE
    )

    def __str__(self):
        return self.label
