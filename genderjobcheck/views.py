from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import redirect

import assess
import wordlists

def home(request):
    if request.method == 'GET':
        return render(request, 'home.html', {})

@csrf_exempt
def assessJobAd(request):
    if request.method == 'POST':
        ad_text = request.POST["texttotest"]
        if len(ad_text):
            results = assess.assess(ad_text)        
            return render(request, 'results.html', results
                )
        else:
           	return redirect('/')
           	
def about(request):
    if request.method == 'GET':
        return render(request, 'about.html',
        	{"masculine_coded_words": wordlists.masculine_coded_words,
    		"feminine_coded_words": wordlists.feminine_coded_words}
    		)