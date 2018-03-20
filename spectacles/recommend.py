# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals

from django.conf import settings

from nndb.client import Client
from nndb.client import RPCException


_ann_client = None
def ann_client():
    global _ann_client
    if _ann_client is None:
        _ann_client = Client(
                settings.NNDB_SERVICES['annotations']['service_name'])
    return _ann_client


_doc_client = None
def doc_client():
    global _doc_client
    if _doc_client is None:
        _doc_client = Client(
                settings.NNDB_SERVICES['documents']['service_name'])
    return _doc_client



def make_recommender(client_fetcher):
    def recommender(t, n=20, search_k=1000):
        c = client_fetcher()
        v = t.get_vector()
        if v is None:
            # TODO: alternate type of recommendation engine here?
            return None
        try:
            return c.neighbors_by_vector(v, n, search_k=search_k)
        except RPCException as e:
            print(e)
            return []
    return recommender

recommend_documents = make_recommender(doc_client)
recommend_annotations = make_recommender(ann_client)
