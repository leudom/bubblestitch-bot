# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

import os
import pandas as pd
import json
import requests
from newspaper import Article
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

"""
def extract_article(url):
    article = Article(url)
    try:
        article.download()
        article.parse()
    except:
        logger.exception('Article could not be downloaded and parsed', exc_info=True)

    return article.title, article.text

title, body = extract_article(r'https://dietagespresse.com/weil-regierung-es-nicht-hinkriegt-tagespresse-startet-eigene-impflotterie/')
#print(title)
#print(body)

def prepare_model_input (title, body):
    return title + ' ' + body

input_txt = prepare_model_input(title, body)
print(input_txt)

def predict(endpoint_url, input):
    payload = {'data': [input]}
    headers = {'Content-Type':'appliction/json'}
    r = requests.post(url=endpoint_url,
                  data=(json.dumps(payload)),
                  headers=headers)
    logger.info(r.status_code)
    logger.info(r.json())
    return r.json()
"""

class FakeNewsAgent():

    def __init__(self, endpoint_url):
        self.endpoint_url = endpoint_url

    def extract_article(self, url):
        article = Article(url)
        try:
            article.download()
            article.parse()
        except:
            logger.exception('Article could not be downloaded and parsed', exc_info=True)

        return article.title, article.text

    def _prepare_model_input (self, title, body):

        return title + ' ' + body


    def predict(self, url):

        title, body = self.extract_article(url)
        input = self._prepare_model_input(title, body)

        payload = {'data': [input]}
        headers = {'Content-Type':'appliction/json'}

        r = requests.post(url=self.endpoint_url,
                data=(json.dumps(payload)),
                headers=headers)

        logger.info(r.status_code)
        logger.info(r.json())

        return r.json()

agent = FakeNewsAgent(os.getenv('ENDPOINT_URL'))

url = 'https://dietagespresse.com/weil-regierung-es-nicht-hinkriegt-tagespresse-startet-eigene-impflotterie/'
json_out = agent.predict(url)
print(json_out)
print(type(json_out))
print(json_out['data'][0])

