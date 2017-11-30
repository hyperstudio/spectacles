# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def documents(request):
    docs = Document.objects.all()[:100]
    return render(request, 'polls/detail.html', {'poll': p})
