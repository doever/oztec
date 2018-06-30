#!/usr/bin/python3
from django.shortcuts import render,redirect,reverse

def courses_index(request):
    return render(request,'courses/course_index.html')

def courses_detail(request,courses_id):
    return render(request,'courses/course_detail.html')
