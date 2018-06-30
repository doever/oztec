from django.shortcuts import render
from django.views.generic import View

def index(request):
    return render(request,'news/index.html')

def news_detail(request,news_id):
    return render(request,'news/news_detail.html')

def search(request):
    return render(request,'search/search.html')