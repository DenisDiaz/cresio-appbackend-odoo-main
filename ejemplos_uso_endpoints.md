# 🚀 Guía de Uso de Endpoints REST

## 📋 Endpoints Disponibles

1. **POST** `/api/v1/branch-offices/get-all` - Obtener todas las sucursales
2. **POST** `/api/v1/on-boarding/get-by-id` - Obtener onboarding por ID
3. **POST** `/api/v1/pharmacy/list` - Listar farmacias con paginación
4. **POST** `/api/v1/pharmacy/get-detail` - Detalle de farmacia

---

## 🔧 Método 1: Usando cURL (Terminal)

### Obtener todas las sucursales
```bash
curl -X POST http://localhost:8070/api/v1/branch-offices/get-all \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Obtener onboarding por ID
```bash
curl -X POST http://localhost:8070/api/v1/on-boarding/get-by-id \
  -H "Content-Type: application/json" \
  -d '{"id": 1}'
```

### Listar farmacias (sin coordenadas)
```bash
curl -X POST http://localhost:8070/api/v1/pharmacy/list \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Listar farmacias (con coordenadas y paginación)
```bash
curl -X POST http://localhost:8070/api/v1/pharmacy/list \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 4.6097,
    "longitude": -74.0817,
    "page": 1,
    "limit": 10
  }'
```

### Detalle de farmacia
```bash
curl -X POST http://localhost:8070/api/v1/pharmacy/get-detail \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "latitude": 4.6097,
    "longitude": -74.0817
  }'
```

---

## 💻 Método 2: Usando PowerShell (Windows)

### Obtener todas las sucursales
```powershell
$response = Invoke-RestMethod -Uri "http://localhost:8070/api/v1/branch-offices/get-all" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{}'

$response | ConvertTo-Json -Depth 10
```

### Listar farmacias con coordenadas
```powershell
$body = @{
    latitude = 4.6097
    longitude = -74.0817
    page = 1
    limit = 10
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8070/api/v1/pharmacy/list" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body

$response | ConvertTo-Json -Depth 10
```

### Detalle de farmacia
```powershell
$body = @{
    id = 1
    latitude = 4.6097
    longitude = -74.0817
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8070/api/v1/pharmacy/get-detail" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body

$response | ConvertTo-Json -Depth 10
```

---

## 🐍 Método 3: Usando Python

### Script completo
```python
import requests
import json

# URL base
BASE_URL = "http://localhost:8070"

# 1. Obtener todas las sucursales
print("1. Obteniendo sucursales...")
response = requests.post(
    f"{BASE_URL}/api/v1/branch-offices/get-all",
    headers={'Content-Type': 'application/json'},
    json={}
)
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))

# 2. Listar farmacias con coordenadas
print("\n2. Listando farmacias...")
response = requests.post(
    f"{BASE_URL}/api/v1/pharmacy/list",
    headers={'Content-Type': 'application/json'},
    json={
        "latitude": 4.6097,
        "longitude": -74.0817,
        "page": 1,
        "limit": 10
    }
)
print(f"Status: {response.status_code}")
data = response.json()
print(f"Total farmacias: {data['pagination']['total']}")
for pharmacy in data['data']:
    print(f"  - {pharmacy['nombre']} ({pharmacy['distancia']} km)")

# 3. Detalle de farmacia
print("\n3. Obteniendo detalle de farmacia...")
response = requests.post(
    f"{BASE_URL}/api/v1/pharmacy/get-detail",
    headers={'Content-Type': 'application/json'},
    json={
        "id": 1,
        "latitude": 4.6097,
        "longitude": -74.0817
    }
)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    pharmacy = response.json()
    print(f"Nombre: {pharmacy['nombre']}")
    print(f"Dirección: {pharmacy['direccion']}")
    print(f"Teléfono: {pharmacy['telefono']}")
    print(f"Distancia: {pharmacy['distancia']} km")
```

---

## 🌐 Método 4: Usando JavaScript (Navegador o Node.js)

### Fetch API (Navegador)
```javascript
// 1. Obtener sucursales
fetch('http://localhost:8070/api/v1/branch-offices/get-all', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({})
})
.then(response => response.json())
.then(data => {
  console.log('Sucursales:', data);
})
.catch(error => console.error('Error:', error));

// 2. Listar farmacias
fetch('http://localhost:8070/api/v1/pharmacy/list', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    latitude: 4.6097,
    longitude: -74.0817,
    page: 1,
    limit: 10
  })
})
.then(response => response.json())
.then(data => {
  console.log('Farmacias:', data.data);
  console.log('Total:', data.pagination.total);
})
.catch(error => console.error('Error:', error));

// 3. Detalle de farmacia
fetch('http://localhost:8070/api/v1/pharmacy/get-detail', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    id: 1,
    latitude: 4.6097,
    longitude: -74.0817
  })
})
.then(response => response.json())
.then(pharmacy => {
  console.log('Farmacia:', pharmacy.nombre);
  console.log('Dirección:', pharmacy.direccion);
  console.log('Distancia:', pharmacy.distancia, 'km');
})
.catch(error => console.error('Error:', error));
```

### Axios (Node.js)
```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8070';

// 1. Obtener sucursales
async function getSucursales() {
  try {
    const response = await axios.post(
      `${BASE_URL}/api/v1/branch-offices/get-all`,
      {},
      { headers: { 'Content-Type': 'application/json' } }
    );
    console.log('Sucursales:', response.data);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// 2. Listar farmacias
async function listarFarmacias() {
  try {
    const response = await axios.post(
      `${BASE_URL}/api/v1/pharmacy/list`,
      {
        latitude: 4.6097,
        longitude: -74.0817,
        page: 1,
        limit: 10
      },
      { headers: { 'Content-Type': 'application/json' } }
    );
    console.log('Farmacias:', response.data);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// 3. Detalle de farmacia
async function detalleFarmacia(id) {
  try {
    const response = await axios.post(
      `${BASE_URL}/api/v1/pharmacy/get-detail`,
      {
        id: id,
        latitude: 4.6097,
        longitude: -74.0817
      },
      { headers: { 'Content-Type': 'application/json' } }
    );
    console.log('Detalle:', response.data);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// Ejecutar
getSucursales();
listarFarmacias();
detalleFarmacia(1);
```

---

## 📱 Método 5: Usando Postman

1. Abre Postman
2. Crea una nueva request
3. Configura:
   - **Método:** POST
   - **URL:** `http://localhost:8070/api/v1/pharmacy/list`
   - **Headers:** 
     - Key: `Content-Type`
     - Value: `application/json`
   - **Body:** Selecciona "raw" y "JSON"
   ```json
   {
     "latitude": 4.6097,
     "longitude": -74.0817,
     "page": 1,
     "limit": 10
   }
   ```
4. Click en "Send"

---

## 🧪 Método 6: Usando el HTML Tester (Ya incluido)

Abre en tu navegador:
```
file:///C:/Users/ALIENWARE/Desktop/FREELANCER/Colombia/cresio-appbackend-odoo-main/api_tester.html
```

O ejecuta:
```bash
abrir_tester.bat
```

---

## 📊 Respuestas Esperadas

### Sucursales (200 OK)
```json
{
  "data": [
    {
      "name": "Farmacia Central",
      "street": "Carrera 7 # 32-16",
      "city": "Bogotá",
      "phone": "+57 1 234 5678",
      "email": "contacto@farmacia.com",
      "partner_latitude": 4.6097,
      "partner_longitude": -74.0817
    }
  ],
  "http_status": 200
}
```

### Farmacias con Paginación (200 OK)
```json
{
  "data": [
    {
      "id": 1,
      "nombre": "Farmacia Central",
      "latitude": 4.6097,
      "longitude": -74.0817,
      "direccion": "Carrera 7 # 32-16, Bogotá",
      "distancia": 0.0
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 5,
    "pages": 1
  }
}
```

### Detalle de Farmacia (200 OK)
```json
{
  "id": 1,
  "nombre": "Farmacia Central",
  "latitude": 4.6097,
  "longitude": -74.0817,
  "telefono": "+57 1 234 5678",
  "web": "https://www.farmacia.com",
  "direccion": "Carrera 7 # 32-16, Bogotá",
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

---

## ⚠️ Códigos de Error

| Código | Descripción | Solución |
|--------|-------------|----------|
| 400 | Bad Request | Verifica los parámetros enviados |
| 404 | Not Found | El recurso no existe o endpoint incorrecto |
| 500 | Server Error | Revisa los logs de Odoo |

---

## 🔍 Verificar que Odoo está corriendo

```bash
# Ver contenedores activos
docker ps

# Ver logs de Odoo
docker logs odoo_zublime_enterprise

# Probar conexión
curl http://localhost:8070
```

---

## 📝 Notas Importantes

1. **Puerto:** El servidor corre en `http://localhost:8070` (Enterprise)
2. **Método:** Todos los endpoints usan **POST**
3. **Content-Type:** Siempre debe ser `application/json`
4. **Coordenadas:** Son opcionales pero recomendadas para calcular distancias
5. **Paginación:** Por defecto page=1, limit=10

---

¡Listo para usar! 🚀
