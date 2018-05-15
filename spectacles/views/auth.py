# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.db.utils import IntegrityError
from django.middleware import csrf
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from spectacles.utils import props_template
from spectacles.models import User


@require_http_methods(['POST', 'GET'])
@ensure_csrf_cookie
@props_template('spectacles/login.html')
def login(request):
    props = {
        'csrftoken': csrf.get_token(request),
    }
    next_ = request.POST.get('next', request.GET.get('next', None))
    if next_ is not None:
        props['next'] = next_

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if next_ is not None:
                return redirect(next_)
            return redirect('spectacles-root')
        props.update({
            'username': username,
            'password': '',
            'error': True,
        })
    return props


@require_http_methods(['POST', 'GET'])
@ensure_csrf_cookie
@props_template('spectacles/register.html')
def register(request):
    props = {
        'csrftoken': csrf.get_token(request),
    }
    next_ = request.POST.get('next', request.GET.get('next', None))
    if next_ is not None:
        props['next'] = next_

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        error = None
        try:
            user = User.objects.create(email=username, password=password)
        except IntegrityError as e:
            user = None
            error = e

        if user is not None:
            auth_login(request, user)
            if next_ is not None:
                return redirect(next_)
            return redirect('spectacles-root')

        props.update({
            'username': username,
            'password': '',
            'error': True,
        })
    return props


@require_http_methods(['POST', 'GET'])
@ensure_csrf_cookie
def logout(request):
    auth_logout(request)
    return redirect('spectacles-root')
