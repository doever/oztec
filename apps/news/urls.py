from django.urls import path,re_path
from . import views

app_name = 'news'

urlpatterns = [
    path('<int:news_id>',views.news_detail,name='news_detail'),
    # path('',)
]