from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from .views import work,imgurl

urlpatterns=[
    url('predict',work,name='entery'),
    url('imgurl',imgurl,name='imgurl'),

]
