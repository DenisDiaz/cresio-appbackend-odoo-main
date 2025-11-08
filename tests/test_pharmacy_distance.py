#!/usr/bin/env python3
"""
Test del cálculo de distancia del endpoint de farmacia
"""
import requests
import json

url = "http://localhost:8070"
endpoint = f"{url}/api/v1/pharmacy/get-detail"

print("\n" + "=" * 70)
print("  TEST: Cálculo de Distancia - Farmacia")
print("=" * 70 + "\n")

# ID de la farmacia de prueba (ajustar según tu base de datos)
pharmacy_id = 18

# Diferentes ubicaciones para probar el cálculo de distancia
test_locations = [
    {
        "name": "Misma ubicación (0 km)",
        "latitude": 4.6097,
        "longitude": -74.0817
    },
    {
        "name": "Centro de Bogotá (~5 km)",
        "latitude": 4.5981,
        "longitude": -74.0758
    },
    {
        "name": "Norte de Bogotá (~10 km)",
        "latitude": 4.7110,
        "longitude": -74.0721
    },
    {
        "name": "Soacha (~15 km)",
        "latitude": 4.5794,
        "longitude": -74.2169
    }
]

for location in test_locations:
    print("=" * 70)
    print(f"TEST: {location['name']}")
    print("=" * 70)
    
    data = {
        "id": pharmacy_id,
        "latitude": location['latitude'],
        "longitude": location['longitude']
    }
    
    print(f"Ubicación: Lat {location['latitude']}, Lon {location['longitude']}")
    
    try:
        response = requests.post(
            endpoint,
            headers={'Content-Type': 'application/json'},
            json=data,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Respuesta exitosa")
            print(f"   Farmacia: {result['nombre']}")
            print(f"   📏 Distancia calculada: {result['distancia']} km")
            print(f"   📍 Coordenadas farmacia: {result['latitude']}, {result['longitude']}")
            print(f"   📍 Coordenadas usuario: {location['latitude']}, {location['longitude']}")
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(response.json())
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print()

print("=" * 70)
print("TESTS COMPLETADOS")
print("=" * 70)
