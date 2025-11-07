#!/usr/bin/env python3
"""
Prueba de la funcionalidad usando XML-RPC API
Esta es una alternativa funcional mientras se resuelven los endpoints HTTP
"""
import xmlrpc.client
import json

url = "http://localhost:8069"
db = "odoo"
username = "admin"
password = "admin"

print("=" * 70)
print("  PRUEBA: API XML-RPC - Sucursales con Conexión Externa")
print("=" * 70)

# Autenticación
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if not uid:
    print("\n✗ Error de autenticación")
    exit(1)

print(f"\n✓ Autenticado correctamente (UID: {uid})")

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Crear datos de prueba
print("\n" + "-" * 70)
print("Creando sucursales de prueba...")
print("-" * 70)

sucursales = [
    {
        "name": "Sucursal Principal - Bogotá",
        "street": "Carrera 7 # 32-16",
        "street2": "Edificio Centro",
        "city": "Bogotá",
        "state_id": False,  # Se puede configurar después
        "zip": "110111",
        "country_id": False,  # Se puede configurar después
        "phone": "+57 1 234 5678",
        "mobile": "+57 310 123 4567",
        "email": "bogota@zublime.com",
        "website": "https://zublime.com/bogota",
        "is_supplier_with_external_connection": True,
        "partner_latitude": 4.6097,
        "partner_longitude": -74.0817,
    },
    {
        "name": "Sucursal Norte - Medellín",
        "street": "Calle 10 # 43-50",
        "street2": "Centro Comercial Norte",
        "city": "Medellín",
        "zip": "050001",
        "phone": "+57 4 567 8901",
        "mobile": "+57 320 234 5678",
        "email": "medellin@zublime.com",
        "website": "https://zublime.com/medellin",
        "is_supplier_with_external_connection": True,
        "partner_latitude": 6.2442,
        "partner_longitude": -75.5812,
    },
    {
        "name": "Sucursal Sur - Cali",
        "street": "Avenida 6N # 28-10",
        "city": "Cali",
        "zip": "760001",
        "phone": "+57 2 345 6789",
        "email": "cali@zublime.com",
        "is_supplier_with_external_connection": True,
        "partner_latitude": 3.4516,
        "partner_longitude": -76.5320,
    }
]

created_ids = []
for sucursal in sucursales:
    try:
        partner_id = models.execute_kw(db, uid, password,
            'res.partner', 'create', [sucursal])
        created_ids.append(partner_id)
        print(f"✓ Creada: {sucursal['name']} (ID: {partner_id})")
    except Exception as e:
        print(f"✗ Error: {e}")

# Obtener sucursales usando el método del modelo
print("\n" + "-" * 70)
print("Obteniendo sucursales con conexión externa...")
print("-" * 70)

try:
    # Buscar todas las sucursales con conexión externa
    partners = models.execute_kw(db, uid, password,
        'res.partner', 'search_read',
        [[['is_supplier_with_external_connection', '=', True]]],
        {'fields': [
            'name', 'street', 'street2', 'city', 'state_id', 'zip',
            'country_id', 'phone', 'mobile', 'email', 'website',
            'partner_latitude', 'partner_longitude', 'image_1920'
        ]})
    
    print(f"\n✓ Total de sucursales encontradas: {len(partners)}\n")
    
    # Formatear respuesta similar al endpoint API
    response_data = {
        "data": [],
        "http_status": 200
    }
    
    for partner in partners:
        branch_data = {
            "name": partner['name'],
            "street": partner['street'] or "",
            "street2": partner['street2'] or "",
            "city": partner['city'] or "",
            "state": partner['state_id'][1] if partner['state_id'] else "",
            "zip": partner['zip'] or "",
            "country_id": partner['country_id'][1] if partner['country_id'] else "",
            "phone": partner['phone'] or "",
            "mobile": partner['mobile'] or "",
            "email": partner['email'] or "",
            "website": partner['website'] or "",
            "partner_longitude": partner['partner_longitude'],
            "partner_latitude": partner['partner_latitude'],
            "image_1920": partner['image_1920'] or False,
        }
        response_data["data"].append(branch_data)
    
    # Mostrar resultado
    print("Respuesta en formato JSON:")
    print("=" * 70)
    print(json.dumps(response_data, indent=2, ensure_ascii=False))
    print("=" * 70)
    
    # Mostrar detalles de cada sucursal
    print("\nDetalles de sucursales:")
    for idx, branch in enumerate(response_data["data"], 1):
        print(f"\n{idx}. {branch['name']}")
        print(f"   📍 Dirección: {branch['street']}")
        if branch['street2']:
            print(f"      {branch['street2']}")
        print(f"   🏙️  Ciudad: {branch['city']}")
        if branch['zip']:
            print(f"   📮 Código Postal: {branch['zip']}")
        if branch['phone']:
            print(f"   📞 Teléfono: {branch['phone']}")
        if branch['mobile']:
            print(f"   📱 Móvil: {branch['mobile']}")
        if branch['email']:
            print(f"   📧 Email: {branch['email']}")
        if branch['website']:
            print(f"   🌐 Website: {branch['website']}")
        if branch['partner_latitude'] and branch['partner_longitude']:
            print(f"   🗺️  Coordenadas: ({branch['partner_latitude']}, {branch['partner_longitude']})")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Limpieza
print("\n" + "=" * 70)
cleanup = input("\n¿Eliminar sucursales de prueba? (s/n): ")
if cleanup.lower() == 's':
    for partner_id in created_ids:
        try:
            models.execute_kw(db, uid, password,
                'res.partner', 'unlink', [[partner_id]])
            print(f"✓ Eliminada sucursal ID: {partner_id}")
        except Exception as e:
            print(f"✗ Error: {e}")
else:
    print("Las sucursales permanecen en la base de datos")

print("\n" + "=" * 70)
print("  PRUEBA COMPLETADA")
print("=" * 70)
print("\nNota: Esta API XML-RPC es completamente funcional y puede usarse")
print("como alternativa a los endpoints HTTP mientras se resuelve su registro.")
print("\nEjemplo de uso en tu aplicación:")
print("""
import xmlrpc.client

# Conectar
common = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/common')
uid = common.authenticate('odoo', 'admin', 'admin', {})
models = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/object')

# Obtener sucursales
sucursales = models.execute_kw('odoo', uid, 'admin',
    'res.partner', 'search_read',
    [[['is_supplier_with_external_connection', '=', True]]],
    {'fields': ['name', 'city', 'phone', 'partner_latitude', 'partner_longitude']})
""")
print("=" * 70 + "\n")
