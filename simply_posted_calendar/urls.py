from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'get_all/$', views.get_all),
    url(r'get_new/$', views.get_new),
    url(r'(?P<pk>\d+)/approve/$', views.approve),
    url(r'(?P<pk>\d+)/reject/$', views.reject),
    url(r'(?P<pk>\d+)/publish/$', views.publish)
]
