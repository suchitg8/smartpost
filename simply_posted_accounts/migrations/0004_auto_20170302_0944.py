# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-02 09:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('simply_posted_accounts', '0003_contentprovider_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='DBform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('playful_title', models.CharField(help_text='Enter the playful title', max_length=200, verbose_name='Play Full')),
                ('corporate_title', models.CharField(help_text='Enter the corporate title', max_length=200, verbose_name='Corporate Title')),
                ('blog_link', models.CharField(help_text='Enter the Blog Link', max_length=200, verbose_name='Blog Link')),
                ('imagelink', models.CharField(help_text='Enter the image link', max_length=200, verbose_name='Image Link')),
                ('category', models.CharField(help_text='Enter the category', max_length=5, verbose_name='category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='contentprovider',
            name='password',
            field=models.CharField(help_text='Enter the password (min 8 character)', max_length=80, verbose_name='password'),
        ),
        migrations.AddField(
            model_name='dbform',
            name='contentwriter',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='simply_posted_accounts.ContentProvider'),
        ),
    ]