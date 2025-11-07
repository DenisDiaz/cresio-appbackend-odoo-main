#!/usr/bin/env python3
import requests

url = "http://localhost:8069"

print("Verificando rutas disponibles en Odoo...")
print("=" * 60)

# Intentar acceder a diferentes variaciones del endpoint
endpoints = [
    "/api/v1/branch-offices/get-all",
    "/api/v1/on-boarding/get-by-id",
    "/web/database/list",
]

for endpoint in endpoints:
    try:
        # Probar con GET
        response_get = requests.get(f"{url}{endpoint}", timeout=2)
        print(f"\nGET {endpoint}")
        print(f"  Status: {response_get.status_code}")
        
        # Probar con POST
        response_post = requests.post(
            f"{url}{endpoint}",
            headers={'Content-Type': 'application/json'},
            json={},
            timeout=2
        )
        print(f"POST {endpoint}")
        print(f"  Status: {response_post.status_code}")
        
    except Exception as e:
        print(f"\n{endpoint}: Error - {e}")

print("\n" + "=" * 60)
