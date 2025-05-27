@echo off
REM Copiar los archivos SQL al contenedor
docker cp "data/clean_database.sql" oracle_db:/tmp/clean_database.sql
docker cp "data/dm_academico_modified.sql" oracle_db:/tmp/dm_academico.sql

REM Ejecutar los scripts SQL dentro del contenedor
echo @/tmp/clean_database.sql >> temp.sql
echo @/tmp/dm_academico.sql >> temp.sql
echo exit; >> temp.sql
docker exec -i oracle_db sqlplus C##DM_ACADEMICO/YourPassword123@//localhost:1521/XEPDB1 < temp.sql
del temp.sql 