from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^idcs/(?P<pk>\d+)?/?$', IdcView.as_view(), name='idcs'),
    url(r'^api_idcs/(?P<pk>\d+)?/?$', APIIdcView.as_view(), name='api_idcs'),
    url(r'^racks/(?P<pk>\d+)?/?$', RackView.as_view(), name='racks'),
    url(r'^api_racks/(?P<pk>\d+)?/?$', APIRackView.as_view(), name='api_racks'),
    url(r'^servers/(?P<pk>\d+)?/?$', ServerView.as_view(), name='servers'),
    url(r'^api_servers/?(?P<pk>\d+)?/?$', APIServerView.as_view(), name='api_servers'),
    url(r'^dashboard/$', DashBoardView.as_view(), name='dashboard'),
    url(r'^api_dashboard/$', APIDashBoardView.as_view(), name='apidashboard'),
    url(r'^vms/(?P<pk>\d+)?/?$', VmView.as_view(), name='vms'),
    url(r'^api_vms/?(?P<pk>\d+)?/?$', APIVmView.as_view(), name='api_vms'),

]