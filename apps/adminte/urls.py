from django.urls import path, re_path
from . import views

app_name = 'adminlte'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.backed_index, name='backed_index'),
    path('write_news/', views.WriteNewsView.as_view(), name='write_news'),
    path('news_category/', views.NewsCategoryView.as_view(), name='news_category'),
    path('category_detail/<category_id>/', views.categorydetail, name='categorydetail'),
    re_path('upload_file/(?P<way>.*)/', views.upload_file, name='upload_file'),
    path('banner_list/', views.BannerList.as_view(), name='banner_list'),
    path('banner/<banner_id>/', views.BannerView.as_view(), name='banner'),
    path('news_list/', views.NewsListView.as_view(), name='news_list'),
    # re_path('banner/(?P<banner_id>/d+)/', views.BannerView.as_view(), name='banner'),
]