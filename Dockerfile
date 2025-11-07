# Dockerfile para Odoo 18 Enterprise
FROM odoo:18.0

USER root

# Clonar repositorio Enterprise (requiere acceso)
# Necesitas reemplazar con tus credenciales o token de GitHub
RUN apt-get update && apt-get install -y git

# Opción A: Si tienes el código Enterprise localmente, cópialo
# COPY ./enterprise /mnt/enterprise

# Opción B: Si tienes acceso al repositorio privado de Odoo
# RUN git clone --depth 1 --branch 18.0 https://github.com/odoo/enterprise.git /mnt/enterprise

# Configurar addons path para incluir enterprise
ENV ODOO_ADDONS_PATH="/mnt/extra-addons,/mnt/enterprise"

USER odoo
