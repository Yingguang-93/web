from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UserNameCountView.as_view()),
    re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    re_path(r'^register/$', views.RegisterView.as_view()),
    re_path(r'^login/$', views.LoginView.as_view()),
    re_path(r'^logout/$', views.LogoutView.as_view()),
    re_path(r'^info/$', views.UserInfoView.as_view()),
    re_path(r'^emails/$', views.UserEmailView.as_view()),
    re_path(r'^emails/verification/$', views.VerifyEmailView.as_view()),
    re_path(r'^addresses/create/$', views.IncreaseAddressVIew.as_view()),
    re_path(r'^addresses/$', views.ShowAddressView.as_view()),
    re_path(r'^addresses/(?P<address_id>\d+)/$', views.ChangeDestryAddressView.as_view()),
    re_path(r'^addresses/(?P<address_id>\d+)/default/$', views.DefaultView.as_view()),
    re_path(r'^addresses/(?P<address_id>\d+)/title/$', views.TetilView.as_view()),
    re_path(r'^password/$', views.ChangePasswordView.as_view()),
]
