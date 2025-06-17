# ============================================
# SETUP SAIKU CDB CON DOCKER EXEC (SIMPLIFICADO)
# ============================================

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "CONFIGURANDO SAIKU PARA CDB CON DOCKER EXEC" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Verificar contenedor Docker
Write-Host "`n[INFO] Verificando contenedor oracle_db..." -ForegroundColor Yellow

$containerStatus = docker ps --filter "name=oracle_db" --format "{{.Status}}"
if ($containerStatus -match "Up") {
    Write-Host "[OK] Contenedor oracle_db ejecutandose" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Contenedor oracle_db no disponible. Ejecute: docker-compose up -d" -ForegroundColor Red
    exit 1
}

# Verificar conexión básica
Write-Host "`n[INFO] Verificando conexion basica..." -ForegroundColor Yellow
try {
    $testScript = "SELECT 'OK' FROM DUAL; EXIT;"
    $testScript | Out-File -FilePath "test.sql" -Encoding ASCII
    docker cp test.sql oracle_db:/tmp/test.sql
    $testResult = docker exec oracle_db bash -c "sqlplus -S sys/YourStrongPassword123@XE as sysdba @/tmp/test.sql"
    Remove-Item test.sql -Force
    docker exec oracle_db rm -f /tmp/test.sql
    
    if ($testResult -match "OK") {
        Write-Host "[OK] Conexion establecida" -ForegroundColor Green
    } else {
        throw "Conexion fallida"
    }
} catch {
    Write-Host "[ERROR] No se puede conectar a Oracle en el contenedor" -ForegroundColor Red
    exit 1
}

# Crear y copiar script SQL al contenedor
Write-Host "`n[INFO] Preparando script de configuracion..." -ForegroundColor Yellow

$setupScript = @"
-- Crear usuario C##DM_ACADEMICO
DROP USER C##DM_ACADEMICO CASCADE;

CREATE USER C##DM_ACADEMICO IDENTIFIED BY "YourPassword123@" CONTAINER=ALL;
GRANT CONNECT, RESOURCE TO C##DM_ACADEMICO CONTAINER=ALL;
GRANT CREATE DATABASE LINK TO C##DM_ACADEMICO CONTAINER=ALL;
GRANT CREATE VIEW TO C##DM_ACADEMICO CONTAINER=ALL;
GRANT CREATE SYNONYM TO C##DM_ACADEMICO CONTAINER=ALL;
GRANT UNLIMITED TABLESPACE TO C##DM_ACADEMICO CONTAINER=ALL;

-- Conectar como nuevo usuario
CONNECT C##DM_ACADEMICO/"YourPassword123@"@XE;

-- Crear database link
-- Usar el usuario común que existe en ambos containers
CREATE DATABASE LINK XEPDB1_LINK 
CONNECT TO C##DM_ACADEMICO IDENTIFIED BY "YourPassword123@"
USING 'localhost:1521/XEPDB1';

-- Crear vistas
CREATE VIEW D_CURSO_ACADEMICO AS SELECT * FROM dm_academico.D_CURSO_ACADEMICO@XEPDB1_LINK;
CREATE VIEW D_CENTRO AS SELECT * FROM dm_academico.D_CENTRO@XEPDB1_LINK;  
CREATE VIEW D_ASIGNATURA AS SELECT * FROM dm_academico.D_ASIGNATURA@XEPDB1_LINK;
CREATE VIEW D_SEXO AS SELECT * FROM dm_academico.D_SEXO@XEPDB1_LINK;
CREATE VIEW F_MATRICULA AS SELECT * FROM dm_academico.F_MATRICULA@XEPDB1_LINK;

-- Verificar
SELECT 'Setup completado - ' || COUNT(*) || ' vistas creadas' AS RESULTADO 
FROM USER_VIEWS;

EXIT;
"@

# Guardar script temporalmente
$tempFile = "setup_temp.sql"
$setupScript | Out-File -FilePath $tempFile -Encoding ASCII

# Copiar al contenedor
docker cp $tempFile oracle_db:/tmp/setup_saiku.sql

# Ejecutar script
Write-Host "`n[INFO] Ejecutando configuracion..." -ForegroundColor Yellow
$result = docker exec oracle_db bash -c "sqlplus -S sys/YourStrongPassword123@XE as sysdba @/tmp/setup_saiku.sql"

Write-Host "`n[INFO] Resultado de la configuracion:" -ForegroundColor Yellow
Write-Host $result -ForegroundColor Gray

# Limpiar archivos temporales
Remove-Item $tempFile -Force -ErrorAction SilentlyContinue
docker exec oracle_db rm -f /tmp/setup_saiku.sql

# Verificar configuración final
Write-Host "`n[INFO] Verificando configuracion final..." -ForegroundColor Yellow
$verifyScript = "SELECT VIEW_NAME FROM USER_VIEWS ORDER BY VIEW_NAME; EXIT;"
$verifyScript | Out-File -FilePath "verify.sql" -Encoding ASCII
docker cp verify.sql oracle_db:/tmp/verify.sql
$verifyResult = docker exec oracle_db bash -c "sqlplus -S C##DM_ACADEMICO/\\\"YourPassword123@\\\"@XE @/tmp/verify.sql"
Remove-Item verify.sql -Force
docker exec oracle_db rm -f /tmp/verify.sql

Write-Host "Vistas creadas:" -ForegroundColor Gray
Write-Host $verifyResult -ForegroundColor White

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
Write-Host "============================================" -ForegroundColor Cyan

Write-Host "`n[INFO] Configuracion completada con Docker exec!" -ForegroundColor Green
