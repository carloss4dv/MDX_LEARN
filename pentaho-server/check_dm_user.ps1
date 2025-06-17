# Script para verificar usuario dm_academico en XEPDB1

Write-Host "Verificando usuarios en XEPDB1..." -ForegroundColor Yellow

# Crear script para verificar usuarios
$checkUsers = @"
SELECT USERNAME, ACCOUNT_STATUS FROM DBA_USERS WHERE USERNAME LIKE '%DM%' OR USERNAME LIKE '%ACADEMICO%';
EXIT;
"@

$checkUsers | Out-File -FilePath "check_users.sql" -Encoding ASCII
docker cp check_users.sql oracle_db:/tmp/check_users.sql

Write-Host "`nUsuarios encontrados:" -ForegroundColor Gray
$userResult = docker exec oracle_db bash -c "sqlplus -S sys/YourStrongPassword123@XEPDB1 as sysdba @/tmp/check_users.sql"
Write-Host $userResult

# Limpiar
Remove-Item check_users.sql -Force
docker exec oracle_db rm -f /tmp/check_users.sql

# Intentar diferentes contraseñas comunes
$passwords = @("dm_academico", "YourPassword123@", "password", "oracle")

Write-Host "`nProbando diferentes contraseñas para dm_academico:" -ForegroundColor Yellow

foreach ($pwd in $passwords) {
    $testScript = "SELECT 'CONEXION OK CON: $pwd' FROM DUAL; EXIT;"
    $testScript | Out-File -FilePath "test_pwd.sql" -Encoding ASCII
    docker cp test_pwd.sql oracle_db:/tmp/test_pwd.sql
    
    $result = docker exec oracle_db bash -c "sqlplus -S dm_academico/$pwd@XEPDB1 @/tmp/test_pwd.sql" 2>$null
    
    if ($result -match "CONEXION OK") {
        Write-Host "[OK] Contraseña correcta: $pwd" -ForegroundColor Green
        break
    } else {
        Write-Host "[X] Contraseña incorrecta: $pwd" -ForegroundColor Red
    }
    
    Remove-Item test_pwd.sql -Force
    docker exec oracle_db rm -f /tmp/test_pwd.sql
}
