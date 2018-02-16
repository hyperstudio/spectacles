# coding: utf-8
from elasticsearch_dsl.query import MultiMatch
from elasticsearch_dsl.query import QueryString

from datastore.documents import ESAnnotation, ESDocument


def find_annotations(query, max_count=50, highlight='text', document_id=None):
    m = QueryString(
        query=query,
        #fields=['creator__email', 'creator__name', 'quote', 'text', 'tags'],
        fuzziness='AUTO'
    )
    s = ESAnnotation.search()
    if highlight is not None:
        s = s.highlight_options(order='score')
        s = s.highlight(highlight, fragment_size=50)
    if document_id is not None:
        s = s.filter('match', document_id=document_id)
    s = s.source(include=['quote', 'text', 'tags', 'creator', 'document_id', 'updated_at', 'created_at', 'uuid'])
    return s.query(m).execute()


def find_documents(query, max_count=50, highlight='text'):
    m = MultiMatch(
        query=query,
        fields=['text', 'title', 'author', 'creator__name', 'creator__email', 'updated_at', 'created_at'],
        fuzziness='AUTO'
    )
    s = ESDocument.search()
    if highlight is not None:
        s = s.highlight_options(order='score')
        s = s.highlight(highlight, fragment_size=50)
    s = s.source(include=['title', 'author', 'creator', 'tags'])
    return s.query(m).execute()
