# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-07 16:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simply_posted_calendar', '0007_publication_reject_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='corporate_title',
            field=models.BooleanField(default=True),
        ),
    ]
