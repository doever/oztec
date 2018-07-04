#!/usr/bin/python3
from django.urls import path
from . import views

app_name = 'ozauth'
urlpatterns = [
    path("login/",views.login_view,name='login'),
    path("logout/",views.logout_view,name='logout'),
    path("img_captcha/",views.img_captcha,name='img_captcha'),
    path("sms_code/",views.sms_code,name='sms_code'),
    path("register/",views.register,name='register'),
    path("add/",views.add_user,name='add'),
    path("cache/",views.test_cache,name='cache'),
]