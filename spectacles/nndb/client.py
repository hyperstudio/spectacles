# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals
from functools import wraps
from pyRpc import RpcConnection


class RPCException(Exception): pass


def fname(name):
    def wrapper(fn):
        fn.__name__ = fn.func_name = name
        return fn
    return wrapper


def result_or_error(resp):
    if resp.status != 0:
        raise RPCException(resp.error)
    return resp.result


def proxyfn(remote, name):
    @fname(name)
    def proxy(*args, **kwargs):
        resp = remote.call(name, args=args, kwargs=kwargs)
        return result_or_error(resp)
    return proxy


class Client(object):
    __service_name__ = None

    def __init__(self, service_name=None):
        if not (self.__service_name__ or service_name):
            raise NotImplementedError('No service name configured')
        self.__remote = remote = RpcConnection(self.__service_name__ or service_name)
        result = result_or_error(remote.availableServices())
        for x in result:
            setattr(self, x['service'], proxyfn(remote, x['service']))
