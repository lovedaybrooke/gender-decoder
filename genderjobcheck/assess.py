import re

import wordlists

def assess(ad_text):
    ad_text = re.sub("[\.\t\,\:;\(\)\.]", "", ad_text, 0, 0).split(" ")
    
    masculine_coded_words = [adword for adword in ad_text
        for word in wordlists.masculine_coded_words
        if adword.startswith(word)]
    
    feminine_coded_words = [adword for adword in ad_text
        for word in wordlists.feminine_coded_words
        if adword.startswith(word)]
    
    if feminine_coded_words and not masculine_coded_words:
        result = "strongly feminine-coded"
    elif masculine_coded_words and not feminine_coded_words:
        result = "strongly masculine-coded"
    elif not masculine_coded_words and not feminine_coded_words:
        result = "neutral"
    else: 
        if len(feminine_coded_words) == len(masculine_coded_words):
            result = "neutral"
        if ((len(feminine_coded_words) / len(masculine_coded_words)) >= 2 and 
            len(feminine_coded_words) > 5):
            result = "strongly feminine-coded"
        if ((len(masculine_coded_words) / len(feminine_coded_words)) >= 2 and 
            len(masculine_coded_words) > 5):
            result = "strongly masculine-coded"
        if len(feminine_coded_words) > len(masculine_coded_words):
            result = "feminine-coded"
        if len(masculine_coded_words) > len(feminine_coded_words):
            result = "masculine-coded"
    
    if "feminine" in result:
        explanation = ("This job ad uses more words that are stereotypically feminine "
            "than words that are stereotypically masculine. Fortunately, the research "
            "suggests this will have only a slight effect on how appealing the job is "
            "to men, and will encourage women applicants.")
    elif "masculine" in result:
        explanation = ("This job ad uses more words that are stereotypically masculine "
            "than words that are stereotypically feminine. It risks putting women off "
            "applying, but will probably encourage men to apply.")
    else:
        explanation = ("This job ad uses an equal number of words that are "
            "stereotypically masculine and stereotypically feminine. It probably won't "
            "be off-putting to men or women applicants.")

    return {"result": result,
            "explanation": explanation,
            "masculine_coded_words": list(set(masculine_coded_words)),
            "feminine_coded_words": list(set(feminine_coded_words))
            }
