# 🔐 Configuración de Odoo Enterprise

## ⚠️ IMPORTANTE: NO SUBIR A GITHUB

La carpeta `enterprise/` contiene código propietario de Odoo S.A. y **NO debe subirse a GitHub** por las siguientes razones:

### 🚫 Razones Legales

1. **Violación de Licencia**: Los módulos Enterprise son propiedad de Odoo S.A.
2. **Requiere Licencia de Pago**: Solo usuarios con suscripción válida pueden usarlos
3. **Consecuencias Legales**: Odoo puede tomar acciones legales por piratería
4. **DMCA Takedown**: GitHub eliminará tu repositorio si subes código propietario

### ✅ Configuración Actual

El archivo `.gitignore` ya está configurado para excluir Enterprise:

```gitignore
# Enterprise (no subir el código de Enterprise por licencia)
enterprise/
enterprise.zip
```

## 📥 Cómo Obtener Odoo Enterprise

### Opción 1: Suscripción Oficial (Recomendado)

1. Compra una suscripción en https://www.odoo.com/pricing
2. Accede a tu cuenta en https://www.odoo.com/my/home
3. Descarga el código desde tu portal de cliente
4. Coloca el código en `enterprise/enterprise/`

### Opción 2: GitHub (Si tienes acceso)

Si tu empresa tiene acceso al repositorio privado de Odoo:

```bash
cd enterprise
git clone git@github.com:odoo/enterprise.git --branch 18.0 --depth 1
```

### Opción 3: Repositorio Interno de la Empresa

Si tu empresa mantiene un repositorio interno:

```bash
cd enterprise
git clone [URL_REPOSITORIO_INTERNO] enterprise
```

## 🔧 Configuración para Nuevos Desarrolladores

### Paso 1: Clonar el Proyecto

```bash
git clone [URL_DEL_PROYECTO]
cd cresio-appbackend-odoo-main
```

### Paso 2: Obtener Enterprise

**⚠️ NUNCA hagas esto:**
```bash
# ❌ INCORRECTO - NO HACER
git add enterprise/
git commit -m "Agregando enterprise"
```

**✅ Correcto:**
```bash
# Obtener Enterprise de fuente autorizada
cd enterprise
# [Usar una de las opciones de arriba]
cd ..
```

### Paso 3: Verificar que Enterprise NO esté en Git

```bash
# Verificar que enterprise está ignorado
git status --ignored | grep enterprise

# Debería mostrar:
# enterprise/
```

### Paso 4: Iniciar Docker

```bash
# Windows
setup_enterprise.bat

# Linux/Mac
./setup_enterprise.sh
```

## 📋 Estructura de Carpetas

```
cresio-appbackend-odoo-main/
├── enterprise/                    # ⚠️ NO SUBIR A GIT
│   └── enterprise/               # Código de Odoo Enterprise
│       ├── account_accountant/
│       ├── helpdesk/
│       ├── hr_payroll/
│       └── ... (400+ módulos)
├── zub_utils/                    # ✅ Subir a Git
├── zub_supplier_connector/       # ✅ Subir a Git
├── zub_onboarding/              # ✅ Subir a Git
├── zub_loyalty/                 # ✅ Subir a Git
└── .gitignore                   # ✅ Configurado correctamente
```

## 🔍 Verificación de Seguridad

### Antes de hacer Push

Siempre verifica que enterprise NO esté incluido:

```bash
# Ver qué archivos se van a subir
git status

# Ver archivos ignorados
git status --ignored

# Verificar que enterprise está ignorado
git check-ignore -v enterprise/
```

### Si Accidentalmente Agregaste Enterprise

```bash
# Remover del staging
git reset HEAD enterprise/

# Asegurarte que está en .gitignore
echo "enterprise/" >> .gitignore
git add .gitignore
git commit -m "Asegurar que enterprise está ignorado"
```

### Si Ya lo Subiste a GitHub (Emergencia)

1. **Eliminar del historial:**
```bash
git filter-branch --force --index-filter \
  "git rm -rf --cached --ignore-unmatch enterprise/" \
  --prune-empty --tag-name-filter cat -- --all

git push origin --force --all
```

2. **Contactar a Odoo:** Informa a Odoo sobre el incidente
3. **Cambiar credenciales:** Si había credenciales en los archivos

## 🤝 Trabajo en Equipo

### Compartir con el Equipo

**❌ NO hacer:**
- Subir enterprise a GitHub
- Compartir por email/Slack
- Subirlo a Dropbox/Google Drive público

**✅ Hacer:**
- Cada desarrollador obtiene su propia copia de fuente autorizada
- Usar repositorio privado interno de la empresa (si aplica)
- Documentar el proceso en este archivo

### Onboarding de Nuevos Desarrolladores

1. Dar acceso a la suscripción de Odoo (si aplica)
2. Compartir este documento (ENTERPRISE_SETUP.md)
3. Verificar que tienen `.gitignore` configurado
4. Revisar su primer commit para asegurar que no incluye enterprise

## 📝 Checklist de Seguridad

Antes de cada commit, verifica:

- [ ] `git status` no muestra archivos de `enterprise/`
- [ ] `.gitignore` incluye `enterprise/`
- [ ] No hay archivos `.zip` de enterprise en el proyecto
- [ ] No hay credenciales de Odoo en el código

## 🆘 Preguntas Frecuentes

### ¿Puedo usar Odoo Community en su lugar?

Sí, Odoo Community es gratuito y open source:

```bash
docker-compose up -d  # Usa docker-compose.yml (Community)
```

### ¿Qué pasa si no tengo Enterprise?

El proyecto funcionará con Community, pero sin módulos premium como:
- Contabilidad avanzada
- Nómina
- Helpdesk
- IoT
- Studio
- Etc.

### ¿Cómo actualizo Enterprise?

```bash
cd enterprise/enterprise
git pull origin 18.0
cd ../..
docker-compose -f docker-compose.enterprise.yml restart
```

### ¿Puedo compartir Enterprise con mi equipo?

Solo si todos tienen licencias válidas de Odoo Enterprise. Consulta los términos de tu suscripción.

## 📞 Contacto

Para dudas sobre licencias de Odoo Enterprise:
- Web: https://www.odoo.com/contactus
- Email: sales@odoo.com
- Teléfono: Consulta el sitio web de Odoo

---

**Recuerda:** La carpeta `enterprise/` debe estar siempre en `.gitignore` y nunca debe subirse a repositorios públicos o privados no autorizados.
