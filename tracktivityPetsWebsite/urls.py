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
    url(r'^fitbit_link', views.fitbit_link, name='fitbit_link'),
    url(r'^store/$', views.store, name='store'),
    url(r'^inventory/$', views.inventory, name='inventory'),
    url(r'^inventory/(?P<tab>[a-z]+)/$', views.inventory, name='inventory'),
    url(r'^challenges/$', views.challenges, name='challenges'),
    url(r'^view_purchased_pet/$', views.view_purchased_pet, name='view_purchased_pet'),
    url(r'^view_purchased_pet/(?P<pet_index>[0-9]+)/$', views.view_purchased_pet, name='view_purchased_pet'),
    url(r'^view_unpurchased_pet/$', views.view_unpurchased_pet, name='view_unpurchased_pet'),
    url(r'^view_unpurchased_pet/(?P<pet_index>[0-9]+)/$', views.view_unpurchased_pet, name='view_unpurchased_pet'),
    url(r'^set_current_pet/$', views.set_current_pet, name='set_current_pet'),
    url(r'^set_current_pet/(?P<pet_index>[0-9]+)/$', views.set_current_pet, name='set_current_pet'),
    url(r'^view_purchased_item/$', views.view_purchased_item, name='view_purchased_item'),
    url(r'^view_purchased_item/(?P<item_index>[0-9]+)/$', views.view_purchased_item, name='view_purchased_item'),
    url(r'^view_purchased_scenery/$', views.view_purchased_scenery, name='view_purchased_scenery'),
    url(r'^view_purchased_scenery/(?P<scenery_index>[0-9]+)/$', views.view_purchased_scenery, name='view_purchased_scenery'),
    url(r'^view_unpurchased_scenery/$', views.view_unpurchased_scenery, name='view_unpurchased_scenery'),
    url(r'^view_unpurchased_scenery/(?P<scenery_index>[0-9]+)/$', views.view_unpurchased_scenery, name='view_unpurchased_scenery'),
    url(r'^view_unpurchased_item/$', views.view_unpurchased_item, name='view_unpurchased_item'),
    url(r'^view_unpurchased_item/(?P<item_index>[0-9]+)/$', views.view_unpurchased_item, name='view_unpurchased_item'),
    url(r'^purchase/$', views.purchase, name='purchase'),
    url(r'^purchase/(?P<tab>[a-z]+)/(?P<index>[0-9]+)/$', views.purchase, name='purchase'),
    url(r'^set_current_scenery/$', views.set_current_scenery, name='set_current_scenery'),
    url(r'^set_current_scenery/(?P<scenery_index>[0-9]+)/$', views.set_current_scenery, name='set_current_scenery'),
    url(r'^equip_item/$', views.equip_item, name='equip_item'),
    url(r'^equip_item/(?P<item_index>[0-9]+)/$', views.equip_item, name='equip_item'),
    url(r'^equip_item/(?P<item_index>[0-9]+)/(?P<equip>[a-z]+)/$', views.equip_item, name='equip_item'),
    url(r'^challenges/get_available_challenges/$', views.get_available_challenge_names, name="get_available_challenges"),
    url(r'^challenges/get_active_challenges/$', views.get_active_challenge_names, name="get_active_challenges"),
    url(r'^challenges/get_complete_challenges/$', views.get_completed_challenge_names, name="get_complete_challenges"),
    url(r'^challenges/get_challenge_details/(?P<challenge_pk>[0-9]+)/$', views.get_challenge_details, name="challenge_detail"),
    url(r'^challenges/get_active_challenge_details/(?P<user_challenge_pk>[0-9]+)/$', views.get_active_challenge_details, name="active_challenge_detail"),
    url(r'^challenges/get_complete_challenge_details/(?P<user_challenge_pk>[0-9]+)/$', views.get_complete_challenge_details, name="active_challenge_detail"),
    url(r'^/test_challenges/$', views.test_challenge_check, name="challenge_check")
)
