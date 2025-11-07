# 🧪 Tests - Cresio Backend

Scripts de prueba para verificar la funcionalidad de Odoo Enterprise y los módulos personalizados.

## 📋 Tests Disponibles

### 🎯 Tests del Endpoint de Registro (Principales)

#### `test_register_simple.py` ⭐
Test básico del endpoint de registro de usuarios.

```bash
python tests/test_register_simple.py
```

**Prueba:**
- Registro de un usuario nuevo
- Autologin automático
- Generación de session_id

#### `test_register_complete.py` ⭐
Suite completa de tests con todas las validaciones.

```bash
python tests/test_register_complete.py
```

**Prueba (6 casos):**
- ✅ Datos incompletos (400)
- ✅ Contraseña muy corta (417)
- ✅ Email inválido (417)
- ✅ Registro exitoso (200)
- ✅ Email duplicado (417)
- ✅ Pasaporte duplicado (417)

#### `test_register.html` ⭐
Test manual interactivo en el navegador.

```bash
# Abrir en el navegador
start tests/test_register.html
```

**Características:**
- Formulario visual
- Validación en tiempo real
- Respuestas formateadas

#### `test_register.http` ⭐
Tests para REST Client (VS Code extension).

```bash
# Usar con la extensión REST Client de VS Code
# Abrir el archivo y hacer clic en "Send Request"
```

### 🔧 Tests de Infraestructura

#### `test_endpoints_enterprise.py`
Prueba completa de todos los endpoints HTTP en Odoo Enterprise.

```bash
python tests/test_endpoints_enterprise.py
```

**Verifica:**
- Autenticación XML-RPC
- Módulos instalados (zub_*)
- Endpoint `/api/v1/branch-offices/get-all`
- Endpoint `/api/v1/on-boarding/get-by-id`
- Endpoint `/api/v1/auth/register`

#### `test_xmlrpc_api.py`
Prueba completa de la API XML-RPC.

```bash
python tests/test_xmlrpc_api.py
```

**Incluye:**
- Autenticación XML-RPC
- Creación de sucursales con coordenadas
- Búsqueda y filtrado
- Formato de respuesta JSON

#### `check_modules_status.py`
Verifica el estado de instalación de los módulos personalizados.

```bash
python tests/check_modules_status.py
```

**Muestra:**
- ✅ zub_utils: installed/uninstalled
- ✅ zub_supplier_connector: installed/uninstalled
- ✅ zub_onboarding: installed/uninstalled
- ✅ zub_loyalty: installed/uninstalled

## 🚀 Uso Rápido

### Verificar Endpoint de Registro

```bash
# Test rápido
python tests/test_register_simple.py

# Test completo con todas las validaciones
python tests/test_register_complete.py
```

### Verificar Infraestructura

```bash
# 1. Verificar módulos instalados
python tests/check_modules_status.py

# 2. Probar todos los endpoints
python tests/test_endpoints_enterprise.py

# 3. Probar API XML-RPC
python tests/test_xmlrpc_api.py
```

## 📊 Resultados Esperados

### Test de Registro Exitoso
```json
{
  "session_id": "abc123xyz..."
}
```

### Test Completo
```
✅ PASS - Datos incompletos (400)
✅ PASS - Contraseña muy corta (417)
✅ PASS - Email inválido (417)
✅ PASS - Registro exitoso (200)
✅ PASS - Email duplicado (417)
✅ PASS - Pasaporte duplicado (417)
```

## ⚙️ Configuración

Los scripts usan por defecto:

```python
# Odoo Enterprise
url = "http://localhost:8070"
db = "odoo_enterprise"
username = "admin"
password = "admin"
```

Para cambiar la configuración, edita las variables al inicio de cada script.

## 🐛 Solución de Problemas

### Error de conexión
```bash
# Verificar que Odoo esté corriendo
docker ps | grep odoo

# Ver logs
docker logs odoo_zublime_enterprise
```

### Error de autenticación
Verifica las credenciales:
- Usuario: `admin`
- Contraseña: `admin`
- Base de datos: `odoo_enterprise`

### Módulos no encontrados
```bash
# Instalar módulos desde la interfaz web
# http://localhost:8070
# Apps > Buscar "zub" > Instalar
```

### Tests fallan
```bash
# Reiniciar Odoo
docker-compose -f docker-compose.enterprise.yml restart

# Esperar 30 segundos y volver a probar
```

## 📝 Estructura de Tests

```
tests/
├── README.md                      # Este archivo
│
├── Endpoint de Registro (Principal)
│   ├── test_register_simple.py    # Test básico
│   ├── test_register_complete.py  # Test completo
│   ├── test_register.html         # Test manual
│   └── test_register.http         # REST Client
│
└── Infraestructura
    ├── test_endpoints_enterprise.py  # Todos los endpoints
    ├── test_xmlrpc_api.py           # API XML-RPC
    └── check_modules_status.py      # Estado de módulos
```

## 🎯 Casos de Uso

### Desarrollo
```bash
# Después de hacer cambios en el endpoint
python tests/test_register_complete.py
```

### CI/CD
```bash
# En pipeline de integración continua
python tests/test_register_complete.py
python tests/test_endpoints_enterprise.py
```

### Debug
```bash
# Test manual con interfaz visual
start tests/test_register.html
```

### Documentación
```bash
# Usar test_register.http como ejemplos
# para documentación de API
```

## 📚 Documentación Relacionada

- **ENDPOINT_REGISTRO.md** - Documentación técnica completa del endpoint
- **RESUMEN_IMPLEMENTACION.md** - Resumen ejecutivo de la implementación
- **ENTERPRISE_SETUP.md** - Guía de configuración de Odoo Enterprise

---

**Ejecuta los tests para verificar que todo funciona correctamente** ✅
