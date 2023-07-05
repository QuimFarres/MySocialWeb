from django.urls import path, include
from .import views
from django.conf import settings
from django.contrib import admin

from django.views.static import serve
from django.conf.urls.static import url


urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name = 'signin'),
    path('logout', views.logout, name='logout'),
    path('create_post/', views.create_post, name='create_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('add_comment/<int:tweet_id>/', views.add_comment, name='add_comment'),
    path('like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),

]
