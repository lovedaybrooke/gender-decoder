import importlib

__all__ = ["en"]
# __all__ = ["en", "test"]

all_lists = {}

for item in __all__:
    my_module = importlib.import_module('.{0}'.format(item), 'app.wordlists')
    all_lists[my_module.language_code] = {
        "language_name": my_module.language_name,
        "feminine_coded_words": sorted(my_module.feminine_coded_words),
        "masculine_coded_words": sorted(my_module.masculine_coded_words)
    }