from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.conf import settings
from django.http import Http404
from django.db.models import Avg, Count

from .models import NewsCategory, News, Comment
from apps.adminte.models import Banner
from utils import restful
from .serializers import NewsSerializer, CommentSerializer
from .forms import PublishComment
from apps.ozauth.decorators import auth_login_required


def index(request):
    page_count = settings.NEWS_COUNT
    news = News.objects.select_related('author', 'category').all()[0:page_count]
    hot_news = News.objects.select_related().filter(category_id=1)[0:2]
    categorys = NewsCategory.objects.all()
    banners = Banner.objects.filter(is_del=0).order_by('position')[0:5]
    # for banner in banners:
    #     print(banner.banner_url, banner.link_url)
    context = {
        'news': news,
        'categorys': categorys,
        'hot_news': hot_news,
        'banners': banners
    }
    return render(request, 'news/index.html', context=context)


def news_list(request):
    '''新闻列表'''
    page = request.GET.get('page', 1)
    category = request.GET.get('category', 0)
    start_page = (int(page)-1)*settings.NEWS_COUNT
    end_page = start_page + settings.NEWS_COUNT
    if int(category) == 0:
        news = News.objects.select_related('author', 'category').all()[start_page:end_page]
    else:
        news = News.objects.select_related('author', 'category').filter(category=category)[start_page:end_page]
    new_serializer = NewsSerializer(news, many=True)
    return restful.ok(data=new_serializer.data)


def news_detail(request, news_id):
    try:
        new = News.objects.select_related('author', 'category').get(pk=news_id)
        hot_news = News.objects.select_related('author', 'category').filter(category_id=1).exclude(pk=news_id)[0:2]
        comments = new.comment_set.select_related().all()
        count = new.comment_set.aggregate(comment_count=Count('id'))
        print(count)
        context = {
            'new': new,
            'hot_news': hot_news,
            'comments': comments,
            'count': count
        }
    except:
        raise Http404
    return render(request, 'news/news_detail.html', context=context)


@auth_login_required
def publish_comment(request):
    '''发布评论功能,增加登录限制'''
    form = PublishComment(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        new = form.cleaned_data.get('new')
        comment = Comment.objects.create(content=content, new=new, author=request.user)
        comment_serializer = CommentSerializer(comment)
        return restful.ok(data=comment_serializer.data)
    else:
        return restful.params_error(message=form.get_errors())


def search(request):
    return render(request,'search/search.html')

