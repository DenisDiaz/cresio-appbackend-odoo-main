#!/usr/bin/env python3
"""
Prueba del endpoint de registro de usuarios
POST /api/v1/auth/register
"""
import requests
import json
import random
import string

print("\n" + "=" * 70)
print("  TEST: Endpoint de Registro de Usuarios")
print("=" * 70 + "\n")

url = "http://localhost:8070"
endpoint = f"{url}/api/v1/auth/register"

def generate_random_email():
    """Genera un email aleatorio para pruebas"""
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_str}@example.com"

def generate_random_passport():
    """Genera un número de pasaporte aleatorio"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Test 1: Registro exitoso (200)
print("1. Test: Registro exitoso (200)")
print("-" * 70)

test_data = {
    "name": "Usuario Test",
    "passport_number": generate_random_passport(),
    "password": "test123",
    "email": generate_random_email()
}

print(f"Datos de prueba:")
print(json.dumps(test_data, indent=2))
print()

try:
    response = requests.post(
        endpoint,
        headers={'Content-Type': 'application/json'},
        json=test_data,
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✓ Registro exitoso!")
        print(f"Session ID: {data.get('result', {}).get('session_id', 'N/A')}")
        print(f"User ID: {data.get('result', {}).get('user_id', 'N/A')}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Respuesta: {response.text[:300]}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 2: Datos incompletos (400)
print("2. Test: Datos incompletos (400 - Bad Request)")
print("-" * 70)

incomplete_data = {
    "name": "Usuario Test",
    "password": "test123"
    # Faltan email y passport_number
}

try:
    response = requests.post(
        endpoint,
        headers={'Content-Type': 'application/json'},
        json=incomplete_data,
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 400:
        print("✓ Validación correcta: Datos incompletos detectados")
        data = response.json()
        print(f"Mensaje: {data.get('result', {}).get('message', 'N/A')}")
    else:
        print(f"✗ Se esperaba 400, se obtuvo: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 3: Contraseña corta (417)
print("3. Test: Contraseña inválida (417 - Expected Failed)")
print("-" * 70)

short_password_data = {
    "name": "Usuario Test",
    "passport_number": generate_random_passport(),
    "password": "123",  # Muy corta
    "email": generate_random_email()
}

try:
    response = requests.post(
        endpoint,
        headers={'Content-Type': 'application/json'},
        json=short_password_data,
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 417:
        print("✓ Validación correcta: Contraseña muy corta detectada")
        data = response.json()
        print(f"Mensaje: {data.get('result', {}).get('message', 'N/A')}")
    else:
        print(f"✗ Se esperaba 417, se obtuvo: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 4: Email inválido (417)
print("4. Test: Email inválido (417 - Expected Failed)")
print("-" * 70)

invalid_email_data = {
    "name": "Usuario Test",
    "passport_number": generate_random_passport(),
    "password": "test123",
    "email": "email_invalido"  # Sin @
}

try:
    response = requests.post(
        endpoint,
        headers={'Content-Type': 'application/json'},
        json=invalid_email_data,
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 417:
        print("✓ Validación correcta: Email inválido detectado")
        data = response.json()
        print(f"Mensaje: {data.get('result', {}).get('message', 'N/A')}")
    else:
        print(f"✗ Se esperaba 417, se obtuvo: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 5: Email duplicado (417)
print("5. Test: Email duplicado (417 - Expected Failed)")
print("-" * 70)

# Primero registramos un usuario
first_user = {
    "name": "Usuario Duplicado",
    "passport_number": generate_random_passport(),
    "password": "test123",
    "email": generate_random_email()
}

print("Registrando primer usuario...")
response1 = requests.post(endpoint, headers={'Content-Type': 'application/json'}, json=first_user, timeout=10)
print(f"Primer registro: {response1.status_code}")

# Intentamos registrar con el mismo email
duplicate_email_data = {
    "name": "Usuario Duplicado 2",
    "passport_number": generate_random_passport(),
    "password": "test123",
    "email": first_user["email"]  # Mismo email
}

print("Intentando registrar con email duplicado...")
try:
    response = requests.post(
        endpoint,
        headers={'Content-Type': 'application/json'},
        json=duplicate_email_data,
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 417:
        print("✓ Validación correcta: Email duplicado detectado")
        data = response.json()
        print(f"Mensaje: {data.get('result', {}).get('message', 'N/A')}")
    else:
        print(f"✗ Se esperaba 417, se obtuvo: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 6: Cédula/Pasaporte duplicado (417)
print("6. Test: Cédula/Pasaporte duplicado (417 - Expected Failed)")
print("-" * 70)

# Primero registramos un usuario
first_user2 = {
    "name": "Usuario Pasaporte Duplicado",
    "passport_number": generate_random_passport(),
    "password": "test123",
    "email": generate_random_email()
}

print("Registrando primer usuario...")
response1 = requests.post(endpoint, headers={'Content-Type': 'application/json'}, json=first_user2, timeout=10)
print(f"Primer registro: {response1.status_code}")

# Intentamos registrar con el mismo pasaporte
duplicate_passport_data = {
    "name": "Usuario Pasaporte Duplicado 2",
    "passport_number": first_user2["passport_number"],  # Mismo pasaporte
    "password": "test123",
    "email": generate_random_email()
}

print("Intentando registrar con pasaporte duplicado...")
try:
    response = requests.post(
        endpoint,
        headers={'Content-Type': 'application/json'},
        json=duplicate_passport_data,
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 417:
        print("✓ Validación correcta: Pasaporte duplicado detectado")
        data = response.json()
        print(f"Mensaje: {data.get('result', {}).get('message', 'N/A')}")
    else:
        print(f"✗ Se esperaba 417, se obtuvo: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 7: Contraseña muy larga (417)
print("7. Test: Contraseña muy larga (417 - Expected Failed)")
print("-" * 70)

long_password_data = {
    "name": "Usuario Test",
    "passport_number": generate_random_passport(),
    "password": "1234567890123456",  # 16 caracteres (máximo 15)
    "email": generate_random_email()
}

try:
    response = requests.post(
        endpoint,
        headers={'Content-Type': 'application/json'},
        json=long_password_data,
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 417:
        print("✓ Validación correcta: Contraseña muy larga detectada")
        data = response.json()
        print(f"Mensaje: {data.get('result', {}).get('message', 'N/A')}")
    else:
        print(f"✗ Se esperaba 417, se obtuvo: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print()
print("=" * 70)
print("  PRUEBAS COMPLETADAS")
print("=" * 70)
print()
print("Resumen de códigos HTTP esperados:")
print("  200 - Success: Registro exitoso")
print("  400 - Bad Request: Datos incompletos")
print("  417 - Expected Failed: Validaciones de negocio")
print("  500 - Server Error: Error interno")
print()
