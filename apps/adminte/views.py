import os

from django.shortcuts import render
from django.views.generic import View
from django.http import QueryDict
from django.views.decorators.http import require_POST,require_GET
from django.conf import settings
import qiniu

from apps.news.models import NewsCategory
from utils import restful,login_require
from utils.login_require import login_require
from .forms import WriteNewsForm
from apps.news.models import News


class WriteNewsView(View):
    def get(self,request):
        categorys = NewsCategory.objects.all()
        context = {
            'categorys':categorys
        }
        return render(request, 'adminlte/write_news.html',context=context)

    def post(self,request):
        form = WriteNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.create(title=title, desc=desc, thumbnail=thumbnail, content=content, category=category, author=request.user)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


class NewsCategoryView(View):
    def get(self,request):
        categorys = NewsCategory.objects.all()
        return render(request,'adminlte/news_category.html',context={'categorys':categorys})

    def post(self,request):
        category = request.POST.get("category","")
        nums = request.POST.get("nums","")
        print(category,nums)
        NewsCategory.objects.create(name=category,nums=nums)
        return restful.ok()

    def put(self,request):
        qd = QueryDict(request.body)
        put_dict = {k: v[0] if len(v) == 1 else v for k, v in qd.lists()}
        category_id = put_dict.get("category_id","")
        category_name = put_dict.get("category_name","")
        nums = put_dict.get("nums","")
        category = NewsCategory.objects.get(pk=category_id)
        category.name = category_name
        category.nums = nums
        category.save()
        return restful.ok()

    def delete(self,request):
        qd = QueryDict(request.body)
        delete_dict = {k: v[0] if len(v) == 1 else v for k, v in qd.lists()}
        category_id = delete_dict.get("category_id", "")
        NewsCategory.objects.get(pk=category_id).delete()
        return restful.ok()


def categorydetail(request,category_id):
    category = NewsCategory.objects.filter(pk=int(category_id)).first()
    return render(request,"adminlte/news_category_edit.html",context={"category":category})


# 处理layer open的模板
def templateview(request,template):
    return render(request,'adminlte/%s' % template)


@require_POST
def upload_file(request):
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT,'newsthumbnail',name),'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL+'newsthumbnail/'+name)
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


def login_view(request):
    return render(request,'adminlte/login.html')


@login_require
def backed_index(request):
    print('aaaaaaaaaaa')
    return render(request, 'adminlte/index.html')