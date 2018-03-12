# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.middleware import csrf
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from spectacles.utils import props_template


# TODO: clean up this views file?
@require_http_methods(['POST', 'GET'])
@ensure_csrf_cookie
@props_template('app/login.html')
def login(request):
    props = {
        'csrftoken': csrf.get_token(request),
    }
    next_ = request.GET.get('next', None)
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
            'password': password,
            'error': True,
        })
    return props


@require_http_methods(['POST', 'GET'])
@ensure_csrf_cookie
def logout(request):
    auth_logout(request)
    return redirect('spectacles-root')
