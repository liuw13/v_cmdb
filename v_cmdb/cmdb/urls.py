
from django.urls import path,re_path,include
from .views import *

urlpatterns = [
    re_path('^dashboard/$', DashBoardView.as_view()),
    re_path('^api_dashboard/$', APIDashBaord.as_view()),
    re_path('^idcs/(?P<pk>\d+)?/?',IdcView.as_view()),
    re_path('^api_idcs/(?P<pk>\d+)?/?',APIIdcView.as_view()),
    re_path('^racks/(?P<pk>\d+)?/?', RackView.as_view()),
    re_path('^api_racks/(?P<pk>\d+)?/?', APIRackView.as_view()),
    re_path('^servers/(?P<pk>\d+)?/?', ServerView.as_view()),
    re_path('^api_servers/(?P<pk>\d+)?/?', APIServerView.as_view()),
    re_path('^vms/(?P<pk>\d+)?/?', VmView.as_view()),
    re_path('^api_vms/(?P<pk>\d+)?/?', APIVmView.as_view())
]