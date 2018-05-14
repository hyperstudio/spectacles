# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
import json
import uuid
from datetime import datetime

from django.views.decorators.http import require_GET
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest as R400, HttpResponseNotFound as R404

from spectacles.utils import json_response
from spectacles.utils import to_dict
from datastore.auth import generate_consumer_token
from datastore.models import Document
from datastore.models import Annotation


# TODO: weird URI and permissions updating shouldn't have to happen Remove
# these functions / fix the data model internally.
def _clean_ann(a, document_id):
    a['uri'] = document_id
    return a

def _clean_annotations(annotations, document_id):
    for a in annotations:
        yield _clean_ann(a.data, document_id)


@require_GET
@login_required
@json_response
def token(request):
    return generate_consumer_token(request.user.id)


@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@ensure_csrf_cookie
@json_response
def crud(request, document_id, annotation_id=None):
    doc = get_object_or_404(Document, id=document_id)

    # TODO: separate data parsing from utility methods, which shouldn't need to
    # take a "request" and should instead operate on internal data only.
    if request.method == 'GET':
        return get(request, doc)
    if request.method == 'DELETE':
        return delete(request, doc, annotation_id)
    if request.method == 'POST':
        return create(request, doc)
    if request.method == 'PUT':
        return update(request, doc, annotation_id)

    # TODO: correct error raising here
    return R400(request.method)


def get(request, doc):
    return to_dict(list(_clean_annotations(
        doc.annotations.all(),
        doc.id
    )))


def delete(request, doc, annotation_uuid):
    print('annotation__uuid:', annotation_uuid)
    ann = doc.annotations.filter(uuid=annotation_uuid)
    if ann.exists():
        ann = ann[0]
    else:
        return R404()
    ann.delete()
    return None


def create(request, doc):
    try:
        req_data = json.loads(request.body)
    except (TypeError, ValueError):
        return R400()
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
    return _clean_ann(to_dict(ann), doc.id)
    return to_dict(_clean_ann(ann.data, doc.id))


def update(request, doc, annotation_uuid):
    ann = doc.annotations.filter(uuid=annotation_uuid)
    if ann.exists():
        ann = ann[0]
    else:
        return R404()
    try:
        updated = json.loads(request.body)
    except (TypeError, ValueError):
        return R400()

    ann.data.update(updated)
    ann.save()
    return _clean_ann(to_dict(ann), doc.id)
    #return to_dict(_clean_ann(ann.data, doc.id))
