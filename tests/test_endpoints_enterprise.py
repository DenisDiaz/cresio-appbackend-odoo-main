#!/usr/bin/env python3
"""
Prueba completa de endpoints HTTP en Odoo 18 Enterprise
"""
import xmlrpc.client
import requests
import json

print("\n" + "=" * 70)
print("  PRUEBA DE ENDPOINTS - ODOO 18 ENTERPRISE")
print("=" * 70 + "\n")

# Configuración
url = "http://localhost:8070"
db = "odoo_enterprise"
username = "admin"
password = "admin"

# Test 1: Autenticación
print("1. Autenticando en Odoo Enterprise...")
try:
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    
    if uid:
        print(f"   ✓ Autenticado correctamente (UID: {uid})")
    else:
        print("   ✗ Error de autenticación")
        exit(1)
except Exception as e:
    print(f"   ✗ Error: {e}")
    exit(1)

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Test 2: Verificar módulos instalados
print("\n2. Verificando módulos instalados...")
try:
    modules = models.execute_kw(db, uid, password,
        'ir.module.module', 'search_read',
        [[['name', 'in', ['zub_utils', 'zub_supplier_connector', 'zub_onboarding']]]],
        {'fields': ['name', 'state']})
    
    for module in modules:
        status = "✓" if module['state'] == 'installed' else "✗"
        print(f"   {status} {module['name']}: {module['state']}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Crear contactos de prueba
print("\n3. Creando contactos de prueba con conexión externa...")
test_partners = [
    {
        "name": "Sucursal Enterprise Test 1",
        "street": "Carrera 7 # 32-16",
        "city": "Bogotá",
        "phone": "+57 1 234 5678",
        "email": "test1@enterprise.com",
        "is_supplier_with_external_connection": True,
        "partner_latitude": 4.6097,
        "partner_longitude": -74.0817,
    },
    {
        "name": "Sucursal Enterprise Test 2",
        "street": "Calle 10 # 43-50",
        "city": "Medellín",
        "phone": "+57 4 567 8901",
        "email": "test2@enterprise.com",
        "is_supplier_with_external_connection": True,
        "partner_latitude": 6.2442,
        "partner_longitude": -75.5812,
    }
]

created_ids = []
try:
    for partner_data in test_partners:
        partner_id = models.execute_kw(db, uid, password,
            'res.partner', 'create', [partner_data])
        created_ids.append(partner_id)
        print(f"   ✓ Creado: {partner_data['name']} (ID: {partner_id})")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Probar Endpoint HTTP - Branch Offices
print("\n4. Probando endpoint HTTP: /api/v1/branch-offices/get-all")
print("   Método: POST")
print("   Tipo: JSON")

try:
    response = requests.post(
        f"{url}/api/v1/branch-offices/get-all",
        headers={'Content-Type': 'application/json'},
        json={},
        timeout=10
    )
    
    print(f"   Status HTTP: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✓ ¡ENDPOINT FUNCIONANDO!")
        data = response.json()
        
        if 'data' in data:
            branches = data['data']
            print(f"   ✓ Sucursales encontradas: {len(branches)}")
            
            for idx, branch in enumerate(branches[:2], 1):
                print(f"\n   Sucursal {idx}:")
                print(f"     • Nombre: {branch.get('name')}")
                print(f"     • Ciudad: {branch.get('city')}")
                print(f"     • Teléfono: {branch.get('phone')}")
                if branch.get('partner_latitude') and branch.get('partner_longitude'):
                    print(f"     • Coordenadas: ({branch.get('partner_latitude')}, {branch.get('partner_longitude')})")
        else:
            print(f"   Respuesta: {json.dumps(data, indent=2)}")
    elif response.status_code == 404:
        print("   ✗ Endpoint no encontrado (404)")
        print("   El controlador no se registró correctamente")
    else:
        print(f"   ✗ Error: {response.status_code}")
        print(f"   Respuesta: {response.text[:200]}")
        
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 5: Probar Endpoint HTTP - Onboarding
print("\n5. Probando endpoint HTTP: /api/v1/on-boarding/get-by-id")
print("   Método: POST")
print("   Tipo: JSON")

try:
    response = requests.post(
        f"{url}/api/v1/on-boarding/get-by-id",
        headers={'Content-Type': 'application/json'},
        json={"id": 1},
        timeout=10
    )
    
    print(f"   Status HTTP: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✓ ¡ENDPOINT FUNCIONANDO!")
        data = response.json()
        print(f"   Respuesta: {json.dumps(data, indent=2)[:300]}...")
    elif response.status_code == 404:
        print("   ✗ Endpoint no encontrado (404)")
    else:
        print(f"   Status: {response.status_code}")
        
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 6: Verificar rutas registradas
print("\n6. Verificando otras rutas...")
test_routes = [
    "/api/test/hello",
    "/web/database/list",
]

for route in test_routes:
    try:
        response = requests.post(
            f"{url}{route}",
            headers={'Content-Type': 'application/json'},
            json={},
            timeout=5
        )
        status_icon = "✓" if response.status_code == 200 else "○"
        print(f"   {status_icon} {route}: {response.status_code}")
    except:
        print(f"   ✗ {route}: Error")

# Limpieza
print("\n" + "=" * 70)
cleanup = input("\n¿Eliminar contactos de prueba? (s/n): ")
if cleanup.lower() == 's':
    try:
        for partner_id in created_ids:
            models.execute_kw(db, uid, password,
                'res.partner', 'unlink', [[partner_id]])
            print(f"  ✓ Eliminado contacto ID: {partner_id}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
else:
    print("  Los contactos permanecen en la base de datos")

print("\n" + "=" * 70)
print("  PRUEBA COMPLETADA")
print("=" * 70 + "\n")
