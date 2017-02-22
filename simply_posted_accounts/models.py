from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

business_type_choices = (
    ('', '---'),
    ('promotional', 'Promotional'),
    ('topical', 'Topical'))

market_type_choices = (
    ('', '---'),
    ('niche', 'Niche market (age, income, location'),
    ('general', 'General market (anyone looking for real estate'))

temp_type_choices = (
    ('', '---'),
    ('corporate', 'Corporate'),
    ('between', 'Somewhere in between'),
    ('lighthearted', 'Lighthearted'))


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    social_report_project_id = models.CharField(max_length=50)
    social_report_user_id = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    business_type = models.CharField(max_length=50)
    market_type = models.CharField(max_length=50)
    temp_type = models.CharField(max_length=50)
    about_business = models.CharField(max_length=100)
    about_topics = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Simply Posted Customer Profiles'
        verbose_name_plural = 'Simply Posted Customer Profiles'


class EmployeeInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Customer Profile'


class UserAdmin(BaseUserAdmin):

    inlines = (EmployeeInline, )

    def company(self, obj):
        try:
            return obj.profile.company
        except UserProfile.DoesNotExist:
            return ''

    list_display = BaseUserAdmin.list_display + ('company',)
    search_fields = BaseUserAdmin.search_fields + ('profile__company',)