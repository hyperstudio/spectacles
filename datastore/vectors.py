# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
import spacy
from bs4 import BeautifulSoup

_nlp = None

def nlp():
    global _nlp
    if _nlp is None:
        print('loading spacy/NLP')
        try:
            _nlp = spacy.load('en_core_web_lg')
        except IOError:
            _nlp = spacy.load('en_core_web_sm')
    return _nlp

def vector_from_html_text(text):
    soup = BeautifulSoup(text, 'html5lib')
    return nlp()(soup.get_text(separator=u'\n', strip=False)).vector
