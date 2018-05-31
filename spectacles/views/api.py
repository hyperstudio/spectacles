# coding: utf-8
from __future__ import print_function, unicode_literals
import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods

from spectacles import search
from spectacles.utils import json_response
from spectacles.utils import to_dict
from spectacles.models import Document, Annotation
from spectacles.recommend import recommend_annotations, recommend_documents


@require_POST
@login_required
@ensure_csrf_cookie
@json_response
def search_annotations(request):
    try:
        req = json.loads(request.body)
    except (TypeError, ValueError):
        raise NotImplementedError('400!')

    anns_r = list(search.find_annotations(
        query=req['query'],
        document_id=req.get('document_id', None),
        creator_id=req.get('creator_id', None)
    ).hits)
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

    fields = set(Document._json_fields)
    fields.remove('text')
    docs_r = list(search.find_documents(
        query=req['query'],
        creator_id=req.get('creator_id', None),
        titles_only=req.get('titles_only', False),
    ).hits)

    return to_dict({
        'documents': to_dict(docs_r, fields=fields)
    })

@require_POST
@login_required
@ensure_csrf_cookie
@json_response
def similar_annotations(request, annotation_id):
    ann = get_object_or_404(Annotation.objects.with_doc_info(), uuid=annotation_id)
    similar  = recommend_annotations(ann, search_k=10000)
    objs = [to_dict(Annotation.objects.with_doc_info().get(id=id_)) for id_ in similar]
    return objs

@require_POST
@login_required
@ensure_csrf_cookie
@json_response
def similar_documents(request, document_id):
    raise NotImplementedError

@require_http_methods(['GET', 'POST', 'DELETE'])
@login_required
@ensure_csrf_cookie
@json_response
def bookmark_crud(request, bookmark_id=None):
    if request.method == 'POST':
        return bookmark_create(request)

    if request.method == 'GET':
        return bookmark_get(bookmark_id)

    if request.method == 'DELETE':
        return bookmark_delete(bookmark_id)

    # TODO: correct error raising here
    raise NotImplementedError(request.method)

def create_bookmark(request):
    try:
        req_data = json.loads(request.body)
    except (TypeError, ValueError):
        # TODO: Raise the correct type of error, return to JS
        raise NotImplementedError('400!')
    # document_id, annotation_uuid
    annotation_uuid = req_data.get('annotation_uuid', None)
    if annotation_uuid is not None:
        annotation = get_object_or_404(Annotation.objects.with_doc_info(), uuid=annotation_uuid)
        document = annotation.document
    else:
        annotation = None
        document = get_object_or_404(Document, id=req_data['document_id'])

    bookmark = Bookmark(
        creator=request.user,
        document=document,
        annotation=annotation,
    )
    bookmark.save()
    return to_dict(bookmark)


def bookmark_get(bookmark_id):
    return to_dict(get_object_or_404(Bookmark, id=bookmark_id))

def bookmark_delete(bookmark_id):
    bookmark = get_object_or_404(Bookmark, id=bookmark_id)
    bookmark.delete()
    return {'success': True}
