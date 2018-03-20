# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals
import re
import json
from elasticsearch_dsl.query import MultiMatch
from elasticsearch_dsl.query import QueryString

from datastore.documents import ESAnnotation, ESDocument

def intelligent_match(query, fields, fuzziness='AUTO'):
    # Queries surrounded by [.. brackets ..] should be parsed, without those
    # brackets, by the ES QueryString parser. Otherwise, default to normal
    # fuzzy search over all of the appropriate fields.
    r = re.match('^\[(.*)\]$', query)
    if r:
        return QueryString(
            query=r.groups()[0],
            fields=fields,
            fuzziness=fuzziness
        )
    else:
        return MultiMatch(
            query=query,
            fields=fields,
            fuzziness=fuzziness,
        )


def find_annotations(query, max_count=50, highlight='text', document_id=None):
    q = intelligent_match(
        query=query,
        fields=['creator.email', 'creator.name', 'quote', 'text', 'tags'],
        fuzziness='AUTO'
    )
    s = ESAnnotation.search()
    s = s.source(include=['quote', 'text', 'tags', 'creator', 'document_id', 'updated_at', 'created_at', 'uuid'])
    if highlight is not None:
        s = s.highlight_options(order='score')
        s = s.highlight(highlight, fragment_size=50)
    if document_id is not None:
        s = s.filter('match', document_id=document_id)
    s = s.query(q)
    #print(json.dumps(s.to_dict(), indent=2))
    return s.execute()
    results = s.execute()


def find_documents(query, max_count=50, highlight='text', archive_id=None):
    m = intelligent_match(
        query=query,
        fields=['text', 'title', 'author', 'creator.name', 'creator.email'],
        fuzziness='AUTO'
    )
    s = ESDocument.search()
    if highlight is not None:
        # TODO: Need to make sure we're using the existing analysis vectors instead of the plain
        # highlighter, for performance purposes. Also, need to return the offsets of the highlights
        s = s.highlight_options(order='score')
        s = s.highlight(highlight, fragment_size=50)
    if archive_id is not None:
        s = s.filter('match', archive_id=archive_id)
    s = s.source(include=['title', 'author', 'creator', 'tags', 'updated_at', 'created_at'])
    return s.query(m).execute()
