#!/usr/bin/python3
from django.urls import path
from . import views

app_name = 'payinfo'
urlpatterns = [
    path('',views.payinfo_index,name='payinfo_index'),
]