from django.urls import path,re_path
from . import views

app_name = 'adminlte'

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('backed_index/',views.backed_index,name='backed_index'),
    path('write_news/',views.write_news,name='write_news'),
    path('news_category/',views.NewsCategory.as_view(),name='news_category'),
    path('category_detail/<category_id>/',views.categorydetail,name='categorydetail'),
    path('upload_file/',views.upload_file,name='upload_file')
]