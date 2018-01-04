# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
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
    anns_r = list(search.find_annotations(req['query']).hits)

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
    docs_r = list(search.find_documents(req['query']).hits)

    return to_dict({
        'documents': to_dict(docs_r, fields=fields)
    })
