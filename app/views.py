# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
import pdb
import json
import uuid
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.middleware import csrf

from app.utils import json_response
from app.utils import props_template
from app.utils import to_dict
from app.utils import to_json
from app.search import find_annotations
from app.search import find_documents
from datastore.auth import generate_consumer_token
from datastore.models import Annotation
from datastore.models import Document


@require_GET
@login_required
@ensure_csrf_cookie
@props_template('app/documents.html')
def documents(request):
    user = request.user
    if not user.is_authenticated:
        user = None
    # Fetch the documents without the 'text' attribute, because for the listing
    # view it's unnecessary.
    fields = set(Document._json_fields)
    fields.remove('text')
    docs = Document.objects.defer('text')[:100]
    return {
        'documents': to_dict(docs, fields=fields),
        'user': to_dict(user),
    }


@require_GET
@login_required
@ensure_csrf_cookie
@props_template('app/document.html')
def document(request, document_id):
    doc = get_object_or_404(Document, id=document_id)
    return {
        'document': doc,
        'annotations': doc.annotations.all(),
    }

# TODO: move these api views to a separate file?

@require_GET
@login_required
@json_response
def api_token(request):
    token = generate_consumer_token(request.user.id)
    return token

def _clean_ann(a, document_id):
    # TODO: weird URI and permissions updating shouldn't have to happen
    a['uri'] = document_id
    a['permissions'] = {
        'read': [],
        'update': [],
        'delete': [],
        'admin': [],
    }
    return a

def _clean_annotations(annotations, document_id):
    for a in annotations:
        yield _clean_ann(a.data, document_id)


@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@ensure_csrf_cookie
@json_response
def api_store_crud(request, document_id, annotation_id=None):
    print('request.method =', request.method)
    print('  document_id =', document_id)
    print('  annotation_id =', annotation_id)
    doc = get_object_or_404(Document, id=document_id)

    if request.method == 'GET':
        return to_dict(list(_clean_annotations(
            doc.annotations.all(),
            document_id
        )))

    if request.method == 'DELETE':
        ann = doc.annotations.filter(data__id=annotation_id)
        if ann.exists():
            ann = ann[0]
        else:
            raise NotImplementedError('404!')
        ann.delete()
        return None

    if request.method == 'POST':
        try:
            req_data = json.loads(request.body)
        except (TypeError, ValueError):
            raise NotImplementedError('400!')
        new_id = uuid.uuid4()
        now = datetime.utcnow()

        # Can't end up passing through a Lazy object wrapper (request.user)
        # because the elasticsearch-dsl code doesn't handle it well.
        user = request.user
        if hasattr(user, '_wrapped'):
            user = user._wrapped

        ann_data = {
            'id': new_id.hex,
            'annotator_schema_version': 'v1.0',
            'created': now.isoformat(),
            'updated': now.isoformat(),
            'text': req_data['text'],
            'quote': req_data['quote'],
            'uri': req_data['uri'],
            'ranges': req_data['ranges'],
            'user': user.email,
            'consumer': 'spectacles',
            'tags': req_data.get('tags', []),
            'permissions': req_data.get('permissions', {
                'read': [],
                'admin': [],
                'update': [],
                'delete': [],
                '_default': True,
            }),
        }
        ann = Annotation(
            uuid=new_id,
            created_at=now,
            updated_at=now,
            creator=user,
            document=doc,
            data=ann_data,
        )
        ann.save()
        return to_dict(_clean_ann(ann.data, document_id))

    if request.method == 'PUT':
        ann = doc.annotations.filter(data__id=annotation_id)
        if ann.exists():
            ann = ann[0]
        else:
            raise NotImplementedError('404!')
        try:
            updated = json.loads(request.body)
        except (TypeError, ValueError):
            raise NotImplementedError('400!')

        ann.data.update(updated)
        ann.save()
        return to_dict(_clean_ann(ann.data, document_id))

    raise NotImplementedError(request.method)


@require_POST
@login_required
@ensure_csrf_cookie
@json_response
def api_search_documents(request):
    fields = set(Document._json_fields)
    fields.remove('text')
    try:
        req = json.loads(request.body)
    except (TypeError, ValueError):
        raise NotImplementedError('400!')
    return to_dict(find_documents(req['query']), fields=fields)

@require_POST
@login_required
@ensure_csrf_cookie
@json_response
def api_search_annotations(request):
    try:
        req = json.loads(request.body)
    except (TypeError, ValueError):
        raise NotImplementedError('400!')
    return to_dict(find_annotations(req['query']))


# TODO: clean up this views file?
@require_http_methods(['POST', 'GET'])
@ensure_csrf_cookie
@props_template('app/login.html')
def login(request):
    props = {
        'csrftoken': csrf.get_token(request),
    }
    next_ = request.GET.get('next', None)
    if next_ is not None:
        props['next'] = next_

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if next_ is not None:
                return redirect(next_)
            return redirect('app-root')
        props.update({
            'username': username,
            'password': password,
            'error': True,
        })
    return props


@require_http_methods(['POST', 'GET'])
@ensure_csrf_cookie
def logout(request):
    auth_logout(request)
    return redirect('app-root')
