from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect

from models import *
import wordlists


def home(request):
    if request.method == 'GET':
        return render(request, 'home.html', {})


@csrf_exempt
def assessJobAd(request):
    if request.method == 'POST':
        ad_text = request.POST["texttotest"]
        if len(ad_text):
            job_ad = JobAd.create(ad_text)
            return redirect("results", ad_id=job_ad.hash)
        else:
            return redirect('/')


def about(request):
    if request.method == 'GET':
        return render(request, 'about.html',
            {"masculine_coded_words": wordlists.masculine_coded_words,
            "feminine_coded_words": wordlists.feminine_coded_words}
        )


def results(request, ad_id):
    job_ad = get_object_or_404(JobAd, hash=ad_id)
    return render(request, 'results.html', job_ad.results_dictionary())
