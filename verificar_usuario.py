#!/usr/bin/env python3
"""
Verificar que el usuario se registró correctamente
"""
import xmlrpc.client
import sys

print("\n" + "=" * 60)
print("  VERIFICANDO USUARIO REGISTRADO")
print("=" * 60 + "\n")

# Configuración
url = "http://localhost:8070"
db = "odoo_enterprise"
username = "admin"
password = "admin"

# Email del usuario que acabamos de registrar
if len(sys.argv) > 1:
    user_email = sys.argv[1]
else:
    user_email = input("Email del usuario a verificar: ")

try:
    # Autenticación como admin
    print("1. Autenticando como admin...")
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    
    if not uid:
        print("   ✗ Error de autenticación")
        sys.exit(1)
    
    print(f"   ✓ Autenticado (UID: {uid})")
    
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # Buscar el usuario
    print(f"\n2. Buscando usuario con email: {user_email}")
    users = models.execute_kw(db, uid, password,
        'res.users', 'search_read',
        [[['login', '=', user_email]]],
        {'fields': ['id', 'name', 'login', 'partner_id', 'create_date']})
    
    if not users:
        print("   ✗ Usuario no encontrado")
        sys.exit(1)
    
    user = users[0]
    print(f"   ✓ Usuario encontrado!")
    print(f"\n   Datos del Usuario:")
    print(f"   • ID: {user['id']}")
    print(f"   • Nombre: {user['name']}")
    print(f"   • Email/Login: {user['login']}")
    print(f"   • Fecha de creación: {user['create_date']}")
    
    # Buscar el partner asociado
    print(f"\n3. Verificando datos del contacto (Partner)...")
    partner_id = user['partner_id'][0]
    partners = models.execute_kw(db, uid, password,
        'res.partner', 'search_read',
        [[['id', '=', partner_id]]],
        {'fields': ['id', 'name', 'email', 'vat', 'phone', 'street', 'city']})
    
    if partners:
        partner = partners[0]
        print(f"   ✓ Contacto encontrado!")
        print(f"\n   Datos del Contacto:")
        print(f"   • ID: {partner['id']}")
        print(f"   • Nombre: {partner['name']}")
        print(f"   • Email: {partner['email']}")
        print(f"   • Cédula/Pasaporte: {partner['vat']}")
        print(f"   • Teléfono: {partner.get('phone', 'N/A')}")
        print(f"   • Dirección: {partner.get('street', 'N/A')}")
        print(f"   • Ciudad: {partner.get('city', 'N/A')}")
    
    # Verificar grupos del usuario
    print(f"\n4. Verificando grupos de acceso...")
    user_groups = models.execute_kw(db, uid, password,
        'res.users', 'read',
        [[user['id']]],
        {'fields': ['groups_id']})
    
    if user_groups and user_groups[0].get('groups_id'):
        group_ids = user_groups[0]['groups_id']
        groups = models.execute_kw(db, uid, password,
            'res.groups', 'read',
            [group_ids],
            {'fields': ['name', 'category_id']})
        
        print(f"   ✓ Usuario tiene {len(groups)} grupos asignados")
        print(f"\n   Grupos principales:")
        for group in groups[:5]:  # Mostrar solo los primeros 5
            category = group.get('category_id', [False, 'Sin categoría'])[1]
            print(f"   • {group['name']} ({category})")
    
    print("\n" + "=" * 60)
    print("  ✓ VERIFICACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 60 + "\n")
    
except Exception as e:
    print(f"\n✗ Error: {e}\n")
    sys.exit(1)
