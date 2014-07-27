from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt

import views

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^assess$', csrf_exempt(views.assessJobAd))
)
