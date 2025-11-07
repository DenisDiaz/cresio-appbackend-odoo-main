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
import re
import logging
import json

_logger = logging.getLogger(__name__)

def make_http_json_response(data, status=200):
    """Helper para crear respuestas JSON HTTP"""
    return Response(
        json.dumps(data),
        status=status,
        content_type='application/json'
    )

class CommonController(http.Controller):

    @http.route('/api/v1/on-boarding/get-by-id', type='json', auth='public', csrf=False)
    def pp_get_onboarding(self, **kw):
        model = request.env['zub.onboarding'].sudo()
        try:
            data, status = model.get_onboarding(kw)
        except Exception as e:
            data, status = {"message": str(e)}, 403
        return make_json_response(data, status=status)

    @http.route('/api/v1/auth/register', type='http', auth='public', csrf=False, methods=['POST'])
    def register_user(self, **params):
        """
        Endpoint para registro de usuarios
        
        Request JSON:
        {
            "name": "Nombre completo",
            "passport_number": "Cédula o pasaporte",
            "password": "contraseña",
            "email": "correo electrónico"
        }
        
        Response Codes:
        200 - Success: Usuario registrado correctamente
        400 - Bad Request: Datos de entrada incompletos
        417 - Expected Failed: Validaciones de negocio fallidas
        500 - Server Error: Error interno del servidor
        """
        try:
            # Parsear JSON del request
            data = json.loads(request.httprequest.data.decode('utf-8'))
            
            # Obtener y limpiar datos
            name = data.get('name', '').strip() if data.get('name') else ''
            passport_number = data.get('passport_number', '').strip() if data.get('passport_number') else ''
            password = data.get('password', '') if data.get('password') else ''
            email = data.get('email', '').strip() if data.get('email') else ''
            
            # Validación 1: Datos completos (400 - Bad Request)
            if not all([name, passport_number, password, email]):
                return make_http_json_response({
                    "error": "Datos incompletos",
                    "message": "Todos los campos son requeridos: name, passport_number, password, email"
                }, status=400)
            
            # Validación 2: Longitud de contraseña (417 - Expected Failed)
            if len(password) < 6 or len(password) > 15:
                return make_http_json_response({
                    "error": "Contraseña inválida",
                    "message": "La contraseña debe tener entre 6 y 15 caracteres"
                }, status=417)
            
            # Validación 3: Formato de email (417 - Expected Failed)
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, email):
                return make_http_json_response({
                    "error": "Email inválido",
                    "message": "El formato del correo electrónico no es válido"
                }, status=417)
            
            # Validación 4: Email ya registrado (417 - Expected Failed)
            existing_user_email = request.env['res.users'].sudo().search([
                ('login', '=', email)
            ], limit=1)
            
            if existing_user_email:
                return make_http_json_response({
                    "error": "Email ya registrado",
                    "message": "El correo electrónico ya está registrado en el sistema"
                }, status=417)
            
            # Validación 5: Formato de cédula/pasaporte (417 - Expected Failed)
            # Acepta: números, letras, guiones y espacios (mínimo 5 caracteres)
            passport_regex = r'^[A-Za-z0-9\-\s]{5,20}$'
            if not re.match(passport_regex, passport_number):
                return make_http_json_response({
                    "error": "Cédula/Pasaporte inválido",
                    "message": "El formato de la cédula o pasaporte no es válido"
                }, status=417)
            
            # Validación 6: Cédula/Pasaporte ya registrado (417 - Expected Failed)
            existing_partner = request.env['res.partner'].sudo().search([
                ('vat', '=', passport_number)
            ], limit=1)
            
            if existing_partner:
                return make_http_json_response({
                    "error": "Cédula/Pasaporte ya registrado",
                    "message": "La cédula o pasaporte ya está registrado en el sistema"
                }, status=417)
            
            # Crear el partner (contacto)
            partner_vals = {
                'name': name,
                'email': email,
                'vat': passport_number,
            }
            
            partner = request.env['res.partner'].sudo().create(partner_vals)
            
            # Crear el usuario
            user_vals = {
                'name': name,
                'login': email,
                'password': password,
                'partner_id': partner.id,
                'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],  # Grupo portal
            }
            
            user = request.env['res.users'].sudo().create(user_vals)
            
            # Enviar email de bienvenida
            try:
                template = request.env.ref('zub_onboarding.email_template_welcome', raise_if_not_found=False)
                if template:
                    template.sudo().send_mail(user.id, force_send=True)
                    _logger.info(f"Email de bienvenida enviado a: {email}")
                else:
                    _logger.warning("Template de bienvenida no encontrado")
            except Exception as e:
                _logger.error(f"Error enviando email de bienvenida: {e}")
            
            # Auto-login: Autenticar al usuario y crear sesión
            try:
                # Forzar el login manualmente estableciendo el uid en la sesión
                request.session.uid = user.id
                request.session.login = request.env.cr.dbname
                request.session.password = password
                
                # Obtener el session_id
                session_id = request.session.sid
                
                _logger.info(f"Usuario registrado y autenticado exitosamente: {email}, session_id: {session_id}")
                
                # Respuesta exitosa (200 - Success) con session_id
                return make_http_json_response({
                    "session_id": session_id
                }, status=200)
                
            except Exception as auth_error:
                _logger.error(f"Error en autenticación después del registro: {str(auth_error)}")
                # Si falla el autologin, aún así el usuario fue creado
                # Devolvemos éxito pero sin session_id
                return make_http_json_response({
                    "success": True,
                    "message": "Usuario registrado exitosamente, pero falló el autologin",
                    "user_id": user.id
                }, status=200)
            
        except Exception as e:
            _logger.error(f"Error en registro de usuario: {str(e)}")
            return make_http_json_response({
                "error": "Error interno del servidor",
                "message": str(e)
            }, status=500)
