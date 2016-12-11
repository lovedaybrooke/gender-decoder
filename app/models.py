import datetime
import os
import re
from binascii import hexlify

from app import app, db
from wordlists import *


class JobAd(db.Model):
    hash = db.Column(db.String(), primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    jobAdText = db.Column(db.Text)
    masculine_word_count = db.Column(db.Integer, default=0)
    feminine_word_count = db.Column(db.Integer, default=0)
    masculine_coded_words = db.Column(db.Text)
    feminine_coded_words = db.Column(db.Text)
    coding = db.Column(db.String())

    def __init__(self, jobAdText):
        self.hash = hexlify(os.urandom(8))  # need to make sure it's unique
        self.jobAdText = jobAdText
        self.analyse()
        db.session.add(self)
        db.session.commit()

    def analyse(self):
        word_list = self.clean_up_word_list()
        self.extract_coded_words(word_list)
        self.assess_coding()

    def clean_up_word_list(self):
        cleaner_text = ''.join([i if ord(i) < 128 else ' '
            for i in self.jobAdText])
        cleaner_text = re.sub("[\\s]", " ", cleaner_text, 0, 0)
        cleaned_word_list = re.sub("[\.\t\,\:;\(\)\./&]", " ", cleaner_text,
            0, 0).split(" ")
        return [word.lower() for word in cleaned_word_list if word != ""]

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
        return masculine_coded_words, feminine_coded_words
