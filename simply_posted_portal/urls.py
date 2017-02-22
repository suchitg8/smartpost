from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib import admin
from calendarium.views import MonthView, CalendariumRedirectView

import simply_posted_accounts.views


urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r"^account/confirm_email/(?P<key>\w+)/$", simply_posted_accounts.views.ConfirmEmailView.as_view(), name="account_confirm_email"),
    url(r"^account/schedule/(?P<year>\d+)/(?P<month>\d+)/$", MonthView.as_view(template_name='account/schedule.html'), name="calendar_month"),
    url(r"^account/schedule/$", login_required(CalendariumRedirectView.as_view(), login_url='/account/login/'),name='calendar_current_month'),
    url(r"^account/social/$", login_required(simply_posted_accounts.views.social_profile_settings, login_url='/account/login/'), name="social_profiles_settings"),
    url(r"^account/voice/$", simply_posted_accounts.views.VoiceView.as_view(), name="voice_settings"),
    url(r"^account/signup/$", simply_posted_accounts.views.SignupView.as_view(template_name="account/signup.html"), name="account_signup"),
    url(r"^account/login/$", simply_posted_accounts.views.LoginView.as_view(), name="account_signup"),
    url(r"^account/", include("account.urls")),
    url(r"^payments/", include("pinax.stripe.urls"))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
