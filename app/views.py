# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pdb

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
    fields = set(Document._json_fields)
    fields.remove('text')
    docs = Document.objects.defer('text')[:100]
    user = request.user
    if not user.is_authenticated:
        user = None
    return {
        'documents': to_dict(docs, fields=fields),
        'user': to_dict(user),
    }


@require_http_methods(['GET'])
@ensure_csrf_cookie
@props_template('app/document.html')
def document(request, document_id):
    doc = get_object_or_404(Document, id=document_id)
    annotations = doc.annotations.all()
    return {
        'document': doc,
        'annotations': annotations,
    }


@require_GET
#@login_required
@json_response
def api_token(request):
    #https://spectacles.cc/api/token
    user = request.user
    if user.is_authenticated:
        user_id = user.id
    else:
        user_id = None
    token = generate_consumer_token(user.id)
    return token


@require_http_methods(['POST', 'GET'])
@ensure_csrf_cookie
@props_template('app/login.html')
def login(request):
    props = {
        'csrftoken': csrf.get_token(request),
    }

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('app-root')
        else:
            props.update({
                'username': username,
                'password': password,
                'error': True,
            })
    next_ = request.GET.get('next')
    if next_ is not None:
        props['next'] = next_
    path = 'art/login.html'
    return props
    #context = {PROPS: to_json(props), request: request}
    #print('context:', context)
    #return render(request, path, context)


@require_http_methods(['POST', 'GET'])
@ensure_csrf_cookie
def logout(request):
    print('in logout()')
    auth_logout(request)
    print('returning a redirect')
    return redirect('app-root')
