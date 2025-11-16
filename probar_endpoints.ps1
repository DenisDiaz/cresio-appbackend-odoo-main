# Script para probar los endpoints REST de Odoo
# Ejecutar: .\probar_endpoints.ps1

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  PROBANDO ENDPOINTS REST - ODOO" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$baseUrl = "http://localhost:8070"

# Test 1: Obtener todas las sucursales
Write-Host "1. Probando: /api/v1/branch-offices/get-all" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/v1/branch-offices/get-all" `
        -Method Post `
        -ContentType "application/json" `
        -Body '{}'
    
    Write-Host "   ✓ Status: 200 OK" -ForegroundColor Green
    Write-Host "   Sucursales encontradas: $($response.data.Count)" -ForegroundColor Green
    
    if ($response.data.Count -gt 0) {
        Write-Host "`n   Primera sucursal:" -ForegroundColor Cyan
        $first = $response.data[0]
        Write-Host "   - Nombre: $($first.name)" -ForegroundColor White
        Write-Host "   - Ciudad: $($first.city)" -ForegroundColor White
        Write-Host "   - Teléfono: $($first.phone)" -ForegroundColor White
    }
} catch {
    Write-Host "   ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Listar farmacias sin coordenadas
Write-Host "`n2. Probando: /api/v1/pharmacy/list (sin coordenadas)" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/v1/pharmacy/list" `
        -Method Post `
        -ContentType "application/json" `
        -Body '{}'
    
    Write-Host "   ✓ Status: 200 OK" -ForegroundColor Green
    Write-Host "   Total farmacias: $($response.pagination.total)" -ForegroundColor Green
    Write-Host "   Página: $($response.pagination.page) de $($response.pagination.pages)" -ForegroundColor Green
    
    if ($response.data.Count -gt 0) {
        Write-Host "`n   Farmacias:" -ForegroundColor Cyan
        foreach ($pharmacy in $response.data | Select-Object -First 3) {
            Write-Host "   - $($pharmacy.nombre) ($($pharmacy.direccion))" -ForegroundColor White
        }
    }
} catch {
    Write-Host "   ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Listar farmacias con coordenadas
Write-Host "`n3. Probando: /api/v1/pharmacy/list (con coordenadas)" -ForegroundColor Yellow
try {
    $body = @{
        latitude = 4.6097
        longitude = -74.0817
        page = 1
        limit = 5
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$baseUrl/api/v1/pharmacy/list" `
        -Method Post `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "   ✓ Status: 200 OK" -ForegroundColor Green
    Write-Host "   Farmacias ordenadas por distancia:" -ForegroundColor Green
    
    if ($response.data.Count -gt 0) {
        foreach ($pharmacy in $response.data) {
            Write-Host "   - $($pharmacy.nombre): $($pharmacy.distancia) km" -ForegroundColor White
        }
    }
} catch {
    Write-Host "   ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Obtener detalle de farmacia
Write-Host "`n4. Probando: /api/v1/pharmacy/get-detail" -ForegroundColor Yellow

# Primero obtener el ID de una farmacia
try {
    $listResponse = Invoke-RestMethod -Uri "$baseUrl/api/v1/pharmacy/list" `
        -Method Post `
        -ContentType "application/json" `
        -Body '{}'
    
    if ($listResponse.data.Count -gt 0) {
        $pharmacyId = $listResponse.data[0].id
        
        $body = @{
            id = $pharmacyId
            latitude = 4.6097
            longitude = -74.0817
        } | ConvertTo-Json
        
        $response = Invoke-RestMethod -Uri "$baseUrl/api/v1/pharmacy/get-detail" `
            -Method Post `
            -ContentType "application/json" `
            -Body $body
        
        Write-Host "   ✓ Status: 200 OK" -ForegroundColor Green
        Write-Host "`n   Detalle de farmacia:" -ForegroundColor Cyan
        Write-Host "   - ID: $($response.id)" -ForegroundColor White
        Write-Host "   - Nombre: $($response.nombre)" -ForegroundColor White
        Write-Host "   - Dirección: $($response.direccion)" -ForegroundColor White
        Write-Host "   - Teléfono: $($response.telefono)" -ForegroundColor White
        Write-Host "   - Email: $($response.email)" -ForegroundColor White
        Write-Host "   - Web: $($response.web)" -ForegroundColor White
        Write-Host "   - Distancia: $($response.distancia) km" -ForegroundColor White
        Write-Host "   - Imágenes: $($response.imagenes.Count)" -ForegroundColor White
    } else {
        Write-Host "   ⚠ No hay farmacias disponibles para probar" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 5: Onboarding
Write-Host "`n5. Probando: /api/v1/on-boarding/get-by-id" -ForegroundColor Yellow
try {
    $body = @{
        id = 1
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$baseUrl/api/v1/on-boarding/get-by-id" `
        -Method Post `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "   ✓ Status: 200 OK" -ForegroundColor Green
    Write-Host "   Respuesta recibida correctamente" -ForegroundColor Green
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    if ($statusCode -eq 404) {
        Write-Host "   ⚠ Endpoint responde pero no hay datos (404)" -ForegroundColor Yellow
    } else {
        Write-Host "   ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  PRUEBAS COMPLETADAS" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Para más información, revisa: ejemplos_uso_endpoints.md`n" -ForegroundColor Gray
