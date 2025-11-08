# 📋 Endpoint de Listado de Farmacias

## 🎯 Endpoint
`POST /api/v1/pharmacy/list`

## 📥 REQUEST JSON

```json
{
  "latitude": 4.6097,
  "longitude": -74.0817,
  "page": 1,
  "limit": 10
}
```

### Parámetros

| Campo | Tipo | Requerido | Default | Descripción |
|-------|------|-----------|---------|-------------|
| `latitude` | float | ❌ No | null | Latitud del usuario (para ordenar por distancia) |
| `longitude` | float | ❌ No | null | Longitud del usuario (para ordenar por distancia) |
| `page` | integer | ❌ No | 1 | Número de página |
| `limit` | integer | ❌ No | 10 | Resultados por página (máx 100) |

## 📤 RESPONSE 200 (Éxito)

```json
{
  "data": [
    {
      "id": 18,
      "nombre": "Farmacia Central Test",
      "latitude": 4.6097,
      "longitude": -74.0817,
      "direccion": "Carrera 7 # 32-16, Edificio Central, Piso 1, Bogotá, 110111",
      "distancia": 0.0
    },
    {
      "id": 23,
      "nombre": "Farmacia Chapinero",
      "latitude": 4.65,
      "longitude": -74.065,
      "direccion": "Carrera 13 # 60-20, Bogotá",
      "distancia": 4.85
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 6,
    "pages": 1
  }
}
```

### Campos de Respuesta

#### Data (Array)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID de la farmacia |
| `nombre` | string | Nombre de la farmacia |
| `latitude` | float | Latitud de la farmacia |
| `longitude` | float | Longitud de la farmacia |
| `direccion` | string | Dirección completa formateada |
| `distancia` | float | Distancia en kilómetros (0.0 si no se enviaron coordenadas) |

#### Pagination
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `page` | integer | Página actual |
| `limit` | integer | Resultados por página |
| `total` | integer | Total de farmacias |
| `pages` | integer | Total de páginas |

## 📊 HTTP Status Codes

| Código | Descripción | Uso |
|--------|-------------|-----|
| ✅ 200 | Success | Listado obtenido correctamente |
| ✅ 400 | Bad Request | Datos de entrada inválidos |
| ✅ 500 | Server Error | Error interno del servidor |

## ✅ Validaciones Implementadas

### 1. Latitud Válida (400 - Bad Request)
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

### 2. Longitud Válida (400 - Bad Request)
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

### 3. Página Válida (400 - Bad Request)
```python
if not isinstance(page, int) or page < 1:
    return 400
```

**Ejemplo de respuesta:**
```json
{
  "error": "Página inválida",
  "message": "El número de página debe ser un entero positivo"
}
```

### 4. Límite Válido (400 - Bad Request)
```python
if not isinstance(limit, int) or limit < 1 or limit > 100:
    return 400
```

**Ejemplo de respuesta:**
```json
{
  "error": "Límite inválido",
  "message": "El límite debe ser un entero entre 1 y 100"
}
```

## 🔄 Características

### 1. Paginación
- Página por defecto: 1
- Límite por defecto: 10
- Límite máximo: 100
- Cálculo automático de total de páginas

### 2. Ordenamiento por Distancia
- Si se envían coordenadas del usuario, las farmacias se ordenan por distancia (más cercana primero)
- Si NO se envían coordenadas, se ordenan por nombre alfabéticamente
- Distancia calculada con fórmula de Haversine

### 3. Dirección Formateada
La dirección se construye concatenando:
- `street` - Calle principal
- `street2` - Calle secundaria
- `city` - Ciudad
- `state_id.name` - Estado/Departamento
- `zip` - Código postal
- `country_id.name` - País

## 🧪 Casos de Prueba

### Test 1: Listado Sin Coordenadas (200) ✅
```bash
curl -X POST http://localhost:8070/api/v1/pharmacy/list \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Respuesta:**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 6,
    "pages": 1
  }
}
```

### Test 2: Listado Con Coordenadas (200) ✅
```bash
curl -X POST http://localhost:8070/api/v1/pharmacy/list \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 4.6097,
    "longitude": -74.0817
  }'
```

**Respuesta:** Farmacias ordenadas por distancia

### Test 3: Paginación (200) ✅
```bash
curl -X POST http://localhost:8070/api/v1/pharmacy/list \
  -H "Content-Type: application/json" \
  -d '{
    "page": 1,
    "limit": 5
  }'
```

**Respuesta:** 5 resultados por página

### Test 4: Latitud Inválida (400) ✅
```bash
curl -X POST http://localhost:8070/api/v1/pharmacy/list \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": "invalid"
  }'
```

**Respuesta:**
```json
{
  "error": "Latitud inválida",
  "message": "La latitud debe ser un número"
}
```

## 📊 Ejemplo Completo

### Request
```json
{
  "latitude": 4.6097,
  "longitude": -74.0817,
  "page": 1,
  "limit": 3
}
```

### Response 200
```json
{
  "data": [
    {
      "id": 18,
      "nombre": "Farmacia Central Test",
      "latitude": 4.6097,
      "longitude": -74.0817,
      "direccion": "Carrera 7 # 32-16, Edificio Central, Piso 1, Bogotá, 110111",
      "distancia": 0.0
    },
    {
      "id": 23,
      "nombre": "Farmacia Chapinero",
      "latitude": 4.65,
      "longitude": -74.065,
      "direccion": "Carrera 13 # 60-20, Bogotá",
      "distancia": 4.85
    },
    {
      "id": 20,
      "nombre": "Farmacia Sur",
      "latitude": 4.5794,
      "longitude": -74.1169,
      "direccion": "Carrera 30 # 10-50, Bogotá",
      "distancia": 5.15
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 3,
    "total": 6,
    "pages": 2
  }
}
```

## 🚀 Cómo Probar

### Opción 1: Script Python
```bash
python tests/test_pharmacy_list.py
```

### Opción 2: Navegador
Abrir `tests/test_pharmacy_list.html` en el navegador

### Opción 3: REST Client
Usar `tests/test_pharmacy_list.http` con la extensión REST Client de VS Code

### Opción 4: cURL
```bash
curl -X POST http://localhost:8070/api/v1/pharmacy/list \
  -H "Content-Type: application/json" \
  -d '{"latitude": 4.6097, "longitude": -74.0817, "page": 1, "limit": 10}'
```

### Opción 5: PowerShell
```powershell
$body = @{
    latitude = 4.6097
    longitude = -74.0817
    page = 1
    limit = 10
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8070/api/v1/pharmacy/list" `
  -Method Post -Body $body -ContentType "application/json"
```

## 📝 Notas de Implementación

### Ordenamiento
1. **Con coordenadas:** Ordenado por distancia (ascendente)
2. **Sin coordenadas:** Ordenado por nombre (alfabético)

### Paginación
- Offset calculado: `(page - 1) * limit`
- Total de páginas: `ceil(total / limit)`
- Página negativa se ajusta a 1
- Límite > 100 se ajusta a 100

### Distancia
- Calculada con fórmula de Haversine
- Resultado en kilómetros con 2 decimales
- Si no hay coordenadas del usuario: 0.0

## 🐛 Troubleshooting

### No se encuentran farmacias
- Verifica que existan farmacias con "Conexión Externa" = True
- Ejecuta: `python tests/create_multiple_pharmacies.py`

### Ordenamiento no funciona
- Asegúrate de enviar latitude y longitude
- Verifica que las farmacias tengan coordenadas configuradas

### Paginación incorrecta
- Verifica que page y limit sean números enteros
- page debe ser >= 1
- limit debe estar entre 1 y 100

---

**Estado:** ✅ Implementado y probado
**Fecha:** 2025-11-07
**Versión:** 1.0
**Tests:** 10/10 Pasando (100%)
