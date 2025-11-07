#!/usr/bin/env python3
"""
Demostración rápida de la funcionalidad del módulo zub_supplier_connector
"""
import xmlrpc.client

print("\n🚀 DEMO RÁPIDA - Módulo zub_supplier_connector\n")

# Configuración
url = "http://localhost:8069"
db, username, password = "odoo", "admin", "admin"

# Conectar
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

print(f"✅ Conectado a Odoo (UID: {uid})\n")

# Buscar sucursales con conexión externa
sucursales = models.execute_kw(db, uid, password,
    'res.partner', 'search_read',
    [[['is_supplier_with_external_connection', '=', True]]],
    {'fields': ['name', 'city', 'phone'], 'limit': 5})

print(f"📍 Sucursales con Conexión Externa: {len(sucursales)}\n")

if sucursales:
    for i, s in enumerate(sucursales, 1):
        print(f"{i}. {s['name']}")
        print(f"   Ciudad: {s.get('city', 'N/A')}")
        print(f"   Teléfono: {s.get('phone', 'N/A')}\n")
else:
    print("   (No hay sucursales registradas)\n")

print("✅ Demo completada\n")
print("💡 Tip: Usa test_xmlrpc_api.py para ver la funcionalidad completa\n")
