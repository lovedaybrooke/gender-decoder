#!flask/bin/python
# -*- coding: utf-8 -*-

import datetime
import os
import sys
import re
import logging
import uuid
import importlib

from binascii import hexlify

from app import app, db
from app.wordlists import *


class JobAd(db.Model):
    hash = db.Column(db.String(), primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    ad_text = db.Column(db.Text)
    language = db.Column(db.String(), default="en", nullable=True)
    masculine_word_count = db.Column(db.Integer, default=0)
    feminine_word_count = db.Column(db.Integer, default=0)
    masculine_coded_words = db.Column(db.Text)
    feminine_coded_words = db.Column(db.Text)
    coding = db.Column(db.String())
    coded_word_counter = db.relationship("CodedWordCounter", backref='job_ad')


    def __init__(self, ad_text, language="en"):
        self.hash = str(uuid.uuid4())
        self.ad_text = ad_text
        self.language = language
        self.analyse()
        db.session.add(self)
        db.session.commit()
        CodedWordCounter.process_ad(self)

    # old method for recalculating ads eg after changes to clean_up_word_list
    def fix_ad(self):
        self.analyse()
        CodedWordCounter.process_ad(self)
        db.session.add(self)
        db.session.commit()

    def analyse(self):
        translated_wordlists = TranslatedWordlist(self.language)
        advert_word_list = self.clean_up_word_list(translated_wordlists)
        self.extract_coded_words(advert_word_list, translated_wordlists)
        self.assess_coding()

    def clean_up_word_list(self, translated_wordlists):
        cleaner_text = ''.join([i if ord(i) < 128  or ord(i) > 192 and ord(i) < 257
            else ' ' for i in self.ad_text])
        cleaner_text = re.sub("[\\s]", " ", cleaner_text, 0, 0)
        cleaned_word_list = re.sub(u"[\.\t\,“”‘’<>\*\?\!\"\[\]\@\':;\(\)\./&]", " ", cleaner_text, 0, 0).split(" ")
        advert_word_list = [word.lower() for word in cleaned_word_list 
                            if word != ""]
        return self.de_hyphen_non_coded_words(advert_word_list, 
                                              translated_wordlists)

    def de_hyphen_non_coded_words(self, advert_word_list, translated_wordlists):
        for word in advert_word_list:
            if word.find("-"):
                is_coded_word = False
                for coded_word in translated_wordlists.hyphenated_coded_words:
                    if word.startswith(coded_word):
                        is_coded_word = True
                if not is_coded_word:
                    word_index = advert_word_list.index(word)
                    advert_word_list.remove(word)
                    split_words = word.split("-")
                    advert_word_list = (advert_word_list[:word_index]
                        + split_words + advert_word_list[word_index:])
        return advert_word_list

    def extract_coded_words(self, advert_word_list, translated_wordlists):
        words, count = self.find_and_count_coded_words(advert_word_list,
            translated_wordlists.masculine_coded_words)
        self.masculine_coded_words, self.masculine_word_count = words, count
        words, count = self.find_and_count_coded_words(advert_word_list,
            translated_wordlists.feminine_coded_words)
        self.feminine_coded_words, self.feminine_word_count = words, count

    def find_and_count_coded_words(self, advert_word_list, gendered_word_list):
        gender_coded_words = [word for word in advert_word_list
            for coded_word in gendered_word_list
            if word.startswith(coded_word)]
        return (",").join(gender_coded_words), len(gender_coded_words)

    def assess_coding(self):
        coding_score = self.feminine_word_count - self.masculine_word_count
        if coding_score == 0:
            if self.feminine_word_count:
                self.coding = "neutral"
            else:
                self.coding = "empty"
        elif coding_score > 3:
            self.coding = "strongly feminine-coded"
        elif coding_score > 0:
            self.coding = "feminine-coded"
        elif coding_score < -3:
            self.coding = "strongly masculine-coded"
        else:
            self.coding = "masculine-coded"

    def list_words(self):
        if self.masculine_coded_words == "":
            masculine_coded_words = []
        else:
            masculine_coded_words = self.masculine_coded_words.split(",")
        if self.feminine_coded_words == "":
            feminine_coded_words = []
        else:
            feminine_coded_words = self.feminine_coded_words.split(",")
        masculine_coded_words = self.handle_duplicates(masculine_coded_words)
        feminine_coded_words = self.handle_duplicates(feminine_coded_words)
        return masculine_coded_words, feminine_coded_words

    def handle_duplicates(self, word_list):
        d = {}
        l = []
        for item in word_list:
            if item not in d.keys():
                d[item] = 1
            else:
                d[item] += 1
        for key, value in d.items():
            if value == 1:
                l.append(key)
            else:
                l.append("{0} ({1} times)".format(key, value))
        return l

    def provide_explanation(self):
        if self.coding == "feminine-coded":
            return ("This job ad uses more words that are subtly coded as "
                    "feminine than words that are subtly coded as masculine "
                    "(according to the research). Fortunately, the research "
                    "suggests this will have only a slight effect on how "
                    "appealing the job is to men, and will encourage women "
                    "applicants.")
        elif self.coding == "strongly feminine-coded": 
            return ("This job ad uses more words that are subtly coded as "
                    "feminine than words that are subtly coded as masculine "
                    "(according to the research). Fortunately, the research "
                    "suggests this will have only a slight effect on how "
                    "appealing the job is to men, and will encourage women "
                    "applicants.")
        elif self.coding == "masculine-coded":
            return ("This job ad uses more words that are subtly coded as "
                    "masculine than words that are subtly coded as feminine"
                    "(according to the research). It risks putting women off "
                    "applying, but will probably encourage men to apply.")
        elif self.coding == "strongly masculine-coded": 
            return ("This job ad uses more words that are subtly coded as "
                    "masculine than words that are subtly coded as feminine "
                    "(according to the research). It risks putting women off "
                    "applying, but will probably encourage men to apply.")
        elif self.coding == "empty": 
            return ("This job ad doesn't use any words that are subtly coded "
              "as masculine or feminine (according to the research). It "
              "probably won't be off-putting to men or women applicants.")
        elif self.coding == "neutral": 
            return ("This job ad uses an equal number of words that are "
              "subtly coded as masculine and feminine (according to the "
              "research). It probably won't be off-putting to men or women "
              "applicants.")


class CodedWordCounter(db.Model):
    __tablename__ = "coded_word_counter"
    id = db.Column(db.Integer, primary_key=True)
    ad_hash = db.Column(db.String(), db.ForeignKey('job_ad.hash'))
    word = db.Column(db.Text)
    coding = db.Column(db.Text)
    count = db.Column(db.Integer)

    def __init__(self, ad, word, coding):
        self.ad_hash = ad.hash
        self.word = word
        self.coding = coding
        self.count = 1
        db.session.add(self)
        db.session.commit()

    @classmethod
    def increment_or_create(cls, ad, word, coding):
        existing_counter = cls.query.filter_by(ad_hash=ad.hash).filter_by(
            word=word).first()
        if existing_counter:
            existing_counter.count += 1
            db.session.add(existing_counter)
            db.session.commit()
        else:
            new_counter = cls(ad, word, coding)

    @classmethod
    def process_ad(cls, ad):
        cls.query.filter_by(ad_hash=ad.hash).delete()

        masc_words = ad.masculine_coded_words.split(",")
        masc_words = filter(None, masc_words)
        for word in masc_words:
            cls.increment_or_create(ad, word, 'masculine')

        fem_words = ad.feminine_coded_words.split(",")
        fem_words = filter(None, fem_words)
        for word in fem_words:
            cls.increment_or_create(ad, word, 'feminine')


class TranslatedWordlist(object):
    
    def __init__(self, language):
        wordlists = importlib.import_module('.{0}'.format(language),
                                            'app.wordlists')

        self.hyphenated_coded_words = wordlists.hyphenated_coded_words
        self.masculine_coded_words = wordlists.masculine_coded_words
        self.feminine_coded_words = wordlists.feminine_coded_words

    @classmethod
    def get_language_name_and_source(cls, language):
        my_module = importlib.import_module('.{0}'.format(language),
                                            'app.wordlists')
        return (my_module.language_name,
                my_module.language_code,
                my_module.source)