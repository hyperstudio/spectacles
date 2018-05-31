#!/usr/bin/env python
from __future__ import print_function
from __future__ import unicode_literals
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spectacles.settings")
import django
django.setup()
# --------------------------------------------------------------------
from django.conf import settings
from django.db import transaction

from spectacles.models import Document
from spectacles.nndb import Indexer


class DocumentIndexer(Indexer):
    def initial_load(self):
        qs = (Document
                .objects
                .only('id', 'vector')
                .filter(vector__isnull=False)
                .iterator())
        i = 0
        for d in qs:
            if not d.has_vector():
                continue
            i += 1
            self.mapping[d.id] = d.get_vector()
        print('[documents] loaded %d vectors' % i)

    def update(self):
        qs = (Document
                .objects
                .only('id', 'vector')
                .filter(vector__isnull=False, vector_needs_synch=True)
                .iterator())
        i = 0
        for d in qs:
            if not d.has_vector():
                continue
            i += 1
            self.mapping[d.id] = d.get_vector()
            d.vector_needs_synch = False
            d.save()
        if i > 0:
            print('[documents] updated %d vectors' % i)
        return i


indexer = DocumentIndexer(
    index_path=settings.NNDB_SERVICES['documents']['index_path'],
    update_interval=10,
    index_trees=20,
)

if __name__ == '__main__':
    indexer.run()
