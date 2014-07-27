# 1. Assessor:
# - breaks words into list
# - checks for each word in the the target list in the actual list
# - if it finds the word, stores it in a new dict of masc & fem
# - calculates the balance of masc & fem
# - returns score in form of image and list of words for masc & fem

from wordlists import *

user_input = raw_input("Please paste your job ad.")

job_ad_language = user_input.translate(None, "!,.;:?()").split(" ")

masculine_coded_language = [adword for adword in job_ad_language
	for word in masculine_coded_words
	if adword[:len(word)] == word]
	
feminine_coded_language = [adword for adword in job_ad_language
	for word in feminine_coded_words
	if adword[:len(word)] == word]

print "\n\n"
	
if feminine_coded_language > masculine_coded_language:
	print ("Your job ad uses more words associated with stereotypes of women "
		"than words that are stereotypically masculine.")
else:
	print ("Your job ad uses more words associated with stereotypes of men than "
		"words that are stereotypically feminine.")
	
print "\n"

if feminine_coded_language:
	print "FEMININE LANGUAGE"
	print feminine_coded_language
	
if masculine_coded_language:
	print "MASCULINE LANGUAGE"
	print masculine_coded_language