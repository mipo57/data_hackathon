# -*- coding: utf-8 -*-

import urllib
import urllib2
import requests
import json
import pickle
from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

url = "http://multiservice.nlp.ipipan.waw.pl/pl/addRequest"

def get_phrases(text):
    params = u"request=%7B%22text%22%3A%22" + urllib.quote_plus(text.encode('utf8')) + u"%3F%22%2C%22processingChain%22%3A%5B%7B%22serviceName%22%3A%22Concraft%22%2C%22options%22%3A%7B%7D%7D%2C%7B%22serviceName%22%3A%22Spejd%22%2C%22options%22%3A%7B%7D%7D%2C%7B%22serviceName%22%3A%22Nerf%22%2C%22options%22%3A%7B%7D%7D%2C%7B%22serviceName%22%3A%22MentionStat%22%2C%22options%22%3A%7B%7D%7D%2C%7B%22serviceName%22%3A%22Bartek3%22%2C%22options%22%3A%7B%7D%7D%5D%2C%22clrs%22%3A%220%22%7D"


    the_page = requests.get(url, params).json()
    results = requests.get("http://multiservice.nlp.ipipan.waw.pl/pl/getResult/json/" + the_page['token'])

    phrases = results.json()['result']['coreferences']
    return phrases


with open("cities.pickle", "r") as f:
    cities = pickle.load(f)
def extract_city(phrases):
    exceptions = ["okolica"]

    for phrase in phrases:
        value = phrase['dominant'].lower()

        if value in cities and value not in exceptions:
            return value
    return ""

def extract_type(phrases):
    possible_criterias = {
        u'liceum': 'Liceum Ogólnokształcące'
    }

    for phrase in phrases:
        phrase = phrase['dominant'].lower()

        for key, value in possible_criterias.items():
            if key in phrase:
                return value

    return ""

def extract_performance_criteria(phrases):
    possible_criterias = {
        u"angielski": "18", 
        u"niemiecki": "21", 
        u"francuski": "19", 
        u"włoski": "85", 
        u"matematyka": "87",
        u"matematyczny": "87",
        u"językowy": "88",
        u"językowy": "88",
        u"kryminolog": "44",
        u"kryminologia": "44",
        u"administracja": "0",
        u"analityka gospodarczy": "1",
        u"analiza dana": "2",
        u"architektura": "3",
        u"architekt": "3",
        u"lotnictwo": "47",
        u"lotnik": "47",
        u"kosmonautyka": "47",
        u"kosmonauta": "47"
    }

    for phrase in phrases:
        phrase = phrase['dominant'].lower()

        for key, value in possible_criterias.items():
            if key in phrase:
                return value

    return ""

def check_is_local_search(phrases):
    local_tags = [u"okolica", u"pobliże"]

    for phrase in phrases:
        phrase = phrase['dominant'].lower()

        for local_tag  in local_tags:
            if local_tag in phrase:
                return True

    return False

def check_is_sorted(phrases):
    positive_tags = ["dobry", "wielki"]

    for phrase in phrases:
        phrase = phrase['dominant'].lower()

        for local_tag in positive_tags:
            if local_tag in phrase:
                return True

    return False

def check_is_for_disabled(phrases):
    positive_tags = [u"niepełnosprawny", u"kaleka", u"inwalida"]

    for phrase in phrases:
        phrase = phrase['dominant'].lower()

        for local_tag in positive_tags:
            if local_tag in phrase:
                return True

    return False

@app.route('/process_text')
def process_text():
    text = request.args.get("text")

    phrases = get_phrases(text)
    print(phrases)

    city = extract_city(phrases)
    criteria = extract_performance_criteria(phrases)
    is_sorted = check_is_sorted(phrases)
    is_local = not city and check_is_local_search(phrases)
    is_for_disabled = check_is_for_disabled(phrases)
    school_type = extract_type(phrases)

    ret = {
        "city": city,
        "criteria": criteria,
        "sorted": is_sorted,
        "local": is_local,
        "for_disabled": is_for_disabled,
        "type": school_type
    }

    return json.dumps(ret)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
