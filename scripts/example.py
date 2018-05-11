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

print('Done setting up!')
import spectacles
print('Successfully imported the spectacles django application.')
