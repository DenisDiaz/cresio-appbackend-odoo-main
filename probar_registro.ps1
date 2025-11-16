# Script para probar el endpoint de registro
# Ejecutar: .\probar_registro.ps1

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  PROBANDO ENDPOINT DE REGISTRO" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$baseUrl = "http://localhost:8070"

# Generar datos únicos para evitar duplicados
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$randomNum = Get-Random -Minimum 1000 -Maximum 9999

# Test 1: Registro exitoso
Write-Host "1. Probando registro exitoso" -ForegroundColor Yellow
try {
    $body = @{
        name = "Usuario Test $timestamp"
        email = "test$timestamp@example.com"
        passport_number = "TEST$randomNum"
        password = "test123456"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$baseUrl/api/v1/auth/register" `
        -Method Post `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "   ✓ Status: 200 OK" -ForegroundColor Green
    Write-Host "   Session ID: $($response.session_id)" -ForegroundColor Green
    Write-Host "   Usuario creado exitosamente!" -ForegroundColor Green
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Write-Host "   ✗ Error: $statusCode" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        $errorData = $_.ErrorDetails.Message | ConvertFrom-Json
        Write-Host "   Mensaje: $($errorData.message)" -ForegroundColor Red
    }
}

# Test 2: Datos incompletos (400)
Write-Host "`n2. Probando datos incompletos (debe fallar con 400)" -ForegroundColor Yellow
try {
    $body = @{
        name = "Usuario Incompleto"
        email = "incompleto@example.com"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$baseUrl/api/v1/auth/register" `
        -Method Post `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "   ✗ No debería llegar aquí" -ForegroundColor Red
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    if ($statusCode -eq 400) {
        Write-Host "   ✓ Error 400 esperado" -ForegroundColor Green
        if ($_.ErrorDetails.Message) {
            $errorData = $_.ErrorDetails.Message | ConvertFrom-Json
            Write-Host "   Mensaje: $($errorData.message)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ✗ Error inesperado: $statusCode" -ForegroundColor Red
    }
}

# Test 3: Contraseña muy corta (417)
Write-Host "`n3. Probando contraseña muy corta (debe fallar con 417)" -ForegroundColor Yellow
try {
    $body = @{
        name = "Usuario Test"
        email = "test2@example.com"
        passport_number = "TEST123"
        password = "123"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$baseUrl/api/v1/auth/register" `
        -Method Post `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "   ✗ No debería llegar aquí" -ForegroundColor Red
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    if ($statusCode -eq 417) {
        Write-Host "   ✓ Error 417 esperado" -ForegroundColor Green
        if ($_.ErrorDetails.Message) {
            $errorData = $_.ErrorDetails.Message | ConvertFrom-Json
            Write-Host "   Mensaje: $($errorData.message)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ✗ Error inesperado: $statusCode" -ForegroundColor Red
    }
}

# Test 4: Email inválido (417)
Write-Host "`n4. Probando email inválido (debe fallar con 417)" -ForegroundColor Yellow
try {
    $body = @{
        name = "Usuario Test"
        email = "email-invalido"
        passport_number = "TEST456"
        password = "test123456"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$baseUrl/api/v1/auth/register" `
        -Method Post `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "   ✗ No debería llegar aquí" -ForegroundColor Red
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    if ($statusCode -eq 417) {
        Write-Host "   ✓ Error 417 esperado" -ForegroundColor Green
        if ($_.ErrorDetails.Message) {
            $errorData = $_.ErrorDetails.Message | ConvertFrom-Json
            Write-Host "   Mensaje: $($errorData.message)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ✗ Error inesperado: $statusCode" -ForegroundColor Red
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  PRUEBAS COMPLETADAS" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Para probar desde el navegador:" -ForegroundColor Gray
Write-Host "1. Ejecuta: iniciar_probador.bat" -ForegroundColor Gray
Write-Host "2. Ve a: http://localhost:8888" -ForegroundColor Gray
Write-Host "3. Busca la sección 'Registrar Usuario'`n" -ForegroundColor Gray
