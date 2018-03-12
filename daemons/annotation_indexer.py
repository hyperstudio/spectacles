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

from datastore.models import Annotation
from nndb import Indexer


class AnnotationIndexer(Indexer):
    def initial_load(self):
        qs = (Annotation
                .objects
                .only('id', 'vector')
                .filter(vector__isnull=False)
                .iterator())
        for a in qs:
            if not a.has_vector():
                continue
            self.mapping[a.id] = a.get_vector()

    def update(self):
        changed = 0
        qs = (Annotation
                .objects
                .only('id', 'vector')
                .filter(vector__isnull=False, vector_needs_synch=True)
                .iterator())
        for a in qs:
            if not a.has_vector():
                continue
            with transaction.atomic():
                changed += 1
                self.mapping[a.id] = a.get_vector()
                a.vector_needs_sync = False
                a.save()
        return changed


indexer = AnnotationIndexer(
    index_path=settings.NNDB_SERVICES['annotations']['index_path'],
    update_interval=10,
    index_trees=20,
)

if __name__ == '__main__':
    indexer.run()
