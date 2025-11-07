#!/usr/bin/env python3
"""
Prueba simple del endpoint de registro
"""
import requests
import json
import time

url = "http://localhost:8070"
endpoint = f"{url}/api/v1/auth/register"

print("\n🧪 Prueba Simple del Endpoint de Registro\n")

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
    print(f"  Intento {i+1}/10...")
    time.sleep(3)

# Test: Registro exitoso
print("=" * 60)
print("TEST: Registro de Usuario")
print("=" * 60)

timestamp = int(time.time())
test_data = {
    "name": "Juan Pérez Test",
    "passport_number": f"PASS{timestamp}",
    "password": "test123456",
    "email": f"juan.test.{timestamp}@example.com"
}

print("\nDatos de registro:")
print(json.dumps(test_data, indent=2))
print()

try:
    print("Enviando petición...")
    response = requests.post(
        endpoint,
        headers={'Content-Type': 'application/json'},
        json=test_data,
        timeout=15
    )
    
    print(f"\n📊 Status Code: {response.status_code}")
    print(f"📊 Headers: {dict(response.headers)}\n")
    
    try:
        data = response.json()
        print("📦 Respuesta JSON:")
        print(json.dumps(data, indent=2))
        print()
        
        if response.status_code == 200:
            if 'session_id' in data:
                print("✅ ¡REGISTRO EXITOSO CON AUTOLOGIN!")
                print(f"   Session ID: {data['session_id']}")
                print(f"   Datos de prueba:")
                print(f"   - Email: {test_data['email']}")
                print(f"   - Password: {test_data['password']}")
            elif data.get('success'):
                print("✅ ¡REGISTRO EXITOSO!")
                print(f"   User ID: {data.get('user_id', 'N/A')}")
                print("   ⚠️  Pero sin session_id (autologin falló)")
            else:
                print("⚠️  Respuesta 200 pero sin session_id ni success")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except json.JSONDecodeError:
        print("❌ Respuesta no es JSON:")
        print(response.text[:500])
        
except requests.exceptions.Timeout:
    print("❌ Timeout: El servidor no respondió a tiempo")
except requests.exceptions.ConnectionError as e:
    print(f"❌ Error de conexión: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
