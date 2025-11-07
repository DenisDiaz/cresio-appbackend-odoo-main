#!/usr/bin/env python3
"""
Script de prueba completo para verificar todos los módulos Zublime
"""
import xmlrpc.client
import requests
import json
import time

# Configuración
url = "http://localhost:8069"
db = "odoo"
username = "admin"
password = "admin"

def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def wait_for_odoo(max_attempts=10):
    """Espera a que Odoo esté disponible"""
    print("\nEsperando a que Odoo esté disponible...")
    for i in range(max_attempts):
        try:
            response = requests.get(f"{url}/web/database/list", timeout=2)
            if response.status_code in [200, 400]:
                print("✓ Odoo está disponible")
                return True
        except:
            pass
        print(f"  Intento {i+1}/{max_attempts}...")
        time.sleep(2)
    return False

# Esperar a que Odoo esté disponible
if not wait_for_odoo():
    print("✗ No se pudo conectar a Odoo")
    exit(1)

print_section("TEST 1: Verificar Estado de Módulos")

try:
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    
    if not uid:
        print("✗ Error de autenticación")
        exit(1)
    
    print(f"✓ Autenticado como usuario ID: {uid}")
    
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # Verificar módulos
    modules = models.execute_kw(db, uid, password,
        'ir.module.module', 'search_read',
        [[['name', 'in', ['zub_utils', 'zub_supplier_connector', 'zub_onboarding', 'zub_loyalty']]]],
        {'fields': ['name', 'state']})
    
    print("\nEstado de módulos:")
    for module in modules:
        status_icon = "✓" if module['state'] == 'installed' else "✗"
        print(f"  {status_icon} {module['name']}: {module['state']}")

except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

print_section("TEST 2: Verificar Campo 'Conexión Externa'")

try:
    # Verificar que el campo existe
    fields = models.execute_kw(db, uid, password,
        'res.partner', 'fields_get',
        [],
        {'attributes': ['string', 'type']})
    
    if 'is_supplier_with_external_connection' in fields:
        field_info = fields['is_supplier_with_external_connection']
        print(f"✓ Campo encontrado:")
        print(f"  - Nombre técnico: is_supplier_with_external_connection")
        print(f"  - Etiqueta: {field_info['string']}")
        print(f"  - Tipo: {field_info['type']}")
    else:
        print("✗ Campo 'is_supplier_with_external_connection' no encontrado")

except Exception as e:
    print(f"✗ Error: {e}")

print_section("TEST 3: Crear Contactos de Prueba")

test_partners = [
    {
        "name": "Sucursal Test 1 - Bogotá",
        "street": "Carrera 7 # 32-16",
        "city": "Bogotá",
        "phone": "+57 1 234 5678",
        "email": "test1@zublime.com",
        "is_supplier_with_external_connection": True,
        "partner_latitude": 4.6097,
        "partner_longitude": -74.0817,
    },
    {
        "name": "Sucursal Test 2 - Medellín",
        "street": "Calle 10 # 43-50",
        "city": "Medellín",
        "phone": "+57 4 567 8901",
        "email": "test2@zublime.com",
        "is_supplier_with_external_connection": True,
        "partner_latitude": 6.2442,
        "partner_longitude": -75.5812,
    },
    {
        "name": "Cliente Test - Sin Conexión",
        "street": "Avenida 6N # 28-10",
        "city": "Cali",
        "is_supplier_with_external_connection": False,
    }
]

created_ids = []
try:
    for partner_data in test_partners:
        partner_id = models.execute_kw(db, uid, password,
            'res.partner', 'create', [partner_data])
        created_ids.append(partner_id)
        status = "✓" if partner_data['is_supplier_with_external_connection'] else "○"
        print(f"{status} Creado: {partner_data['name']} (ID: {partner_id})")
except Exception as e:
    print(f"✗ Error creando contactos: {e}")

print_section("TEST 4: Verificar Contactos con Conexión Externa")

try:
    partners = models.execute_kw(db, uid, password,
        'res.partner', 'search_read',
        [[['is_supplier_with_external_connection', '=', True]]],
        {'fields': ['name', 'city', 'phone']})
    
    print(f"\nTotal de proveedores con conexión externa: {len(partners)}")
    for partner in partners:
        print(f"  ✓ {partner['name']} - {partner.get('city', 'N/A')}")

except Exception as e:
    print(f"✗ Error: {e}")

print_section("TEST 5: Probar Endpoint API - Branch Offices")

try:
    response = requests.post(
        f"{url}/api/v1/branch-offices/get-all",
        headers={'Content-Type': 'application/json'},
        json={},
        timeout=5
    )
    
    print(f"\nURL: {url}/api/v1/branch-offices/get-all")
    print(f"Método: POST")
    print(f"Status HTTP: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Respuesta exitosa")
        
        if 'data' in data:
            branches = data['data']
            print(f"\nSucursales encontradas: {len(branches)}")
            for idx, branch in enumerate(branches[:3], 1):  # Mostrar solo las primeras 3
                print(f"\n  Sucursal {idx}:")
                print(f"    • Nombre: {branch.get('name')}")
                print(f"    • Ciudad: {branch.get('city')}")
                print(f"    • Teléfono: {branch.get('phone')}")
                if branch.get('partner_latitude') and branch.get('partner_longitude'):
                    print(f"    • Coordenadas: ({branch.get('partner_latitude')}, {branch.get('partner_longitude')})")
        else:
            print(f"\nRespuesta: {json.dumps(data, indent=2)}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Respuesta: {response.text[:200]}")

except Exception as e:
    print(f"✗ Error: {e}")

print_section("TEST 6: Probar Endpoint API - Onboarding")

try:
    response = requests.post(
        f"{url}/api/v1/on-boarding/get-by-id",
        headers={'Content-Type': 'application/json'},
        json={"id": 1},
        timeout=5
    )
    
    print(f"\nURL: {url}/api/v1/on-boarding/get-by-id")
    print(f"Método: POST")
    print(f"Status HTTP: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Respuesta exitosa")
        print(f"Respuesta: {json.dumps(data, indent=2)[:300]}...")
    elif response.status_code == 404:
        print(f"○ Endpoint no encontrado (puede ser normal si no hay datos)")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Respuesta: {response.text[:200]}")

except Exception as e:
    print(f"✗ Error: {e}")

print_section("TEST 7: Probar Endpoint de Test")

try:
    response = requests.post(
        f"{url}/api/test/hello",
        headers={'Content-Type': 'application/json'},
        json={},
        timeout=5
    )
    
    print(f"\nURL: {url}/api/test/hello")
    print(f"Método: POST")
    print(f"Status HTTP: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Respuesta exitosa")
        print(f"Mensaje: {data.get('message', 'N/A')}")
    else:
        print(f"✗ Error: {response.status_code}")

except Exception as e:
    print(f"✗ Error: {e}")

print_section("LIMPIEZA: Eliminar Datos de Prueba")

cleanup = input("\n¿Deseas eliminar los contactos de prueba? (s/n): ")
if cleanup.lower() == 's':
    try:
        for partner_id in created_ids:
            models.execute_kw(db, uid, password,
                'res.partner', 'unlink', [[partner_id]])
            print(f"  ✓ Eliminado contacto ID: {partner_id}")
    except Exception as e:
        print(f"  ✗ Error eliminando contactos: {e}")
else:
    print("  Los contactos de prueba permanecen en la base de datos")

print_section("RESUMEN DE PRUEBAS")
print("\n✓ Pruebas completadas")
print("\nPara acceder a Odoo:")
print(f"  URL: {url}")
print(f"  Usuario: {username}")
print(f"  Contraseña: {password}")
print("\n" + "=" * 70 + "\n")
