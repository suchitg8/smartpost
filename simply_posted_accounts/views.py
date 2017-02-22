from django.shortcuts import redirect
from django.views.generic.edit import FormView
from account.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from account.utils import default_redirect
from account.conf import settings
from account.models import EmailAddress
from social_django.models import UserSocialAuth
import account.forms
import account.views
import simply_posted_accounts.forms
import requests
import time

def social_profile_settings(request):
    user = request.user

    try:
        pinterest_login = user.social_auth.get(provider='pinterest')
    except UserSocialAuth.DoesNotExist:
        pinterest_login = None

    try:
        linkedin_login = user.social_auth.get(provider='linkedin-oauth2')
    except UserSocialAuth.DoesNotExist:
        linkedin_login = None

    try:
        instagram_login = user.social_auth.get(provider='instagram')
    except UserSocialAuth.DoesNotExist:
        instagram_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'account/social.html', {
        'pinterest_login': pinterest_login,
        'linkedin_login': linkedin_login,
        'instagram_login': instagram_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

class LoginView(account.views.LoginView):

    form_class = account.forms.LoginEmailForm

class SignupView(account.views.SignupView):

    form_class = simply_posted_accounts.forms.SignupForm
    identifier_field = "email"

    def after_signup(self, form):
        self.create_profile(form)
        self.set_timezone(form)
        super(SignupView, self).after_signup(form)

    def create_profile(self, form):
        self.created_user.first_name = form.cleaned_data["first_name"]
        self.created_user.last_name = form.cleaned_data["last_name"]
        self.created_user.save()
        profile = self.created_user.profile
        profile.company = form.cleaned_data["company"]
        profile.save()

    def set_timezone(self,form):
        fields = {}
        fields["timezone"] = form.cleaned_data["timezone"]
        if fields:
            account = self.created_user.account
            for k, v in fields.items():
                setattr(account, k, v)
            account.save()

    def generate_username(self, form):
        return form.cleaned_data["email"]


class VoiceView(LoginRequiredMixin, FormView):

    template_name = "account/voice.html"
    form_class = simply_posted_accounts.forms.VoiceForm
    redirect_field_name = "next"
    messages = {
        "settings_updated": {
            "level": messages.SUCCESS,
            "text": _("Voice settings updated.")
        },
    }

    def get_form_class(self):
        # @@@ django: this is a workaround to not having a dedicated method
        # to initialize self with a request in a known good state (of course
        # this only works with a FormView)
        self.primary_email_address = EmailAddress.objects.get_primary(self.request.user)
        return super(VoiceView, self).get_form_class()

    def get_initial(self):
        initial = super(VoiceView, self).get_initial()
        if self.request.user.profile.business_type:
            initial["business_type"] = self.request.user.profile.business_type
        if self.request.user.profile.market_type:
            initial["market_type"] = self.request.user.profile.market_type
        if self.request.user.profile.temp_type:
            initial["temp_type"] = self.request.user.profile.temp_type
        if self.request.user.profile.about_business:
            initial["about_business"] = self.request.user.profile.about_business
        if self.request.user.profile.about_business:
            initial["about_topics"] = self.request.user.profile.about_topics
        return initial

    def update_voice(self, form):
        profile = self.request.user.profile
        if "business_type" in form.cleaned_data:
            profile.business_type = form.cleaned_data["business_type"]
        if "market_type" in form.cleaned_data:
           profile.market_type = form.cleaned_data["market_type"]
        if "temp_type" in form.cleaned_data:
            profile.temp_type = form.cleaned_data["temp_type"]
        if "about_business" in form.cleaned_data:
            profile.about_business = form.cleaned_data["about_business"]
        if "about_topics" in form.cleaned_data:
            profile.about_topics = form.cleaned_data["about_topics"]
        profile.save()


    def form_valid(self, form):
        self.update_voice(form)
        if self.messages.get("settings_updated"):
            messages.add_message(
                self.request,
                self.messages["settings_updated"]["level"],
                self.messages["settings_updated"]["text"]
            )
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        ctx = super(VoiceView, self).get_context_data(**kwargs)
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.POST.get(redirect_field_name, self.request.GET.get(redirect_field_name, "")),
        })
        return ctx

    def update_account(self, form):
        pass

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.VOICE_SETTINGS_REDIRECT_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)


class ConfirmEmailView(account.views.ConfirmEmailView):

    def create_social_report_user(self, confirmation):
        user = confirmation.email_address.user
        create_user_url = 'https://api.socialreport.com/projectAddUser.svc'
        headers = {
            'api_key': settings.SOCIAL_REPORT_API_TOKEN,
            'Content-Type': 'application/json'
        }
        params = {
            'project': user.profile.social_report_project_id,
            'email': user.email,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'company': user.profile.company,
            'password': user.password[0:10],
            'active': 'yes',
            'accounts': 'yes',
            'addAccount': 'yes',
            'agents': 'no',
            'campaigns': 'no',
            'publish': 'no_approve',
            'publication_review': 'no',
            'contacts': 'no',
            'export': 'no',
            'goals': 'no',
            'reports': 'no',
            'api': 'no',
            'notifications': 'no',
            'automations': 'no',
            'users': 'no'
        }
        retry = True
        while retry:
            response = requests.post(create_user_url, params=params, headers=headers)
            if response.status_code == requests.codes.ok:
                data = response.json()
                if type(data) == type(dict()):
                    if 'id' in data:
                        user.profile.social_report_user_id = item['id']
                        user.profile.save()
                        retry = False
                    elif 'error' in data:
                        if data['error'] == 'going to fast, one call per second is allowed':
                            print "API request too fast, retrying..."
                            time.sleep(0.5)
                        else:
                            # TODO Log this somewhere
                            print data['error']
                            retry = False
                    else:
                        # TODO Log this somewhere
                        print data
                        retry = False
                elif type(data) == type(list()):
                    for item in data:
                        if 'id' in item:
                            user.profile.social_report_user_id = item['id']
                            user.profile.save()
                            retry = False
                        elif 'error' in item:
                            if item['error'] == 'going to fast, one call per second is allowed':
                                print "API request too fast, retrying..."
                                time.sleep(.5)
                            else:
                                # TODO Log this somewhere
                                print item['error']
                                retry = False
                else:
                    # TODO Log this somewhere
                    print type(data)
                    retry = False

    def create_social_report_project(self, confirmation):
        user = confirmation.email_address.user
        create_project_url = 'https://api.socialreport.com/projectCreate.svc'
        headers = {
            'api_key': settings.SOCIAL_REPORT_API_TOKEN,
            'Content-Type': 'application/json'
        }
        params = {
            'name': user.profile.company,
            'timezone': user.account.timezone
        }
        retry = True
        while retry:
            response = requests.post(create_project_url, params=params, headers=headers)
            if response.status_code == requests.codes.ok:
                data = response.json()
                if type(data) == type(dict()):
                    if 'id' in data:
                        user.profile.social_report_project_id = item['id']
                        user.profile.save()
                        retry = False
                    elif 'error' in data:
                        if data['error'] == 'going to fast, one call per second is allowed':
                            print "API request too fast, retrying..."
                            time.sleep(0.5)
                        else:
                            # TODO Log this somewhere
                            print data['error']
                            retry = False
                    else:
                        # TODO Log this somewhere
                        print data
                        retry = False
                elif type(data) == type(list()):
                    for item in data:
                        if 'id' in item:
                            user.profile.social_report_project_id = item['id']
                            user.profile.save()
                            retry = False
                        elif 'error' in item:
                            if item['error'] == 'going to fast, one call per second is allowed':
                                print "API request too fast, retrying..."
                                time.sleep(.5)
                            else:
                                # TODO Log this somewhere
                                print item['error']
                                retry = False
                else:
                    # TODO Log this somewhere
                    print type(data)
                    retry = False

    def after_confirmation(self, confirmation):
        super(ConfirmEmailView, self).after_confirmation(confirmation)
        self.create_social_report_project(confirmation)
        self.create_social_report_user(confirmation)
