from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TracktivityPets.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^fitbit/', include('fitapp.urls')),
    url(r'^', include('tracktivityPetsWebsite.urls', namespace="tracktivityPetsWebsite")),
)
