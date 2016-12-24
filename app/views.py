from flask import Flask
from flask import render_template, redirect, request
from wtforms.validators import ValidationError
import datetime
from app import app, db
from forms import JobAdForm
from models import JobAd, CodedWordCounter
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


@app.route('/calculate/<hash>', methods=['POST'])
def calculate(hash):
    hashes = [counter.ad_hash for counter in CodedWordCounter.query.all()]
    unique_hashes = set(hashes)
    if hash not in unique_hashes:
        ad = JobAd.query.filter_by(hash=hash).first()
        CodedWordCounter.process_ad(ad)
    return render_template('about.html')


@app.route('/fix/<hash>', methods=['POST'])
def fix(hash):
    ad = JobAd.query.filter_by(hash=hash).first()
    ad.fix_ad()
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
