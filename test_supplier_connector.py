#!/usr/bin/env python3
import xmlrpc.client
import requests
import json

# Configuración
url = "http://localhost:8069"
db = "odoo"
username = "admin"
password = "admin"

print("=" * 60)
print("TEST: Módulo zub_supplier_connector")
print("=" * 60)

# 1. Autenticación
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if not uid:
    print("✗ Error de autenticación")
    exit(1)

print(f"\n✓ Autenticado como usuario ID: {uid}")

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# 2. Crear contactos de prueba con conexión externa
print("\n" + "=" * 60)
print("Creando contactos de prueba...")
print("=" * 60)

test_partners = [
    {
        "name": "Proveedor Mayorista 1",
        "street": "Calle 123",
        "city": "Bogotá",
        "phone": "+57 1 234 5678",
        "email": "proveedor1@example.com",
        "is_supplier_with_external_connection": True,
        "partner_latitude": 4.7110,
        "partner_longitude": -74.0721,
    },
    {
        "name": "Proveedor Mayorista 2",
        "street": "Carrera 45",
        "city": "Medellín",
        "phone": "+57 4 567 8901",
        "email": "proveedor2@example.com",
        "is_supplier_with_external_connection": True,
        "partner_latitude": 6.2442,
        "partner_longitude": -75.5812,
    },
    {
        "name": "Cliente Normal",
        "street": "Avenida 789",
        "city": "Cali",
        "phone": "+57 2 345 6789",
        "email": "cliente@example.com",
        "is_supplier_with_external_connection": False,
    }
]

created_ids = []
for partner_data in test_partners:
    try:
        partner_id = models.execute_kw(db, uid, password,
            'res.partner', 'create', [partner_data])
        created_ids.append(partner_id)
        status = "✓" if partner_data['is_supplier_with_external_connection'] else "○"
        print(f"{status} Creado: {partner_data['name']} (ID: {partner_id})")
    except Exception as e:
        print(f"✗ Error creando {partner_data['name']}: {e}")

# 3. Verificar contactos creados
print("\n" + "=" * 60)
print("Verificando contactos con conexión externa...")
print("=" * 60)

partners = models.execute_kw(db, uid, password,
    'res.partner', 'search_read',
    [[['is_supplier_with_external_connection', '=', True]]],
    {'fields': ['name', 'city', 'is_supplier_with_external_connection']})

print(f"\nTotal de proveedores con conexión externa: {len(partners)}")
for partner in partners:
    print(f"  ✓ {partner['name']} - {partner['city']}")

# 4. Probar el endpoint API
print("\n" + "=" * 60)
print("Probando endpoint API: /api/office_branches")
print("=" * 60)

try:
    response = requests.get(f"{url}/api/office_branches")
    print(f"\nEstado HTTP: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Respuesta exitosa")
        print(f"\nNúmero de sucursales: {len(data.get('data', []))}")
        
        print("\nDatos de sucursales:")
        for idx, branch in enumerate(data.get('data', []), 1):
            print(f"\n  Sucursal {idx}:")
            print(f"    - Nombre: {branch.get('name')}")
            print(f"    - Ciudad: {branch.get('city')}")
            print(f"    - Dirección: {branch.get('street')}")
            print(f"    - Teléfono: {branch.get('phone')}")
            print(f"    - Email: {branch.get('email')}")
            if branch.get('partner_latitude') and branch.get('partner_longitude'):
                print(f"    - Coordenadas: {branch.get('partner_latitude')}, {branch.get('partner_longitude')}")
    else:
        print(f"✗ Error en la respuesta: {response.text}")
        
except Exception as e:
    print(f"✗ Error al llamar al endpoint: {e}")

# 5. Limpiar datos de prueba
print("\n" + "=" * 60)
print("Limpieza de datos de prueba")
print("=" * 60)

cleanup = input("\n¿Deseas eliminar los contactos de prueba? (s/n): ")
if cleanup.lower() == 's':
    for partner_id in created_ids:
        try:
            models.execute_kw(db, uid, password,
                'res.partner', 'unlink', [[partner_id]])
            print(f"✓ Eliminado contacto ID: {partner_id}")
        except Exception as e:
            print(f"✗ Error eliminando contacto {partner_id}: {e}")
else:
    print("Los contactos de prueba se mantienen en la base de datos")

print("\n" + "=" * 60)
print("Test completado")
print("=" * 60)
