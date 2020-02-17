# -*- coding: utf-8 -*-

"""member URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import url, include
from board.views import * 
# ArticleListView, ArticleDetailView, ArticleCreateUpdateView,post_create, add_comment_to_post, CommentUpdate, CommentDelete
#list_article, detail_article, create_or_update_article
from accounts.views import UserRegistrationView, UserLoginView, user_info

from django.views.generic import RedirectView

from django.contrib.auth.views import LogoutView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='article/create/')),             # 바로 login url / 알아 둘 것!!
    url(r'^summernote/', include('django_summernote.urls')),
    #url(r'^article/(?P<article_id>\d+)/delete', ArticleDeleteView.as_view()),
    url(r'^article/(?P<article_id>\d+)/update', ArticleCreateUpdateView.as_view()),       #게시판 수정
    #url(r'^article/(?P<article_id>\d+)/delete', ArticleDeleteView.as_view()), #삭제
    
    url(r'^comment/(?P<pk>\d+)/update/$', CommentUpdate.as_view()),
    url(r'^comment/(?P<pk>\d+)/delete/$', CommentDelete.as_view()),
    url(r'^article/(?P<pk>\d+)/comment/$', add_comment_to_post, name='add_comment_to_post'),
    url(r'^article/comment/', post_create),
    url(r'^article/(?P<article_id>\d+)/$', ArticleDetailView.as_view()),                    #게시판 세부정보
    url(r'^article/create', ArticleCreateUpdateView.as_view()),                    #게시물 만들기   
    #url(r'^article', add_comment, name='add_comment'),
    url(r'^article', ArticleListView.as_view()),                                   #게시판 전체 출력
    
    url(r'^index', index_get, name='index_get' ),
    url(r'^accounts/mypage/', user_info, name= 'user_info'), #마이페이지
    url(r'^accounts/create/', UserRegistrationView.as_view()),   #회원가입
    url(r'^accounts/login/', UserLoginView.as_view()),             #로그인
    url(r'^accounts/logout/', LogoutView.as_view()),               #로그아웃
    
    #url(r'^accounts/update/' views.update, name='update'),
    #url(r'^accounts/mypage', views.userinfo, name="mypage"),
    
    url(r'^admin/', admin.site.urls),
    
    #FBV방식
    #url(r'^hello/<to>', hello),
    #url(r'^article/', list_article),
    #url(r'^article/create/', create_or_update_article, {'article_id': None}), # {'article_id':None} 필수
    #url(r'^article/<article_id>/', detail_article),
    #url(r'^article/<article_id>/update/', create_or_update_article),
    
]
