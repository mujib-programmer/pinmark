"""pinmark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from bookmarks.views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # Browsing
    url(r'^$', main_page),
    url(r'^user/(?P<username>\w+)/$', user_page), # allow only alphanumeric character
    url(r'^tag/(?P<tag_name>\S+)/$', tag_page),   # any non-whitespace character is allowed
    url(r'^tag/$', tag_cloud_page),
    url(r'^search/$', search_page),

    # Ajax
    url(r'^ajax/tag/autocomplete/$', ajax_tag_autocomplete),

    # Session management
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
    url(r'^register/$', register_page),

    # Account management
    url(r'^save/$', bookmark_save_page),

]
