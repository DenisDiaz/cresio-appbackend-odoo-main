#!/usr/bin/env python3
import xmlrpc.client
import json

# Configuración de conexión
url = "http://localhost:8069"
db = "odoo"
username = "admin"
password = "admin"

# Autenticación
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if uid:
    print(f"✓ Autenticado como usuario ID: {uid}")
    
    # Conexión a la API
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # Verificar que el campo existe en el modelo
    print("\n1. Verificando campos del modelo res.partner...")
    fields = models.execute_kw(db, uid, password,
        'res.partner', 'fields_get',
        [],
        {'attributes': ['string', 'type', 'help']})
    
    if 'is_supplier_with_external_connection' in fields:
        print("✓ Campo 'is_supplier_with_external_connection' encontrado:")
        print(f"  - Etiqueta: {fields['is_supplier_with_external_connection']['string']}")
        print(f"  - Tipo: {fields['is_supplier_with_external_connection']['type']}")
    else:
        print("✗ Campo 'is_supplier_with_external_connection' NO encontrado")
        print("\nCampos disponibles que contienen 'supplier' o 'external':")
        for field_name, field_info in fields.items():
            if 'supplier' in field_name.lower() or 'external' in field_name.lower():
                print(f"  - {field_name}: {field_info['string']}")
    
    # Verificar vistas heredadas
    print("\n2. Verificando vistas del módulo zub_supplier_connector...")
    views = models.execute_kw(db, uid, password,
        'ir.ui.view', 'search_read',
        [[['name', 'like', 'zub_supplier_connector']]],
        {'fields': ['name', 'model', 'type', 'inherit_id', 'active']})
    
    if views:
        for view in views:
            print(f"✓ Vista encontrada: {view['name']}")
            print(f"  - Modelo: {view['model']}")
            print(f"  - Tipo: {view['type']}")
            print(f"  - Hereda de: {view['inherit_id']}")
            print(f"  - Activa: {view['active']}")
    else:
        print("✗ No se encontraron vistas del módulo")
    
    # Verificar estado del módulo
    print("\n3. Verificando estado del módulo zub_supplier_connector...")
    module = models.execute_kw(db, uid, password,
        'ir.module.module', 'search_read',
        [[['name', '=', 'zub_supplier_connector']]],
        {'fields': ['name', 'state', 'latest_version']})
    
    if module:
        print(f"✓ Módulo: {module[0]['name']}")
        print(f"  - Estado: {module[0]['state']}")
        print(f"  - Versión: {module[0]['latest_version']}")
    else:
        print("✗ Módulo no encontrado")
        
else:
    print("✗ Error de autenticación")
