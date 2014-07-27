import re

# 1. Assessor:
# - breaks words into list
# - checks for each word in the the target list in the actual list
# - if it finds the word, stores it in a new dict of masc & fem
# - calculates the balance of masc & fem
# - returns score in form of image and list of words for masc & fem

import wordlists

def assess(ad_text):
    ad_text = re.sub("[\.\t\,\:;\(\)\.]", "", ad_text, 0, 0).split(" ")
    
    masculine_coded_words = [adword for adword in ad_text
        for word in wordlists.masculine_coded_words
        if adword[:len(word)] == word]
    
    feminine_coded_words = [adword for adword in ad_text
        for word in wordlists.feminine_coded_words
        if adword[:len(word)] == word]
    
    score = calculate_score(len(feminine_coded_words), len(masculine_coded_words))
    
    if score == 4:
        explanation = ("This job ad has an equal number of words that are stereotypically"
            " masculine and stereotypically feminine. It probably won't be off-putting to"
            " men or women applicants.")
    elif score < 4:
        explanation = ("This job ad has more words that are stereotypically masculine "
            "than words that are stereotypically feminine. It risks putting women off "
            "applying, but will probably encourage men to apply.")
    elif score > 4:
        explanation = ("This job ad has more words that are stereotypically feminine "
            "than words that are stereotypically masculine. Fortunately, the research "
            "suggests this will have only a slight effect on how appealing the job is "
            "to men, and will encourage women applicants.")
        
    return {"score": score,
            "explanation": explanation,
            "masculine_coded_words": list(set(masculine_coded_words)),
            "feminine_coded_words": list(set(feminine_coded_words))
        }

def calculate_score(number_of_feminine_words, number_of_masculine_words):
    # 7 is overwhelmingly feminine-coded, 1 is overwhelmingly masculine-coded
    if not number_of_masculine_words:
        return 7
    if not number_of_feminine_words:
        return 1
    if number_of_feminine_words == number_of_masculine_words:
        return 4
    if ((number_of_feminine_words / number_of_masculine_words) >= 2 and 
        number_of_feminine_words > 5):
        return 6
    if ((number_of_masculine_words / number_of_feminine_words) >= 2 and 
        number_of_masculine_words > 5):
        return 2
    if number_of_feminine_words > number_of_masculine_words:
        return 5
    if number_of_masculine_words > number_of_feminine_words:
        return 3
