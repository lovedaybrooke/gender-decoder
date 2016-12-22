import requests
import unicodecsv as csv
import json

with open("allnewtoold.csv", "r") as inputfile:
    csvreader = csv.reader(inputfile)
    url = 'http://0.0.0.0:5000/upload'
    for line in csvreader:
        if line[0] != "hash":
            text = line[1]
            hash = line[0]
            date = line[2]
            requests.post(url, 
                headers={'Content-Type': 'application/json'}, 
                data=json.dumps({'date': date, 'hash': hash, 'text': text}))
            print hash

