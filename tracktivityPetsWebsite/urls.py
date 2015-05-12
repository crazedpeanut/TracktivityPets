from django.conf.urls import patterns, include, url
from django.contrib import admin
from tracktivityPetsWebsite import views

urlpatterns = patterns('',
    #url(r'^$', 'views.home', name='home'),
    url(r'^login/$', views.user_login, name='user_login'), #ie mysite.com/login/
    url(r'^logout/$', views.user_logout, name='user_logout'), #ie mysite.com/logout/
    url(r'^register/$', views.register, name='register'), #ie mysite.com/register/
    url(r'^$', views.dashboard, name='dashboard'), #ie mysite.com
    url(r'^feedback/$', views.feedback, name='feedback'), 
    url(r'^pet_selection/$', views.pet_selection, name='pet_selection'),
    url(r'^main_story$', views.main_story, name='main_story'),
    
)
