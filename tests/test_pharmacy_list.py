#!/usr/bin/env python3
"""
Test del endpoint de listado de farmacias
POST /api/v1/pharmacy/list
"""
import requests
import json
import time

url = "http://localhost:8070"
endpoint = f"{url}/api/v1/pharmacy/list"

print("\n" + "=" * 70)
print("  TEST: Endpoint de Listado de Farmacias")
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
        
        if status_ok:
            print(f"✅ PASS - Status: {response.status_code}")
            if response.status_code == 200:
                data_list = result.get('data', [])
                pagination = result.get('pagination', {})
                print(f"   📋 Farmacias encontradas: {len(data_list)}")
                print(f"   📄 Página: {pagination.get('page')}/{pagination.get('pages')}")
                print(f"   📊 Total: {pagination.get('total')}")
                print(f"   📏 Límite: {pagination.get('limit')}")
                
                if data_list:
                    print(f"\n   Primera farmacia:")
                    first = data_list[0]
                    print(f"   - Nombre: {first.get('nombre')}")
                    print(f"   - Dirección: {first.get('direccion')}")
                    print(f"   - Distancia: {first.get('distancia')} km")
        else:
            print(f"❌ FAIL - Status esperado: {expected_status}, recibido: {response.status_code}")
            print(f"Respuesta: {json.dumps(result, indent=2)}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()

# Test 1: Listado sin coordenadas (200)
test_endpoint(
    "Listado sin coordenadas",
    {},
    200
)

# Test 2: Listado con coordenadas (200)
test_endpoint(
    "Listado con coordenadas (ordenado por distancia)",
    {
        "latitude": 4.6097,
        "longitude": -74.0817
    },
    200
)

# Test 3: Listado con paginación (200)
test_endpoint(
    "Listado con paginación - Página 1, Límite 5",
    {
        "latitude": 4.6097,
        "longitude": -74.0817,
        "page": 1,
        "limit": 5
    },
    200
)

# Test 4: Listado página 2 (200)
test_endpoint(
    "Listado - Página 2",
    {
        "page": 2,
        "limit": 5
    },
    200
)

# Test 5: Latitud inválida (400)
test_endpoint(
    "Latitud inválida",
    {
        "latitude": "invalid",
        "longitude": -74.0817
    },
    400
)

# Test 6: Longitud inválida (400)
test_endpoint(
    "Longitud inválida",
    {
        "latitude": 4.6097,
        "longitude": "invalid"
    },
    400
)

# Test 7: Página inválida (400)
test_endpoint(
    "Página inválida",
    {
        "page": "abc"
    },
    400
)

# Test 8: Límite inválido (400)
test_endpoint(
    "Límite inválido",
    {
        "limit": "xyz"
    },
    400
)

# Test 9: Límite muy grande (se ajusta a 100)
test_endpoint(
    "Límite muy grande (se ajusta a 100)",
    {
        "limit": 500
    },
    200
)

# Test 10: Página negativa (se ajusta a 1)
test_endpoint(
    "Página negativa (se ajusta a 1)",
    {
        "page": -5
    },
    200
)

print("=" * 70)
print("TESTS COMPLETADOS")
print("=" * 70)
print("\n💡 Nota: Asegúrate de tener farmacias con 'Conexión Externa' = True")
print()
