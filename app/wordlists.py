# These words are written as the stem to make it easier to match all variants.
# In other words, the suffix is intentionally left out.

non_coded_exceptions = [
    "sharepoint"
]

feminine_coded_words = [
    "agree",
    "affectionate",
    "child",
    "cheer",
    "collab",
    "commit",
    "communal",
    "compassion",
    "connect",
    "considerate",
    "cooperat",
    "co-operat",
    "depend",
    "emotiona",
    "empath",
    "feel",
    "flatterable",
    "gentle",
    "honest",
    "interpersonal",
    "interdependen",
    "interpersona",
    "inter-personal",
    "inter-dependen",
    "inter-persona",
    "kind",
    "kinship",
    "loyal",
    "modesty",
    "nag",
    "nurtur",
    "pleasant",
    "polite",
    "quiet",
    "respon",
    "sensitiv",
    "submissive",
    "support",
    "sympath",
    "tender",
    "together",
    "trust",
    "understand",
    "warm",
    "whin",
    "enthusias",
    "inclusive",
    "yield",
    "share",
    "sharin"
]

masculine_coded_words = [
    "active",
    "adventurous",
    "aggress",
    "ambitio",
    "analy",
    "assert",
    "athlet",
    "autonom",
    "battle",
    "boast",
    "challeng",
    "champion",
    "compet",
    "confident",
    "courag",
    "decid",
    "decision",
    "decisive",
    "defend",
    "determin",
    "domina",
    "dominant",
    "driven",
    "fearless",
    "fight",
    "force",
    "greedy",
    "head-strong",
    "headstrong",
    "hierarch",
    "hostil",
    "impulsive",
    "independen",
    "individual",
    "intellect",
    "lead",
    "logic",
    "objective",
    "opinion",
    "outspoken",
    "persist",
    "principle",
    "reckless",
    "self-confiden",
    "self-relian",
    "self-sufficien",
    "selfconfiden",
    "selfrelian",
    "selfsufficien",
    "stubborn",
    "superior",
    "unreasonab"
]

hyphenated_coded_words = [
    "co-operat",
    "inter-personal",
    "inter-dependen",
    "inter-persona",
    "self-confiden",
    "self-relian",
    "self-sufficien"
]

possible_codings = (
    "strongly feminine-coded",
    "feminine-coded",
    "neutral",
    "masculine-coded",
    "strongly masculine-coded"
)

explanations = {
    "feminine-coded": ("This job ad uses more words that "
                        "are subtly coded as feminine than words that are "
                        "subtly coded as masculine (according to the "
                        "research). Fortunately, the research suggests "
                        "this will have only a slight effect on how appealing "
                        "the job is to men, and will encourage women applicants."),
    "masculine-coded": ("This job ad uses more words that "
                        "are subtly coded as masculine than words that are "
                        "subtly coded as feminine (according to the research). "
                        "It risks putting women off applying, but will probably "
                        "encourage men to apply."),
    "strongly feminine-coded": ("This job ad uses more words that "
                        "are subtly coded as feminine than words that are "
                        "subtly coded as masculine (according to the "
                        "research). Fortunately, the research suggests this "
                        "will have only a slight effect on how appealing the "
                        "job is to men, and will encourage women applicants."),
    "strongly masculine-coded": ("This job ad uses more words that "
                        "are subtly coded as masculine than words that are subtly "
                        "coded as feminine (according to the research). It risks "
                        "putting women off applying, but will probably encourage "
                        "men to apply."),
    "empty": ("This job ad doesn't use any words "
              "that are subtly coded as masculine or feminine (according to "
              "the research). It probably won't be off-putting to men or "
              "women applicants."),
    "neutral": ("This job ad uses an equal number "
              "of words that are subtly coded as masculine and feminine "
              "(according to the research). It probably won't be off-putting "
              "to men or women applicants.")
}
