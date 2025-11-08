# -*- coding: utf-8 -*-
from odoo.http import request, Response
from odoo import _, http, service
from odoo.addons.zub_utils.tools.http import make_json_response
import json
import logging

_logger = logging.getLogger(__name__)

def make_http_json_response(data, status=200):
    """Helper para crear respuestas JSON HTTP"""
    return Response(
        json.dumps(data),
        status=status,
        content_type='application/json'
    )

class CommonController(http.Controller):

    @http.route('/api/v1/branch-offices/get-all', type='json', auth='public', csrf=False)
    def pp_get_onboarding(self, **kw):
        model = request.env['res.partner'].sudo()
        try:
            data, status = model.get_office_branches()
        except Exception as e:
            data, status = {"message": str(e)}, 403
        return make_json_response(data, status=status)
    
    @http.route('/api/v1/pharmacy/get-detail', type='http', auth='public', csrf=False, methods=['POST'])
    def get_pharmacy_detail(self, **params):
        """
        Endpoint para obtener el detalle de una farmacia
        
        Request JSON:
        {
            "id": 123,
            "latitude": 4.6097,
            "longitude": -74.0817
        }
        
        Response Codes:
        200 - Success: Detalle de farmacia obtenido
        400 - Bad Request: Datos de entrada incompletos
        404 - Not Found: Farmacia no encontrada
        500 - Server Error: Error interno del servidor
        """
        try:
            # Parsear JSON del request
            data = json.loads(request.httprequest.data.decode('utf-8'))
            
            # Obtener parámetros
            pharmacy_id = data.get('id')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            
            _logger.info(f"Pharmacy detail request - ID: {pharmacy_id}, Lat: {latitude}, Lon: {longitude}")
            
            # Validación 1: ID de farmacia requerido (400 - Bad Request)
            if not pharmacy_id:
                return make_http_json_response({
                    "error": "Datos incompletos",
                    "message": "El ID de la farmacia es requerido"
                }, status=400)
            
            # Validar que el ID sea un número
            try:
                pharmacy_id = int(pharmacy_id)
            except (ValueError, TypeError):
                return make_http_json_response({
                    "error": "ID inválido",
                    "message": "El ID de la farmacia debe ser un número"
                }, status=400)
            
            # Validar coordenadas (opcionales pero deben ser números si se envían)
            if latitude is not None:
                try:
                    latitude = float(latitude)
                except (ValueError, TypeError):
                    return make_http_json_response({
                        "error": "Latitud inválida",
                        "message": "La latitud debe ser un número"
                    }, status=400)
            
            if longitude is not None:
                try:
                    longitude = float(longitude)
                except (ValueError, TypeError):
                    return make_http_json_response({
                        "error": "Longitud inválida",
                        "message": "La longitud debe ser un número"
                    }, status=400)
            
            # Obtener detalle de la farmacia
            model = request.env['res.partner'].sudo()
            result, status = model.get_pharmacy_detail(pharmacy_id, latitude, longitude)
            
            return make_http_json_response(result, status=status)
            
        except json.JSONDecodeError:
            return make_http_json_response({
                "error": "JSON inválido",
                "message": "El cuerpo de la petición debe ser un JSON válido"
            }, status=400)
        except Exception as e:
            _logger.error(f"Error en get_pharmacy_detail: {str(e)}")
            return make_http_json_response({
                "error": "Error interno del servidor",
                "message": str(e)
            }, status=500)
