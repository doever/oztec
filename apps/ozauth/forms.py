from django import forms
from django.core import validators
from django.core.cache import cache

from apps.forms import FormMiXin
from .models import User


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


class RegisterForm(forms.Form,FormMiXin):
    telephone = forms.CharField(validators=[validators.RegexValidator(r'1[3-9]\d{9}',message='手机号码格式错误')],error_messages={
        'required': '请输入手机号码'
    })
    username = forms.CharField(max_length=20,error_messages={
        'max_length':'用户名超出长度',
        'invalid':'请输入有效的用户名'
    })
    password = forms.CharField(max_length=16,min_length=6,error_messages={
        'max_length':'密码过长',
        'min_length':'密码过短'
    })
    re_password = forms.CharField(max_length=16, min_length=6, error_messages={
        'max_length': '密码过长',
        'min_length': '密码过短'
    })
    sms_captcha = forms.CharField(min_length=4,max_length=4)
    img_captcha = forms.CharField(min_length=4,max_length=4)

    def clean(self):
        cleaned_data = super(RegisterForm,self).clean()
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')
        telephone = cleaned_data.get('telephone')

        if password != re_password:
            raise forms.ValidationError(message='两次密码不一致')

        sms_captcha = cleaned_data.get('sms_captcha')
        cache_sms_captcha = cache.get(telephone)
        if not cache_sms_captcha or sms_captcha.lower() != cache_sms_captcha.lower():
            raise forms.ValidationError(message='短信验证码错误')

        img_captcha = cleaned_data.get('img_captcha')
        try:
            cache_img_captcha = cache.get(img_captcha.lower())
        except:
            raise forms.ValidationError(message='请输入图形验证码')

        if not cache_img_captcha or img_captcha != cache_img_captcha:
            raise forms.ValidationError(message='图形验证码错误')

        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            raise forms.ValidationError(message='该用户手机已注册')

        return cleaned_data


