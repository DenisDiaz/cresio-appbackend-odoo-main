# Cómo usar Odoo 18 Enterprise con Docker

## Requisitos
- Tener una licencia/suscripción de Odoo Enterprise
- Acceso al código fuente de Odoo Enterprise

## Pasos:

### 1. Descargar Odoo Enterprise
Tienes dos opciones:

**Opción A: Desde tu cuenta de Odoo.com**
1. Ve a https://www.odoo.com/my/home
2. Descarga Odoo Enterprise 18.0
3. Extrae el archivo en una carpeta llamada `enterprise` en este directorio

**Opción B: Desde GitHub (si tienes acceso)**
```bash
git clone --depth 1 --branch 18.0 https://github.com/odoo/enterprise.git enterprise
```

### 2. Estructura de carpetas
Tu proyecto debería verse así:
```
cresio-appbackend-odoo-main/
├── enterprise/              # Módulos Enterprise
├── zub_onboarding/          # Tus módulos
├── zub_supplier_connector/
├── zub_loyalty/
├── zub_utils/
├── docker-compose.yml
└── Dockerfile
```

### 3. Modificar docker-compose.yml
Agrega el volumen de enterprise:

```yaml
services:
  web:
    volumes:
      - ./enterprise:/mnt/enterprise
    environment:
      - ADDONS_PATH=/mnt/extra-addons,/mnt/enterprise
```

### 4. Iniciar con Enterprise
```bash
docker-compose down -v
docker-compose up -d
```

### 5. Activar Enterprise
1. Crea una nueva base de datos
2. Ve a Settings > Activate Enterprise
3. Ingresa tu código de suscripción

## Alternativa: Usar solo Community
Si no tienes licencia Enterprise, la versión Community es suficiente para:
- Desarrollar módulos personalizados
- Usar APIs REST
- Todas las funcionalidades básicas de Odoo

Los módulos `zub_*` funcionan perfectamente con Community.

## Diferencias Community vs Enterprise
**Community (Gratis):**
- Ventas, CRM, Inventario, Contabilidad básica
- Desarrollo de módulos personalizados
- APIs y integraciones

**Enterprise (De pago):**
- Módulos adicionales (Studio, IoT, Firma electrónica, etc.)
- Soporte oficial de Odoo
- Actualizaciones automáticas
- Hosting en Odoo.sh
