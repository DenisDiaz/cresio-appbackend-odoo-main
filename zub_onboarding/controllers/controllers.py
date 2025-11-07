# -*- coding: utf-8 -*-
# from odoo import http


# class ZubOnboarding(http.Controller):
#     @http.route('/zub_onboarding/zub_onboarding', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/zub_onboarding/zub_onboarding/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('zub_onboarding.listing', {
#             'root': '/zub_onboarding/zub_onboarding',
#             'objects': http.request.env['zub_onboarding.zub_onboarding'].search([]),
#         })

#     @http.route('/zub_onboarding/zub_onboarding/objects/<model("zub_onboarding.zub_onboarding"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('zub_onboarding.object', {
#             'object': obj
#         })


from odoo.http import request, Response
from odoo import _, http, service
from odoo.addons.zub_utils.tools.http import make_json_response

class CommonController(http.Controller):

    @http.route('/api/v1/on-boarding/get-by-id', type='json', auth='public', csrf=False)
    def pp_get_onboarding(self, **kw):
        model = request.env['zub.onboarding'].sudo()
        try:
            data, status = model.get_onboarding(kw)
        except Exception as e:
            data, status = {"message": str(e)}, 403
        return make_json_response(data, status=status)
