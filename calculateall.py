from __future__ import division

import requests
import unicodecsv as csv

with open("allhashes.csv", "r") as inputfile:
    csvreader = csv.reader(inputfile)
    lines = 18088
    i = 1
    url = 'http://0.0.0.0:8000/calculate/'
    for line in csvreader:
        if line[0] != "hash":
            requests.post(url+line[0])
            percent = int((i*100)/lines)
            print "{0} done ({1}%), just called {2}".format(i, percent, line[0])
            i += 1