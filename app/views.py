# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from app.utils import json_response
from app.utils import props_template
from app.utils import to_dict
from app.utils import to_json
from datastore.models import Document
from datastore.models import Annotation


@require_http_methods(['GET'])
@ensure_csrf_cookie
@props_template('app/documents.html')
def documents(request):
    docs = Document.objects.all().only(*Document._json_fields)[:100]
    return {
        'documents': docs,
    }


@require_http_methods(['GET'])
@ensure_csrf_cookie
@props_template('app/documents.html')
def document(request, document_id):
    doc = get_object_or_404(Document, id=document_id)
    return {
        'document': doc,
    }
