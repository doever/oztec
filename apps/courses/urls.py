#!/usr/bin/python3
from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
    path('',views.courses_index,name='courses_index'),
    path('<int:courses_id>',views.courses_detail,name='courses_detail'),
]