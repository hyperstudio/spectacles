# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
import spacy
import warnings
from bs4 import BeautifulSoup

warnings.filterwarnings('ignore', category=UserWarning, module='bs4')

_nlp = None

def nlp():
    global _nlp
    if _nlp is None:
        print('loading spacy/NLP')
        _nlp = spacy.load('en_core_web_sm')
    return _nlp

def vector_from_html_text(text):
    soup = BeautifulSoup(text, 'html5lib')
    text = soup.get_text(separator=u'\n', strip=False)
    vector = nlp()(text).vector
    # Blank text consisting of <p><br/></p> will have a 0-length vector after
    # text cleaning.
    if vector.shape[0] > 0:
        return vector
    return None
