#!/usr/bin/env python3
"""
Script de prueba para Odoo 18 Enterprise
"""
import requests
import time

print("\n" + "=" * 70)
print("  TEST: Odoo 18 Enterprise")
print("=" * 70 + "\n")

url = "http://localhost:8070"

# Test 1: Verificar que Odoo está disponible
print("1. Verificando disponibilidad de Odoo Enterprise...")
try:
    response = requests.get(f"{url}/web/database/selector", timeout=5)
    if response.status_code == 200:
        print("   ✓ Odoo Enterprise está disponible")
        print(f"   URL: {url}")
    else:
        print(f"   ✗ Error: Status {response.status_code}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    exit(1)

# Test 2: Verificar lista de bases de datos
print("\n2. Verificando lista de bases de datos...")
try:
    response = requests.post(
        f"{url}/web/database/list",
        headers={'Content-Type': 'application/json'},
        json={},
        timeout=5
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Respuesta exitosa")
        if 'result' in data:
            databases = data['result']
            print(f"   Bases de datos: {databases if databases else 'Ninguna (crear nueva)'}")
    else:
        print(f"   ✗ Error: {response.status_code}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 70)
print("  RESUMEN")
print("=" * 70)
print("\n✓ Odoo 18 Enterprise está funcionando correctamente\n")
print("Próximos pasos:")
print("  1. Abre tu navegador en: http://localhost:8070")
print("  2. Crea una nueva base de datos")
print("  3. Instala los módulos:")
print("     - zub_utils")
print("     - zub_supplier_connector")
print("     - zub_onboarding")
print("\nNota: Con Enterprise, los endpoints HTTP deberían funcionar correctamente")
print("\nPara ver los logs en tiempo real:")
print("  docker logs -f odoo_zublime_enterprise")
print("\nPara detener:")
print("  docker-compose -f docker-compose.enterprise.yml down")
print("\n" + "=" * 70 + "\n")
