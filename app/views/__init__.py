# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET

from app.utils import props_template
from app.utils import to_dict
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
    # TODO: create a new manager for 'text'-less documents, make the 'slim'
    # document format consistent.
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
