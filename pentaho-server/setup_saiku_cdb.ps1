# ============================================
# SCRIPT PARA CONFIGURAR S# Crear archivo temporal con la configuracion correcta
$tempScript = $scriptPath -replace "\.sql$", "_temp.sql"
$scriptContent = Get-Content $scriptPath -Raw
# El script ya está configurado para docker exec, solo copiamos
$scriptContent | Out-File -FilePath $tempScript -Encoding UTF8CDB
# ============================================
# Este script configura automaticamente los database links
# para que Saiku pueda acceder a los datos desde CDB
# Configurado para usar el contenedor Docker de Oracle
# ============================================

param(
    [SecureString]$OraclePassword
)

# Convertir SecureString a string para uso con sqlplus
# Usar la contraseña del Docker por defecto
if (-not $OraclePassword) {
    $OraclePassword = ConvertTo-SecureString "YourStrongPassword123" -AsPlainText -Force
}
$PlainPassword = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($OraclePassword))

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "CONFIGURANDO SAIKU PARA CDB CON DATABASE LINKS" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Verificar que Oracle este ejecutandose (usando docker exec)
Write-Host "`n[INFO] Verificando conexion a Oracle con SYSDBA..." -ForegroundColor Yellow

try {
    $testQuery = "SELECT 1 FROM DUAL; EXIT;"
    $result = docker exec oracle_db bash -c "echo `"$testQuery`" | sqlplus -S sys/YourStrongPassword123@XE as sysdba" 2>$null
    if ($result -notmatch "1") {
        throw "No se puede conectar a Oracle"
    }
    Write-Host "[OK] Conexion a Oracle establecida con SYSDBA" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] No se puede conectar a Oracle. Verifique que:" -ForegroundColor Red
    Write-Host "  - El contenedor Docker oracle_db este ejecutandose" -ForegroundColor Red
    Write-Host "  - La contrasena SYS sea correcta (YourStrongPassword123)" -ForegroundColor Red
    Write-Host "  - Oracle este completamente iniciado en el contenedor" -ForegroundColor Red
    exit 1
}

# Verificar que XEPDB1 este disponible
Write-Host "`n[INFO] Verificando XEPDB1..." -ForegroundColor Yellow

# Verificar que XEPDB1 este disponible (usando docker exec)
Write-Host "`n[INFO] Verificando XEPDB1..." -ForegroundColor Yellow

try {
    $testQuery = "SELECT 1 FROM DUAL; EXIT;"
    $result = docker exec oracle_db bash -c "echo `"$testQuery`" | sqlplus -S dm_academico/YourPassword123@@XEPDB1" 2>$null
    if ($result -notmatch "1") {
        throw "No se puede conectar a XEPDB1"
    }
    Write-Host "[OK] XEPDB1 esta disponible" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] No se puede conectar a XEPDB1. Verifique que:" -ForegroundColor Red
    Write-Host "  - XEPDB1 este abierto y disponible en el contenedor" -ForegroundColor Red  
    Write-Host "  - El usuario dm_academico exista en XEPDB1" -ForegroundColor Red
    Write-Host "  - Las tablas del Data Mart esten creadas" -ForegroundColor Red
    Write-Host "  - La contrasena dm_academico sea YourPassword123@" -ForegroundColor Red
    exit 1
}

# Ejecutar script de configuracion
Write-Host "`n[INFO] Ejecutando configuracion de database links..." -ForegroundColor Yellow

$scriptPath = Join-Path $PSScriptRoot "setup_saiku_cdb_links.sql"

if (!(Test-Path $scriptPath)) {
    Write-Host "[ERROR] No se encuentra el archivo setup_saiku_cdb_links.sql" -ForegroundColor Red
    Write-Host "Asegurese de que el archivo este en el directorio: $PSScriptRoot" -ForegroundColor Red
    exit 1  
}

# Crear archivo temporal con la contrasena correcta
$tempScript = $scriptPath -replace "\.sql$", "_temp.sql"
$scriptContent = Get-Content $scriptPath -Raw
$scriptContent = $scriptContent -replace "system/password@", "sys/$PlainPassword@"
$scriptContent = $scriptContent -replace "localhost:1521", "$OracleHost`:$OraclePort"
# Añadir AS SYSDBA a las conexiones
$scriptContent = $scriptContent -replace "CONNECT sys/", "CONNECT sys/"
$scriptContent = $scriptContent -replace "@localhost:\d+/XE;", "@$OracleHost`:$OraclePort/XE AS SYSDBA;"
$scriptContent | Out-File -FilePath $tempScript -Encoding UTF8

try {
    # Copiar script al contenedor y ejecutarlo
    docker cp $tempScript oracle_db:/tmp/setup_script.sql
    docker exec oracle_db bash -c "sqlplus -S sys/YourStrongPassword123@XE as sysdba @/tmp/setup_script.sql" 2>$null | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Configuracion completada exitosamente" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] El script se ejecuto pero pueden haber errores. Revise la salida anterior." -ForegroundColor Yellow
    }
} catch {
    Write-Host "[ERROR] Error ejecutando el script de configuracion: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
} finally {
    # Limpiar archivos temporales
    if (Test-Path $tempScript) {
        Remove-Item $tempScript -Force
    }
    docker exec oracle_db rm -f /tmp/setup_script.sql 2>$null
}

# Verificar configuracion
Write-Host "`n[INFO] Verificando configuracion..." -ForegroundColor Yellow

try {
    $verifyScript = "SELECT 'Configuracion OK - ' || COUNT(*) || ' vistas creadas' AS STATUS FROM USER_VIEWS WHERE VIEW_NAME IN ('D_CURSO_ACADEMICO', 'D_CENTRO', 'D_ASIGNATURA', 'D_SEXO', 'F_MATRICULA'); EXIT;"
    
    $verifyResult = docker exec oracle_db bash -c "echo `"$verifyScript`" | sqlplus -S C##DM_ACADEMICO/YourPassword123@@XE" 2>$null
    
    if ($verifyResult -match "Configuracion OK") {
        $cleanResult = ($verifyResult -split "`n" | Where-Object { $_ -match "Configuracion OK" })[0].Trim()
        Write-Host "[OK] $cleanResult" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] Verificacion inconclusa. Revise manualmente." -ForegroundColor Yellow
    }
} catch {
    Write-Host "[WARNING] No se pudo verificar la configuracion automaticamente" -ForegroundColor Yellow
}

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "CONFIGURACION PARA SAIKU" -ForegroundColor Cyan  
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Driver: Oracle JDBC Thin" -ForegroundColor White
Write-Host "URL: jdbc:oracle:thin:@localhost:1521:XE" -ForegroundColor White
Write-Host "Username: C##DM_ACADEMICO" -ForegroundColor White
Write-Host "Password: YourPassword123@" -ForegroundColor White
Write-Host "`nTablas disponibles:" -ForegroundColor White
Write-Host "  - D_CURSO_ACADEMICO" -ForegroundColor Gray
Write-Host "  - D_CENTRO" -ForegroundColor Gray
Write-Host "  - D_ASIGNATURA" -ForegroundColor Gray
Write-Host "  - D_SEXO" -ForegroundColor Gray
Write-Host "  - F_MATRICULA" -ForegroundColor Gray
Write-Host "  - F_RENDIMIENTO (si existe)" -ForegroundColor Gray
Write-Host "============================================" -ForegroundColor Cyan

Write-Host "`n[INFO] Configuracion completada. Ahora puede configurar Saiku con los parametros mostrados arriba." -ForegroundColor Green
