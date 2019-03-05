"""
Decorators
"""
from __future__ import unicode_literals
from django.conf import settings
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.http.response import Http404, HttpResponseRedirectBase, \
    HttpResponseServerError
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.decorators import available_attrs
from django.utils.encoding import force_text
from django.views.debug import ExceptionReporter

import logging
from functools import wraps

logger = logging.getLogger(__name__)

# Available since django 1.6
REASON_PHRASES = {
    100: 'CONTINUE',
    101: 'SWITCHING PROTOCOLS',
    102: 'PROCESSING',
    200: 'OK',
    201: 'CREATED',
    202: 'ACCEPTED',
    203: 'NON-AUTHORITATIVE INFORMATION',
    204: 'NO CONTENT',
    205: 'RESET CONTENT',
    206: 'PARTIAL CONTENT',
    207: 'MULTI-STATUS',
    208: 'ALREADY REPORTED',
    226: 'IM USED',
    300: 'MULTIPLE CHOICES',
    301: 'MOVED PERMANENTLY',
    302: 'FOUND',
    303: 'SEE OTHER',
    304: 'NOT MODIFIED',
    305: 'USE PROXY',
    306: 'RESERVED',
    307: 'TEMPORARY REDIRECT',
    400: 'BAD REQUEST',
    401: 'UNAUTHORIZED',
    402: 'PAYMENT REQUIRED',
    403: 'FORBIDDEN',
    404: 'NOT FOUND',
    405: 'METHOD NOT ALLOWED',
    406: 'NOT ACCEPTABLE',
    407: 'PROXY AUTHENTICATION REQUIRED',
    408: 'REQUEST TIMEOUT',
    409: 'CONFLICT',
    410: 'GONE',
    411: 'LENGTH REQUIRED',
    412: 'PRECONDITION FAILED',
    413: 'REQUEST ENTITY TOO LARGE',
    414: 'REQUEST-URI TOO LONG',
    415: 'UNSUPPORTED MEDIA TYPE',
    416: 'REQUESTED RANGE NOT SATISFIABLE',
    417: 'EXPECTATION FAILED',
    418: "I'M A TEAPOT",
    422: 'UNPROCESSABLE ENTITY',
    423: 'LOCKED',
    424: 'FAILED DEPENDENCY',
    426: 'UPGRADE REQUIRED',
    428: 'PRECONDITION REQUIRED',
    429: 'TOO MANY REQUESTS',
    431: 'REQUEST HEADER FIELDS TOO LARGE',
    500: 'INTERNAL SERVER ERROR',
    501: 'NOT IMPLEMENTED',
    502: 'BAD GATEWAY',
    503: 'SERVICE UNAVAILABLE',
    504: 'GATEWAY TIMEOUT',
    505: 'HTTP VERSION NOT SUPPORTED',
    506: 'VARIANT ALSO NEGOTIATES',
    507: 'INSUFFICIENT STORAGE',
    508: 'LOOP DETECTED',
    510: 'NOT EXTENDED',
    511: 'NETWORK AUTHENTICATION REQUIRED',
}


def render_to_dict(response, *args, **kwargs):
    """
    Creates the main structure and returns the JSON response.
    """
    data = {}
    # determine the status code
    if hasattr(response, 'status_code'):
        status_code = response.status_code
        if issubclass(type(response), HttpResponseRedirectBase):
            data['HttpResponse'] = response.url
        elif issubclass(type(response), TemplateResponse):
            data['HttpResponse'] = response.rendered_content
        elif issubclass(type(response), HttpResponse):
            data['HttpResponse'] = response.content
        elif issubclass(type(response), Exception) \
             or isinstance(response, bytes):
            return force_text(response)

    elif issubclass(type(response), Http404):
        status_code = 404
        data['HttpResponse'] = response
    elif issubclass(type(response), Exception):
        status_code = 500
        logger.exception(
            str(response), extra={'request': kwargs.pop('request', None)}
        )
        
        if settings.DEBUG:
            import sys
            reporter = ExceptionReporter(None, *sys.exc_info())
            data['HttpResponse'] = reporter.get_traceback_text()
        else:
            data['HttpResponse'] = "An error occured while processing an AJAX \
                                    request."
    else:
        status_code = 200
        data.update(response)

    # creating main structure
    data.update({
        'status': status_code,
        'statusText': REASON_PHRASES.get(status_code, 'UNKNOWN STATUS CODE'),
    })
    
    return data

def ajax_response(function=None, mandatory=True, **ajax_kwargs):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            if mandatory and not request.is_ajax():
                return HttpResponseBadRequest()

            if request.is_ajax():
                # return json response
                try:
                    response = func(request, *args, **kwargs)
                    if not isinstance(response, JsonResponse):
                        response = render_to_dict(response, **ajax_kwargs)
                    return response
                except Exception as exception:
                    return render_to_dict(exception, **{'request': request})
            else:
                # return standard response
                return func(request, *args, **kwargs)

        return inner

    if function:
        return decorator(function)

    return decorator

def ajax_messages(function=None, **ajax_kwargs):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            if request.is_ajax():
                # add rendered messages to response
                response = func(request, *args, **kwargs)
                if not isinstance(response, JsonResponse):
                    response['django_messages'] = render_to_string(
                        "main_site/django_messages.html",
                        {"messages": messages.get_messages(request)}
                    )

                return response
                
            else:
                # return standard response
                return func(request, *args, **kwargs)

        return inner

    if function:
        return decorator(function)

    return decorator

def ajax(function=None, mandatory=True, **ajax_kwargs):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            if mandatory and not request.is_ajax():
                return HttpResponseBadRequest()

            if request.is_ajax():
                # return json response
                try:
                    response = func(request, *args, **kwargs)
                    if not response:
                        response = {}
                        
                    if not isinstance(response, JsonResponse):
                        response = render_to_dict(response, **kwargs)
                        response['django_messages'] = render_to_string(
                        "alexecx_django/django_messages.html",
                        {"messages": messages.get_messages(request)}
                    )
                    return JsonResponse(response, **ajax_kwargs)
                except Exception as exception:
                    response = render_to_dict(exception, **{'request': request})
                    return JsonResponse(response, **ajax_kwargs)
            else:
                # return standard response
                return func(request, *args, **kwargs)

        return inner
    return decorator