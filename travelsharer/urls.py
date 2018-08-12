"""travelsharer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from web import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
     url(r'^$', views.index, name='index'),
     url(r'^index/$', views.index),
     url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^verifycode/(?P<code>\d*)/$', views.verifycode),
    url(r'^loginout/$', views.loginout),
    url(r'^post_artcle/$', views.post_artcle),
    url(r'^post_pic/$', views.post_pic),
    url(r'^travelNote/$', views.travelNote),
    url(r'^pics/$', views.pics),
    url(r'^about/$', views.about),
    url(r'^discover/$', views.discover),
    url(r'^members/$', views.members),
    url(r'^collection/$', views.collection),
    url(r'^myPics/$', views.myPics),
    url(r'^located/$', views.located),
    url(r'^myArticle/$', views.myArticle),
    url(r'^detailPage/(?P<id>\d*)/$', views.detailPage),
    url(r'^noteCollection/(?P<id>\d*)/$', views.noteCollection),
    url(r'^travelLike/(?P<id>\d*)/$', views.travelLike),
    url(r'^traveComment/(?P<id>\d*)/$', views.traveComment),
    url(r'^delTraveNoteComment/(?P<id>\d*)/$', views.delTraveNoteComment),
    url(r'^delcollection/(?P<id>\d*)/$', views.delcollection),
    url(r'^delPic/(?P<id>\d*)/$', views.delPic),
    url(r'^delArticle/(?P<id>\d*)/$', views.delArticle),
    url(r'^travelType/(?P<type>\d*)/$', views.travelType),
    url(r'^picType/(?P<type>\d*)/$', views.picType),
    url(r'^discoverType/(?P<type>\d*)/$', views.discoverType),
    url(r'upload/$', views.upload, name='upload_img'),
    url(r'^test/$', views.test),
    url(r'^oauth2callbackgoogle/$', views.oauth2callbackgoogle),
]
