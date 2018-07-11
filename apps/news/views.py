from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.generic import View
from django.conf import settings
from django.http import Http404

from .models import NewsCategory,News
from utils import restful
from .serializers import NewsSerializer


def index(request):
    page_count = settings.NEWS_COUNT
    news = News.objects.select_related('author','category').all()[0:page_count]
    hot_news = News.objects.select_related().filter(category_id=1)[0:2]
    categorys = NewsCategory.objects.all()
    context = {
        'news':news,
        'categorys':categorys,
        'hot_news':hot_news
    }
    return render(request,'news/index.html',context=context)


def news_list(request):
    page = request.GET.get('page',1)
    category =request.GET.get('category',0)
    start_page = (int(page)-1)*settings.NEWS_COUNT
    end_page = start_page + settings.NEWS_COUNT
    if int(category) == 0:
        news = News.objects.select_related('author','category').all()[start_page:end_page]
    else:
        news = News.objects.select_related('author','category').filter(category=category)[start_page:end_page]
    new_serializer = NewsSerializer(news,many=True)
    return restful.ok(data=new_serializer.data)


def news_detail(request,news_id):
    # news_id = request.GET.get(news_id)
    try:
        new = News.objects.select_related('author','category').get(pk=news_id)
        hot_news = News.objects.select_related('author','category').filter(category_id=1).exclude(pk=news_id)[0:2]
        context = {
            'new':new,
            'hot_news':hot_news
        }
    except:
        raise Http404
    return render(request,'news/news_detail.html',context=context)


def search(request):
    return render(request,'search/search.html')

