# -*- coding: utf-8 -*-

import werkzeug.exceptions
from odoo.addons.zublime_utils.tools.zublime_http_response import HttpResponseApi


class HttpResponseExceptionApi:

    @staticmethod
    def response(exception):
        if isinstance(exception, werkzeug.exceptions.BadRequest):
            return HttpResponseApi.badRequest(exception.description)

        if isinstance(exception, werkzeug.exceptions.Unauthorized):
            return HttpResponseApi.unAuthorized(exception.description)

        if isinstance(exception, werkzeug.exceptions.Forbidden):
            return HttpResponseApi.forbidden(exception.description)

        if isinstance(exception, werkzeug.exceptions.NotFound):
            return HttpResponseApi.notFound(exception.description)

        if isinstance(exception, werkzeug.exceptions.ExpectationFailed):
            return HttpResponseApi.failed(exception.description)

        return HttpResponseApi.serverError(exception)
