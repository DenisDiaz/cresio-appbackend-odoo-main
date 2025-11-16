# 🚀 Cómo Probar los Endpoints desde el Navegador

## ✅ Solución al Error de CORS

El error que viste es un problema de **CORS** (Cross-Origin Resource Sharing). Los navegadores bloquean peticiones entre diferentes orígenes por seguridad.

**Solución:** Usar un servidor proxy que hace de intermediario entre el navegador y Odoo.

---

## 🎯 Método 1: Usar el Probador Web (RECOMENDADO)

### Paso 1: Iniciar el servidor proxy
Ejecuta uno de estos comandos:

**Opción A - Archivo .bat:**
```bash
iniciar_probador.bat
```

**Opción B - Python directo:**
```bash
python proxy_server.py
```

### Paso 2: Usar la interfaz
El navegador se abrirá automáticamente en: **http://localhost:8888**

Si no se abre, ve manualmente a: http://localhost:8888

### Paso 3: Probar los endpoints
1. Llena los campos (las coordenadas se auto-completan)
2. Click en "🔍 Probar Endpoint"
3. Ve la respuesta JSON en tiempo real

### Paso 4: Detener el servidor
Presiona `Ctrl+C` en la terminal cuando termines

---

## 📋 Endpoints Disponibles en la Interfaz

### 1. 📋 Listar Farmacias
- **Endpoint:** `/api/v1/pharmacy/list`
- **Parámetros opcionales:**
  - Latitud: 4.6097 (Bogotá)
  - Longitud: -74.0817 (Bogotá)
  - Página: 1
  - Límite: 10

### 2. 🏥 Detalle de Farmacia
- **Endpoint:** `/api/v1/pharmacy/get-detail`
- **Parámetros:**
  - ID: (requerido) - Ejemplo: 18
  - Latitud: (opcional)
  - Longitud: (opcional)

### 3. 🏢 Obtener Sucursales
- **Endpoint:** `/api/v1/branch-offices/get-all`
- Sin parámetros

### 4. 👤 Onboarding
- **Endpoint:** `/api/v1/on-boarding/get-by-id`
- **Parámetros:**
  - ID: 1

---

## 🔧 Método 2: Usar PowerShell (Sin navegador)

Si prefieres la terminal:

```powershell
# Listar farmacias
Invoke-RestMethod -Uri "http://localhost:8070/api/v1/pharmacy/list" `
  -Method Post -ContentType "application/json" -Body '{}'

# Con coordenadas
$body = @{
    latitude = 4.6097
    longitude = -74.0817
    page = 1
    limit = 10
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8070/api/v1/pharmacy/list" `
  -Method Post -ContentType "application/json" -Body $body
```

O ejecuta el script completo:
```powershell
.\probar_endpoints.ps1
```

---

## 🐍 Método 3: Usar Python

```bash
python probar_endpoints.py
```

---

## ❓ Preguntas Frecuentes

### ¿Por qué no puedo abrir directamente el HTML?
Los navegadores modernos bloquean peticiones entre diferentes orígenes (CORS). El archivo HTML local (`file://`) no puede hacer peticiones a `http://localhost:8070`.

### ¿Qué hace el servidor proxy?
El proxy recibe las peticiones del navegador y las reenvía a Odoo, agregando los headers necesarios para evitar el bloqueo de CORS.

### ¿Puedo usar Postman en lugar del navegador?
Sí, Postman no tiene restricciones de CORS. Puedes hacer peticiones directamente a `http://localhost:8070/api/v1/...`

### ¿El puerto 8888 está ocupado?
Si el puerto 8888 está ocupado, edita `proxy_server.py` y cambia:
```python
PORT = 8888  # Cambia a otro puerto, ej: 9000
```

---

## 🎯 Ejemplo de Uso Completo

1. **Iniciar Odoo Enterprise:**
   ```bash
   docker-compose -f docker-compose.enterprise.yml up
   ```

2. **Iniciar el probador:**
   ```bash
   iniciar_probador.bat
   ```

3. **En el navegador (http://localhost:8888):**
   - Ir a "Listar Farmacias"
   - Dejar coordenadas: 4.6097, -74.0817
   - Click en "Probar Endpoint"
   - Ver las 6 farmacias ordenadas por distancia

4. **Probar detalle:**
   - Ir a "Detalle de Farmacia"
   - ID: 18
   - Click en "Probar Endpoint"
   - Ver información completa de la farmacia

---

## 📊 Respuestas Esperadas

### Listar Farmacias (200 OK)
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

### Detalle de Farmacia (200 OK)
```json
{
  "id": 18,
  "nombre": "Farmacia Central Test",
  "telefono": "+57 1 234 5678",
  "email": "contacto@farmaciacentral.com",
  "web": "https://www.farmaciacentral.com",
  "direccion": "Carrera 7 # 32-16, Bogotá",
  "distancia": 0.0
}
```

---

## 🔍 Verificar que Todo Funciona

### 1. Verificar Odoo
```bash
docker ps | findstr odoo
```
Debe mostrar: `odoo_zublime_enterprise` corriendo

### 2. Verificar conexión a Odoo
```powershell
Invoke-WebRequest -Uri "http://localhost:8070" -Method Get
```
Debe retornar código 200 o 303

### 3. Probar endpoint directo
```powershell
.\probar_endpoints.ps1
```
Todos deben mostrar "✓ Status: 200 OK"

---

## 🛠️ Solución de Problemas

### Error: "Failed to fetch"
- Verifica que Odoo esté corriendo: `docker ps`
- Verifica que el proxy esté corriendo en puerto 8888
- Intenta reiniciar el proxy: Ctrl+C y vuelve a ejecutar

### Error: "Puerto ocupado"
- Cambia el puerto en `proxy_server.py`
- O cierra el programa que está usando el puerto 8888

### Error: "Farmacia no encontrada"
- Verifica que existan farmacias en Odoo
- Ve a http://localhost:8070 y crea farmacias de prueba
- Marca "Conexión Externa" = True

---

¡Listo para probar! 🎉

**Comando rápido:**
```bash
iniciar_probador.bat
```

Luego abre: http://localhost:8888
