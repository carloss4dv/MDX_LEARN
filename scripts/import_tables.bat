@echo off
REM Copiar el archivo SQL al contenedor
docker cp "data/dm_academico_modified.sql" oracle_db:/tmp/dm_academico.sql

REM Ejecutar el script SQL dentro del contenedor
echo @/tmp/dm_academico.sql >> temp.sql
echo exit; >> temp.sql
docker exec -i oracle_db sqlplus C##DM_ACADEMICO/YourPassword123@//localhost:1521/XEPDB1 < temp.sql
del temp.sql 