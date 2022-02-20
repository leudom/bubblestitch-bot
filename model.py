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

