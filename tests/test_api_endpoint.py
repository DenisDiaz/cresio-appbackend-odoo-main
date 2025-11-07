#!/usr/bin/env python3
import requests
import json
import xmlrpc.client

# Configuración
url = "http://localhost:8069"
db = "odoo"
username = "admin"
password = "admin"

print("=" * 70)
print("TEST: API Endpoint /api/v1/branch-offices/get-all")
print("=" * 70)

# 1. Crear contactos de prueba
print("\n1. Creando contactos de prueba...")
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if not uid:
    print("✗ Error de autenticación")
    exit(1)

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

test_partners = [
    {
        "name": "Sucursal Centro - Bogotá",
        "street": "Carrera 7 # 32-16",
        "city": "Bogotá",
        "phone": "+57 1 234 5678",
        "email": "centro@zublime.com",
        "is_supplier_with_external_connection": True,
        "partner_latitude": 4.6097,
        "partner_longitude": -74.0817,
    },
    {
        "name": "Sucursal Norte - Medellín",
        "street": "Calle 10 # 43-50",
        "city": "Medellín",
        "phone": "+57 4 567 8901",
        "email": "norte@zublime.com",
        "is_supplier_with_external_connection": True,
        "partner_latitude": 6.2442,
        "partner_longitude": -75.5812,
    },
    {
        "name": "Sucursal Sur - Cali",
        "street": "Avenida 6N # 28-10",
        "city": "Cali",
        "phone": "+57 2 345 6789",
        "email": "sur@zublime.com",
        "is_supplier_with_external_connection": True,
        "partner_latitude": 3.4516,
        "partner_longitude": -76.5320,
    }
]

created_ids = []
for partner_data in test_partners:
    try:
        partner_id = models.execute_kw(db, uid, password,
            'res.partner', 'create', [partner_data])
        created_ids.append(partner_id)
        print(f"  ✓ Creado: {partner_data['name']} (ID: {partner_id})")
    except Exception as e:
        print(f"  ✗ Error: {e}")

# 2. Probar el endpoint API con POST
print("\n2. Probando endpoint API (POST)...")
print(f"   URL: {url}/api/v1/branch-offices/get-all")

try:
    headers = {
        'Content-Type': 'application/json',
    }
    
    response = requests.post(
        f"{url}/api/v1/branch-offices/get-all",
        headers=headers,
        json={}
    )
    
    print(f"\n   Estado HTTP: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Respuesta exitosa\n")
        
        if 'data' in data:
            branches = data['data']
            print(f"   Total de sucursales: {len(branches)}\n")
            
            for idx, branch in enumerate(branches, 1):
                print(f"   Sucursal {idx}:")
                print(f"     • Nombre: {branch.get('name')}")
                print(f"     • Ciudad: {branch.get('city')}")
                print(f"     • Dirección: {branch.get('street')}")
                print(f"     • Teléfono: {branch.get('phone')}")
                print(f"     • Email: {branch.get('email')}")
                if branch.get('partner_latitude') and branch.get('partner_longitude'):
                    print(f"     • Coordenadas: ({branch.get('partner_latitude')}, {branch.get('partner_longitude')})")
                print()
        else:
            print(f"   Respuesta completa: {json.dumps(data, indent=2)}")
    else:
        print(f"   ✗ Error: {response.status_code}")
        print(f"   Respuesta: {response.text[:500]}")
        
except Exception as e:
    print(f"   ✗ Excepción: {e}")

# 3. Limpiar datos
print("\n" + "=" * 70)
cleanup = input("¿Eliminar contactos de prueba? (s/n): ")
if cleanup.lower() == 's':
    for partner_id in created_ids:
        try:
            models.execute_kw(db, uid, password,
                'res.partner', 'unlink', [[partner_id]])
            print(f"  ✓ Eliminado ID: {partner_id}")
        except Exception as e:
            print(f"  ✗ Error eliminando {partner_id}: {e}")
else:
    print("  Los contactos permanecen en la base de datos")

print("\n" + "=" * 70)
print("Test completado")
print("=" * 70)
