# ============================================
# PRUEBA RÁPIDA DE DOCKER EXEC CON ORACLE
# ============================================
# Script simple para probar comandos docker exec
# ============================================

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "PRUEBA DOCKER EXEC CON ORACLE" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Verificar contenedor
Write-Host "`n[INFO] Verificando contenedor..." -ForegroundColor Yellow
$containerStatus = docker ps --filter "name=oracle_db" --format "{{.Names}} - {{.Status}}"
if ($containerStatus) {
    Write-Host "[OK] $containerStatus" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Contenedor oracle_db no encontrado" -ForegroundColor Red
    exit 1
}

# Prueba básica
Write-Host "`n[INFO] Prueba basica de conexion..." -ForegroundColor Yellow
$basicTest = docker exec oracle_db bash -c "echo 'SELECT SYSDATE FROM DUAL;' | sqlplus -S sys/YourStrongPassword123@XE as sysdba"
Write-Host "Resultado:" -ForegroundColor Gray
Write-Host $basicTest -ForegroundColor White

# Verificar XEPDB1
Write-Host "`n[INFO] Verificando XEPDB1..." -ForegroundColor Yellow  
$pdbTest = docker exec oracle_db sqlplus -S sys/YourStrongPassword123@XE as sysdba -c "SELECT NAME, OPEN_MODE FROM V\`$PDBS WHERE NAME='XEPDB1';"
Write-Host "PDBs disponibles:" -ForegroundColor Gray
Write-Host $pdbTest -ForegroundColor White

# Probar usuario dm_academico
Write-Host "`n[INFO] Probando usuario dm_academico..." -ForegroundColor Yellow
$userTest = docker exec oracle_db sqlplus -S dm_academico/YourPassword123@@XEPDB1 -c "SELECT USER FROM DUAL;" 2>$null
if ($userTest -match "DM_ACADEMICO") {
    Write-Host "[OK] Usuario dm_academico conectado" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Usuario dm_academico no disponible" -ForegroundColor Yellow
    Write-Host "Resultado: $userTest" -ForegroundColor Gray
}

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "PRUEBA COMPLETADA" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
