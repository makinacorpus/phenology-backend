from django.template import Library
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from backoffice import register
from backoffice.utils import json_serial


def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return simplejson.dumps(object, default=json_serial)

register.filter('jsonify', jsonify)
