from django.conf.urls import patterns, include, url
from django.contrib import admin
from tracktivityPetsWebsite import views

urlpatterns = patterns('',
    #url(r'^$', 'views.home', name='home'),
    url(r'^login/', views.user_login, name='user_login'), #ie mysite.com/login/
    url(r'^logout/', views.user_logout, name='user_logout'), #ie mysite.com/logout/
    url(r'^', views.dashboard, name='dashboard'), #ie mysite.com/logout/
)
