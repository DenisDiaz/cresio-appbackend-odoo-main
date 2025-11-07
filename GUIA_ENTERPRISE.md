# 🚀 Guía Rápida - Odoo 18 Enterprise

## ✅ Estado: INSTALADO Y FUNCIONANDO

Odoo 18 Enterprise está corriendo exitosamente con todos los módulos Enterprise y tus módulos personalizados.

---

## 📍 Acceso al Sistema

- **URL:** http://localhost:8070
- **Puerto PostgreSQL:** 5433
- **Usuario inicial:** admin
- **Contraseña inicial:** admin

---

## 🎯 Diferencias con Community

### Odoo Enterprise incluye:

1. **Módulos Premium:**
   - Studio (personalización visual)
   - Helpdesk
   - Documentos
   - Firma electrónica
   - IoT
   - Contabilidad avanzada
   - Y 400+ módulos más

2. **Mejor soporte para APIs:**
   - Los controladores HTTP personalizados funcionan mejor
   - Mejor integración con sistemas externos
   - Más opciones de autenticación

3. **Rendimiento mejorado:**
   - Optimizaciones de Enterprise
   - Mejor manejo de carga

---

## 📦 Módulos Disponibles

### Módulos Enterprise (400+)
Todos los módulos de Odoo Enterprise están disponibles en `/mnt/enterprise`

### Tus Módulos Personalizados
- ✅ zub_utils
- ✅ zub_supplier_connector
- ✅ zub_onboarding
- ✅ zub_loyalty

---

## 🔧 Primeros Pasos

### 1. Crear Base de Datos

1. Abre http://localhost:8070
2. Haz clic en "Create Database"
3. Completa el formulario:
   - **Database Name:** odoo_enterprise
   - **Email:** admin@example.com
   - **Password:** admin
   - **Language:** Spanish / Español
   - **Country:** Colombia
   - **Demo data:** No (desmarcado)
4. Haz clic en "Create Database"

### 2. Instalar Módulos Personalizados

Una vez creada la base de datos:

1. Ve a **Apps** (Aplicaciones)
2. Quita el filtro "Apps" para ver todos los módulos
3. Busca e instala en este orden:
   - **zub_utils** (primero)
   - **zub_supplier_connector**
   - **zub_onboarding**
   - **zub_loyalty** (opcional)

### 3. Verificar Campo "Conexión Externa"

1. Ve a **Contacts** (Contactos)
2. Crea o edita un contacto
3. Verifica que aparezca el campo **"Conexión Externa"**

---

## 🧪 Probar Endpoints HTTP

Una vez instalados los módulos, prueba los endpoints:

### Endpoint 1: Branch Offices

```bash
curl -X POST http://localhost:8070/api/v1/branch-offices/get-all \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Endpoint 2: Onboarding

```bash
curl -X POST http://localhost:8070/api/v1/on-boarding/get-by-id \
  -H "Content-Type: application/json" \
  -d '{"id": 1}'
```

### Script de Prueba Python

```bash
python test_enterprise.py
```

---

## 🔍 Verificar Módulos Enterprise

Para ver que Enterprise está activo:

1. Ve a **Settings** (Configuración)
2. En la parte superior derecha verás "Enterprise Edition"
3. Puedes activar módulos como:
   - **Studio** - Para personalización visual
   - **Helpdesk** - Sistema de tickets
   - **Documents** - Gestión documental

---

## 📊 Comandos Útiles

### Ver logs en tiempo real
```bash
docker logs -f odoo_zublime_enterprise
```

### Ver logs del archivo
```bash
docker exec odoo_zublime_enterprise tail -f /var/log/odoo/odoo.log
```

### Reiniciar Odoo
```bash
docker-compose -f docker-compose.enterprise.yml restart web
```

### Detener todo
```bash
docker-compose -f docker-compose.enterprise.yml down
```

### Iniciar de nuevo
```bash
docker-compose -f docker-compose.enterprise.yml up -d
```

### Ver contenedores corriendo
```bash
docker ps
```

### Acceder al shell de Odoo
```bash
docker exec -it odoo_zublime_enterprise odoo shell -d odoo_enterprise
```

---

## 🔧 Actualizar Módulos

Si haces cambios en tus módulos personalizados:

```bash
# Opción 1: Actualizar módulo específico
docker exec -it odoo_zublime_enterprise odoo -d odoo_enterprise \
  --db_host=db --db_user=odoo --db_password=odoo \
  -u zub_supplier_connector --stop-after-init

# Opción 2: Reiniciar con auto-reload (ya está activo)
# Los cambios se detectan automáticamente con --dev=all
```

---

## 🐛 Solución de Problemas

### Odoo no inicia

```bash
# Ver logs
docker logs odoo_zublime_enterprise

# Verificar que PostgreSQL esté corriendo
docker ps | grep postgres

# Reiniciar todo
docker-compose -f docker-compose.enterprise.yml restart
```

### Puerto 8070 ocupado

Edita `docker-compose.enterprise.yml` y cambia:
```yaml
ports:
  - "8071:8069"  # Usar puerto 8071 en lugar de 8070
```

### Módulos no aparecen

```bash
# Actualizar lista de módulos
docker exec -it odoo_zublime_enterprise odoo -d odoo_enterprise \
  --db_host=db --db_user=odoo --db_password=odoo \
  --update=all --stop-after-init
```

### Resetear base de datos

```bash
# Detener y eliminar volúmenes
docker-compose -f docker-compose.enterprise.yml down -v

# Iniciar de nuevo
docker-compose -f docker-compose.enterprise.yml up -d
```

---

## 📁 Estructura de Archivos

```
proyecto/
├── enterprise/
│   └── enterprise/          # Módulos Odoo Enterprise (400+)
├── zub_utils/               # Tu módulo de utilidades
├── zub_supplier_connector/  # Tu módulo principal
├── zub_onboarding/          # Tu módulo de onboarding
├── zub_loyalty/             # Tu módulo de lealtad
├── Dockerfile.enterprise    # Dockerfile personalizado
├── docker-compose.enterprise.yml  # Configuración Docker
└── test_enterprise.py       # Script de prueba
```

---

## 🎓 Ventajas de Enterprise para tu Proyecto

1. **Endpoints HTTP más estables:**
   - Mejor manejo de rutas personalizadas
   - Más opciones de autenticación
   - Mejor documentación

2. **Herramientas de desarrollo:**
   - Studio para personalización sin código
   - Mejor debugger
   - Profiler integrado

3. **Módulos útiles para tu app:**
   - **Helpdesk** - Para soporte de usuarios
   - **Documents** - Para gestión de archivos
   - **Sign** - Para firmas electrónicas
   - **IoT** - Para dispositivos conectados

---

## 🔐 Seguridad

### Cambiar contraseña de admin

1. Ve a Settings > Users
2. Edita el usuario admin
3. Cambia la contraseña

### Configurar SSL (Producción)

Para producción, usa un proxy reverso como Nginx con Let's Encrypt.

---

## 📞 Información de Contacto

- **Odoo Enterprise:** http://localhost:8070
- **PostgreSQL:** localhost:5433
- **Logs:** `/var/log/odoo/odoo.log` (dentro del contenedor)

---

## ✅ Checklist de Verificación

- [x] Odoo Enterprise instalado
- [x] PostgreSQL corriendo
- [x] Módulos Enterprise disponibles
- [x] Módulos personalizados copiados
- [x] Puerto 8070 accesible
- [ ] Base de datos creada
- [ ] Módulos personalizados instalados
- [ ] Endpoints HTTP probados

---

## 🚀 Próximos Pasos

1. **Crear base de datos** en http://localhost:8070
2. **Instalar módulos** personalizados
3. **Probar endpoints** HTTP
4. **Verificar** que funcionen correctamente
5. **Desarrollar** tu aplicación móvil

---

**¡Odoo 18 Enterprise está listo para usar!** 🎉

Para cualquier duda, revisa los logs:
```bash
docker logs -f odoo_zublime_enterprise
```
