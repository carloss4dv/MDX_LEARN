# ============================================
# VERIFICAR CONTENEDOR DOCKER ORACLE
# ============================================
# Este script verifica que el contenedor Docker
# de Oracle esté ejecutándose correctamente
# ============================================

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "VERIFICANDO CONTENEDOR ORACLE DOCKER" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Verificar Docker
Write-Host "`n[INFO] Verificando Docker..." -ForegroundColor Yellow

try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker no encontrado"
    }
    Write-Host "[OK] Docker disponible: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Docker no esta instalado o no está en el PATH" -ForegroundColor Red
    exit 1
}

# Verificar contenedor oracle_db
Write-Host "`n[INFO] Verificando contenedor oracle_db..." -ForegroundColor Yellow

try {
    $containerStatus = docker ps --filter "name=oracle_db" --format "{{.Status}}" 2>$null
    if ([string]::IsNullOrEmpty($containerStatus)) {
        throw "Contenedor oracle_db no encontrado"
    }
    
    if ($containerStatus -match "Up") {
        Write-Host "[OK] Contenedor oracle_db esta ejecutandose" -ForegroundColor Green
        Write-Host "     Estado: $containerStatus" -ForegroundColor Gray
    } else {
        throw "Contenedor oracle_db no esta ejecutándose"
    }
} catch {
    Write-Host "[ERROR] Contenedor oracle_db no esta disponible" -ForegroundColor Red
    Write-Host "Para iniciarlo ejecute: docker-compose up -d" -ForegroundColor Yellow
    exit 1
}

# Verificar puertos
Write-Host "`n[INFO] Verificando mapeo de puertos..." -ForegroundColor Yellow

try {
    $portMapping = docker port oracle_db 1521 2>$null
    if ([string]::IsNullOrEmpty($portMapping)) {
        throw "Puerto 1521 no mapeado"
    }
    Write-Host "[OK] Puerto mapeado: $portMapping" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] No se pudo verificar el mapeo de puertos" -ForegroundColor Yellow
}

# Probar conexión SYS usando docker exec
Write-Host "`n[INFO] Probando conexion SYS..." -ForegroundColor Yellow

try {
    $testQuery = "SELECT 'Oracle ' || BANNER FROM V`$VERSION WHERE ROWNUM = 1; EXIT;"
    $result = docker exec oracle_db bash -c "echo `"$testQuery`" | sqlplus -S sys/YourStrongPassword123@XE as sysdba" 2>$null
    
    if ($result -match "Oracle") {
        Write-Host "[OK] Conexion SYS exitosa" -ForegroundColor Green
        $cleanResult = ($result -split "`n" | Where-Object { $_ -match "Oracle" })[0].Trim()
        Write-Host "     $cleanResult" -ForegroundColor Gray
    } else {
        throw "Conexion fallida"
    }
} catch {
    Write-Host "[ERROR] No se pudo conectar como SYS" -ForegroundColor Red
    Write-Host "Verificar que Oracle este completamente iniciado" -ForegroundColor Yellow
}

# Verificar XEPDB1 usando docker exec
Write-Host "`n[INFO] Verificando XEPDB1..." -ForegroundColor Yellow

try {
    $pdbQuery = "SELECT NAME, OPEN_MODE FROM V`$PDBS WHERE NAME='XEPDB1'; EXIT;"
    $pdbResult = docker exec oracle_db bash -c "echo `"$pdbQuery`" | sqlplus -S sys/YourStrongPassword123@XE as sysdba" 2>$null
    
    if ($pdbResult -match "READ WRITE") {
        Write-Host "[OK] XEPDB1 esta abierto y disponible" -ForegroundColor Green
    } elseif ($pdbResult -match "XEPDB1") {
        Write-Host "[WARNING] XEPDB1 encontrado pero puede no estar abierto" -ForegroundColor Yellow
        Write-Host "     Intentando abrir XEPDB1..." -ForegroundColor Yellow
        $openPDB = "ALTER PLUGGABLE DATABASE XEPDB1 OPEN; EXIT;"
        docker exec oracle_db bash -c "echo `"$openPDB`" | sqlplus -S sys/YourStrongPassword123@XE as sysdba" 2>$null | Out-Null
    } else {
        throw "XEPDB1 no encontrado"
    }
} catch {
    Write-Host "[ERROR] No se pudo verificar XEPDB1" -ForegroundColor Red
}

# Verificar usuario dm_academico en XEPDB1 usando docker exec
Write-Host "`n[INFO] Verificando usuario dm_academico en XEPDB1..." -ForegroundColor Yellow

try {
    $userQuery = "SELECT 'Usuario OK' FROM DUAL; EXIT;"
    $userResult = docker exec oracle_db bash -c "echo `"$userQuery`" | sqlplus -S dm_academico/YourPassword123@@XEPDB1" 2>$null
    
    if ($userResult -match "Usuario OK") {
        Write-Host "[OK] Usuario dm_academico disponible en XEPDB1" -ForegroundColor Green
    } else {
        throw "Usuario no disponible"
    }
} catch {
    Write-Host "[WARNING] Usuario dm_academico no disponible en XEPDB1" -ForegroundColor Yellow
    Write-Host "Ejecute los scripts de setup del Data Mart primero" -ForegroundColor Yellow
}

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "VERIFICACION COMPLETADA" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

Write-Host "`nSi todas las verificaciones son exitosas, puede ejecutar:" -ForegroundColor Green
Write-Host ".\setup_saiku_cdb.ps1" -ForegroundColor Yellow
