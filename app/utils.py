from django.shortcuts import render
from django.http import JsonResponse
from django.db.models.query import QuerySet
from django.core.serializers.json import DjangoJSONEncoder
from django.http.response import HttpResponseBase
import json
import pdb

PROPS = 'PROPS'


class DictModel():
    def to_dict(self, fields=None, json_fields=None):
        out = {}
        for field in (fields or self._json_fields):
            out[field] = to_dict(getattr(self, field))
        for field, l in (json_fields or getattr(self, '_json_fields_m2m', None) or {}).items():
            out[field] = to_dict(l(self, getattr(self, field)))
        return out

    def to_json(self):
        return to_json(self)


def to_dict(blob, **kwargs):
    try:
        if isinstance(blob, dict):
            return {key: to_dict(value, **kwargs) for key, value in blob.items()}
        if isinstance(blob, list):
            return [to_dict(value, **kwargs) for value in blob]
        if isinstance(blob, DictModel):
            return blob.to_dict(**kwargs)
        if isinstance(blob, QuerySet):
            return [to_dict(v, **kwargs) for v in blob]
    except Exception as e:
        pdb.set_trace()
    return blob


def to_json(blob, **kwargs):
    return json.dumps(to_dict(blob, **kwargs), cls=DjangoJSONEncoder)


# TODO: implement Enum serialization, and add the `state` field to the
# Datastore model serialization fields.
def props_template(path):
    def _1(fn):
        def _2(request, *args, **kwargs):
            kwargs = {}
            context = fn(request, *args, **kwargs)
            if isinstance(context, HttpResponseBase):
                return context
            if isinstance(context, tuple):
                context, kwargs = context

            user = request.user if request.user.is_authenticated else None

            props = context.get(PROPS, None)
            if props:
                props.setdefault('user', user)
                context[PROPS] = to_json(props, **kwargs)
            else:
                props = context
                props.setdefault('user', user)
                context = {
                    PROPS: to_json(props, **kwargs),
                    request: request
                }
            return render(request, path, context)
        return _2
    return _1


def json_response(fn):
    def inner(*args, **kwargs):
        # TODO: custom Exception class for easy error raising
        return JsonResponse(fn(*args, **kwargs), safe=False)
    return inner
