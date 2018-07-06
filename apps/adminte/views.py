from django.shortcuts import render
from django.views.generic import View
from django.http import QueryDict

from .models import NewCategory
from utils import restful


def login_view(request):
    return render(request,'adminlte/login.html')


def backed_index(request):
    return render(request, 'adminlte/index.html')


def news_add(request):
    return render(request, 'adminlte/news_add.html')


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


