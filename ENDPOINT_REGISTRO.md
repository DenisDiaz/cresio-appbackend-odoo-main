# 📋 Endpoint de Registro - Verificación de Requisitos

## 🎯 Endpoint
`POST /api/v1/auth/register`

## 📥 REQUEST JSON

```json
{
  "name": "Nombre completo",
  "passport_number": "Cédula o pasaporte",
  "password": "contraseña",
  "email": "correo electrónico"
}
```

## 📤 RESPONSE 200 (Éxito)

```json
{
  "session_id": "hash generado por odoo de la sesión"
}
```

## 📊 HTTP Status Codes Implementados

| Código | Descripción | Uso en el Endpoint |
|--------|-------------|-------------------|
| ✅ 200 | Success | Usuario registrado correctamente + autologin |
| ✅ 400 | Bad Request | Datos de entrada incompletos |
| ⚠️ 401 | Unauthorized | No aplica en registro (sin sesión previa) |
| ⚠️ 403 | Forbidden | No aplica en registro (endpoint público) |
| ⚠️ 404 | Not Found | Manejado por Odoo (endpoint no existe) |
| ✅ 417 | Expected Failed | Validaciones de negocio fallidas |
| ✅ 500 | Server Error | Cualquier otro tipo de error |

## ✅ Validaciones Implementadas

### 1. Datos Completos (400 - Bad Request)
```python
if not all([name, passport_number, password, email]):
    return 400
```

**Ejemplo de respuesta:**
```json
{
  "error": "Datos incompletos",
  "message": "Todos los campos son requeridos: name, passport_number, password, email"
}
```

### 2. Longitud de Contraseña (417 - Expected Failed)
```python
if len(password) < 6 or len(password) > 15:
    return 417
```

**Regla:** Mínimo 6 caracteres, máximo 15 caracteres

**Ejemplo de respuesta:**
```json
{
  "error": "Contraseña inválida",
  "message": "La contraseña debe tener entre 6 y 15 caracteres"
}
```

### 3. Formato de Email (417 - Expected Failed)
```python
email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
if not re.match(email_regex, email):
    return 417
```

**Ejemplo de respuesta:**
```json
{
  "error": "Email inválido",
  "message": "El formato del correo electrónico no es válido"
}
```

### 4. Email Ya Registrado (417 - Expected Failed)
```python
existing_user = search([('login', '=', email)])
if existing_user:
    return 417
```

**Ejemplo de respuesta:**
```json
{
  "error": "Email ya registrado",
  "message": "El correo electrónico ya está registrado en el sistema"
}
```

### 5. Formato de Cédula/Pasaporte (417 - Expected Failed)
```python
passport_regex = r'^[A-Za-z0-9\-\s]{5,20}$'
if not re.match(passport_regex, passport_number):
    return 417
```

**Regla:** Acepta letras, números, guiones y espacios. Mínimo 5, máximo 20 caracteres.

**Ejemplo de respuesta:**
```json
{
  "error": "Cédula/Pasaporte inválido",
  "message": "El formato de la cédula o pasaporte no es válido"
}
```

### 6. Cédula/Pasaporte Ya Registrado (417 - Expected Failed)
```python
existing_partner = search([('vat', '=', passport_number)])
if existing_partner:
    return 417
```

**Ejemplo de respuesta:**
```json
{
  "error": "Cédula/Pasaporte ya registrado",
  "message": "La cédula o pasaporte ya está registrado en el sistema"
}
```

## 🔄 Flujo de Registro Exitoso

```
1. Validar datos de entrada
   ↓
2. Crear Partner (contacto)
   ↓
3. Crear Usuario (res.users)
   ↓
4. Enviar email de bienvenida
   ↓
5. Autologin (autenticar usuario)
   ↓
6. Devolver session_id (200)
```

## 📧 Email de Bienvenida

El sistema intenta enviar un email de bienvenida usando el template:
- Template ID: `zub_onboarding.email_template_welcome`
- Si el template no existe, se registra un warning pero el registro continúa
- El email se envía de forma asíncrona

## 🔐 Autologin

Después del registro exitoso:
1. Se autentica automáticamente al usuario
2. Se crea una sesión en Odoo
3. Se devuelve el `session_id` en la respuesta

**Método usado:**
```python
uid = request.session.authenticate(dbname, email, password)
session_id = request.session.sid
```

## 🧪 Casos de Prueba

### Test 1: Registro Exitoso
```bash
curl -X POST http://localhost:8070/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "passport_number": "1234567890",
    "password": "test123456",
    "email": "juan@example.com"
  }'
```

**Respuesta esperada (200):**
```json
{
  "session_id": "abc123xyz..."
}
```

### Test 2: Datos Incompletos
```bash
curl -X POST http://localhost:8070/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "password": "test123456"
  }'
```

**Respuesta esperada (400):**
```json
{
  "error": "Datos incompletos",
  "message": "Todos los campos son requeridos: name, passport_number, password, email"
}
```

### Test 3: Contraseña Muy Corta
```bash
curl -X POST http://localhost:8070/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "passport_number": "1234567890",
    "password": "123",
    "email": "juan@example.com"
  }'
```

**Respuesta esperada (417):**
```json
{
  "error": "Contraseña inválida",
  "message": "La contraseña debe tener entre 6 y 15 caracteres"
}
```

### Test 4: Email Inválido
```bash
curl -X POST http://localhost:8070/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "passport_number": "1234567890",
    "password": "test123456",
    "email": "invalid-email"
  }'
```

**Respuesta esperada (417):**
```json
{
  "error": "Email inválido",
  "message": "El formato del correo electrónico no es válido"
}
```

### Test 5: Email Duplicado
```bash
# Primer registro (exitoso)
curl -X POST http://localhost:8070/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "passport_number": "1234567890",
    "password": "test123456",
    "email": "juan@example.com"
  }'

# Segundo registro con mismo email (falla)
curl -X POST http://localhost:8070/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "María García",
    "passport_number": "9876543210",
    "password": "test123456",
    "email": "juan@example.com"
  }'
```

**Respuesta esperada (417):**
```json
{
  "error": "Email ya registrado",
  "message": "El correo electrónico ya está registrado en el sistema"
}
```

### Test 6: Pasaporte Duplicado
```bash
# Primer registro (exitoso)
curl -X POST http://localhost:8070/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "passport_number": "1234567890",
    "password": "test123456",
    "email": "juan@example.com"
  }'

# Segundo registro con mismo pasaporte (falla)
curl -X POST http://localhost:8070/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "María García",
    "passport_number": "1234567890",
    "password": "test123456",
    "email": "maria@example.com"
  }'
```

**Respuesta esperada (417):**
```json
{
  "error": "Cédula/Pasaporte ya registrado",
  "message": "La cédula o pasaporte ya está registrado en el sistema"
}
```

## 📝 Checklist de Requisitos

### Códigos HTTP
- [x] 200 - Success (registro exitoso + autologin)
- [x] 400 - Bad Request (datos incompletos)
- [ ] 401 - Unauthorized (no aplica en registro)
- [ ] 403 - Forbidden (no aplica en registro)
- [ ] 404 - Not Found (manejado por Odoo)
- [x] 417 - Expected Failed (validaciones de negocio)
- [x] 500 - Server Error (errores no controlados)

### Campos de Entrada
- [x] name (nombre completo)
- [x] passport_number (cédula o pasaporte)
- [x] password (contraseña)
- [x] email (correo electrónico)

### Validaciones
- [x] Contraseña: 6-15 caracteres
- [x] Email no registrado (417 si existe)
- [x] Formato de email válido (regex)
- [x] Formato de cédula/pasaporte válido (regex)
- [x] Cédula/pasaporte no registrado (417 si existe)

### Funcionalidades
- [x] Registrar usuario en Odoo
- [x] Enviar email de bienvenida
- [x] Autologin del usuario
- [x] Devolver session_id en respuesta 200

### Respuesta 200
- [x] Contiene `session_id`
- [x] Session ID es generado por Odoo

## 🔧 Archivos Modificados

1. `zub_onboarding/controllers/controllers.py` - Endpoint principal
2. `tests/test_register_simple.py` - Test básico
3. `tests/test_register_complete.py` - Test completo de validaciones
4. `tests/test_register.html` - Test manual en navegador
5. `tests/test_register.http` - Test con REST Client

## 🚀 Ejecutar Tests

```bash
# Test simple
python tests/test_register_simple.py

# Test completo
python tests/test_register_complete.py

# Test HTML
# Abrir tests/test_register.html en el navegador
```

## 📊 Resultados Esperados

Todos los tests deben pasar:
- ✅ Datos incompletos → 400
- ✅ Contraseña corta → 417
- ✅ Email inválido → 417
- ✅ Registro exitoso → 200 con session_id
- ✅ Email duplicado → 417
- ✅ Pasaporte duplicado → 417

## 🐛 Troubleshooting

### El autologin falla
Si el autologin falla, el usuario aún se crea correctamente. La respuesta será:
```json
{
  "success": true,
  "message": "Usuario registrado exitosamente, pero falló el autologin",
  "user_id": 123
}
```

### Email no se envía
Verifica:
1. Que el template `zub_onboarding.email_template_welcome` existe
2. Configuración SMTP en Odoo
3. Logs: `docker logs odoo_zublime_enterprise`

### Session ID no se genera
Verifica:
1. Que la contraseña es correcta
2. Que el usuario se creó correctamente
3. Logs de autenticación en Odoo

---

**Última actualización:** 2025-11-07
**Estado:** ✅ Implementado y probado
