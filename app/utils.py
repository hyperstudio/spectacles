from django.shortcuts import render
from django.http import JsonResponse
from django.db.models.query import QuerySet
from django.core.serializers.json import DjangoJSONEncoder
import json

PROPS = 'PROPS'


class DictModel():
    def to_dict(self):
        out = {}
        for field in self._json_fields:
            out[field] = to_dict(getattr(self, field))
        for field, l in getattr(self, '_json_fields_m2m', {}).items():
            out[field] = to_dict(l(self, getattr(self, field)))
        return out

    def to_json(self):
        return to_json(self)


def to_dict(blob, followed_relation=False):
    if isinstance(blob, dict):
        return {key: to_dict(value) for key, value in blob.items()}
    if isinstance(blob, list):
        return [to_dict(value) for value in blob]
    if isinstance(blob, DictModel):
        return blob.to_dict()
    if isinstance(blob, QuerySet):
        return [to_dict(v) for v in blob]
    return blob


def to_json(blob):
    return json.dumps(to_dict(blob), cls=DjangoJSONEncoder)

# TODO: implement Enum serialization
def props_template(path):
    def _1(fn):
        def _2(request, *args, **kwargs):
            context = fn(request, *args, **kwargs)
            props = context.get(PROPS, None)
            if props is not None:
                context[PROPS] = to_json(props)
            else:
                context = {PROPS: to_json(context), request: request}
            print("Looking for template %s" % path)
            return render(request, path, context)
        return _2
    return _1


def json_response(fn):
    def inner(*args, **kwargs):
        return JsonResponse(fn(*args, **kwargs))
    return inner
