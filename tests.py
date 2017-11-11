#!flask/bin/python
# -*- coding: utf-8 -*-

import os
import unittest

from config import basedir
from app import app, db
from app.models import JobAd, CodedWordCounter



class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
            basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_clean_text(self):
        caps = JobAd("Sharing is aS imporTant as ambition")
        self.assertEqual(caps.clean_text(),
            "sharing is as important as ambition")
        tab = JobAd("Qualities: sharing\tambition")
        self.assertEqual(tab.clean_text(),
            "qualities  sharing ambition")
        semicolon = JobAd("Sharing;ambitious")
        self.assertEqual(semicolon.clean_text(),
            "sharing ambitious")
        slash = JobAd(u"Sharing/ambitious")
        self.assertEqual(slash.clean_text(), "sharing ambitious")
        hyphen = JobAd(u"Sharing, co-operative, 'servant-leader'")
        self.assertEqual(hyphen.clean_text(),
            "sharing  cooperative   servantleader ")
        mdash = JobAd(u"Sharing—ambitious")
        self.assertEqual(mdash.clean_text(), "sharing ambitious")
        bracket = JobAd(u"Sharing(ambitious) and (leader)")
        self.assertEqual(bracket.clean_text(),
            "sharing ambitious  and  leader ")
        sqbracket = JobAd(u"Sharing[ambitious] and [leader]")
        self.assertEqual(sqbracket.clean_text(), 
            "sharing ambitious  and  leader ")
        abracket = JobAd(u"Sharing<ambitious> and <leader>")
        self.assertEqual(abracket.clean_text(), 
            "sharing ambitious  and  leader ")
        space = JobAd(u"Sharing ambitious ")
        self.assertEqual(space.clean_text(), "sharing ambitious ")
        amp = JobAd(u"Sharing&ambitious, empathy&kindness,")
        self.assertEqual(amp.clean_text(),
            "sharing ambitious  empathy kindness ")
        asterisk = JobAd(u"Sharing&ambitious*, empathy*kindness,")
        self.assertEqual(asterisk.clean_text(),
            "sharing ambitious   empathy kindness ")
        atandquestion = JobAd(u"Lead \"Developer\" Who is Connect@HBS? We ")
        self.assertEqual(atandquestion.clean_text(),
            "lead  developer  who is connect hbs  we ")
        exclaim = JobAd(u"Lead Developer v good!")
        self.assertEqual(exclaim.clean_text(),
            "lead developer v good ")
        curls = JobAd(u"“Lead” ‘Developer’ v good!")
        self.assertEqual(exclaim.clean_text(),
            "lead developer v good ")


    def test_make_word_dict(self):
        caps = JobAd("Sharing is as important as ambition")
        self.assertEqual(caps.make_word_dict(),
            {'sharing': 1, 'is': 1, 'as': 2, 'important': 1, 'ambition': 1})
        tab = JobAd("Qualities: sharing\tambition")
        self.assertEqual(tab.make_word_dict(),
            {'qualities': 1, 'sharing': 1, 'ambition': 1})
        semicolon = JobAd("Sharing;ambitious")
        self.assertEqual(semicolon.make_word_dict(),
            {'sharing': 1, 'ambitious': 1})
        slash = JobAd(u"Sharing/ambitious")
        self.assertEqual(slash.make_word_dict(), {'sharing': 1, 'ambitious': 1})
        hyphen = JobAd(u"Sharing, co-operative, 'servant-leader'")
        self.assertEqual(hyphen.make_word_dict(),
            {'sharing': 1, 'cooperative': 1, 'servantleader': 1})
        mdash = JobAd(u"Sharing—ambitious")
        self.assertEqual(mdash.make_word_dict(), 
            {'sharing': 1, 'ambitious': 1})
        bracket = JobAd(u"Sharing(ambitious) and (leader)")
        self.assertEqual(bracket.make_word_dict(), 
            {'sharing': 1, 'ambitious': 1, 'and': 1, 'leader': 1})
        sqbracket = JobAd(u"Sharing[ambitious] and [leader]")
        self.assertEqual(sqbracket.make_word_dict(), 
            {'sharing': 1, 'ambitious': 1, 'and': 1, 'leader': 1})
        abracket = JobAd(u"Sharing<ambitious> and <leader>")
        self.assertEqual(abracket.make_word_dict(), 
            {'sharing': 1, 'ambitious': 1, 'and': 1, 'leader': 1})
        space = JobAd(u"Sharing ambitious ")
        self.assertEqual(space.make_word_dict(), 
            {'sharing': 1, 'ambitious': 1})
        amp = JobAd(u"Sharing&ambitious, empathy&kindness,")
        self.assertEqual(amp.make_word_dict(),
            {'sharing': 1, 'ambitious': 1, 'empathy': 1, 'kindness': 1})
        asterisk = JobAd(u"Sharing&ambitious*, empathy*kindness,")
        self.assertEqual(asterisk.make_word_dict(),
            {'sharing': 1, 'ambitious': 1, 'empathy': 1, 'kindness': 1})
        atandquestion = JobAd(u"Lead \"Developer\" Who is Connect@HBS? We ")
        self.assertEqual(atandquestion.make_word_dict(),
            {'lead': 1, 'developer': 1, 'who': 1, 'is': 1,
            'connect': 1, 'hbs': 1, 'we': 1})
        exclaim = JobAd(u"Lead Developer v good!")
        self.assertEqual(exclaim.make_word_dict(),
            {'good': 1, 'v': 1, 'lead': 1, 'developer': 1})
        curls = JobAd(u"“Lead” ‘Developer’ v good!")
        self.assertEqual(exclaim.make_word_dict(),
            {'lead': 1, 'developer': 1, 'v': 1, 'good': 1})

    def test_extract_coded_words(self):
        j1 = JobAd(u"Ambition:competition–decisiveness, empathy&kindness")
        self.assertEqual(j1.masculine_coded_words,
            'decisiveness,competition,ambition')
        self.assertEqual(j1.masculine_word_count, 3)
        self.assertEqual(j1.feminine_coded_words, "kindness,empathy")
        self.assertEqual(j1.feminine_word_count, 2)
        j2 = JobAd(u"empathy&kindness")
        self.assertEqual(j2.masculine_coded_words, "")
        self.assertEqual(j2.masculine_word_count, 0)
        self.assertEqual(j2.feminine_coded_words, "kindness,empathy")
        self.assertEqual(j2.feminine_word_count, 2)
        j3 = JobAd(u"empathy irrelevant words kindness")
        self.assertEqual(j3.masculine_coded_words, "")
        self.assertEqual(j3.masculine_word_count, 0)
        self.assertEqual(j3.feminine_coded_words, "kindness,empathy")
        self.assertEqual(j3.feminine_word_count, 2)
        j4 = JobAd(u"Ambition:competition–decisiveness")
        self.assertEqual(j4.masculine_coded_words,
            'decisiveness,competition,ambition')
        self.assertEqual(j4.masculine_word_count, 3)
        self.assertEqual(j4.feminine_coded_words, "")
        self.assertEqual(j4.feminine_word_count, 0)
        j5 = JobAd(u"Ambition:competition–decisiveness decisiveness")
        self.assertEqual(j5.masculine_coded_words,
            'decisiveness (2 times),competition,ambition')
        self.assertEqual(j5.masculine_word_count, 4)
        self.assertEqual(j5.feminine_coded_words, "")
        self.assertEqual(j5.feminine_word_count, 0)

    def test_assess_coding_neutral_and_empty(self):
        j1 = JobAd("irrelevant words")
        self.assertFalse(j1.masculine_word_count)
        self.assertFalse(j1.feminine_word_count)
        self.assertEqual(j1.coding, "empty")
        j2 = JobAd("sharing versus aggression")
        self.assertEqual(j2.masculine_word_count, j2.feminine_word_count)
        self.assertEqual(j2.coding, "neutral")

    def test_assess_coding_masculine(self):
        j1 = JobAd(u"Ambition:competition–decisiveness, empathy&kindness")
        self.assertEqual(j1.masculine_word_count, 3)
        self.assertEqual(j1.feminine_word_count, 2)
        self.assertEqual(j1.coding, "masculine-coded")
        j2 = JobAd(u"Ambition:competition–decisiveness, other words")
        self.assertEqual(j2.masculine_word_count, 3)
        self.assertEqual(j2.feminine_word_count, 0)
        self.assertEqual(j2.coding, "masculine-coded")
        j3 = JobAd(u"Ambition:competition–decisiveness&leadership, other words")
        self.assertEqual(j3.masculine_word_count, 4)
        self.assertEqual(j3.feminine_word_count, 0)
        self.assertEqual(j3.coding, "strongly masculine-coded")
        # NB: repeated "decisiveness" in j4
        j4 = JobAd(u"Ambition:competition–decisiveness&leadership,"
            " decisiveness, stubborness, sharing and empathy")
        self.assertEqual(j4.masculine_word_count, 6)
        self.assertEqual(j4.feminine_word_count, 2)
        self.assertEqual(j4.coding, "strongly masculine-coded")

    def test_assess_coding_feminine(self):
        j1 = JobAd(u"Ambition:competition, empathy&kindness, co-operation")
        self.assertEqual(j1.masculine_word_count, 2)
        self.assertEqual(j1.feminine_word_count, 3)
        self.assertEqual(j1.coding, "feminine-coded")
        j2 = JobAd(u"empathy&kindness, co-operation and some other words")
        self.assertEqual(j2.masculine_word_count, 0)
        self.assertEqual(j2.feminine_word_count, 3)
        self.assertEqual(j2.coding, "feminine-coded")
        j3 = JobAd(u"empathy&kindness, co-operation, trust and other words")
        self.assertEqual(j3.masculine_word_count, 0)
        self.assertEqual(j3.feminine_word_count, 4)
        self.assertEqual(j3.coding, "strongly feminine-coded")
        j4 = JobAd(u"Ambition:competition, empathy&kindness and"
            " responsibility, co-operation, honesty, trust and other words")
        self.assertEqual(j4.masculine_word_count, 2)
        self.assertEqual(j4.feminine_word_count, 6)
        self.assertEqual(j4.coding, "strongly feminine-coded")

    def test_analyse(self):
        j1 = JobAd(u"Ambition:competition–decisiveness&leadership,"
            " decisiveness, stubborness, sharing and empathy")
        self.assertEqual(j1.ad_text, u"ambition:competition–decisiveness"
            "&leadership, decisiveness, stubborness, sharing and empathy")
        self.assertTrue(j1.coding == "strongly masculine-coded")
        self.assertEqual(j1.masculine_word_count, 6)
        self.assertEqual(j1.masculine_coded_words, "stubborness,decisiveness "
            "(2 times),competition,leadership,ambition")
        self.assertEqual(j1.feminine_word_count, 2)
        self.assertEqual(j1.feminine_coded_words,"sharing,empathy")

if __name__ == '__main__':
    unittest.main()
