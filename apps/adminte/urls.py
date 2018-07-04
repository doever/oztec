from django.urls import path,re_path
from . import views

app_name = 'adminlte'

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('backed_index/',views.backed_index,name='backed_index'),
    path('news_add/',views.news_add,name='news_add'),
    path('news_category/',views.NewsCategory.as_view(),name='news_category'),
    path('category_detail/<category_id>/',views.categorydetail,name='categorydetail')
]