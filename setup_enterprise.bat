@echo off
echo ==========================================
echo   Configuracion Odoo 18 Enterprise
echo ==========================================
echo.

REM Verificar que existe el directorio enterprise
if not exist "enterprise\enterprise" (
    echo [ERROR] No se encuentra el directorio enterprise\enterprise
    echo Por favor, asegurate de tener los modulos Enterprise en:
    echo   .\enterprise\enterprise\
    exit /b 1
)

echo [OK] Directorio Enterprise encontrado
echo.

REM Detener contenedores existentes de Community
echo Deteniendo contenedores de Odoo Community (si existen)...
docker-compose down 2>nul
echo.

REM Limpiar contenedores Enterprise anteriores
echo Limpiando contenedores Enterprise anteriores...
docker-compose -f docker-compose.enterprise.yml down -v
echo.

REM Construir la imagen Enterprise
echo ==========================================
echo   Construyendo imagen Odoo 18 Enterprise
echo ==========================================
echo.
docker-compose -f docker-compose.enterprise.yml build --no-cache

if errorlevel 1 (
    echo [ERROR] Error al construir la imagen
    exit /b 1
)

echo.
echo [OK] Imagen construida exitosamente
echo.

REM Iniciar los contenedores
echo ==========================================
echo   Iniciando Odoo 18 Enterprise
echo ==========================================
echo.
docker-compose -f docker-compose.enterprise.yml up -d

if errorlevel 1 (
    echo [ERROR] Error al iniciar los contenedores
    exit /b 1
)

echo.
echo [OK] Contenedores iniciados exitosamente
echo.

REM Esperar a que Odoo este listo
echo Esperando a que Odoo este disponible...
timeout /t 15 /nobreak >nul

REM Verificar que los contenedores esten corriendo
docker ps | findstr "odoo_zublime_enterprise" >nul
if errorlevel 1 (
    echo [ERROR] Odoo Enterprise no esta corriendo
    echo Mostrando logs:
    docker-compose -f docker-compose.enterprise.yml logs --tail=50
    exit /b 1
)

echo [OK] Odoo Enterprise esta corriendo
echo.

echo ==========================================
echo   Instalacion Completada
echo ==========================================
echo.
echo Odoo 18 Enterprise esta disponible en:
echo   URL: http://localhost:8070
echo   Usuario: admin
echo   Contraseña: admin
echo.
echo Proximos pasos:
echo   1. Abre http://localhost:8070 en tu navegador
echo   2. Crea una nueva base de datos
echo   3. Instala los modulos personalizados:
echo      - zub_utils
echo      - zub_supplier_connector
echo      - zub_onboarding
echo.
echo Para ver los logs:
echo   docker-compose -f docker-compose.enterprise.yml logs -f
echo.
echo Para detener:
echo   docker-compose -f docker-compose.enterprise.yml down
echo.
pause
