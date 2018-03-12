#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spectacles.settings")
import django
django.setup()

import codecs
import uuid
import json
import datetime
from json import loads, dumps
from dateutil import parser
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.conf import settings

print('ES_IGNORE_SIGNALS', settings.ES_IGNORE_SIGNALS)
print('ES_AUTO_REFRESH', settings.ES_AUTO_REFRESH)
print('USE_HEROKU', settings.USE_HEROKU)
print(settings.DATABASES['default'])

from spectacles.models import User
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
        if line:
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
        if d['email'] == 'peterldowns@gmail.com':
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


def insert_documents():
    print('reading mapping...')
    user_mapping = {}
    with open('./user_mapping.json', 'r') as fin:
        user_mapping = loads(fin.read())
    assert user_mapping

    document_mapping = {}
    print('inserting documents...')
    for i, d in enumerate(jsonlines(docfile)):
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
        try:
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
        except:
            continue
        if d['slug']:
            document_mapping[d['slug']] = doc.id
        else:
            sys.stdout.write('.')
            sys.stdout.flush()

    print('writing mapping...')
    with open('./document_mapping.json', 'w') as fout:
        fout.write(dumps(document_mapping))


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
    count = 0
    try:
        with open('./annotation_mapping.jsonlines', 'r') as fin:
            for line in fin.readlines():
                annotation_mapping.update(loads(line))
                count += 1
        print('loaded %d lines' % count)
    except IOError:
        annotation_mapping = {}

    print('inserting annotations...')
    to_create = []
    new_mapping = {}
    user_cache = {}
    document_cache = {}
    for i, a in enumerate(jsonlines(annotationfile)):
        old_uuid = a.get('uuid', None)
        if annotation_mapping.get(old_uuid) or not old_uuid:
            continue

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
        # Has to relate to a known user
        creator_email = a['user'] or None
        creator = None
        if creator_email:
            try:
                creator = user_cache.get(creator_email, None)
                if creator == -1:
                    continue
                if not creator:
                    creator = User.objects.get(email=creator_email)
                    user_cache[creator_email] = creator
            except User.DoesNotExist:
                user_cache[creator_email] = -1
                continue

        document = document_cache.get(document_id, None)
        if not document:
            document = Document.objects.get(id=document_id)
            document_cache[document_id] = document
        # The UUIDs used in Mongo are not compatible with our new data model,
        # and need to be replaced.
        a['uuid'] = uuid.uuid4().hex
        try:
            ann = Annotation(
                uuid=a['uuid'],
                created_at=dt(a['created']['$date']) if a['created'] else datetime.datetime.utcnow(),
                updated_at=dt(a['updated']['$date']) if a['updated'] else datetime.datetime.utcnow(),
                creator=creator,
                document=document,
                data=json.loads(dumps(a))
            )
        except TypeError as e:
            raise e
        to_create.append(ann)
        annotation_mapping[old_uuid] = ann.uuid
        new_mapping[old_uuid] = ann.uuid
        if len(to_create) >= 500:
            print('--> inserting')
            Annotation.objects.bulk_create(to_create)
            with open('./annotation_mapping.jsonlines', 'a') as fout:
                fout.write(dumps(new_mapping))
                fout.write('\n')
            to_create = []
            new_mapping = {}


if __name__ == '__main__':
    print('> executing...')
    #insert_users()
    #insert_documents()
    insert_annotations()
    print('> done.')
