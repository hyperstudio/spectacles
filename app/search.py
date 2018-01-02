# coding: utf-8
from elasticsearch_dsl.query import MultiMatch
from datastore.documents import ESAnnotation, ESDocument


def find_annotations(query, max_count=50, highlight='quote'):
    m = MultiMatch(
        query=query,
        fields=['creator__email', 'creator__name', 'quote', 'text', 'tags'],
        fuzziness='AUTO'
    )
    s = ESAnnotation.search()
    if highlight is not None:
        s = s.highlight_options(order='score')
        s = s.highlight(highlight, fragment_size=50)
    s = s.source(include=['quote', 'text', 'tags', 'creator'])
    return s.query(m).execute()

def find_documents(query):
    m = MultiMatch(
        query=query,
        fields=['text', 'title', 'author', 'creator__name', 'creator__email'],
        fuzziness='AUTO'
    )
    return ESDocument.search().query(m).to_queryset()