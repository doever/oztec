#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'doever'
__date__ = '2018/7/24 9:27'

from django.shortcuts import redirect, reverse


def login_require(func):
    print('wrapper running')
    def wrapper(request, **kwargs):
        if not request.user:
            print('running')
            return redirect(reverse('adminlte:login'))
        return func(request, **kwargs)
    return wrapper
