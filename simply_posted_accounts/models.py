from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Added by vikrant
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _

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

# Code added by vikrant
class ContentProvider(TimeStampedModel):
    first_name = models.CharField(
        max_length=50,
        verbose_name=_("First Name"),
        help_text=_("Enter the first name")
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name=_("Last Name"),
        help_text=_("Enter the last name")
    )
    email = models.CharField(
        max_length=50,
        verbose_name=_("email"),
        help_text=_("Enter the your email name")
    )
    password = models.CharField(
        max_length=80,
        verbose_name=_("password"),
        help_text=_("Enter the password (min 8 character)")
    )
    customer_id = models.CharField(
        max_length=80,default=None, null=True, blank=True
    )
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.email


# Import Table
class DBform(TimeStampedModel):
    playful_title = models.CharField(
        max_length=200,
        verbose_name=_("Play Full"),
        help_text=_("Enter the playful title")
    )
    corporate_title = models.CharField(
        max_length=200,
        verbose_name=_("Corporate Title"),
        help_text=_("Enter the corporate title")
    )
    blog_link = models.CharField(
        max_length=200,
        verbose_name=_("Blog Link"),
        help_text=_("Enter the Blog Link")
    )
    image_link = models.CharField(
        max_length=200,
        verbose_name=_("Image Link"),
        help_text=_("Enter the image link")
    )
    category  = models.CharField(
        max_length=5,
        verbose_name=_("category"),
        help_text=_("Enter the category")
    )
    contentprovider = models.ForeignKey(ContentProvider, default=None, null=True, blank=True)