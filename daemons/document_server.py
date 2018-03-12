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
from nndb import Server


server = Server(
    index_path=settings.NNDB_SERVICES['documents']['index_path'],
    service_name=settings.NNDB_SERVICES['documents']['service_name'],
    update_interval=5,
)

if __name__ == '__main__':
    server.run()

