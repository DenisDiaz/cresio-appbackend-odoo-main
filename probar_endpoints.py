#!/usr/bin/env python3
"""
Script simple para probar los endpoints REST de Odoo
Ejecutar: python probar_endpoints.py
"""
import requests
import json

print("\n" + "=" * 60)
print("  PROBANDO ENDPOINTS REST - ODOO")
print("=" * 60 + "\n")

BASE_URL = "http://localhost:8070"

def test_endpoint(name, url, data=None):
    """Función helper para probar endpoints"""
    print(f"\n{name}")
    print("-" * 60)
    try:
        response = requests.post(
            url,
            headers={'Content-Type': 'application/json'},
            json=data or {},
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Éxito!")
            return response.json()
        elif response.status_code == 404:
            print("⚠ Endpoint no encontrado o sin datos")
            return None
        else:
            print(f"✗ Error: {response.status_code}")
            print(response.text[:200])
            return None
            
    except Exception as e:
        print(f"✗ Error de conexión: {e}")
        return None

# Test 1: Obtener sucursales
print("\n1. OBTENER SUCURSALES")
data = test_endpoint(
    "GET /api/v1/branch-offices/get-all",
    f"{BASE_URL}/api/v1/branch-offices/get-all"
)

if data and 'data' in data:
    print(f"\nSucursales encontradas: {len(data['data'])}")
    for branch in data['data'][:3]:
        print(f"  • {branch.get('name')} - {branch.get('city')}")

# Test 2: Listar farmacias sin coordenadas
print("\n\n2. LISTAR FARMACIAS (sin coordenadas)")
data = test_endpoint(
    "POST /api/v1/pharmacy/list",
    f"{BASE_URL}/api/v1/pharmacy/list"
)

if data and 'data' in data:
    print(f"\nTotal: {data['pagination']['total']} farmacias")
    print(f"Página: {data['pagination']['page']} de {data['pagination']['pages']}")
    print("\nFarmacias:")
    for pharmacy in data['data'][:3]:
        print(f"  • {pharmacy['nombre']}")
        print(f"    {pharmacy['direccion']}")

# Test 3: Listar farmacias con coordenadas
print("\n\n3. LISTAR FARMACIAS (con coordenadas)")
data = test_endpoint(
    "POST /api/v1/pharmacy/list (con ubicación)",
    f"{BASE_URL}/api/v1/pharmacy/list",
    {
        "latitude": 4.6097,
        "longitude": -74.0817,
        "page": 1,
        "limit": 5
    }
)

if data and 'data' in data:
    print("\nFarmacias ordenadas por distancia:")
    for pharmacy in data['data']:
        print(f"  • {pharmacy['nombre']}: {pharmacy['distancia']} km")

# Test 4: Detalle de farmacia
print("\n\n4. DETALLE DE FARMACIA")

# Primero obtener una farmacia
list_data = test_endpoint(
    "Obteniendo lista para ID",
    f"{BASE_URL}/api/v1/pharmacy/list"
)

if list_data and list_data['data']:
    pharmacy_id = list_data['data'][0]['id']
    print(f"\nObteniendo detalle de farmacia ID: {pharmacy_id}")
    
    data = test_endpoint(
        "POST /api/v1/pharmacy/get-detail",
        f"{BASE_URL}/api/v1/pharmacy/get-detail",
        {
            "id": pharmacy_id,
            "latitude": 4.6097,
            "longitude": -74.0817
        }
    )
    
    if data:
        print("\nDetalle:")
        print(f"  Nombre: {data.get('nombre')}")
        print(f"  Dirección: {data.get('direccion')}")
        print(f"  Teléfono: {data.get('telefono')}")
        print(f"  Email: {data.get('email')}")
        print(f"  Web: {data.get('web')}")
        print(f"  Distancia: {data.get('distancia')} km")
        print(f"  Imágenes: {len(data.get('imagenes', []))}")

# Test 5: Onboarding
print("\n\n5. ONBOARDING")
data = test_endpoint(
    "POST /api/v1/on-boarding/get-by-id",
    f"{BASE_URL}/api/v1/on-boarding/get-by-id",
    {"id": 1}
)

if data:
    print("\nDatos de onboarding recibidos correctamente")

print("\n" + "=" * 60)
print("  PRUEBAS COMPLETADAS")
print("=" * 60)
print("\nPara más ejemplos, revisa: ejemplos_uso_endpoints.md\n")
