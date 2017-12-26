# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
import pdb
import json

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
from datastore.auth import generate_consumer_token
from datastore.models import Annotation
from datastore.models import Document


@require_http_methods(['GET'])
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


@require_http_methods(['GET'])
@ensure_csrf_cookie
@props_template('app/document.html')
def document(request, document_id):
    doc = get_object_or_404(Document, id=document_id)
    return {
        'document': doc,
        'annotations': doc.annotations.all(),
    }


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


@ensure_csrf_cookie
@json_response
def api_store_crud(request, document_id, annotation_id=None):
    doc = get_object_or_404(Document, id=document_id)

    if request.method == 'GET':
        return to_dict(list(_clean_annotations(
            doc.annotations.all(),
            document_id
        )))

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

@ensure_csrf_cookie
@json_response
def api_store_search(request, document_id):
    raise NotImplementedError('search')


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
