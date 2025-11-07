# -*- coding: utf-8 -*-
import traceback
from odoo.http import SessionExpiredException, request
from odoo.tools import ustr


class HttpResponseApi:
    @staticmethod
    def success(data, package=True):
        response_data = {
            "data": data
        }

        if not package:
            response_data = data

        return request.make_json_response(response_data, status=200)

    @staticmethod
    def created(data):
        return request.make_json_response({
            "data": data
        }, status=201)

    @staticmethod
    def badRequest(data):
        return request.make_json_response({
            "data": data
        }, status=400)

    @staticmethod
    def unAuthorized(data):
        return request.make_json_response({
            "data": data
        }, status=401)

    @staticmethod
    def forbidden(data):
        return request.make_json_response({
            "data": data
        }, status=403)

    @staticmethod
    def notFound(data):
        return request.make_json_response({
            "data": data
        }, status=404)

    @staticmethod
    def failed(data):
        return request.make_json_response({
            "data": data
        }, status=417)

    @staticmethod
    def serverError(exception):
        return request.make_json_response({
            "name": type(exception).__module__ + "." + type(exception).__name__ if type(exception).__module__ else type(exception).__name__,
            "debug": traceback.format_exc(),
            "message": ustr(exception),
            "arguments": exception.args,
            "context": getattr(exception, 'context', {}),
        }, status=500)
