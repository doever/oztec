from django import forms
from apps.forms import FormMiXin
from django.core import validators

class LoginForm(forms.Form,FormMiXin):
    telephone = forms.CharField(validators=[validators.RegexValidator(r'1[3-9]\d{9}',message='手机号码格式错误')],error_messages={
        'required': '请输入手机号码'
    })
    password = forms.CharField(max_length=16,min_length=6,error_messages={
        'max_length':'密码不能超过16位',
        'min_length': '密码不能少于6位',
        'required':'请输入密码'
    })
    remember = forms.IntegerField(required=False)


