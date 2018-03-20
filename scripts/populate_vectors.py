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
#---------------------------------------------------------------------
from datastore.models import Annotation, Document
from django.core.paginator import Paginator
from tqdm import tqdm


MAX_LEN = 500 * 1000
def vectorize(queryset, page_size=500):
    p = Paginator(queryset, page_size)
    for pn in tqdm(p.page_range, total=p.num_pages, initial=1):
        for obj in tqdm(p.page(pn), total=page_size):
            if len(obj.text) > MAX_LEN:
                obj.delete()
                continue
            obj.recalculate_vector()
            obj.vector_needs_synch = False
            obj.save()

print('vectorizing Documents.')
vectorize(Document.objects.filter(vector__isnull=True).order_by('id'), page_size=200)
print('vectorizing Annotations.')
vectorize(Annotation.objects.filter(vector__isnull=True).order_by('id'), page_size=1000)
print('done.')
