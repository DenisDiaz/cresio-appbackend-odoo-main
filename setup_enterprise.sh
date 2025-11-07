#!/bin/bash

echo "=========================================="
echo "  Configuración Odoo 18 Enterprise"
echo "=========================================="
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar que existe el directorio enterprise
if [ ! -d "enterprise/enterprise" ]; then
    echo -e "${RED}✗ Error: No se encuentra el directorio enterprise/enterprise${NC}"
    echo "  Por favor, asegúrate de tener los módulos Enterprise en:"
    echo "  ./enterprise/enterprise/"
    exit 1
fi

echo -e "${GREEN}✓ Directorio Enterprise encontrado${NC}"
echo ""

# Detener contenedores existentes de Community
echo "Deteniendo contenedores de Odoo Community (si existen)..."
docker-compose down 2>/dev/null || true
echo ""

# Limpiar contenedores Enterprise anteriores
echo "Limpiando contenedores Enterprise anteriores..."
docker-compose -f docker-compose.enterprise.yml down -v
echo ""

# Construir la imagen Enterprise
echo "=========================================="
echo "  Construyendo imagen Odoo 18 Enterprise"
echo "=========================================="
echo ""
docker-compose -f docker-compose.enterprise.yml build --no-cache

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Error al construir la imagen${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ Imagen construida exitosamente${NC}"
echo ""

# Iniciar los contenedores
echo "=========================================="
echo "  Iniciando Odoo 18 Enterprise"
echo "=========================================="
echo ""
docker-compose -f docker-compose.enterprise.yml up -d

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Error al iniciar los contenedores${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ Contenedores iniciados exitosamente${NC}"
echo ""

# Esperar a que Odoo esté listo
echo "Esperando a que Odoo esté disponible..."
sleep 10

# Verificar que los contenedores estén corriendo
if docker ps | grep -q "odoo_zublime_enterprise"; then
    echo -e "${GREEN}✓ Odoo Enterprise está corriendo${NC}"
else
    echo -e "${RED}✗ Error: Odoo Enterprise no está corriendo${NC}"
    echo "Mostrando logs:"
    docker-compose -f docker-compose.enterprise.yml logs --tail=50
    exit 1
fi

echo ""
echo "=========================================="
echo "  ✓ Instalación Completada"
echo "=========================================="
echo ""
echo -e "${GREEN}Odoo 18 Enterprise está disponible en:${NC}"
echo "  URL: http://localhost:8070"
echo "  Usuario: admin"
echo "  Contraseña: admin"
echo ""
echo -e "${YELLOW}Próximos pasos:${NC}"
echo "  1. Abre http://localhost:8070 en tu navegador"
echo "  2. Crea una nueva base de datos"
echo "  3. Instala los módulos personalizados:"
echo "     - zub_utils"
echo "     - zub_supplier_connector"
echo "     - zub_onboarding"
echo ""
echo "Para ver los logs:"
echo "  docker-compose -f docker-compose.enterprise.yml logs -f"
echo ""
echo "Para detener:"
echo "  docker-compose -f docker-compose.enterprise.yml down"
echo ""
