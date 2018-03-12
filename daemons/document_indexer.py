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

from datastore.models import Document
from nndb import Indexer


class DocumentIndexer(Indexer):
    def initial_load(self):
        for d in Document.objects.filter(vector__isnull=False):
            if not d.has_vector():
                continue
            self.mapping[d.id] = d.get_vector()

    def update(self):
        for d in Document.objects.filter(vector__isnull=False, vector_needs_synch=True):
            if not d.has_vector():
                continue
            with transaction.atomic():
                self.mapping[d.id] = d.get_vector()
                d.vector_needs_sync = False
                d.save()



indexer = DocumentIndexer(
    index_path=settings.NNDB_SERVICES['documents']['index_path'],
    update_interval=10,
    index_trees=20,
)

if __name__ == '__main__':
    indexer.run()
