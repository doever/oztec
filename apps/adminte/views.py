import os

import qiniu
from django.shortcuts import render
from django.views.generic import View
from django.http import QueryDict
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings
from django.core.paginator import Paginator

from apps.news.models import NewsCategory
from utils import restful, login_require
from utils.login_require import login_require
from .forms import WriteNewsForm, AddBannerFrom
from apps.news.models import News
from .models import Banner
from .serializers import BannerSerializer


class WriteNewsView(View):
    def get(self, request):
        categorys = NewsCategory.objects.all()
        context = {
            'categorys': categorys
        }
        return render(request, 'adminlte/write_news.html', context=context)

    def post(self, request):
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
    def get(self, request):
        categorys = NewsCategory.objects.all()
        return render(request, 'adminlte/news_category.html', context={'categorys': categorys})

    def post(self, request):
        category = request.POST.get("category", "")
        nums = request.POST.get("nums", "")
        print(category, nums)
        NewsCategory.objects.create(name=category, nums=nums)
        return restful.ok()

    def put(self, request):
        qd = QueryDict(request.body)
        put_dict = {k: v[0] if len(v) == 1 else v for k, v in qd.lists()}
        category_id = put_dict.get("category_id", "")
        category_name = put_dict.get("category_name", "")
        nums = put_dict.get("nums", "")
        category = NewsCategory.objects.get(pk=category_id)
        category.name = category_name
        category.nums = nums
        category.save()
        return restful.ok()

    def delete(self, request):
        qd = QueryDict(request.body)
        delete_dict = {k: v[0] if len(v) == 1 else v for k, v in qd.lists()}
        category_id = delete_dict.get("category_id", "")
        NewsCategory.objects.get(pk=category_id).delete()
        return restful.ok()


def categorydetail(request, category_id):
    category = NewsCategory.objects.filter(pk=int(category_id)).first()
    return render(request, "adminlte/news_category_edit.html", context={"category": category})


# 处理layer open的模板
def templateview(request, template):
    return render(request, 'adminlte/%s' % template)


@require_POST
def upload_file(request, way):
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT, way, name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL+way+'/'+name)
    # http://127.0.1:8000/media/abc.jpg
    return restful.result(data={'url': url})


@require_GET
def qntoken(request):
    access_key = settings.QINIU_ACCESS_KEY
    secret_key = settings.QINIU_SECRET_KEY

    bucket = settings.QINIU_BUCKET_NAME
    q = qiniu.Auth(access_key, secret_key)

    token = q.upload_token(bucket)

    return restful.result(data={"token": token})


def login_view(request):
    return render(request,'adminlte/login.html')


@login_require
def backed_index(request):
    print('aaaaaaaaaaa')
    return render(request, 'adminlte/index.html')


class BannerList(View):
    '''轮播图管理,采用restful风格'''
    def get(self, request):
        '''返回轮播图管理界面'''
        banners = Banner.objects.filter(is_del=0)
        return render(request, 'adminlte/banner.html', context={'banners': banners})

    def post(self, request):
        '''添加轮播图'''
        form = AddBannerFrom(request.POST)
        if form.is_valid():
            form.save()
            # Banner.objects.create(link_url=link_url, position=position, banner_url=banner_url)
        else:
            return restful.params_error(form.get_first_error())
        return restful.ok()


class BannerView(View):
    def get(self, request, banner_id):
        banner = Banner.objects.get(pk=banner_id)
        if not banner:
            return restful.params_error(message='轮播图不存在')
        return

    def put(self, request, banner_id):
        '''修改轮播图'''
        qd = QueryDict(request.body)
        put_dict = {k: v[0] if len(v) == 1 else v for k, v in qd.lists()}
        banner = Banner.objects.get(pk=banner_id)
        if not banner:
            return restful.params_error(message='轮播图不存在')
        position = put_dict.get('position')
        link_url = put_dict.get('link_url')
        # Banner.objects.filter(pk=banner_id).update(position=position, link_url=link_url)
        banner.position = position
        banner.link_url = link_url
        banner.save()
        return restful.ok()

    def delete(self, request, banner_id):
        '''删除轮播图'''
        banner = Banner.objects.get(pk=banner_id)
        if not banner:
            return restful.params_error(message='轮播图不存在')
        banner.is_del = 1
        banner.save()
        return restful.ok()


# def banner(request):
#     '''返回轮播图管理界面'''
#     banners = Banner.objects.filter(is_del=0)
#     return render(request, 'adminlte/banner.html', context={'banners': banners})
#
#
# def add_banner(request):
#     '''添加轮播图'''
#     form = AddBannerFrom(request.POST)
#     if form.is_valid():
#         form.save()
#         # Banner.objects.create(link_url=link_url, position=position, banner_url=banner_url)
#     else:
#         return restful.params_error(form.get_first_error())
#     return restful.ok()


class NewsListView(View):
    '''新闻列表'''
    def get(self, request):
        page = int(request.GET.get('page', 1))
        newes = News.objects.select_related('category', 'author').all()
        paginator = Paginator(newes, 5)
        try:
            page_obj = paginator.page(page)
        except:
            return render(request, "404.html")
        context_data = self.get_pagination_data(paginator, page_obj)
        context = {
            'categories': NewsCategory.objects.all(),
            'newses': page_obj.object_list,
            'paginator': paginator,
            'page_obj': page_obj
        }
        context.update(context_data)
        return render(request, "adminlte/news_list.html", context=context)

    def get_pagination_data(self, paginator, page_obj, arround_page=2):
        '''分页算法'''
        current_page = page_obj.number
        num_pages = paginator.num_pages
        left_has_more = False
        right_has_more = False
        if current_page <= arround_page+2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page-arround_page, current_page)
        if current_page >= num_pages-arround_page-1:
            right_pages = range(current_page+1, num_pages+1)
        else:
            right_has_more = True
            right_pages = range(current_page+1, current_page+arround_page+1)
        return {
            "current_page": current_page,
            "left_pages": left_pages,
            "right_pages": right_pages,
            "left_has_more": left_has_more,
            "right_has_more": right_has_more,
            "num_pages": num_pages
        }

