# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET

from spectacles.utils import props_template
from spectacles.utils import json_response
from spectacles.utils import to_dict
from spectacles.utils import flatten
from spectacles.recommend import recommend_annotations, recommend_documents
from spectacles.utils import PROPS
from datastore.models import Document, Annotation



@require_GET
@ensure_csrf_cookie
@props_template('spectacles/index.html')
def index(request):
    user = request.user if request.user.is_authenticated else None
    return {
        'user': user,
    }



@require_GET
@login_required
@ensure_csrf_cookie
@props_template('spectacles/archive.html')
def archive(request):
    user = request.user
    if not user.is_authenticated:
        user = None
    # Fetch the documents without the 'text' attribute, because for the listing
    # view it's unnecessary.
    docs = Document.slim.all()[:100]
    recs = {
        'docs': to_dict(Document.slim.all()[200:210], fields=Document._slim_fields),
        'anns': to_dict(Annotation.objects.all()[200:210]),
    }

    print('# docs:', len(recs['docs']))
    print('# anns:', len(recs['anns']))
    return to_dict({
        'archive': None,
        'documents': to_dict(docs, fields=Document._slim_fields),
        'recs': recs,
        'user': user,
    })


@require_GET
@login_required
@ensure_csrf_cookie
@props_template('spectacles/document.html')
def document(request, document_id):
    doc = get_object_or_404(Document, id=document_id)

    similar  = recommend_documents(doc, search_k=10000)
    recs = {
        'docs': [
            to_dict(Document.slim.get(id=id_),
                    fields=Document._slim_fields)
            for id_ in similar
        ]
    }
    print(recs['docs'][0])


    return {
        'recs': recs,
        'document': doc,
        'annotations': flatten(to_dict(doc.annotations.all()))
    }


@require_GET
@login_required
@ensure_csrf_cookie
@props_template('spectacles/user.html')
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
        'user': to_dict(user),
        'logged_in': to_dict(request.user),
        'documents': flatten(to_dict(documents, fields=Document._slim_fields)),
        'annotations': flatten(to_dict(annotations)),
    }
