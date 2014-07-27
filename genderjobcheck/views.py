from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

import assess

def home(request):
    if request.method == 'GET':
        return render(request, 'home.html', {})

@csrf_exempt
def assessJobAd(request):
    if request.method == 'POST':
        ad_text = request.POST["adtext"]
        results = assess.assess(ad_text)        
        return render(request, 'results.html', results
        	)