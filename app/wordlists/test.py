source = "novelty lorem ipsum generators"
language_name = "Gobbledegook"
language_code = "test"

feminine_coded_words = [
    "humblebrag",
    "ready-made",
    "cloud",
    "sourdough",
    "pabst"
]

masculine_coded_words = [
    "glendronach",
    "spritzer",
    "sake",
    "manhattan",
    "sun-down"
]

hyphenated_coded_words = [word for word in feminine_coded_words
                          if "-" in word] + [
                          word for word in masculine_coded_words 
                          if "-" in word]
