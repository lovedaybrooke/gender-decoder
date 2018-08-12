import datetime

from flask import Flask
from flask import render_template, redirect, request
from wtforms.validators import ValidationError

from app import app, db
from app.forms import JobAdForm
from app.models import JobAd, CodedWordCounter, TranslatedWordlist
import app.wordlists as wordlists


@app.route('/', methods=['GET', 'POST'])
def home():
    form = JobAdForm()
    if request.method == "POST" and form.validate_on_submit():
        ad = JobAd(form.texttotest.data, form.language.data)
        return redirect('results/{0}'.format(ad.hash))
    return render_template('home.html',
                          form=form,
                          number_of_languages=len(wordlists.__all__))


@app.route('/about')
def about():
    language = request.values.get('language')
    if language not in wordlists.all_lists.keys():
        language = "en"
    return render_template('about.html',
        language_code=language,
        language_name=wordlists.all_lists[language]["language_name"],
        masculine_coded_words=wordlists.all_lists[language]['masculine_coded_words'],
        feminine_coded_words=wordlists.all_lists[language]['feminine_coded_words']
        )


@app.route('/results/<ad_hash>')
def results(ad_hash):
    job_ad = JobAd.query.get_or_404(ad_hash)
    masculine_coded_words, feminine_coded_words = job_ad.list_words()
    name, code, source = TranslatedWordlist.get_language_name_and_source(
                       job_ad.language)
    return render_template('results.html', job_ad=job_ad,
        masculine_coded_words=masculine_coded_words,
        feminine_coded_words=feminine_coded_words,
        explanation=job_ad.provide_explanation(),
        language_name=name,
        language_code=code,
        source=source)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
