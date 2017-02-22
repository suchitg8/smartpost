from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "simply_posted_portal"

    def ready(self):
        import_module("simply_posted_portal.receivers")
