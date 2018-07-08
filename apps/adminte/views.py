import os

from django.shortcuts import render
from django.views.generic import View
from django.http import QueryDict
from django.views.decorators.http import require_POST,require_GET
from django.conf import settings
import qiniu

from .models import NewCategory
from utils import restful


def login_view(request):
    return render(request,'adminlte/login.html')


def backed_index(request):
    return render(request, 'adminlte/index.html')


def write_news(request):
    return render(request, 'adminlte/write_news.html')


# def news_category(request):
#     return render(request, 'adminlte/news_category.html')

class NewsCategory(View):
    def get(self,request):
        categorys = NewCategory.objects.all()
        return render(request,'adminlte/news_category.html',context={'categorys':categorys})

    def post(self,request):
        category = request.POST.get("category","")
        nums = request.POST.get("nums","")
        print(category,nums)
        NewCategory.objects.create(name=category,nums=nums)
        return restful.ok()

    def put(self,request):
        qd = QueryDict(request.body)
        put_dict = {k: v[0] if len(v) == 1 else v for k, v in qd.lists()}
        category_id = put_dict.get("category_id","")
        category_name = put_dict.get("category_name","")
        nums = put_dict.get("nums","")
        category = NewCategory.objects.get(pk=category_id)
        category.name = category_name
        category.nums = nums
        category.save()
        return restful.ok()

    def delete(self,request):
        qd = QueryDict(request.body)
        delete_dict = {k: v[0] if len(v) == 1 else v for k, v in qd.lists()}
        category_id = delete_dict.get("category_id", "")
        NewCategory.objects.get(pk=category_id).delete()
        return restful.ok()


def categorydetail(request,category_id):
    category = NewCategory.objects.filter(pk=int(category_id)).first()
    return render(request,"adminlte/news_category_edit.html",context={"category":category})


# 处理layer open的模板
def templateview(request,template):
    return render(request,'adminlte/%s' % template)


@require_POST
def upload_file(request):
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT,name),'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL+name)
    # http://127.0.1:8000/media/abc.jpg
    return restful.result(data={'url':url})


@require_GET
def qntoken(request):
    access_key = settings.QINIU_ACCESS_KEY
    secret_key = settings.QINIU_SECRET_KEY

    bucket = settings.QINIU_BUCKET_NAME
    q = qiniu.Auth(access_key,secret_key)

    token = q.upload_token(bucket)

    return restful.result(data={"token":token})