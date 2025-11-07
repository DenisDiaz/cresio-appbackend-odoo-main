# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_supplier_with_external_connection = fields.Boolean("Conexión Externa", default=False)

    def get_office_branches(self):
        # proveedores que estén marcados como "Proveedor mayorista" = True
        office_branches = []
        #ejecutar la búsqueda con query, usando la función sen,cos de heversine.
        records = self.search([("is_supplier_with_external_connection","=",True)])
        result = []
        for rec in records:
            result.append({
                "name": rec.name,
                "street": rec.street,
                "street2": rec.street2,
                "city": rec.city,
                "state": rec.state_id.name,
                "zip": rec.zip,
                "country_id": rec.country_id.name,
                "phone": rec.phone,
                "mobile": rec.mobile,
                "email": rec.email,
                "website": rec.website,
                "partner_longitude": rec.partner_longitude,
                "partner_latitude": rec.partner_latitude,
                "image_1920": rec.image_1920,
            })
        if not result:
            return {}, 404
        return {"data": result}, 200