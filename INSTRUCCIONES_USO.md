# 📖 Instrucciones de Uso - Módulo zub_supplier_connector

## ✅ Estado: COMPLETAMENTE FUNCIONAL

---

## 🎯 Funcionalidad Principal

El módulo `zub_supplier_connector` añade un campo "Conexión Externa" a los contactos de Odoo, permitiendo identificar proveedores mayoristas que tienen conexión con sistemas externos.

---

## 🚀 Inicio Rápido

### 1. Verificar que los módulos estén instalados

```bash
python check_modules_status.py
```

**Resultado esperado:**
```
✓ zub_utils: installed
✓ zub_supplier_connector: installed
✓ zub_onboarding: installed
```

### 2. Ejecutar demo rápida

```bash
python demo_rapido.py
```

### 3. Ejecutar prueba completa

```bash
python test_xmlrpc_api.py
```

---

## 💻 Uso desde la Interfaz Web

### Acceder a Odoo

1. Abrir navegador: `http://localhost:8069`
2. Credenciales:
   - **Usuario:** admin
   - **Contraseña:** admin
   - **Base de datos:** odoo

### Crear/Editar Contacto con Conexión Externa

1. Ir a: **Contactos** (menú principal)
2. Crear nuevo contacto o editar existente
3. Buscar el campo: **"Conexión Externa"** (checkbox)
4. Marcar el checkbox para activar
5. Completar datos adicionales:
   - Nombre
   - Dirección
   - Ciudad
   - Teléfono
   - Email
   - Coordenadas (partner_latitude, partner_longitude)
6. Guardar

### Filtrar Contactos con Conexión Externa

1. En la vista de Contactos
2. Usar el filtro personalizado
3. Buscar por: `Conexión Externa = Sí`

---

## 🔌 Uso desde API (Python)

### Instalación de Dependencias

```bash
pip install xmlrpc
```

### Código de Ejemplo Completo

```python
import xmlrpc.client

# ========================================
# CONFIGURACIÓN
# ========================================
URL = "http://localhost:8069"
DB = "odoo"
USERNAME = "admin"
PASSWORD = "admin"

# ========================================
# AUTENTICACIÓN
# ========================================
common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USERNAME, PASSWORD, {})

if not uid:
    print("Error de autenticación")
    exit(1)

print(f"✓ Autenticado (UID: {uid})")

# ========================================
# API DE MODELOS
# ========================================
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

# ========================================
# EJEMPLO 1: CREAR SUCURSAL
# ========================================
nueva_sucursal = {
    "name": "Mi Sucursal",
    "street": "Calle Principal 123",
    "city": "Bogotá",
    "phone": "+57 1 234 5678",
    "email": "sucursal@empresa.com",
    "is_supplier_with_external_connection": True,
    "partner_latitude": 4.6097,
    "partner_longitude": -74.0817,
}

sucursal_id = models.execute_kw(DB, uid, PASSWORD,
    'res.partner', 'create', [nueva_sucursal])

print(f"✓ Sucursal creada con ID: {sucursal_id}")

# ========================================
# EJEMPLO 2: BUSCAR SUCURSALES
# ========================================
sucursales = models.execute_kw(DB, uid, PASSWORD,
    'res.partner', 'search_read',
    [[['is_supplier_with_external_connection', '=', True]]],
    {'fields': [
        'name', 'street', 'city', 'phone', 'email',
        'partner_latitude', 'partner_longitude'
    ]})

print(f"\n✓ Sucursales encontradas: {len(sucursales)}")

for sucursal in sucursales:
    print(f"\n  • {sucursal['name']}")
    print(f"    Ciudad: {sucursal['city']}")
    print(f"    Teléfono: {sucursal['phone']}")
    if sucursal['partner_latitude'] and sucursal['partner_longitude']:
        print(f"    Coordenadas: ({sucursal['partner_latitude']}, {sucursal['partner_longitude']})")

# ========================================
# EJEMPLO 3: ACTUALIZAR SUCURSAL
# ========================================
models.execute_kw(DB, uid, PASSWORD,
    'res.partner', 'write',
    [[sucursal_id], {
        'phone': '+57 1 999 8888',
        'email': 'nueva@empresa.com'
    }])

print(f"\n✓ Sucursal {sucursal_id} actualizada")

# ========================================
# EJEMPLO 4: ELIMINAR SUCURSAL
# ========================================
models.execute_kw(DB, uid, PASSWORD,
    'res.partner', 'unlink', [[sucursal_id]])

print(f"✓ Sucursal {sucursal_id} eliminada")
```

---

## 📱 Integración con Aplicación Móvil

### Flujo Recomendado

```
1. App Móvil → Autenticación → Odoo XML-RPC
2. App Móvil → Solicitar Sucursales → Odoo
3. Odoo → Buscar contactos con conexión externa → PostgreSQL
4. Odoo → Retornar JSON → App Móvil
5. App Móvil → Mostrar en mapa/lista
```

### Ejemplo de Integración (Pseudocódigo)

```javascript
// En tu app móvil (React Native, Flutter, etc.)

async function obtenerSucursales() {
  // 1. Autenticar
  const uid = await authenticate('odoo', 'admin', 'admin');
  
  // 2. Obtener sucursales
  const sucursales = await searchRead(
    'res.partner',
    [['is_supplier_with_external_connection', '=', true]],
    ['name', 'city', 'phone', 'partner_latitude', 'partner_longitude']
  );
  
  // 3. Mostrar en mapa
  sucursales.forEach(sucursal => {
    agregarMarcadorEnMapa({
      lat: sucursal.partner_latitude,
      lng: sucursal.partner_longitude,
      titulo: sucursal.name,
      descripcion: sucursal.city
    });
  });
}
```

---

## 🔍 Campos Disponibles

### Campo Principal

| Campo Técnico | Etiqueta | Tipo | Descripción |
|---------------|----------|------|-------------|
| `is_supplier_with_external_connection` | Conexión Externa | Boolean | Indica si el proveedor tiene conexión externa |

### Campos Relacionados (heredados de res.partner)

| Campo | Descripción |
|-------|-------------|
| `name` | Nombre del contacto/sucursal |
| `street` | Dirección línea 1 |
| `street2` | Dirección línea 2 |
| `city` | Ciudad |
| `state_id` | Estado/Departamento |
| `zip` | Código postal |
| `country_id` | País |
| `phone` | Teléfono fijo |
| `mobile` | Teléfono móvil |
| `email` | Correo electrónico |
| `website` | Sitio web |
| `partner_latitude` | Latitud (coordenadas GPS) |
| `partner_longitude` | Longitud (coordenadas GPS) |
| `image_1920` | Imagen del contacto |

---

## 🛠️ Operaciones CRUD

### CREATE (Crear)

```python
partner_id = models.execute_kw(db, uid, password,
    'res.partner', 'create', [{
        "name": "Nueva Sucursal",
        "is_supplier_with_external_connection": True,
        # ... otros campos
    }])
```

### READ (Leer)

```python
# Buscar y leer
partners = models.execute_kw(db, uid, password,
    'res.partner', 'search_read',
    [[['is_supplier_with_external_connection', '=', True]]],
    {'fields': ['name', 'city']})

# Solo leer (si ya tienes el ID)
partner = models.execute_kw(db, uid, password,
    'res.partner', 'read',
    [[partner_id]], {'fields': ['name', 'city']})
```

### UPDATE (Actualizar)

```python
models.execute_kw(db, uid, password,
    'res.partner', 'write',
    [[partner_id], {
        'phone': '+57 1 999 8888',
        'is_supplier_with_external_connection': False
    }])
```

### DELETE (Eliminar)

```python
models.execute_kw(db, uid, password,
    'res.partner', 'unlink', [[partner_id]])
```

---

## 📊 Consultas Avanzadas

### Buscar por Ciudad

```python
partners = models.execute_kw(db, uid, password,
    'res.partner', 'search_read',
    [[
        ('is_supplier_with_external_connection', '=', True),
        ('city', '=', 'Bogotá')
    ]],
    {'fields': ['name', 'phone']})
```

### Buscar por Coordenadas (Rango)

```python
# Buscar sucursales cerca de una ubicación
partners = models.execute_kw(db, uid, password,
    'res.partner', 'search_read',
    [[
        ('is_supplier_with_external_connection', '=', True),
        ('partner_latitude', '>=', 4.5),
        ('partner_latitude', '<=', 4.7),
        ('partner_longitude', '>=', -74.2),
        ('partner_longitude', '<=', -74.0)
    ]],
    {'fields': ['name', 'city', 'partner_latitude', 'partner_longitude']})
```

### Contar Sucursales

```python
count = models.execute_kw(db, uid, password,
    'res.partner', 'search_count',
    [[['is_supplier_with_external_connection', '=', True]]])

print(f"Total de sucursales: {count}")
```

---

## 🐛 Solución de Problemas

### Error: "No module named 'xmlrpc'"

```bash
pip install xmlrpc
```

### Error: "Authentication failed"

Verificar credenciales:
- Usuario: admin
- Contraseña: admin
- Base de datos: odoo

### Error: "Connection refused"

Verificar que Odoo esté corriendo:
```bash
docker ps
# Debe mostrar odoo_zublime en estado "Up"
```

Si no está corriendo:
```bash
docker start odoo_zublime
```

### Campo no aparece en la interfaz

1. Verificar que el módulo esté instalado:
   ```bash
   python check_modules_status.py
   ```

2. Si no está instalado:
   ```bash
   docker exec -it odoo_zublime odoo -d odoo --db_host=db --db_user=odoo --db_password=odoo -i zub_supplier_connector --stop-after-init
   ```

3. Refrescar el navegador (Ctrl+F5)

---

## 📚 Recursos Adicionales

### Scripts de Prueba

- `test_complete.py` - Suite completa de pruebas
- `test_xmlrpc_api.py` - Prueba detallada de API
- `demo_rapido.py` - Demo rápida
- `check_modules_status.py` - Verificar estado de módulos

### Documentación

- `RESUMEN_FINAL.md` - Resumen completo de funcionalidad
- `RESULTADOS_PRUEBAS.md` - Resultados detallados de pruebas

### Acceso al Sistema

- **URL:** http://localhost:8069
- **Usuario:** admin
- **Contraseña:** admin
- **Base de datos:** odoo

---

## ✅ Checklist de Verificación

Antes de usar en producción, verificar:

- [ ] Módulos instalados correctamente
- [ ] Campo visible en interfaz web
- [ ] API XML-RPC funcional
- [ ] Crear contacto con conexión externa
- [ ] Buscar contactos con conexión externa
- [ ] Actualizar contacto
- [ ] Eliminar contacto
- [ ] Coordenadas GPS guardadas correctamente

---

## 🎓 Mejores Prácticas

1. **Siempre autenticar** antes de hacer operaciones
2. **Manejar errores** en las llamadas a la API
3. **Validar datos** antes de crear/actualizar
4. **Usar campos específicos** en las búsquedas para mejor rendimiento
5. **Cerrar conexiones** después de usarlas
6. **Cachear resultados** cuando sea posible
7. **Usar límites** en búsquedas grandes

---

**¿Necesitas ayuda?** Ejecuta los scripts de prueba para ver ejemplos funcionales.

**Última actualización:** 2025-11-07
