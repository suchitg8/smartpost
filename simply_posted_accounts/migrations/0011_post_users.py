# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-07 14:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('simply_posted_calendar', '0007_publication_reject_count'),
        ('simply_posted_accounts', '0010_socialprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='users',
            field=models.ManyToManyField(through='simply_posted_calendar.Publication', to=settings.AUTH_USER_MODEL),
        ),
    ]