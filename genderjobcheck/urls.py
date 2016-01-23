from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt

import views

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^about$', views.about),
    url(r'^ref-letters$', views.ref_letters),
    url(r'^job-adverts$', views.job_adverts),
    url(r'^job-adverts/assess$', csrf_exempt(views.assessJobAd)),
    url(r"^job-advert/results/(?P<ad_id>[0-9a-z]+)$", csrf_exempt(
        views.job_advert_results), name="job_advert_results"),
    url(r'^job-adverts/word-lists$', views.job_adverts_word_lists),
    url(r'^ref-letters$', views.ref_letters),
    url(r'^ref-letters/assess$', csrf_exempt(views.assess_ref_letter)),
    url(r"^ref-letter/results/(?P<letter_id>[0-9a-z]+)$", csrf_exempt(
        views.ref_letter_results), name="ref-letter-results"),
    url(r'^ref-letters/word-lists$', views.ref_letters_word_lists),
)
