#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'doever'
__date__ = '2018/8/7 20:46'

from utils import restful
from django.shortcuts import redirect


def auth_login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message='请先登录')
            else:
                return redirect('/')
    return wrapper

