# -*- coding: utf-8 -*-
from odoo.http import request, Response
from odoo import _, http, service
from odoo.addons.zub_utils.tools.http import make_json_response

class CommonController(http.Controller):

    @http.route('/api/v1/branch-offices/get-all', type='json', auth='public', csrf=False)
    def pp_get_onboarding(self, **kw):
        model = request.env['res.partner'].sudo()
        try:
            data, status = model.get_office_branches()
        except Exception as e:
            data, status = {"message": str(e)}, 403
        return make_json_response(data, status=status)
