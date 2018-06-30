#!/usr/bin/python3
from django.shortcuts import render,redirect,reverse

def payinfo_index(request):
    return render(request,'payinfo/payinfo.html')
