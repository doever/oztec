from django.urls import path,re_path
from . import views

app_name = 'news'

urlpatterns = [
    path('news_list/',views.news_list,name='news_list'),
    path('<int:news_id>/',views.news_detail,name='news_detail'),
    # path('',)
]

