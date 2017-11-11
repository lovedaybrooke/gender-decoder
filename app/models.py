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
from wordlists import *


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
        app.logger.addHandler(logging.StreamHandler(sys.stdout))
        app.logger.setLevel(logging.INFO)
        app.logger.info("==============================")
        app.logger.info("LET US BEGIN")
        app.logger.info("==============================")
        start_time = datetime.datetime.now()
        app.logger.info("Hash creation started")
        app.logger.info(start_time)
        app.logger.info("---")
        self.hash = str(uuid.uuid4())
        self.ad_text = ad_text
        app.logger.info("Analysis started")
        app.logger.info(datetime.datetime.now())
        app.logger.info("---")
        self.analyse()
        app.logger.info("DB addition started")
        app.logger.info(datetime.datetime.now())
        app.logger.info("---")
        db.session.add(self)
        app.logger.info("DB commit started")
        app.logger.info(datetime.datetime.now())
        db.session.commit()
        app.logger.info("==============================")
        app.logger.info("Time taken: {0}".format(
            datetime.datetime.now() - start_time))
        app.logger.info("==============================")
        # CodedWordCounter.process_ad(self)

    # old method for recalculating ads eg after changes to clean_up_word_list
    def fix_ad(self):
        self.analyse()
        CodedWordCounter.process_ad(self)
        db.session.add(self)
        db.session.commit()

    def analyse(self):
        app.logger.addHandler(logging.StreamHandler(sys.stdout))
        app.logger.setLevel(logging.INFO)
        app.logger.info("Clean up word list started")
        app.logger.info(datetime.datetime.now())
        app.logger.info("---")
        word_dict = self.make_word_dict()
        app.logger.info("Extract coded words started")
        app.logger.info(datetime.datetime.now())
        app.logger.info("---")
        self.extract_coded_words(word_dict)
        app.logger.info("Assess coding started")
        app.logger.info(datetime.datetime.now())
        app.logger.info("---")
        self.assess_coding()
        app.logger.info("Analysis finished")
        app.logger.info(datetime.datetime.now())
        app.logger.info("---")

    def clean_text(self):
        self.ad_text = self.ad_text.replace("-","")
        cleaner_text = self.ad_text.lower()
        cleaner_text = ''.join([i if ord(i) < 128 else ' '
            for i in cleaner_text])
        cleaner_text = re.sub("[\\s]", " ", cleaner_text, 0, 0)
        cleaner_text = re.sub(u"[\.\t\,“”‘’<>\*\?\!\"\[\]\@\':;\(\)\./&]",
            " ", cleaner_text, 0, 0)
        return cleaner_text

    def make_word_dict(self):
        cleaner_text = self.clean_text()
        cleaned_word_list = cleaner_text.split(" ")
        word_dict = {}
        for word in cleaned_word_list:
            if len(word) > 0:
                if word in word_dict.keys():
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1
        return word_dict

    def extract_coded_words(self, advert_word_dict):
        words, count = self.find_and_count_coded_words(advert_word_dict,
            masculine_coded_words)
        self.masculine_coded_words, self.masculine_word_count = words, count
        words, count = self.find_and_count_coded_words(advert_word_dict,
            feminine_coded_words)
        self.feminine_coded_words, self.feminine_word_count = words, count

    def find_and_count_coded_words(self, advert_word_dict, gendered_word_list):
        gender_coded_words = []
        gender_coded_word_count = 0
        for advert_word, count in advert_word_dict.iteritems():
            for coded_word in gendered_word_list:
                if advert_word.startswith(coded_word):
                    gender_coded_word_count += count
                    if count > 1:
                        gender_coded_words.append(
                            "{0} ({1} times)".format(advert_word, count))
                    else:
                        gender_coded_words.append(advert_word)
        return (",").join(gender_coded_words), gender_coded_word_count

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
        return masculine_coded_words, feminine_coded_words


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
