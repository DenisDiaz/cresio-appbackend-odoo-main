# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class TestController(http.Controller):
    
    @http.route('/api/test/hello', type='json', auth='public', csrf=False)
    def test_hello(self, **kw):
        return {"message": "Hello from test controller", "status": 200}
