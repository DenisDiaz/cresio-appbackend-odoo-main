# Script para probar todos los endpoints de forma interactiva

function Show-Menu {
    Clear-Host
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  API TESTER - ODOO ENTERPRISE" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Registro de Usuario" -ForegroundColor Yellow
    Write-Host "2. Listado de Farmacias" -ForegroundColor Yellow
    Write-Host "3. Detalle de Farmacia" -ForegroundColor Yellow
    Write-Host "4. Listado de Sucursales" -ForegroundColor Yellow
    Write-Host "5. Obtener Onboarding" -ForegroundColor Yellow
    Write-Host "6. Probar TODOS los endpoints" -ForegroundColor Green
    Write-Host "0. Salir" -ForegroundColor Red
    Write-Host ""
}

function Test-Register {
    Write-Host "`n=== REGISTRO DE USUARIO ===" -ForegroundColor Cyan
    
    $name = Read-Host "Nombre completo (Enter para usar 'Test User')"
    if ([string]::IsNullOrWhiteSpace($name)) { $name = "Test User" }
    
    $passport = Read-Host "Cédula/Pasaporte (Enter para generar automático)"
    if ([string]::IsNullOrWhiteSpace($passport)) { $passport = "TEST$(Get-Random -Minimum 100000 -Maximum 999999)" }
    
    $email = Read-Host "Email (Enter para generar automático)"
    if ([string]::IsNullOrWhiteSpace($email)) { $email = "test$(Get-Random)@example.com" }
    
    $password = Read-Host "Contraseña (Enter para usar 'test1234')"
    if ([string]::IsNullOrWhiteSpace($password)) { $password = "test1234" }
    
    Write-Host "`nEnviando petición..." -ForegroundColor Yellow
    
    $body = @{
        name = $name
        passport_number = $passport
        email = $email
        password = $password
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8070/api/v1/auth/register" -Method Post -Body $body -ContentType "application/json"
        Write-Host "`n✓ ÉXITO - Usuario registrado" -ForegroundColor Green
        Write-Host "Session ID: $($response.session_id)" -ForegroundColor Cyan
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        $errorBody = $_.ErrorDetails.Message | ConvertFrom-Json
        Write-Host "`n✗ ERROR ($statusCode)" -ForegroundColor Red
        Write-Host "Mensaje: $($errorBody.message)" -ForegroundColor Yellow
    }
    
    Write-Host "`nPresiona Enter para continuar..."
    Read-Host
}

function Test-PharmacyList {
    Write-Host "`n=== LISTADO DE FARMACIAS ===" -ForegroundColor Cyan
    
    $lat = Read-Host "Latitud (Enter para usar 4.6097)"
    if ([string]::IsNullOrWhiteSpace($lat)) { $lat = 4.6097 }
    
    $lon = Read-Host "Longitud (Enter para usar -74.0817)"
    if ([string]::IsNullOrWhiteSpace($lon)) { $lon = -74.0817 }
    
    $page = Read-Host "Página (Enter para usar 1)"
    if ([string]::IsNullOrWhiteSpace($page)) { $page = 1 }
    
    $limit = Read-Host "Límite (Enter para usar 10)"
    if ([string]::IsNullOrWhiteSpace($limit)) { $limit = 10 }
    
    Write-Host "`nEnviando petición..." -ForegroundColor Yellow
    
    $body = @{
        latitude = [double]$lat
        longitude = [double]$lon
        page = [int]$page
        limit = [int]$limit
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8070/api/v1/pharmacy/list" -Method Post -Body $body -ContentType "application/json"
        Write-Host "`n✓ ÉXITO - Farmacias encontradas" -ForegroundColor Green
        Write-Host "Total: $($response.pagination.total) farmacias" -ForegroundColor Cyan
        Write-Host "Página: $($response.pagination.page) de $($response.pagination.pages)" -ForegroundColor Cyan
        Write-Host "`nFarmacias:" -ForegroundColor Yellow
        foreach ($pharmacy in $response.data) {
            Write-Host "  - ID: $($pharmacy.id) | $($pharmacy.nombre) | Distancia: $($pharmacy.distancia) km" -ForegroundColor White
        }
    } catch {
        Write-Host "`n✗ ERROR" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Yellow
    }
    
    Write-Host "`nPresiona Enter para continuar..."
    Read-Host
}

function Test-PharmacyDetail {
    Write-Host "`n=== DETALLE DE FARMACIA ===" -ForegroundColor Cyan
    
    $id = Read-Host "ID de Farmacia (Enter para usar 18)"
    if ([string]::IsNullOrWhiteSpace($id)) { $id = 18 }
    
    $lat = Read-Host "Latitud (Enter para usar 4.6097)"
    if ([string]::IsNullOrWhiteSpace($lat)) { $lat = 4.6097 }
    
    $lon = Read-Host "Longitud (Enter para usar -74.0817)"
    if ([string]::IsNullOrWhiteSpace($lon)) { $lon = -74.0817 }
    
    Write-Host "`nEnviando petición..." -ForegroundColor Yellow
    
    $body = @{
        id = [int]$id
        latitude = [double]$lat
        longitude = [double]$lon
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8070/api/v1/pharmacy/get-detail" -Method Post -Body $body -ContentType "application/json"
        Write-Host "`n✓ ÉXITO - Detalle obtenido" -ForegroundColor Green
        Write-Host "Nombre: $($response.nombre)" -ForegroundColor Cyan
        Write-Host "Dirección: $($response.direccion)" -ForegroundColor White
        Write-Host "Teléfono: $($response.telefono)" -ForegroundColor White
        Write-Host "Email: $($response.email)" -ForegroundColor White
        Write-Host "Web: $($response.web)" -ForegroundColor White
        Write-Host "Distancia: $($response.distancia) km" -ForegroundColor Yellow
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Host "`n✗ ERROR ($statusCode)" -ForegroundColor Red
        if ($statusCode -eq 404) {
            Write-Host "Farmacia no encontrada. IDs disponibles: 18, 19, 20, 21, 22, 23" -ForegroundColor Yellow
        }
    }
    
    Write-Host "`nPresiona Enter para continuar..."
    Read-Host
}

function Test-BranchOffices {
    Write-Host "`n=== LISTADO DE SUCURSALES ===" -ForegroundColor Cyan
    Write-Host "Enviando petición..." -ForegroundColor Yellow
    
    $body = @{} | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8070/api/v1/branch-offices/get-all" -Method Post -Body $body -ContentType "application/json"
        Write-Host "`n✓ ÉXITO - Sucursales obtenidas" -ForegroundColor Green
        Write-Host "Total: $($response.result.data.Count) sucursales" -ForegroundColor Cyan
        Write-Host "`nSucursales:" -ForegroundColor Yellow
        foreach ($branch in $response.result.data) {
            Write-Host "  - $($branch.name)" -ForegroundColor White
            Write-Host "    Dirección: $($branch.street), $($branch.city)" -ForegroundColor Gray
            Write-Host "    Teléfono: $($branch.phone)" -ForegroundColor Gray
        }
    } catch {
        Write-Host "`n✗ ERROR" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Yellow
    }
    
    Write-Host "`nPresiona Enter para continuar..."
    Read-Host
}

function Test-Onboarding {
    Write-Host "`n=== OBTENER ONBOARDING ===" -ForegroundColor Cyan
    
    $id = Read-Host "ID de Onboarding (Enter para usar 1)"
    if ([string]::IsNullOrWhiteSpace($id)) { $id = 1 }
    
    Write-Host "`nEnviando petición..." -ForegroundColor Yellow
    
    $body = @{
        id = [int]$id
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8070/api/v1/on-boarding/get-by-id" -Method Post -Body $body -ContentType "application/json"
        Write-Host "`n✓ ÉXITO - Onboarding obtenido" -ForegroundColor Green
        Write-Host "Nombre: $($response.result.name)" -ForegroundColor Cyan
        Write-Host "Líneas: $($response.result.lines.Count)" -ForegroundColor Cyan
    } catch {
        Write-Host "`n⚠ Onboarding no encontrado" -ForegroundColor Yellow
        Write-Host "Esto es normal si no hay datos de onboarding configurados" -ForegroundColor Gray
    }
    
    Write-Host "`nPresiona Enter para continuar..."
    Read-Host
}

function Test-All {
    Write-Host "`n=== PROBANDO TODOS LOS ENDPOINTS ===" -ForegroundColor Cyan
    Write-Host ""
    
    # 1. Listado de Farmacias
    Write-Host "1. Listado de Farmacias..." -ForegroundColor Yellow
    $body = @{latitude=4.6097;longitude=-74.0817;page=1;limit=5} | ConvertTo-Json
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8070/api/v1/pharmacy/list" -Method Post -Body $body -ContentType "application/json"
        Write-Host "   ✓ OK - $($response.pagination.total) farmacias" -ForegroundColor Green
    } catch {
        Write-Host "   ✗ ERROR" -ForegroundColor Red
    }
    
    # 2. Detalle de Farmacia
    Write-Host "2. Detalle de Farmacia..." -ForegroundColor Yellow
    $body = @{id=18;latitude=4.6097;longitude=-74.0817} | ConvertTo-Json
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8070/api/v1/pharmacy/get-detail" -Method Post -Body $body -ContentType "application/json"
        Write-Host "   ✓ OK - $($response.nombre)" -ForegroundColor Green
    } catch {
        Write-Host "   ✗ ERROR" -ForegroundColor Red
    }
    
    # 3. Sucursales
    Write-Host "3. Listado de Sucursales..." -ForegroundColor Yellow
    $body = @{} | ConvertTo-Json
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8070/api/v1/branch-offices/get-all" -Method Post -Body $body -ContentType "application/json"
        Write-Host "   ✓ OK - $($response.result.data.Count) sucursales" -ForegroundColor Green
    } catch {
        Write-Host "   ✗ ERROR" -ForegroundColor Red
    }
    
    # 4. Registro
    Write-Host "4. Registro de Usuario..." -ForegroundColor Yellow
    $body = @{name="Test User";passport_number="TEST$(Get-Random)";email="test$(Get-Random)@example.com";password="test1234"} | ConvertTo-Json
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8070/api/v1/auth/register" -Method Post -Body $body -ContentType "application/json"
        Write-Host "   ✓ OK - Usuario registrado" -ForegroundColor Green
    } catch {
        Write-Host "   ✗ ERROR" -ForegroundColor Red
    }
    
    Write-Host "`n=== PRUEBAS COMPLETADAS ===" -ForegroundColor Cyan
    Write-Host "`nPresiona Enter para continuar..."
    Read-Host
}

# Menú principal
do {
    Show-Menu
    $option = Read-Host "Selecciona una opción"
    
    switch ($option) {
        '1' { Test-Register }
        '2' { Test-PharmacyList }
        '3' { Test-PharmacyDetail }
        '4' { Test-BranchOffices }
        '5' { Test-Onboarding }
        '6' { Test-All }
        '0' { 
            Write-Host "`nSaliendo..." -ForegroundColor Yellow
            break
        }
        default {
            Write-Host "`nOpción inválida" -ForegroundColor Red
            Start-Sleep -Seconds 1
        }
    }
} while ($option -ne '0')
