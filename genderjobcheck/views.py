from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect

from models import *
import wordlists


def home(request):
    if request.method == 'GET':
        return render(request, 'home.html', {})

def job_adverts(request):
    if request.method == 'GET':
        return render(request, 'job-adverts.html', {})

def ref_letters(request):
    if request.method == 'GET':
        return render(request, 'ref-letters.html', {})

@csrf_exempt
def assessJobAd(request):
    if request.method == 'POST':
        ad_text = request.POST["texttotest"]
        if len(ad_text):
            job_ad = JobAd.create(ad_text)
            return redirect("job_advert_results", ad_id=job_ad.hash)
        else:
            return redirect('/job-adverts')


def job_advert_results(request, ad_id):
    job_ad = get_object_or_404(JobAd, hash=ad_id)
    print(job_ad)
    return render(request, 'job-advert-results.html', job_ad.results_dictionary())

def job_adverts_word_lists(request):
    if request.method == 'GET':
        return render(request, 'job-adverts-word-lists.html',
            {"masculine_coded_words": wordlists.masculine_coded_words,
            "feminine_coded_words": wordlists.feminine_coded_words}
        )

@csrf_exempt
def assess_ref_letter(request):
    if request.method == 'POST':
        gender = request.POST["gender"]
        if not gender:
            gender = "unknown"
        letter_text = request.POST["texttotest"]
        if len(letter_text):
            ref_letter = RefLetter.create(letter_text, gender)
            return redirect("ref-letter-results", letter_id=ref_letter.hash)
        else:
            return redirect('/ref-letters')


def ref_letter_results(request, letter_id):
    ref_letter = get_object_or_404(RefLetter, hash=letter_id)
    return render(request, 'ref-letter-results.html', ref_letter.results_dictionary())

def ref_letters_word_lists(request):
    if request.method == 'GET':
        return render(request, 'ref-letters-word-lists.html',
            {"outstanding_words": wordlists.outstanding_words,
            "ability_words": wordlists.ability_words,
            "grindstone_words": wordlists.grindstone_words}
        )

def about(request):
    if request.method == 'GET':
        return render(request, 'about.html', {})
