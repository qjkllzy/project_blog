"""blog URL Configuration

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
from myblog import views
from django.conf import settings
from myblog.upload import upload_image


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    url(r'^admin/upload/(?P<dir_name>[^/]+)$',upload_image,name='upload_image'),
    url(r'^$', views.index,name='index'),
    url(r'^category/$', views.category,name='category'),
    url(r'^article_xq/$', views.article_xq,name='article_xq'),
    url(r'^wendang/$', views.wendang,name='wendang'),
    url(r'^zhuce/$', views.zhuce, name='zhuce'),
    url(r'^denglu/$', views.denglu, name='denglu'),
    url(r'^logout$', views.zhuxiao, name='zhuxiao'),
    url(r'^write_comment/$', views.write_comment, name='write_comment'),
    url(r'^answer_comment/$', views.answer_comment, name='answer_comment'),
]
