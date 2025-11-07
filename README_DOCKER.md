# Ejecutar Odoo con Docker

## Iniciar el proyecto

```bash
docker-compose up -d
```

## Acceder a Odoo

1. Abre tu navegador en: http://localhost:8069
2. En la primera ejecución, crea una nueva base de datos:
   - Master Password: admin (por defecto)
   - Database Name: zublime (o el nombre que prefieras)
   - Email: tu email
   - Password: tu contraseña
   - Language: Spanish / Español
   - Country: México (o tu país)

## Instalar los módulos personalizados

Una vez dentro de Odoo:
1. Activa el modo desarrollador: Settings > Activate the developer mode
2. Ve a Apps
3. Actualiza la lista de aplicaciones (botón "Update Apps List")
4. Busca y instala los módulos:
   - zub_onboarding
   - zub_supplier_connector
   - zub_loyalty

## Comandos útiles

Ver logs:
```bash
docker-compose logs -f web
```

Detener el proyecto:
```bash
docker-compose down
```

Detener y eliminar volúmenes (reinicio completo):
```bash
docker-compose down -v
```

Reiniciar Odoo:
```bash
docker-compose restart web
```

## APIs disponibles

- GET `/api/v1/branch-offices/get-all` - Obtener todas las sucursales de proveedores
- GET `/api/v1/on-boarding/get-by-id` - Obtener onboarding por ID

## Notas

- Los módulos están montados desde el directorio actual
- Los datos se persisten en volúmenes de Docker
- Puerto: 8069
- Usuario DB: odoo
- Password DB: odoo
