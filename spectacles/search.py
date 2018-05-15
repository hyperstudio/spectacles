# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals
import re
import json
from elasticsearch_dsl.query import MultiMatch
from elasticsearch_dsl.query import Q
from elasticsearch_dsl.query import QueryString

from datastore.documents import ESAnnotation, ESDocument
from datastore.models import Annotation, Document


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


def find_annotations(query, highlight='text', document_id=None, creator_id=None):
    m = intelligent_match(
        query=query,
        fields=['creator.email', 'creator.name', 'quote', 'text', 'tags'],
        fuzziness='AUTO'
    )
    s = ESAnnotation.search()
    s = s.source(include=[
        'id',
        'uuid',
        'document_id',
        'document',

        'quote',
        'text',
        'tags',
        'creator',

        'updated_at',
        'created_at',
    ])
    s = s.query(m)
    if creator_id is not None:
        s = s.query(Q('bool', must=[Q('match', creator__id=creator_id)]))
    if document_id is not None:
        s = s.query(Q('bool', must=[Q('match', document__id=document_id)]))
    if highlight is not None:
        s = s.highlight_options(order='score')
        s = s.highlight(highlight, fragment_size=50)
    results = s.execute()
    return results


def find_documents(query, highlight='text', creator_id=None, titles_only=False):
    fields = ['title', 'author', 'creator.name', 'creator.email']
    if not titles_only:
        fields.append('text')
    m = intelligent_match(
        query=query,
        fields=fields,
        fuzziness='AUTO'
    )
    s = ESDocument.search()
    s = s.source(include=[
        'id',

        'title',
        'author',
        'tags',
        'creator',

        'updated_at',
        'created_at',
    ])
    s = s.query(m)
    if creator_id is not None:
        s = s.query(Q('bool', must=[Q('match', creator__id=creator_id)]))
    if highlight is not None:
        # TODO: Need to make sure we're using the existing analysis vectors instead of the plain
        # highlighter, for performance purposes. Also, need to return the offsets of the highlights
        s = s.highlight_options(order='score')
        s = s.highlight(highlight, fragment_size=50)
    results = s.execute()
    return results
