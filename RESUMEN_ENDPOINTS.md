# 🎯 Resumen Rápido - Cómo Usar los Endpoints

## ✅ Estado Actual
- ✅ Odoo Enterprise corriendo en http://localhost:8070
- ✅ 6 farmacias de prueba disponibles
- ✅ Todos los endpoints funcionando correctamente

---

## 🚀 Forma Más Rápida de Probar

### Opción 1: PowerShell (Recomendado para Windows)
```powershell
.\probar_endpoints.ps1
```

### Opción 2: Python
```bash
python probar_endpoints.py
```

### Opción 3: HTML Tester
```bash
abrir_tester.bat
```

---

## 📋 Endpoints Disponibles

### 1️⃣ Listar Farmacias
**URL:** `POST http://localhost:8070/api/v1/pharmacy/list`

**Ejemplo simple (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://localhost:8070/api/v1/pharmacy/list" `
  -Method Post -ContentType "application/json" -Body '{}'
```

**Con coordenadas:**
```powershell
$body = @{
    latitude = 4.6097
    longitude = -74.0817
    page = 1
    limit = 10
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8070/api/v1/pharmacy/list" `
  -Method Post -ContentType "application/json" -Body $body
```

**Respuesta:**
```json
{
  "data": [
    {
      "id": 18,
      "nombre": "Farmacia Central Test",
      "latitude": 4.6097,
      "longitude": -74.0817,
      "direccion": "Carrera 7 # 32-16, Bogotá",
      "distancia": 0.0
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

---

### 2️⃣ Detalle de Farmacia
**URL:** `POST http://localhost:8070/api/v1/pharmacy/get-detail`

**Ejemplo (PowerShell):**
```powershell
$body = @{
    id = 18
    latitude = 4.6097
    longitude = -74.0817
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8070/api/v1/pharmacy/get-detail" `
  -Method Post -ContentType "application/json" -Body $body
```

**Respuesta:**
```json
{
  "id": 18,
  "nombre": "Farmacia Central Test",
  "latitude": 4.6097,
  "longitude": -74.0817,
  "telefono": "+57 1 234 5678",
  "web": "https://www.farmaciacentral.com",
  "direccion": "Carrera 7 # 32-16, Bogotá",
  "distancia": 0.0,
  "email": "contacto@farmaciacentral.com",
  "imagenes": []
}
```

---

### 3️⃣ Obtener Sucursales (Legacy)
**URL:** `POST http://localhost:8070/api/v1/branch-offices/get-all`

**Ejemplo (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://localhost:8070/api/v1/branch-offices/get-all" `
  -Method Post -ContentType "application/json" -Body '{}'
```

---

### 4️⃣ Onboarding
**URL:** `POST http://localhost:8070/api/v1/on-boarding/get-by-id`

**Ejemplo (PowerShell):**
```powershell
$body = @{ id = 1 } | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8070/api/v1/on-boarding/get-by-id" `
  -Method Post -ContentType "application/json" -Body $body
```

---

## 🔧 Ejemplos con cURL

### Listar farmacias
```bash
curl -X POST http://localhost:8070/api/v1/pharmacy/list \
  -H "Content-Type: application/json" \
  -d '{"latitude": 4.6097, "longitude": -74.0817, "page": 1, "limit": 10}'
```

### Detalle de farmacia
```bash
curl -X POST http://localhost:8070/api/v1/pharmacy/get-detail \
  -H "Content-Type: application/json" \
  -d '{"id": 18, "latitude": 4.6097, "longitude": -74.0817}'
```

---

## 🐍 Ejemplo Python Completo

```python
import requests

BASE_URL = "http://localhost:8070"

# Listar farmacias
response = requests.post(
    f"{BASE_URL}/api/v1/pharmacy/list",
    json={
        "latitude": 4.6097,
        "longitude": -74.0817,
        "page": 1,
        "limit": 10
    }
)

data = response.json()
print(f"Total farmacias: {data['pagination']['total']}")

for pharmacy in data['data']:
    print(f"{pharmacy['nombre']}: {pharmacy['distancia']} km")
```

---

## 🌐 Ejemplo JavaScript (Fetch)

```javascript
// Listar farmacias
fetch('http://localhost:8070/api/v1/pharmacy/list', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    latitude: 4.6097,
    longitude: -74.0817,
    page: 1,
    limit: 10
  })
})
.then(res => res.json())
.then(data => {
  console.log('Total:', data.pagination.total);
  data.data.forEach(pharmacy => {
    console.log(`${pharmacy.nombre}: ${pharmacy.distancia} km`);
  });
});
```

---

## 📊 Parámetros Importantes

### Listar Farmacias
| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| latitude | float | No | null | Latitud del usuario |
| longitude | float | No | null | Longitud del usuario |
| page | int | No | 1 | Número de página |
| limit | int | No | 10 | Resultados por página (máx 100) |

### Detalle de Farmacia
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| id | int | **Sí** | ID de la farmacia |
| latitude | float | No | Latitud del usuario |
| longitude | float | No | Longitud del usuario |

---

## ⚡ Prueba Rápida en Una Línea

**PowerShell:**
```powershell
(Invoke-RestMethod -Uri "http://localhost:8070/api/v1/pharmacy/list" -Method Post -ContentType "application/json" -Body '{}').data | Select-Object nombre, direccion
```

**Python:**
```bash
python -c "import requests; print(requests.post('http://localhost:8070/api/v1/pharmacy/list', json={}).json()['pagination']['total'], 'farmacias')"
```

---

## 🎯 Casos de Uso Comunes

### 1. Buscar farmacias cercanas
```powershell
$body = @{
    latitude = 4.6097
    longitude = -74.0817
    limit = 5
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8070/api/v1/pharmacy/list" `
  -Method Post -ContentType "application/json" -Body $body
```

### 2. Obtener todas las farmacias (sin ordenar por distancia)
```powershell
Invoke-RestMethod -Uri "http://localhost:8070/api/v1/pharmacy/list" `
  -Method Post -ContentType "application/json" -Body '{}'
```

### 3. Paginación
```powershell
$body = @{
    page = 2
    limit = 3
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8070/api/v1/pharmacy/list" `
  -Method Post -ContentType "application/json" -Body $body
```

---

## 📁 Archivos Útiles

- `ejemplos_uso_endpoints.md` - Guía completa con todos los métodos
- `probar_endpoints.ps1` - Script de prueba PowerShell
- `probar_endpoints.py` - Script de prueba Python
- `api_tester.html` - Interfaz web para probar
- `abrir_tester.bat` - Abre el tester HTML

---

## 🔍 Verificar Estado del Servidor

```powershell
# Ver si está corriendo
docker ps | Select-String "odoo"

# Ver logs
docker logs odoo_zublime_enterprise --tail 50

# Probar conexión
Invoke-WebRequest -Uri "http://localhost:8070" -Method Get
```

---

## 📞 Soporte

Si tienes problemas:
1. Verifica que Docker esté corriendo
2. Verifica que Odoo esté en http://localhost:8070
3. Revisa los logs: `docker logs odoo_zublime_enterprise`
4. Ejecuta el script de prueba: `.\probar_endpoints.ps1`

---

¡Todo listo para usar! 🚀
