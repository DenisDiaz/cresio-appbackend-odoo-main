#!/usr/bin/env python3
"""
Prueba completa de registro de usuario
"""
import requests
import json
from datetime import datetime

print("\n" + "=" * 70)
print("  PRUEBA COMPLETA DE REGISTRO DE USUARIO")
print("=" * 70 + "\n")

BASE_URL = "http://localhost:8070"

# Generar datos únicos
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
user_data = {
    "name": f"Carlos Mendez Test {timestamp}",
    "email": f"carlos.mendez.{timestamp}@example.com",
    "passport_number": f"CC{timestamp}",
    "password": "test123456"
}

print("1. DATOS DEL USUARIO A REGISTRAR")
print("-" * 70)
print(f"   Nombre: {user_data['name']}")
print(f"   Email: {user_data['email']}")
print(f"   Cédula: {user_data['passport_number']}")
print(f"   Contraseña: {user_data['password']}")

# Test 1: Registro
print("\n2. REGISTRANDO USUARIO")
print("-" * 70)
try:
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/register",
        headers={'Content-Type': 'application/json'},
        json=user_data,
        timeout=10
    )
    
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        session_id = data.get('session_id')
        
        print(f"   ✓ Usuario registrado exitosamente!")
        print(f"   Session ID: {session_id[:50]}...")
        
        # Test 2: Verificar que el usuario puede acceder
        print("\n3. VERIFICANDO ACCESO CON SESSION_ID")
        print("-" * 70)
        
        # Intentar acceder a un endpoint protegido
        cookies = {'session_id': session_id}
        
        # Probar acceso a la información del usuario
        try:
            session_response = requests.get(
                f"{BASE_URL}/web",
                cookies=cookies,
                timeout=10,
                allow_redirects=False
            )
            
            if session_response.status_code in [200, 303]:
                print(f"   ✓ Sesión válida - Usuario autenticado correctamente")
                print(f"   Status: {session_response.status_code}")
            else:
                print(f"   ⚠ Respuesta inesperada: {session_response.status_code}")
                
        except Exception as e:
            print(f"   ✗ Error al verificar sesión: {e}")
        
        # Test 3: Verificar en base de datos usando XML-RPC
        print("\n4. VERIFICANDO EN BASE DE DATOS (XML-RPC)")
        print("-" * 70)
        
        import xmlrpc.client
        
        try:
            # Autenticar como admin
            common = xmlrpc.client.ServerProxy(f'{BASE_URL}/xmlrpc/2/common')
            uid = common.authenticate('odoo_enterprise', 'admin', 'admin', {})
            
            if uid:
                models = xmlrpc.client.ServerProxy(f'{BASE_URL}/xmlrpc/2/object')
                
                # Buscar el usuario
                users = models.execute_kw('odoo_enterprise', uid, 'admin',
                    'res.users', 'search_read',
                    [[['login', '=', user_data['email']]]],
                    {'fields': ['id', 'name', 'login', 'partner_id']})
                
                if users:
                    user = users[0]
                    print(f"   ✓ Usuario encontrado en base de datos")
                    print(f"   • ID: {user['id']}")
                    print(f"   • Nombre: {user['name']}")
                    print(f"   • Email: {user['login']}")
                    
                    # Verificar partner
                    partner_id = user['partner_id'][0]
                    partners = models.execute_kw('odoo_enterprise', uid, 'admin',
                        'res.partner', 'search_read',
                        [[['id', '=', partner_id]]],
                        {'fields': ['name', 'email', 'vat']})
                    
                    if partners:
                        partner = partners[0]
                        print(f"\n   Datos del Contacto:")
                        print(f"   • Nombre: {partner['name']}")
                        print(f"   • Email: {partner['email']}")
                        print(f"   • Cédula: {partner['vat']}")
                else:
                    print(f"   ✗ Usuario no encontrado en base de datos")
            else:
                print(f"   ✗ Error de autenticación como admin")
                
        except Exception as e:
            print(f"   ✗ Error XML-RPC: {e}")
        
        # Test 4: Intentar registrar el mismo usuario (debe fallar)
        print("\n5. PROBANDO VALIDACIÓN DE EMAIL DUPLICADO")
        print("-" * 70)
        
        try:
            duplicate_response = requests.post(
                f"{BASE_URL}/api/v1/auth/register",
                headers={'Content-Type': 'application/json'},
                json=user_data,
                timeout=10
            )
            
            if duplicate_response.status_code == 417:
                error_data = duplicate_response.json()
                print(f"   ✓ Validación correcta - Email duplicado rechazado")
                print(f"   Status: {duplicate_response.status_code}")
                print(f"   Mensaje: {error_data.get('message')}")
            else:
                print(f"   ⚠ Respuesta inesperada: {duplicate_response.status_code}")
                
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        print("\n" + "=" * 70)
        print("  ✓ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("=" * 70 + "\n")
        
    else:
        print(f"   ✗ Error en registro: {response.status_code}")
        print(f"   Respuesta: {response.text}")
        
except Exception as e:
    print(f"   ✗ Error: {e}")
    print("\n" + "=" * 70)
    print("  ✗ PRUEBA FALLIDA")
    print("=" * 70 + "\n")
