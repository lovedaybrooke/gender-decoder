from __future__ import division
# to force division to return float
import logging
import re
import os
from binascii import hexlify

from django.db import models
from django.db.models import fields

import wordlists


class JobAd(models.Model):
    hash = models.CharField(max_length=16, unique=True)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    masculine_coded_words = models.TextField(blank=True)
    feminine_coded_words = models.TextField(blank=True)

    possible_codings = (
        ("strongly feminine-coded", "strongly feminine-coded"),
        ("feminine-coded", "feminine-coded"),
        ("neutral", "neutral"),
        ("masculine-coded", "masculine-coded"),
        ("strongly masculine-coded", "strongly masculine-coded")
    )

    coding = models.CharField(max_length=24, blank=True,
        choices=possible_codings)

    @classmethod
    def create(cls, ad_text):
        job_ad = cls()
        job_ad.text = ad_text
        job_ad.make_hash()
        job_ad.save()
        job_ad.assess()
        job_ad.save()
        return job_ad

    def make_hash(self):
        while True:
            hash = hexlify(os.urandom(8))
            if hash not in [ad.hash for ad in JobAd.objects.all()]:
                self.hash = hash
                break

    def assess(self):
        ad_text = self.text.replace("\r\n", " ")
        ad_text_list = re.sub("[\.\t\,\:;\(\)\.]", "", ad_text, 0,
            0).split(" ")

        masculine_coded_words = [adword for adword in ad_text_list
            for word in wordlists.masculine_coded_words
            if adword.startswith(word)]
        self.masculine_coded_words = (",").join(masculine_coded_words)

        feminine_coded_words = [adword for adword in ad_text_list
            for word in wordlists.feminine_coded_words
            if adword.startswith(word)]
        self.feminine_coded_words = (",").join(feminine_coded_words)

        if feminine_coded_words and not masculine_coded_words:
            self.coding = "strongly feminine-coded"
        elif masculine_coded_words and not feminine_coded_words:
            self.coding = "strongly masculine-coded"
        elif not masculine_coded_words and not feminine_coded_words:
            self.coding = "neutral"
        else:
            if len(feminine_coded_words) == len(masculine_coded_words):
                self.coding = "neutral"
            if ((len(feminine_coded_words) / len(masculine_coded_words)) >=
                    2 and len(feminine_coded_words) > 5):
                self.coding = "strongly feminine-coded"
            if ((len(masculine_coded_words) / len(feminine_coded_words)) >=
                    2 and len(masculine_coded_words) > 5):
                self.coding = "strongly masculine-coded"
            if len(feminine_coded_words) > len(masculine_coded_words):
                self.coding = "feminine-coded"
            if len(masculine_coded_words) > len(feminine_coded_words):
                self.coding = "masculine-coded"

    def results_dictionary(self):
        if "feminine" in self.coding:
            explanation = ("This job ad uses more words that are "
                "stereotypically feminine than words that are "
                "stereotypically masculine. Fortunately, the research "
                "suggests this will have only a slight effect on how "
                "appealing the job is to men, and will encourage women "
                "applicants.")
        elif "masculine" in self.coding:
            explanation = ("This job ad uses more words that are "
                "stereotypically masculine than words that are "
                "stereotypically feminine. It risks putting women off "
                "applying, but will probably encourage men to apply.")
        elif not self.masculine_coded_words and not self.feminine_coded_words:
            explanation = ("This job ad doesn't use any words that are "
                "stereotypically masculine and stereotypically feminine. It "
                "probably won't be off-putting to men or women applicants.")
        else:
            explanation = ("This job ad uses an equal number of words that "
                "are stereotypically masculine and stereotypically feminine. "
                "It probably won't be off-putting to men or women "
                "applicants.")

        return {"job_ad": self,
            "masculine_coded_words": self.masculine_coded_words.split(","),
            "feminine_coded_words": self.feminine_coded_words.split(","),
            "explanation": explanation}
class RefLetter(models.Model):
    hash = models.CharField(max_length=16, unique=True)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    possible_codings = (
        ("woman", "woman"),
        ("man", "man"),
        ("other", "other"),
        ("unknown", "unknown")
    )
    gender = models.CharField(max_length=7, choices=possible_codings)
    
    word_count = models.IntegerField(default=0)
    outstanding_words = models.TextField(blank=True)
    outstanding_ratio = models.FloatField(default=0)
    outstanding_count = models.IntegerField(default=0)
    ability_words = models.TextField(blank=True)
    ability_ratio = models.FloatField(default=0)
    ability_count = models.IntegerField(default=0)
    grindstone_words = models.TextField(blank=True)
    grindstone_ratio = models.FloatField(default=0)
    grindstone_count = models.IntegerField(default=0)

    @classmethod
    def create(cls, ad_text, gender):
        ref_letter = cls()
        ref_letter.text = ad_text
        ref_letter.make_hash()
        ref_letter.gender = gender
        ref_letter.save()
        ref_letter.assess()
        ref_letter.save()
        return ref_letter

    def make_hash(self):
        while True:
            hash = hexlify(os.urandom(8))
            if hash not in [ad.hash for ad in RefLetter.objects.all()]:
                self.hash = hash
                break

    def assess(self):
        ad_text = self.text.replace("\r\n", " ")
        ad_text_list = re.sub("[\.\t\,\:;\(\)\.]", "", ad_text, 0,
            0).split(" ")

        self.word_count = len(ad_text_list)

        outstanding_words = [adword for adword in ad_text_list
            for word in wordlists.outstanding_words
            if adword.startswith(word)]
        self.outstanding_count = len(outstanding_words)
        self.outstanding_ratio = self.outstanding_count/self.word_count
        self.outstanding_words = (",").join(outstanding_words)

        ability_words = [adword for adword in ad_text_list
            for word in wordlists.ability_words
            if adword.startswith(word)]
        self.ability_count = len(ability_words)
        self.ability_ratio = self.ability_count/self.word_count
        self.ability_words = (",").join(ability_words)

        grindstone_words = [adword for adword in ad_text_list
            for word in wordlists.grindstone_words
            if adword.startswith(word)]
        self.grindstone_count = len(grindstone_words)
        self.grindstone_ratio = self.grindstone_count/self.word_count
        self.grindstone_words = (",").join(grindstone_words)


    def select_outstanding_explanation(self):
        if self.outstanding_ratio >= 0.0007:
             return  ("This reference letter describes the "
                "applicant as outstanding about as much or more as the men's "
                "reference letters in the original research.")
        elif self.outstanding_ratio <= 0.0006:
            return  ("This reference letter describes the "
                "applicant as outstanding about as much or less than the "
                "women's reference letters in the original research.")
        elif self.outstanding_ratio == 0:
            return  ("This reference letter doesn't "
                "use any of the outstanding words we were looking for. "
                "In the original research, this was more common for letters "
                "about women applicants")
        else:
            return ("This reference letter describes the "
                "applicant as outstanding less than the men's reference "
                "letters in the original research, but more than the "
                "women's.")

    def select_ability_grindstone_explanation(self):
            if self.grindstone_ratio > self.ability_ratio:
                return ("The number of 'grindstone' words exceeds the "
                    "number of 'ability' words in this reference letter. ")
            elif self.ability_ratio > self.grindstone_ratio:
                return ("The number of 'ability' words exceeds the "
                    "number of 'grindstone' words in this reference "
                    "letter.")
            elif self.ability_ratio > 0:
                return ("There are an equal number of 'grindstone' and "
                        "'ability' words in this reference letter.")
            else:
                return ("There are neither any 'grindstone' words nor any "
                        "'ability' words in this reference letter.")

    def results_dictionary(self):
        outstanding_explanation = self.select_outstanding_explanation()
        ability_grindstone_explanation = self.select_ability_grindstone_explanation()

        return {"ref_letter": self,
            "outstanding_ratio": "{0:.2f}%".format(self.outstanding_ratio*100),
            "outstanding_count": "{0:.1f}".format(self.outstanding_count),
            "ability_ratio": "{0:.2f}%".format(self.ability_ratio*100),
            "ability_count": "{0:.1f}".format(self.ability_count),
            "grindstone_ratio": "{0:.2f}%".format(self.grindstone_ratio*100),
            "grindstone_count": "{0:.1f}".format(self.grindstone_count),
            "ability_grindstone_explanation": ability_grindstone_explanation,
            "outstanding_explanation": outstanding_explanation}
