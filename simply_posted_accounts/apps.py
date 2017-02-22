from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SimplyPostedAccountsConfig(AppConfig):
    name = 'simply_posted_accounts'
    label = 'simply_posted_accounts'
    verbose_name = _('Simply Posted Account Portal')
