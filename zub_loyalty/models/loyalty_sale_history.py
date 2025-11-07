# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class LoyaltySaleHistory(models.Model):
    _name = "loyalty.sale.history"
    _description = "Loyalty Sale History"
    _inherit = ['mail.activity.mixin', 'mail.thread']

    def name(self):
        return False