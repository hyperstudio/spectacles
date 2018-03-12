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
        for a in Annotation.objects.filter(vector__isnull=False):
            if not d.has_vector():
                continue
            self.mapping[a.id] = a.get_vector()

    def update(self):
        for a in Annotation.objects.filter(vector__isnull=False, vector_needs_synch=True):
            if not a.has_vector():
                continue
            with transaction.atomic():
                self.mapping[a.id] = a.get_vector()
                a.vector_needs_sync = False
                a.save()


indexer = AnnotationIndexer(
    index_path=settings.NNDB_SERVICES['annotations']['index_path'],
    update_interval=10,
    index_trees=20,
)

if __name__ == '__main__':
    indexer.run()
