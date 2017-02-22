from django import forms
from django.utils.translation import ugettext_lazy as _
from account.conf import settings
from simply_posted_accounts.models import business_type_choices, \
    market_type_choices, \
    temp_type_choices
import account.forms

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = None


class SignupForm(account.forms.SignupForm):

    company = forms.CharField(
        label=_("Company"),
        max_length=50,
        widget=forms.TextInput(), required=True)

    first_name = forms.CharField(
        label=_("First Name"),
        max_length=30,
        widget=forms.TextInput(), required=True)

    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=30,
        widget=forms.TextInput(), required=True)

    timezone = forms.ChoiceField(
        label=_("Timezone"),
        choices=[("", "---------")] + settings.ACCOUNT_TIMEZONES,
        required=True)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        del self.fields["username"]
        field_order = ["company", "first_name", "last_name", "email",
                       "password", "password_confirm", "timezone",
                       "code"]
        if not OrderedDict or hasattr(self.fields, "keyOrder"):
            self.fields.keyOrder = field_order
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in field_order)


class VoiceForm(account.forms.SignupForm):

    business_type = forms.ChoiceField(
        label=_('Would you say your business is more "topical" or "promotional?"'),
        choices=business_type_choices,
        required=False)

    market_type = forms.ChoiceField(
        label=_('Do you want to target a "niche" market or make your '
                'content to the "general" real estate field?'),
        choices=market_type_choices,
        required=False)

    temp_type = forms.ChoiceField(
        label=_('Would you say your business is more "lighthearted" or "corporate?"'),
        choices=temp_type_choices,
        required=False)

    about_business = forms.CharField(
        label=_('Tell us about your business? Tell us about your IDEAL clients. '
                'What made them great?'),
        widget=forms.Textarea(),
        max_length=100,
        required=False)

    about_topics = forms.CharField(
        label=_('Tell us about the current topics, blogs, websites you visit '
                'today and share regularly?'),
        widget=forms.Textarea(),
        max_length=100,
        required=False)

    def __init__(self, *args, **kwargs):
        super(VoiceForm, self).__init__(*args, **kwargs)
        field_order = ["business_type", "market_type", "temp_type",
                       "about_business", "about_topics"]
        if not OrderedDict or hasattr(self.fields, "keyOrder"):
            self.fields.keyOrder = field_order
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in field_order)