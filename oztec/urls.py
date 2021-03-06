"""oztec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings

from apps.news import views
from apps.adminte.views import templateview
# import xadmin


urlpatterns = [
    # path('xadmin/', xadmin.site.urls),
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    re_path('templates/(?P<template>.*)/$', templateview, name='template'),
    path('news/', include('apps.news.urls', namespace='news')),
    path('account/', include('apps.ozauth.urls', namespace='ozauth')),
    path('adminlte/', include('apps.adminte.urls', namespace='adminlte')),
    path('courses/', include('apps.courses.urls', namespace='courses')),
    path('payinfo/', include('apps.payinfo.urls', namespace='payinfo')),
    path('ueditor/', include('apps.ueditor.urls', namespace='ueditor')),
    # re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path("__debug__/",include(debug_toolbar.urls)))

