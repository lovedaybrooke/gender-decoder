from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt

import views

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^about$', views.about),
    url(r'^assess$', csrf_exempt(views.assessJobAd)),
    url(r"^results/(?P<ad_id>[0-9a-z]+)$", csrf_exempt(views.results),
        name="results")
)
