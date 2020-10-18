from django.http import Http404
from rest_framework import exceptions, serializers, status
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from rest_framework.views import set_rollback


def drf_custom_exception_handler(exc, context):
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        data = {
            "data": {},
            "errors": []
        }

        if isinstance(exc.detail, (dict,)):
            data['errors'] = exc.detail
        else:
            data['errors'] = {'msg': exc.detail}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None
