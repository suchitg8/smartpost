from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'(?P<pk>\d+)/approve/$', views.approve),
    url(r'(?P<pk>\d+)/reject/$', views.approve)
]
