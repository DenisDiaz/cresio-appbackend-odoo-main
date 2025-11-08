#!/usr/bin/env python3
"""
Test del endpoint de detalle de farmacia
POST /api/v1/pharmacy/get-detail
"""
import requests
import json
import time

url = "http://localhost:8070"
endpoint = f"{url}/api/v1/pharmacy/get-detail"

print("\n" + "=" * 70)
print("  TEST: Endpoint de Detalle de Farmacia")
print("=" * 70 + "\n")

# Esperar a que Odoo esté disponible
print("Esperando a que Odoo esté disponible...")
for i in range(10):
    try:
        response = requests.get(f"{url}/web/database/selector", timeout=2)
        if response.status_code == 200:
            print("✓ Odoo está disponible\n")
            break
    except:
        pass
    if i < 9:
        print(f"  Intento {i+1}/10...")
        time.sleep(3)

def test_endpoint(test_name, data, expected_status):
    """Helper para ejecutar tests"""
    print("=" * 70)
    print(f"TEST: {test_name}")
    print("=" * 70)
    print(f"Datos: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(
            endpoint,
            headers={'Content-Type': 'application/json'},
            json=data,
            timeout=15
        )
        
        result = response.json()
        status_ok = response.status_code == expected_status
        
        print(f"\n📊 Status Code: {response.status_code}")
        print(f"📦 Respuesta:")
        print(json.dumps(result, indent=2))
        
        if status_ok:
            print(f"\n✅ PASS - Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   Farmacia: {result.get('nombre', 'N/A')}")
                print(f"   Distancia: {result.get('distancia', 'N/A')} km")
                print(f"   Dirección: {result.get('direccion', 'N/A')}")
        else:
            print(f"\n❌ FAIL - Status esperado: {expected_status}, recibido: {response.status_code}")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
    
    print()

# Test 1: Sin ID (400)
test_endpoint(
    "Sin ID de farmacia",
    {
        "latitude": 4.6097,
        "longitude": -74.0817
    },
    400
)

# Test 2: ID inválido (400)
test_endpoint(
    "ID inválido (no numérico)",
    {
        "id": "abc",
        "latitude": 4.6097,
        "longitude": -74.0817
    },
    400
)

# Test 3: ID que no existe (404)
test_endpoint(
    "ID que no existe",
    {
        "id": 999999,
        "latitude": 4.6097,
        "longitude": -74.0817
    },
    404
)

# Test 4: Obtener detalle exitoso (200)
# Primero necesitamos obtener un ID válido
print("=" * 70)
print("Obteniendo lista de farmacias para test...")
print("=" * 70)

try:
    list_response = requests.post(
        f"{url}/api/v1/branch-offices/get-all",
        headers={'Content-Type': 'application/json'},
        json={},
        timeout=15
    )
    
    if list_response.status_code == 200:
        list_data = list_response.json()
        pharmacies = list_data.get('result', {}).get('data', [])
        
        if pharmacies:
            # Usar la primera farmacia
            first_pharmacy = pharmacies[0]
            pharmacy_name = first_pharmacy.get('name', 'N/A')
            print(f"✓ Farmacia encontrada: {pharmacy_name}\n")
            
            # Obtener el ID de la farmacia
            # Buscar una farmacia con conexión externa
            import xmlrpc.client
            try:
                common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
                uid = common.authenticate('odoo_enterprise', 'admin', 'admin', {})
                if uid:
                    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
                    pharmacy_ids = models.execute_kw('odoo_enterprise', uid, 'admin',
                        'res.partner', 'search',
                        [[['is_supplier_with_external_connection', '=', True]]], {'limit': 1})
                    if pharmacy_ids:
                        test_pharmacy_id = pharmacy_ids[0]
                    else:
                        test_pharmacy_id = 1
                else:
                    test_pharmacy_id = 1
            except:
                test_pharmacy_id = 1
            
            test_endpoint(
                "Detalle exitoso con coordenadas",
                {
                    "id": test_pharmacy_id,
                    "latitude": 4.6097,
                    "longitude": -74.0817
                },
                200
            )
            
            test_endpoint(
                "Detalle exitoso sin coordenadas",
                {
                    "id": test_pharmacy_id
                },
                200
            )
        else:
            print("⚠️  No hay farmacias en la base de datos")
            print("   Crea una farmacia con 'Conexión Externa' = True\n")
    else:
        print(f"⚠️  Error obteniendo lista: {list_response.status_code}\n")
        
except Exception as e:
    print(f"⚠️  Error: {e}\n")

# Test 5: Latitud inválida (400)
test_endpoint(
    "Latitud inválida",
    {
        "id": 1,
        "latitude": "invalid",
        "longitude": -74.0817
    },
    400
)

# Test 6: Longitud inválida (400)
test_endpoint(
    "Longitud inválida",
    {
        "id": 1,
        "latitude": 4.6097,
        "longitude": "invalid"
    },
    400
)

print("=" * 70)
print("TESTS COMPLETADOS")
print("=" * 70)
print("\n💡 Nota: Para que los tests pasen completamente, asegúrate de:")
print("   1. Tener al menos una farmacia con 'Conexión Externa' = True")
print("   2. Ajustar el ID de prueba según tu base de datos")
print()
