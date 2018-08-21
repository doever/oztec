#!/usr/bin/python3
# -*- coding:utf-8 -*-
from django import forms

from apps.news.models import NewsCategory, News
from .models import Banner
from apps.forms import FormMiXin


class WriteNewsForm(forms.ModelForm,FormMiXin):
    category = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category', 'author', 'pub_time']


class AddBannerFrom(forms.ModelForm, FormMiXin):

    class Meta:
        model = Banner
        exclude = ['add_time']
        error_messages = {
            'banner_url': {
                'require': '请传入轮播图地址',
                'invalid': '请传入合法的参数'
            },
            'position': {
                'require': '请传入优先级',
                'invalid': '请传入合法的参数'
            },
            'link_url': {
                'require': '请传入轮播图地址',
                'invalid': '请传入合法的参数'
            }
        }