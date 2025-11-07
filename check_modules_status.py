#!/usr/bin/env python3
import xmlrpc.client

url = "http://localhost:8069"
db = "odoo"
username = "admin"
password = "admin"

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if uid:
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    modules = models.execute_kw(db, uid, password,
        'ir.module.module', 'search_read',
        [[['name', 'in', ['zub_utils', 'zub_supplier_connector', 'zub_onboarding', 'zub_loyalty']]]],
        {'fields': ['name', 'state']})
    
    print("Estado de los módulos Zublime:")
    print("=" * 50)
    for module in modules:
        status_icon = "✓" if module['state'] == 'installed' else "✗"
        print(f"{status_icon} {module['name']}: {module['state']}")
else:
    print("Error de autenticación")
