# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET

from app.utils import props_template
from app.utils import json_response
from app.utils import to_dict
from app.utils import flatten
from app.utils import PROPS
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
    docs = Document.slim.all()[:100]
    return {
        'documents': to_dict(docs, fields=Document._slim_fields),
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
        'annotations': flatten(to_dict(doc.annotations.all()))
    }


@require_GET
@login_required
@ensure_csrf_cookie
@props_template('app/user.html')
def user(request, user_id=None):
    if user_id is not None:
        user = get_object_or_404(get_user_model(), id=user_id)
    else:
        user = request.user

    documents = user.documents.defer('text').all()
    # Fetch the documents without the 'text' attribute, because for the listing
    # view it's unnecessary.
    annotations = user.annotations.all()
    return {
        'user': user,
        PROPS: {
            'user': to_dict(user),
            'documents': flatten(to_dict(documents, fields=Document._slim_fields)),
            'annotations': flatten(to_dict(annotations)),
        }
    }
