#!/usr/bin/python3
# -*- coding:utf-8 -*-
from django import forms

from .models import NewsCategory,News,Comment
from apps.forms import FormMiXin


class PublishComment(forms.ModelForm,FormMiXin):
    class Meta:
        model = Comment
        fields = ['content','new']