# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class OnBoarding(models.Model):
    _name = 'zub.onboarding'
    _description = 'Onboarding'

    name = fields.Char("Nombre")
    active = fields.Boolean(string='Activo', default=True)
    lines = fields.One2many('zub.onboarding.line','onboarding_id', string='Lineas de onboarding')

    def get_onboarding(self, data):
        id = data['id']
        response = {}
        lines = []
        onboarding = self.browse(id)
        if onboarding:
            for line in onboarding.lines:
                lines.append({
                    'name': line.name, # descripción
                    'image': line.image,
                    'sequence': line.sequence,
                })
            response = {
                "name": onboarding.name,
                "id": onboarding.id,
                "lines": lines,
            }
        if not response:
            return {}, 404
        return response, 200

class OnBoardingLine(models.Model):
    _name = 'zub.onboarding.line'
    _description = 'Onboarding Line'

    name = fields.Char("Descripción")
    image = fields.Image("Image", max_width=1920, max_height=1920)
    sequence = fields.Integer('Sequence', default=1, help="Determine the display order")
    active = fields.Boolean(string='Activo', default=True)
    onboarding_id = fields.Many2one('zub.onboarding', 'Onboarding')