@echo off
REM Copiar el script SQL al contenedor
docker cp "unlock_account.sql" oracle_db:/tmp/unlock_account.sql

REM Ejecutar el script SQL con el usuario SYSTEM
echo @/tmp/unlock_account.sql >> temp_unlock.sql
echo exit; >> temp_unlock.sql
docker exec -i oracle_db sqlplus sys/YourPassword123@//localhost:1521/XEPDB1 as sysdba < temp_unlock.sql
del temp_unlock.sql

echo La cuenta C##DM_ACADEMICO ha sido desbloqueada y la contraseña restablecida. 