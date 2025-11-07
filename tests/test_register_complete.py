#!/usr/bin/env python3
"""
Test completo del endpoint de registro con todas las validaciones
"""
import requests
import json
import time

url = "http://localhost:8070"
endpoint = f"{url}/api/v1/auth/register"

print("\n🧪 Test Completo del Endpoint de Registro\n")

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

def test_endpoint(test_name, data, expected_status, expected_error=None):
    """Helper para ejecutar tests"""
    print("=" * 60)
    print(f"TEST: {test_name}")
    print("=" * 60)
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
        
        if status_ok:
            if expected_error:
                error_ok = expected_error in result.get('error', '')
                if error_ok:
                    print(f"✅ PASS - Status: {response.status_code}, Error: {result.get('error')}")
                else:
                    print(f"❌ FAIL - Error esperado: '{expected_error}', recibido: '{result.get('error')}'")
            else:
                print(f"✅ PASS - Status: {response.status_code}")
                if result.get('success'):
                    print(f"   User ID: {result.get('user_id')}")
        else:
            print(f"❌ FAIL - Status esperado: {expected_status}, recibido: {response.status_code}")
            print(f"   Respuesta: {json.dumps(result, indent=2)}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()

# Test 1: Datos incompletos (400)
test_endpoint(
    "Datos incompletos - Sin nombre",
    {
        "passport_number": "TEST123",
        "password": "test123456",
        "email": "test@example.com"
    },
    400,
    "Datos incompletos"
)

# Test 2: Contraseña muy corta (417)
test_endpoint(
    "Contraseña muy corta",
    {
        "name": "Test User",
        "passport_number": f"TEST{int(time.time())}",
        "password": "12345",
        "email": f"test.{int(time.time())}@example.com"
    },
    417,
    "Contraseña inválida"
)

# Test 3: Email inválido (417)
test_endpoint(
    "Email inválido",
    {
        "name": "Test User",
        "passport_number": f"TEST{int(time.time())}",
        "password": "test123456",
        "email": "invalid-email"
    },
    417,
    "Email inválido"
)

# Test 4: Registro exitoso (200)
timestamp = int(time.time())
test_data = {
    "name": "Usuario Test Completo",
    "passport_number": f"PASS{timestamp}",
    "password": "test123456",
    "email": f"user.test.{timestamp}@example.com"
}
test_endpoint(
    "Registro exitoso",
    test_data,
    200
)

# Test 5: Email duplicado (417)
test_endpoint(
    "Email duplicado",
    test_data,
    417,
    "Email ya registrado"
)

# Test 6: Pasaporte duplicado (417)
test_endpoint(
    "Pasaporte duplicado",
    {
        "name": "Otro Usuario",
        "passport_number": test_data["passport_number"],
        "password": "test123456",
        "email": f"otro.{int(time.time())}@example.com"
    },
    417,
    "Cédula/Pasaporte ya registrado"
)

print("=" * 60)
print("TESTS COMPLETADOS")
print("=" * 60)
