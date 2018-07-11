#!/usr/bin/python3
# -*- coding:utf-8 -*-
from django import forms

from apps.news.models import NewsCategory,News
from apps.forms import FormMiXin


class WriteNewsForm(forms.ModelForm,FormMiXin):
    category = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category','author','pub_time']