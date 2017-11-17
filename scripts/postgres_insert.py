#!/usr/bin/env python
import os
import django
import codecs
import uuid
import json
import sys
import datetime
from bson.json_util import loads, dumps
from dateutil import parser

from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction

sys.path.append('..')  # Root of django app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from app.models import User
from datastore.models import Annotation
from datastore.models import Archive
from datastore.models import Document
from datastore.models import DocumentState
from datastore.models import Upload
from datastore.models import UploadState


docfile = './documents.jsonlines'
userfile = './users.jsonlines'
annotationfile = './annotations.jsonlines'

def jsonlines(fpath):
    for line in codecs.open(fpath, 'r', encoding='utf-8'):
        yield loads(line)

def dt(ts):
    if isinstance(ts, datetime.datetime):
        return ts
    return datetime.datetime.utcfromtimestamp(float(ts) / 1000)


@transaction.atomic
def insert_users():
    print('inserting users...')
    mapping = {}
    for d in jsonlines(userfile):
        if d['email'] == 'downs@mit.edu':
            continue
        u = User.objects.create(
            email=d['email'],
            password='fakepassword',
            name=d.get('firstname', '') + ' ' + d.get('lastname', ''),
            last_login=parser.parse(d['last_sign_in_at']),
            date_joined=parser.parse(d['created_at'])
        )
        u.save()
        mapping[d['id']] = u.id
        print(u.id)

    print('writing mapping...')
    with open('./user_mapping.json', 'w') as fout:
        fout.write(dumps(mapping))


@transaction.atomic
def insert_documents():
    print('reading mapping...')
    user_mapping = {}
    with open('./user_mapping.json', 'r') as fin:
        user_mapping = loads(fin.read())
    assert user_mapping

    document_mapping = {}
    print('inserting documents...')
    for d in jsonlines(docfile):
        if not d['text']:
            d['text'] = ''
        if not d['author']:
            d['author'] = ''
        doc_state = {
            'deleted': DocumentState.DELETED,
            'draft': DocumentState.DRAFT,
            'published': DocumentState.PUBLISHED,
        }.get(d['state'], DocumentState.PUBLISHED)
        creator_id = user_mapping.get(str(d['user_id']), None)
        if creator_id:
            creator = User.objects.get(id=creator_id)
        else:
            creator = User.objects.get(email='downs@mit.edu')
        doc = Document.objects.create(
            state=doc_state,
            title=d['title'],
            text=d['text'],
            created_at=parser.parse(d['created_at']),
            updated_at=parser.parse(d['updated_at']),
            author=d['author'],

            creator=creator,
            upload=None
        )
        doc.save()
        if d['slug']:
            document_mapping[d['slug']] = doc.id
        else:
            sys.stdout.write('.')
            sys.stdout.flush()

    print('writing mapping...')
    with open('./document_mapping.json', 'w') as fout:
        fout.write(dumps(document_mapping))


@transaction.atomic
def insert_annotations():
    print('reading mapping...')
    document_mapping = {}
    with open('./document_mapping.json', 'r') as fin:
        document_mapping = loads(fin.read())
    assert document_mapping
    print('reading mapping...')
    user_mapping = {}
    with open('./user_mapping.json', 'r') as fin:
        user_mapping = loads(fin.read())
    assert user_mapping

    annotation_mapping = {}

    print('inserting annotations...')
    for i, a in enumerate(jsonlines(annotationfile)):

        # Has to relate to a known document
        uri = a.get('uri', None)
        if not uri:
            continue
        document_slug = a['uri'].rsplit('/', 1)[1]
        if i % 100 == 0:
            print('%d -> %s' % (i, document_slug))
        document_id = document_mapping.get(document_slug, None)
        if not document_id:
            continue
        document = Document.objects.get(id=document_id)
        # Has to relate to a known user
        creator_email = a['user'] or None
        creator = None
        if creator_email:
            try:
                creator = User.objects.get(email=creator_email)
            except User.DoesNotExist:
                continue
        # The UUIDs used in Mongo are not compatible with our new data model,
        # and need to be replaced.
        old_uuid = a['uuid']
        a['uuid'] = uuid.uuid4().hex
        ann = Annotation.objects.create(
            uuid=a['uuid'],
            created_at=dt(a['created']) if a['created'] else datetime.datetime.utcnow(),
            updated_at=dt(a['updated']) if a['updated'] else datetime.datetime.utcnow(),
            creator=creator,
            document=document,
            data=json.loads(dumps(a))
        )
        ann.save()
        annotation_mapping[old_uuid] = ann.uuid

    with open('./annotation_mapping.json', 'w') as fout:
        fout.write(dumps(annotation_mapping))


if __name__ == '__main__':
    print('> executing...')
    #insert_users()
    #insert_documents()
    insert_annotations()
    print('> done.')