from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse,JsonResponse
from .forms import LoginForm
from utils import restful
from django.shortcuts import render,redirect,reverse
from utils.captcha.ozcaptcha import Captcha
from io import BytesIO
from utils.aliyunsmssdk import aliyunsms
from apps.ozauth.models import User
from django.core.cache import cache

def add_user(request):
    username='long'
    telephone='15122223333'
    password='111111'
    email = '1584@12com'
    User.object.create_user(username=username,password=password,telephone=telephone,email=email)
    return HttpResponse('成功')


@require_POST
def login_view(request):
    forms = LoginForm(request.POST)
    if forms.is_valid():
        telephone = forms.cleaned_data.get('telephone')
        password = forms.cleaned_data.get('password')
        remember = forms.cleaned_data.get('remember')
        user = authenticate(request,username=telephone,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:
                return restful.unauth(message='您的账号已被冻结')
        else:
            return restful.params_error(message='您的账号或密码错误')

    else:
        errors = forms.get_errors()
        return restful.params_error(message=errors)

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

# 生成验证码
def img_captcha(request):
    text,image = Captcha().gene_code()
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    cache.set(text.upper(),text.upper(),5*60)
    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()
    return response


def sms_code(request):
    telephone = request.GET.get('telephone')
    code = Captcha.gene_text()
    aliyunsms.send_sms(phone_numbers=telephone,code=code)
    cache.set(telephone,code,5*60)
    return restful.ok()

def test_cache(request):
    cache.set('username','chilo',60)
    username=cache.get('username')
    return HttpResponse(username)
