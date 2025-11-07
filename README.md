# 🚀 Cresio - Backend Odoo 18 Enterprise

Backend API para aplicación móvil construido con Odoo 18 Enterprise.

## 📋 Descripción

Sistema backend basado en Odoo 18 Enterprise que proporciona APIs REST y XML-RPC para gestionar sucursales, onboarding de usuarios y programa de lealtad.

## ✨ Características

- ✅ **Odoo 18 Enterprise** con todos los módulos premium
- ✅ **APIs REST** funcionando correctamente
- ✅ **API XML-RPC** para integraciones
- ✅ **Módulos personalizados** instalados y configurados
- ✅ **Docker** para fácil despliegue
- ✅ **PostgreSQL 15** como base de datos

## 🏗️ Arquitectura

```
├── enterprise/              # Módulos Odoo Enterprise (no incluido en repo)
├── zub_utils/              # Utilidades compartidas
├── zub_supplier_connector/ # Gestión de sucursales con conexión externa
├── zub_onboarding/         # Sistema de onboarding
├── zub_loyalty/            # Programa de lealtad
├── tests/                  # Scripts de prueba
├── docker-compose.yml      # Configuración Docker Community
├── docker-compose.enterprise.yml  # Configuración Docker Enterprise
└── README.md               # Este archivo
```

## 🚀 Inicio Rápido

### Requisitos Previos

- Docker Desktop instalado
- Git
- Código de Odoo Enterprise (para versión Enterprise)

### Instalación con Enterprise

#### Windows
```bash
setup_enterprise.bat
```

#### Linux/Mac
```bash
chmod +x setup_enterprise.sh
./setup_enterprise.sh
```

### Instalación con Community

```bash
docker-compose up -d
```

## 🌐 Acceso

### Odoo Enterprise
- **URL:** http://localhost:8070
- **Usuario:** admin
- **Contraseña:** admin
- **Base de datos:** odoo_enterprise

### Odoo Community
- **URL:** http://localhost:8069
- **Usuario:** admin
- **Contraseña:** admin

## 📦 Módulos Personalizados

### zub_utils
Módulo de utilidades compartidas que proporciona funciones helper para respuestas HTTP y otras utilidades comunes.

### zub_supplier_connector
Gestión de sucursales con conexión externa. Incluye:
- Campo "Conexión Externa" en contactos
- API REST para obtener sucursales
- Filtrado por geolocalización

**Endpoint:** `POST /api/v1/branch-offices/get-all`

### zub_onboarding
Sistema de onboarding para nuevos usuarios.

**Endpoint:** `POST /api/v1/on-boarding/get-by-id`

### zub_loyalty
Programa de lealtad y recompensas para clientes.

## 🔌 APIs Disponibles

### REST API

#### Obtener Sucursales
```bash
curl -X POST http://localhost:8070/api/v1/branch-offices/get-all \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Respuesta:**
```json
{
  "data": [
    {
      "name": "Sucursal Centro",
      "street": "Carrera 7 # 32-16",
      "city": "Bogotá",
      "phone": "+57 1 234 5678",
      "email": "centro@empresa.com",
      "partner_latitude": 4.6097,
      "partner_longitude": -74.0817
    }
  ],
  "http_status": 200
}
```

### XML-RPC API

```python
import xmlrpc.client

# Autenticación
common = xmlrpc.client.ServerProxy('http://localhost:8070/xmlrpc/2/common')
uid = common.authenticate('odoo_enterprise', 'admin', 'admin', {})

# API
models = xmlrpc.client.ServerProxy('http://localhost:8070/xmlrpc/2/object')

# Obtener sucursales
sucursales = models.execute_kw('odoo_enterprise', uid, 'admin',
    'res.partner', 'search_read',
    [[['is_supplier_with_external_connection', '=', True]]],
    {'fields': ['name', 'city', 'phone', 'partner_latitude', 'partner_longitude']})
```

## 🧪 Pruebas

Los scripts de prueba están en la carpeta `tests/`:

```bash
# Probar endpoints Enterprise
python tests/test_endpoints_enterprise.py

# Probar API XML-RPC
python tests/test_xmlrpc_api.py

# Verificar módulos instalados
python tests/check_modules_status.py
```

## 📚 Documentación

- **[GUIA_ENTERPRISE.md](GUIA_ENTERPRISE.md)** - Guía completa de Odoo Enterprise
- **[README_DOCKER.md](README_DOCKER.md)** - Documentación de Docker

## 🛠️ Comandos Útiles

### Ver logs
```bash
docker logs -f odoo_zublime_enterprise
```

### Reiniciar Odoo
```bash
docker-compose -f docker-compose.enterprise.yml restart
```

### Detener todo
```bash
docker-compose -f docker-compose.enterprise.yml down
```

### Actualizar módulo
```bash
docker exec -it odoo_zublime_enterprise odoo -d odoo_enterprise \
  --db_host=db --db_user=odoo --db_password=odoo \
  -u zub_supplier_connector --stop-after-init
```

## 🔧 Configuración

### Variables de Entorno

Edita `docker-compose.enterprise.yml`:

```yaml
environment:
  - HOST=db
  - USER=odoo
  - PASSWORD=odoo
  - POSTGRES_DB=postgres
```

### Puertos

- **8070** - Odoo Enterprise
- **5433** - PostgreSQL Enterprise
- **8069** - Odoo Community (si usas Community)
- **5432** - PostgreSQL Community

## 📊 Estado del Proyecto

| Componente | Estado |
|------------|--------|
| Odoo 18 Enterprise | ✅ Funcionando |
| PostgreSQL 15 | ✅ Funcionando |
| Módulos personalizados | ✅ Instalados |
| Endpoints HTTP REST | ✅ 200 OK |
| API XML-RPC | ✅ Funcional |

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Notas

### Odoo Enterprise
El código de Odoo Enterprise NO está incluido en este repositorio por razones de licencia. Debes obtenerlo de:
- Tu suscripción de Odoo
- GitHub (si tienes acceso al repositorio privado)

Coloca el código en: `enterprise/enterprise/`

### Alternativa Community
Si no tienes Enterprise, puedes usar Odoo Community que es gratuito y open source. La mayoría de funcionalidades funcionan igual, excepto algunos módulos premium.

## 🐛 Solución de Problemas

### Odoo no inicia
```bash
docker logs odoo_zublime_enterprise
docker-compose -f docker-compose.enterprise.yml restart
```

### Puerto ocupado
Edita el puerto en `docker-compose.enterprise.yml`

### Módulos no aparecen
Actualiza la lista de módulos desde Apps > Update Apps List

## 📞 Soporte

Para problemas o preguntas:
- Revisa la documentación en `GUIA_ENTERPRISE.md`
- Ejecuta los scripts de prueba en `tests/`
- Revisa los logs de Docker

## 📄 Licencia

Este proyecto usa Odoo que está bajo licencia LGPL-3.0.
Los módulos personalizados están bajo la misma licencia.

---

**Desarrollado para Cresio** 🚀
