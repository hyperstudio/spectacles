#!/usr/bin/env python
import os
import django
import sys
import maya

sys.path.append('..')  # Root of django app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()
