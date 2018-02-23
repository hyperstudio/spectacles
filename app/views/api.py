# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from app import search
from app.utils import json_response
from app.utils import to_dict
from datastore.models import Document


@require_POST
@login_required
@ensure_csrf_cookie
@json_response
def search_annotations(request):
    try:
        req = json.loads(request.body)
    except (TypeError, ValueError):
        raise NotImplementedError('400!')

    print('ANNS query:', req['query'])
    anns_r = list(search.find_annotations(
        query=req['query'],
        document_id=req.get('document_id', None),
    ).hits)
    # TODO: fix this client-side filter (should be happening in ES)
    creator_id = req.get('creator_id', None)
    if creator_id is not None:
        creator = get_object_or_404(get_user_model(), id=creator_id)
        anns_r = filter(lambda x: x.creator.email == creator.email, anns_r)

    return {
        'annotations': to_dict(anns_r),
    }


@require_POST
@login_required
@ensure_csrf_cookie
@json_response
def search_documents(request):
    try:
        req = json.loads(request.body)
    except (TypeError, ValueError):
        raise NotImplementedError('400!')

    print('DOCS query:', req['query'])
    fields = set(Document._json_fields)
    fields.remove('text')
    docs_r = list(search.find_documents(
        query=req['query'],
        archive_id=req.get('archive_id', None),
    ).hits)
    print('FINISHED docs query')

    return to_dict({
        'documents': to_dict(docs_r, fields=fields)
    })
