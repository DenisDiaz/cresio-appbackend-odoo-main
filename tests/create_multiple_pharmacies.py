#!/usr/bin/env python3
"""
Script para crear múltiples farmacias de prueba
"""
import xmlrpc.client

print("\n🏥 Creando Múltiples Farmacias de Prueba\n")

# Configuración
url = "http://localhost:8070"
db = "odoo_enterprise"
username = "admin"
password = "admin"

# Datos de farmacias en diferentes ubicaciones de Bogotá
pharmacies_data = [
    {
        'name': 'Farmacia Norte',
        'street': 'Calle 127 # 15-30',
        'city': 'Bogotá',
        'phone': '+57 1 234 5001',
        'email': 'norte@farmacia.com',
        'website': 'https://www.farmacianorte.com',
        'partner_latitude': 4.7110,
        'partner_longitude': -74.0721,
    },
    {
        'name': 'Farmacia Sur',
        'street': 'Carrera 30 # 10-50',
        'city': 'Bogotá',
        'phone': '+57 1 234 5002',
        'email': 'sur@farmacia.com',
        'website': 'https://www.farmaciasur.com',
        'partner_latitude': 4.5794,
        'partner_longitude': -74.1169,
    },
    {
        'name': 'Farmacia Occidente',
        'street': 'Avenida 68 # 45-20',
        'city': 'Bogotá',
        'phone': '+57 1 234 5003',
        'email': 'occidente@farmacia.com',
        'website': 'https://www.farmaciaoccidente.com',
        'partner_latitude': 4.6500,
        'partner_longitude': -74.1100,
    },
    {
        'name': 'Farmacia Oriente',
        'street': 'Carrera 7 # 80-50',
        'city': 'Bogotá',
        'phone': '+57 1 234 5004',
        'email': 'oriente@farmacia.com',
        'website': 'https://www.farmaciaoriente.com',
        'partner_latitude': 4.6500,
        'partner_longitude': -74.0500,
    },
    {
        'name': 'Farmacia Chapinero',
        'street': 'Carrera 13 # 60-20',
        'city': 'Bogotá',
        'phone': '+57 1 234 5005',
        'email': 'chapinero@farmacia.com',
        'website': 'https://www.farmaciachapinero.com',
        'partner_latitude': 4.6500,
        'partner_longitude': -74.0650,
    },
]

try:
    # Autenticación
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    
    if not uid:
        print("❌ Error de autenticación")
        exit(1)
    
    print(f"✓ Autenticado como usuario ID: {uid}\n")
    
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    created_ids = []
    
    for pharmacy_data in pharmacies_data:
        # Agregar el campo de conexión externa
        pharmacy_data['is_supplier_with_external_connection'] = True
        
        print(f"Creando: {pharmacy_data['name']}...")
        
        pharmacy_id = models.execute_kw(db, uid, password,
            'res.partner', 'create',
            [pharmacy_data])
        
        created_ids.append(pharmacy_id)
        print(f"  ✓ ID: {pharmacy_id}")
    
    print(f"\n✅ {len(created_ids)} farmacias creadas exitosamente!")
    print(f"   IDs: {created_ids}")
    
    # Probar el endpoint de listado
    print("\n" + "=" * 70)
    print("Probando endpoint de listado...")
    print("=" * 70)
    
    import requests
    import json
    
    # Test con coordenadas (Centro de Bogotá)
    response = requests.post(
        f"{url}/api/v1/pharmacy/list",
        headers={'Content-Type': 'application/json'},
        json={
            "latitude": 4.6097,
            "longitude": -74.0817,
            "limit": 10
        },
        timeout=15
    )
    
    print(f"\n📊 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        pharmacies = data.get('data', [])
        pagination = data.get('pagination', {})
        
        print(f"📋 Total de farmacias: {pagination.get('total')}")
        print(f"📄 Página: {pagination.get('page')}/{pagination.get('pages')}")
        print(f"\n🏥 Farmacias ordenadas por distancia:")
        
        for i, pharmacy in enumerate(pharmacies, 1):
            print(f"\n{i}. {pharmacy['nombre']}")
            print(f"   📍 {pharmacy['direccion']}")
            print(f"   📏 Distancia: {pharmacy['distancia']} km")
            print(f"   🗺️  Coordenadas: {pharmacy['latitude']}, {pharmacy['longitude']}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
