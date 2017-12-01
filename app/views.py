# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods

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
    docs = Document.objects.all().only(*fields)[:100]
    return {
        'documents': docs,
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
@login_required
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


