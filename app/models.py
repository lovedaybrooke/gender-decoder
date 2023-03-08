#!flask/bin/python
# -*- coding: utf-8 -*-

import datetime
import os
import sys
import re
import logging
import uuid
from binascii import hexlify

from app import app, db
from app.wordlists import *


class JobAd(db.Model):
    hash = db.Column(db.String(), primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    ad_text = db.Column(db.Text)
    masculine_word_count = db.Column(db.Integer, default=0)
    feminine_word_count = db.Column(db.Integer, default=0)
    masculine_coded_words = db.Column(db.Text)
    feminine_coded_words = db.Column(db.Text)
    coding = db.Column(db.String())
    coded_word_counter = db.relationship("CodedWordCounter", backref='job_ad')

    def __init__(self, ad_text):
        start_time = datetime.datetime.now()
        self.hash = str(uuid.uuid4())
        self.ad_text = ad_text
        self.analyse()
        db.session.add(self)
        db.session.commit()
        # CodedWordCounter.process_ad(self)

    # old method for recalculating ads eg after changes to clean_up_word_list
    def fix_ad(self):
        self.analyse()
        CodedWordCounter.process_ad(self)
        db.session.add(self)
        db.session.commit()

    def analyse(self):
        word_list = self.clean_up_word_list()
        self.extract_coded_words(word_list)
        self.assess_coding()

    def clean_up_word_list(self):
        cleaner_text = ''.join([i if ord(i) < 128 else ' '
            for i in self.ad_text])
        cleaner_text = re.sub("[\\s]", " ", cleaner_text, 0, 0)
        cleaned_word_list = re.sub(u"[\.\t\,“”‘’<>\*\?\!\"\[\]\@\':;\(\)\./&]",
            " ", cleaner_text, 0, 0).split(" ")
        word_list = [word.lower() for word in cleaned_word_list if word != ""]
        return self.de_hyphen_non_coded_words(word_list)

    def de_hyphen_non_coded_words(self, word_list):
        for word in word_list:
            if word.find("-"):
                is_coded_word = False
                for coded_word in hyphenated_coded_words:
                    if word.startswith(coded_word):
                        is_coded_word = True
                if not is_coded_word:
                    word_index = word_list.index(word)
                    word_list.remove(word)
                    split_words = word.split("-")
                    word_list = (word_list[:word_index] + split_words +
                        word_list[word_index:])
        return word_list

    def extract_coded_words(self, advert_word_list):
        words, count = self.find_and_count_coded_words(advert_word_list,
            masculine_coded_words)
        self.masculine_coded_words, self.masculine_word_count = words, count
        words, count = self.find_and_count_coded_words(advert_word_list,
            feminine_coded_words)
        self.feminine_coded_words, self.feminine_word_count = words, count

    def find_and_count_coded_words(self, advert_word_list, gendered_word_list):
        gender_coded_words = [word for word in advert_word_list
            for coded_word in gendered_word_list 
            if (word.startswith(coded_word) and word not in non_coded_exceptions)]
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
