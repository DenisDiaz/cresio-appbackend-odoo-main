# 🧪 Scripts de Prueba

Scripts para probar la funcionalidad de Odoo y los módulos personalizados.

## 📋 Scripts Disponibles

### Pruebas de Enterprise

#### `test_endpoints_enterprise.py`
Prueba completa de todos los endpoints HTTP en Odoo Enterprise.

```bash
python tests/test_endpoints_enterprise.py
```

**Prueba:**
- Autenticación
- Módulos instalados
- Endpoint `/api/v1/branch-offices/get-all`
- Endpoint `/api/v1/on-boarding/get-by-id`
- Creación de contactos de prueba

#### `test_enterprise.py`
Verificación rápida de que Odoo Enterprise está funcionando.

```bash
python tests/test_enterprise.py
```

### Pruebas de API

#### `test_xmlrpc_api.py`
Prueba completa de la API XML-RPC con creación de sucursales.

```bash
python tests/test_xmlrpc_api.py
```

**Incluye:**
- Autenticación XML-RPC
- Creación de sucursales con coordenadas
- Búsqueda y filtrado
- Formato de respuesta JSON

#### `test_api_endpoint.py`
Prueba específica de endpoints API.

```bash
python tests/test_api_endpoint.py
```

### Pruebas de Módulos

#### `test_supplier_connector.py`
Prueba del módulo `zub_supplier_connector`.

```bash
python tests/test_supplier_connector.py
```

**Verifica:**
- Campo "Conexión Externa"
- Creación de contactos
- Endpoint de sucursales

#### `test_field_visibility.py`
Verifica que el campo "Conexión Externa" esté disponible.

```bash
python tests/test_field_visibility.py
```

#### `test_complete.py`
Suite completa de pruebas de todos los componentes.

```bash
python tests/test_complete.py
```

### Utilidades

#### `check_modules_status.py`
Verifica el estado de instalación de los módulos.

```bash
python tests/check_modules_status.py
```

**Muestra:**
- zub_utils: installed/uninstalled
- zub_supplier_connector: installed/uninstalled
- zub_onboarding: installed/uninstalled
- zub_loyalty: installed/uninstalled

#### `check_routes.py`
Verifica qué rutas HTTP están disponibles.

```bash
python tests/check_routes.py
```

**Prueba:**
- `/api/v1/branch-offices/get-all`
- `/api/v1/on-boarding/get-by-id`
- `/web/database/list`

#### `demo_rapido.py`
Demo rápida de funcionalidad básica.

```bash
python tests/demo_rapido.py
```

#### `create_test_contacts.py`
Crea contactos de prueba con conexión externa.

```bash
python tests/create_test_contacts.py
```

## 🚀 Uso Rápido

### Verificar que todo funciona

```bash
# 1. Verificar módulos instalados
python tests/check_modules_status.py

# 2. Probar endpoints
python tests/test_endpoints_enterprise.py

# 3. Demo rápida
python tests/demo_rapido.py
```

### Probar API completa

```bash
# API XML-RPC con datos reales
python tests/test_xmlrpc_api.py
```

### Suite completa

```bash
# Todas las pruebas
python tests/test_complete.py
```

## 📊 Resultados Esperados

Todos los scripts deberían mostrar:
- ✅ Autenticación exitosa
- ✅ Módulos instalados
- ✅ Endpoints respondiendo 200 OK
- ✅ Datos retornados correctamente

## ⚙️ Configuración

Los scripts usan por defecto:

```python
url = "http://localhost:8070"  # Enterprise
db = "odoo_enterprise"
username = "admin"
password = "admin"
```

Para Odoo Community, cambia:
```python
url = "http://localhost:8069"
db = "odoo"
```

## 🐛 Solución de Problemas

### Error de conexión
```bash
# Verificar que Odoo esté corriendo
docker ps | grep odoo
```

### Error de autenticación
```bash
# Verificar credenciales
# Usuario: admin
# Contraseña: admin
# Base de datos: odoo_enterprise
```

### Módulos no encontrados
```bash
# Instalar módulos desde la interfaz web
# Apps > Buscar "zub" > Instalar
```

## 📝 Notas

- Los scripts crean datos de prueba que pueden ser eliminados
- Algunos scripts preguntan si deseas limpiar los datos al final
- Los scripts son seguros y no afectan datos de producción

---

**Ejecuta los scripts para verificar que todo funciona correctamente** ✅
