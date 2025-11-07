#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear contactos de prueba en Odoo
Ejecutar desde el shell de Odoo:
docker exec -it odoo_zublime odoo shell -d zublime < create_test_contacts.py
"""

# Crear contactos de prueba
Partner = env['res.partner']

# Contacto 1
partner1 = Partner.create({
    'name': 'Sucursal Centro',
    'street': 'Calle 10 #20-30',
    'street2': 'Edificio Central',
    'city': 'Bogotá',
    'zip': '110111',
    'phone': '+57 1 234 5678',
    'mobile': '+57 300 123 4567',
    'email': 'centro@example.com',
    'website': 'https://www.example.com',
    'partner_latitude': 4.6097,
    'partner_longitude': -74.0817,
    'is_supplier_with_external_connection': True,
})

# Contacto 2
partner2 = Partner.create({
    'name': 'Sucursal Norte',
    'street': 'Carrera 15 #100-50',
    'street2': 'Centro Comercial Norte',
    'city': 'Bogotá',
    'zip': '110221',
    'phone': '+57 1 345 6789',
    'mobile': '+57 310 234 5678',
    'email': 'norte@example.com',
    'website': 'https://www.example.com',
    'partner_latitude': 4.7110,
    'partner_longitude': -74.0721,
    'is_supplier_with_external_connection': True,
})

# Contacto 3
partner3 = Partner.create({
    'name': 'Sucursal Sur',
    'street': 'Avenida 68 #40-20',
    'street2': 'Local 101',
    'city': 'Bogotá',
    'zip': '110931',
    'phone': '+57 1 456 7890',
    'mobile': '+57 320 345 6789',
    'email': 'sur@example.com',
    'website': 'https://www.example.com',
    'partner_latitude': 4.5709,
    'partner_longitude': -74.1273,
    'is_supplier_with_external_connection': True,
})

env.cr.commit()

print(f"✓ Contacto creado: {partner1.name} (ID: {partner1.id})")
print(f"✓ Contacto creado: {partner2.name} (ID: {partner2.id})")
print(f"✓ Contacto creado: {partner3.name} (ID: {partner3.id})")
print("\n¡Contactos de prueba creados exitosamente!")
