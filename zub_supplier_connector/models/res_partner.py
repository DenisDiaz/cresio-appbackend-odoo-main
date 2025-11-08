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
    
    def get_pharmacy_detail(self, pharmacy_id, user_latitude, user_longitude):
        """
        Obtiene el detalle de una farmacia específica con cálculo de distancia
        
        Args:
            pharmacy_id: ID de la farmacia
            user_latitude: Latitud del usuario
            user_longitude: Longitud del usuario
            
        Returns:
            dict: Detalle de la farmacia con distancia calculada
            int: Status code HTTP
        """
        import math
        
        # Buscar la farmacia por ID
        pharmacy = self.browse(pharmacy_id)
        
        # Validar que existe y tiene conexión externa
        if not pharmacy.exists():
            return {"error": "Farmacia no encontrada", "message": "No existe una farmacia con el ID proporcionado"}, 404
        
        if not pharmacy.is_supplier_with_external_connection:
            return {"error": "Farmacia no disponible", "message": "Esta farmacia no está disponible para consulta"}, 404
        
        # Calcular distancia usando fórmula de Haversine
        distance = 0.0
        if user_latitude and user_longitude and pharmacy.partner_latitude and pharmacy.partner_longitude:
            # Radio de la Tierra en kilómetros
            R = 6371.0
            
            # Convertir grados a radianes
            lat1 = math.radians(user_latitude)
            lon1 = math.radians(user_longitude)
            lat2 = math.radians(pharmacy.partner_latitude)
            lon2 = math.radians(pharmacy.partner_longitude)
            
            # Diferencias
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            # Fórmula de Haversine
            a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = R * c
        
        # Construir dirección completa
        address_parts = []
        if pharmacy.street:
            address_parts.append(pharmacy.street)
        if pharmacy.street2:
            address_parts.append(pharmacy.street2)
        if pharmacy.city:
            address_parts.append(pharmacy.city)
        if pharmacy.state_id:
            address_parts.append(pharmacy.state_id.name)
        if pharmacy.zip:
            address_parts.append(pharmacy.zip)
        if pharmacy.country_id:
            address_parts.append(pharmacy.country_id.name)
        
        direccion = ", ".join(address_parts) if address_parts else ""
        
        # Preparar lista de imágenes (por ahora solo la principal)
        imagenes = []
        if pharmacy.image_1920:
            imagenes.append({
                "url": f"/web/image/res.partner/{pharmacy.id}/image_1920",
                "type": "principal"
            })
        
        # Construir respuesta
        result = {
            "id": pharmacy.id,
            "nombre": pharmacy.name or "",
            "latitude": pharmacy.partner_latitude or 0.0,
            "longitude": pharmacy.partner_longitude or 0.0,
            "telefono": pharmacy.phone or pharmacy.mobile or "",
            "web": pharmacy.website or "",
            "direccion": direccion,
            "distancia": round(distance, 2),  # Distancia en km con 2 decimales
            "imagenes": imagenes,
            "email": pharmacy.email or "",
            "horario": "",  # Campo para futuro uso
        }
        
        return result, 200