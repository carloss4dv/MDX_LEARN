# Verificar esquemas y tablas en XEPDB1

Write-Host "Verificando esquemas y tablas en XEPDB1..." -ForegroundColor Yellow

$checkTables = @"
SELECT OWNER, TABLE_NAME FROM ALL_TABLES 
WHERE OWNER IN ('DM_ACADEMICO', 'C##DM_ACADEMICO') 
OR TABLE_NAME LIKE '%ACADEMICO%' 
OR TABLE_NAME LIKE '%CURSO%'
OR TABLE_NAME LIKE '%CENTRO%'
ORDER BY OWNER, TABLE_NAME;
EXIT;
"@

$checkTables | Out-File -FilePath "check_tables.sql" -Encoding ASCII
docker cp check_tables.sql oracle_db:/tmp/check_tables.sql

Write-Host "`nTablas encontradas:" -ForegroundColor Gray
$tableResult = docker exec oracle_db bash -c "sqlplus -S sys/YourStrongPassword123@XEPDB1 as sysdba @/tmp/check_tables.sql"
Write-Host $tableResult

# Limpiar
Remove-Item check_tables.sql -Force
docker exec oracle_db rm -f /tmp/check_tables.sql

# También verificar todos los esquemas que no sean de sistema
$checkSchemas = @"
SELECT DISTINCT OWNER FROM ALL_TABLES 
WHERE OWNER NOT IN ('SYS', 'SYSTEM', 'CTXSYS', 'DBSNMP', 'GSMADMIN_INTERNAL', 'PDBADMIN', 'XDB', 'WMSYS')
ORDER BY OWNER;
EXIT;
"@

$checkSchemas | Out-File -FilePath "check_schemas.sql" -Encoding ASCII
docker cp check_schemas.sql oracle_db:/tmp/check_schemas.sql

Write-Host "`nEsquemas de usuario encontrados:" -ForegroundColor Gray
$schemaResult = docker exec oracle_db bash -c "sqlplus -S sys/YourStrongPassword123@XEPDB1 as sysdba @/tmp/check_schemas.sql"
Write-Host $schemaResult

# Limpiar
Remove-Item check_schemas.sql -Force
docker exec oracle_db rm -f /tmp/check_schemas.sql
