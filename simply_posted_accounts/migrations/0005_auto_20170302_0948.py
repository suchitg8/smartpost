# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-02 09:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simply_posted_accounts', '0004_auto_20170302_0944'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dbform',
            old_name='imagelink',
            new_name='image_link',
        ),
    ]