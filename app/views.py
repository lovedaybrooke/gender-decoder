from flask import Flask
from flask import render_template, redirect, request
from wtforms.validators import ValidationError
import datetime
from app import app, db
from forms import JobAdForm
from models import JobAd
from wordlists import *


@app.route('/', methods=['GET', 'POST'])
def home():
    form = JobAdForm()
    if request.method == "POST" and form.validate_on_submit():
        ad = JobAd(form.texttotest.data)
        return redirect('results/{0}'.format(ad.hash))
    return render_template('home.html',
                          form=form)


@app.route('/about')
def about():
    return render_template('about.html',
        masculine_coded_words=masculine_coded_words,
        feminine_coded_words=feminine_coded_words)


@app.route('/results/<ad_hash>')
def results(ad_hash):
    job_ad = JobAd.query.get_or_404(ad_hash)
    masculine_coded_words, feminine_coded_words = job_ad.list_words()
    return render_template('results.html', job_ad=job_ad,
        masculine_coded_words=masculine_coded_words,
        feminine_coded_words=feminine_coded_words,
        explanation=explanations[job_ad.coding])

@app.route('/upload', methods=['POST'])
def upload():
    content = request.get_json()
    all_hashes = [ad.hash for ad in JobAd.query.all()]
    if content["hash"] not in all_hashes:
        job_ad = JobAd(content["text"])
        job_ad.hash = content["hash"]
        job_ad.date = datetime.datetime.strptime(content["date"], "%Y-%m-%d")
        db.session.add(job_ad)
        db.session.commit()
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
