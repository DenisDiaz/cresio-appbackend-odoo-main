# 📋 Endpoint de Detalle de Farmacia

## 🎯 Endpoint
`POST /api/v1/pharmacy/get-detail`

## 📥 REQUEST JSON

```json
{
  "id": 123,
  "latitude": 4.6097,
  "longitude": -74.0817
}
```

### Parámetros

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `id` | integer | ✅ Sí | ID de la farmacia |
| `latitude` | float | ❌ No | Latitud del usuario (para calcular distancia) |
| `longitude` | float | ❌ No | Longitud del usuario (para calcular distancia) |

## 📤 RESPONSE 200 (Éxito)

```json
{
  "id": 123,
  "nombre": "Farmacia Central",
  "latitude": 4.6097,
  "longitude": -74.0817,
  "telefono": "+57 1 234 5678",
  "web": "https://www.farmacia.com",
  "direccion": "Carrera 7 # 32-16, Bogotá, Cundinamarca, 110111, Colombia",
  "distancia": 2.45,
  "imagenes": [
    {
      "url": "/web/image/res.partner/123/image_1920",
      "type": "principal"
    }
  ],
  "email": "contacto@farmacia.com",
  "horario": ""
}
```

### Campos de Respuesta

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID de la farmacia |
| `nombre` | string | Nombre de la farmacia |
| `latitude` | float | Latitud de la farmacia |
| `longitude` | float | Longitud de la farmacia |
| `telefono` | string | Teléfono de contacto |
| `web` | string | Sitio web |
| `direccion` | string | Dirección completa formateada |
| `distancia` | float | Distancia en kilómetros (si se enviaron coordenadas) |
| `imagenes` | array | Lista de imágenes de la farmacia |
| `email` | string | Email de contacto |
| `horario` | string | Horario de atención (futuro) |

## 📊 HTTP Status Codes

| Código | Descripción | Uso |
|--------|-------------|-----|
| ✅ 200 | Success | Detalle de farmacia obtenido correctamente |
| ✅ 400 | Bad Request | Datos de entrada incompletos o inválidos |
| ✅ 404 | Not Found | Farmacia no encontrada |
| ✅ 500 | Server Error | Error interno del servidor |

## ✅ Validaciones Implementadas

### 1. ID Requerido (400 - Bad Request)
```python
if not pharmacy_id:
    return 400
```

**Ejemplo de respuesta:**
```json
{
  "error": "Datos incompletos",
  "message": "El ID de la farmacia es requerido"
}
```

### 2. ID Numérico (400 - Bad Request)
```python
if not isinstance(pharmacy_id, int):
    return 400
```

**Ejemplo de respuesta:**
```json
{
  "error": "ID inválido",
  "message": "El ID de la farmacia debe ser un número"
}
```

### 3. Latitud Válida (400 - Bad Request)
```python
if latitude and not isinstance(latitude, float):
    return 400
```

**Ejemplo de respuesta:**
```json
{
  "error": "Latitud inválida",
  "message": "La latitud debe ser un número"
}
```

### 4. Longitud Válida (400 - Bad Request)
```python
if longitude and not isinstance(longitude, float):
    return 400
```

**Ejemplo de respuesta:**
```json
{
  "error": "Longitud inválida",
  "message": "La longitud debe ser un número"
}
```

### 5. Farmacia Existe (404 - Not Found)
```python
if not pharmacy.exists():
    return 404
```

**Ejemplo de respuesta:**
```json
{
  "error": "Farmacia no encontrada",
  "message": "No existe una farmacia con el ID proporcionado"
}
```

### 6. Farmacia Disponible (404 - Not Found)
```python
if not pharmacy.is_supplier_with_external_connection:
    return 404
```

**Ejemplo de respuesta:**
```json
{
  "error": "Farmacia no disponible",
  "message": "Esta farmacia no está disponible para consulta"
}
```

## 🔄 Cálculo de Distancia

El endpoint utiliza la **fórmula de Haversine** para calcular la distancia entre dos puntos geográficos:

```python
# Radio de la Tierra en kilómetros
R = 6371.0

# Convertir grados a radianes
lat1 = math.radians(user_latitude)
lon1 = math.radians(user_longitude)
lat2 = math.radians(pharmacy_latitude)
lon2 = math.radians(pharmacy_longitude)

# Fórmula de Haversine
dlat = lat2 - lat1
dlon = lon2 - lon1
a = sin(dlat/2)² + cos(lat1) * cos(lat2) * sin(dlon/2)²
c = 2 * atan2(√a, √(1-a))
distance = R * c
```

**Resultado:** Distancia en kilómetros con 2 decimales

## 🧪 Casos de Prueba

### Test 1: Detalle Exitoso con Coordenadas
```bash
curl -X POST http://localhost:8070/api/v1/pharmacy/get-detail \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "latitude": 4.6097,
    "longitude": -74.0817
  }'
```

**Respuesta esperada (200):**
```json
{
  "id": 1,
  "nombre": "Farmacia Central",
  "latitude": 4.6097,
  "longitude": -74.0817,
  "telefono": "+57 1 234 5678",
  "web": "https://www.farmacia.com",
  "direccion": "Carrera 7 # 32-16, Bogotá",
  "distancia": 0.0,
  "imagenes": [...],
  "email": "contacto@farmacia.com"
}
```

### Test 2: Detalle sin Coordenadas
```bash
curl -X POST http://localhost:8070/api/v1/pharmacy/get-detail \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1
  }'
```

**Respuesta esperada (200):**
```json
{
  "id": 1,
  "nombre": "Farmacia Central",
  "distancia": 0.0,
  ...
}
```

### Test 3: Sin ID
```bash
curl -X POST http://localhost:8070/api/v1/pharmacy/get-detail \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 4.6097,
    "longitude": -74.0817
  }'
```

**Respuesta esperada (400):**
```json
{
  "error": "Datos incompletos",
  "message": "El ID de la farmacia es requerido"
}
```

### Test 4: ID Inválido
```bash
curl -X POST http://localhost:8070/api/v1/pharmacy/get-detail \
  -H "Content-Type: application/json" \
  -d '{
    "id": "abc",
    "latitude": 4.6097,
    "longitude": -74.0817
  }'
```

**Respuesta esperada (400):**
```json
{
  "error": "ID inválido",
  "message": "El ID de la farmacia debe ser un número"
}
```

### Test 5: Farmacia No Encontrada
```bash
curl -X POST http://localhost:8070/api/v1/pharmacy/get-detail \
  -H "Content-Type: application/json" \
  -d '{
    "id": 999999,
    "latitude": 4.6097,
    "longitude": -74.0817
  }'
```

**Respuesta esperada (404):**
```json
{
  "error": "Farmacia no encontrada",
  "message": "No existe una farmacia con el ID proporcionado"
}
```

## 📝 Notas de Implementación

### Dirección Formateada
La dirección se construye concatenando los siguientes campos (si existen):
- `street` - Calle principal
- `street2` - Calle secundaria
- `city` - Ciudad
- `state_id.name` - Estado/Departamento
- `zip` - Código postal
- `country_id.name` - País

Ejemplo: `"Carrera 7 # 32-16, Edificio Central, Bogotá, Cundinamarca, 110111, Colombia"`

### Imágenes
Actualmente solo se devuelve la imagen principal (`image_1920`). En el futuro se pueden agregar más imágenes.

### Horario
El campo `horario` está preparado para futuras implementaciones.

## 🚀 Cómo Probar

### Opción 1: Script Python
```bash
python tests/test_pharmacy_detail.py
```

### Opción 2: Navegador
Abrir `tests/test_pharmacy_detail.html` en el navegador

### Opción 3: REST Client
Usar `tests/test_pharmacy_detail.http` con la extensión REST Client de VS Code

### Opción 4: cURL
```bash
curl -X POST http://localhost:8070/api/v1/pharmacy/get-detail \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "latitude": 4.6097, "longitude": -74.0817}'
```

### Opción 5: PowerShell
```powershell
$body = @{
    id = 1
    latitude = 4.6097
    longitude = -74.0817
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8070/api/v1/pharmacy/get-detail" `
  -Method Post -Body $body -ContentType "application/json"
```

## 🔧 Configuración Requerida

### Crear Farmacia de Prueba

1. Ir a Odoo: http://localhost:8070
2. Contactos > Crear
3. Llenar datos:
   - Nombre: "Farmacia Central"
   - Calle: "Carrera 7 # 32-16"
   - Ciudad: "Bogotá"
   - Teléfono: "+57 1 234 5678"
   - Email: "contacto@farmacia.com"
   - Website: "https://www.farmacia.com"
   - **Conexión Externa: ✅ Activar**
   - Latitud: 4.6097
   - Longitud: -74.0817
4. Guardar

## 📊 Ejemplo Completo

### Request
```json
{
  "id": 1,
  "latitude": 4.6097,
  "longitude": -74.0817
}
```

### Response 200
```json
{
  "id": 1,
  "nombre": "Farmacia Central",
  "latitude": 4.6097,
  "longitude": -74.0817,
  "telefono": "+57 1 234 5678",
  "web": "https://www.farmacia.com",
  "direccion": "Carrera 7 # 32-16, Bogotá, Cundinamarca, 110111, Colombia",
  "distancia": 2.45,
  "imagenes": [
    {
      "url": "/web/image/res.partner/1/image_1920",
      "type": "principal"
    }
  ],
  "email": "contacto@farmacia.com",
  "horario": ""
}
```

## 🐛 Troubleshooting

### Error: Farmacia no encontrada
- Verifica que el ID existe en la base de datos
- Verifica que la farmacia tiene "Conexión Externa" = True

### Distancia siempre 0.0
- Verifica que enviaste latitude y longitude en el request
- Verifica que la farmacia tiene coordenadas configuradas

### Error de conexión
```bash
# Verificar que Odoo esté corriendo
docker ps | grep odoo

# Ver logs
docker logs odoo_zublime_enterprise
```

---

**Estado:** ✅ Implementado y documentado
**Fecha:** 2025-11-07
**Versión:** 1.0
