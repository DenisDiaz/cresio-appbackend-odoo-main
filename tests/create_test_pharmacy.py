#!/usr/bin/env python3
"""
Script para crear una farmacia de prueba
"""
import xmlrpc.client

print("\n🏥 Creando Farmacia de Prueba\n")

# Configuración
url = "http://localhost:8070"
db = "odoo_enterprise"
username = "admin"
password = "admin"

try:
    # Autenticación
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    
    if not uid:
        print("❌ Error de autenticación")
        exit(1)
    
    print(f"✓ Autenticado como usuario ID: {uid}\n")
    
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # Crear farmacia de prueba
    pharmacy_data = {
        'name': 'Farmacia Central Test',
        'street': 'Carrera 7 # 32-16',
        'street2': 'Edificio Central, Piso 1',
        'city': 'Bogotá',
        'zip': '110111',
        'phone': '+57 1 234 5678',
        'mobile': '+57 300 123 4567',
        'email': 'contacto@farmaciacentral.com',
        'website': 'https://www.farmaciacentral.com',
        'partner_latitude': 4.6097,
        'partner_longitude': -74.0817,
        'is_supplier_with_external_connection': True,
    }
    
    print("Creando farmacia...")
    pharmacy_id = models.execute_kw(db, uid, password,
        'res.partner', 'create',
        [pharmacy_data])
    
    print(f"✅ Farmacia creada exitosamente!")
    print(f"   ID: {pharmacy_id}")
    print(f"   Nombre: {pharmacy_data['name']}")
    print(f"   Dirección: {pharmacy_data['street']}, {pharmacy_data['city']}")
    print(f"   Coordenadas: {pharmacy_data['partner_latitude']}, {pharmacy_data['partner_longitude']}")
    print(f"\n💡 Usa este ID para probar el endpoint: {pharmacy_id}\n")
    
    # Probar el endpoint
    print("=" * 70)
    print("Probando endpoint de detalle...")
    print("=" * 70)
    
    import requests
    import json
    
    response = requests.post(
        f"{url}/api/v1/pharmacy/get-detail",
        headers={'Content-Type': 'application/json'},
        json={
            "id": pharmacy_id,
            "latitude": 4.6097,
            "longitude": -74.0817
        },
        timeout=15
    )
    
    print(f"\n📊 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("📦 Respuesta:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print(f"\n✅ ¡Endpoint funcionando correctamente!")
        print(f"   Farmacia: {data.get('nombre')}")
        print(f"   Distancia: {data.get('distancia')} km")
        print(f"   Dirección: {data.get('direccion')}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
