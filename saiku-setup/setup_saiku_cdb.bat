@echo off
REM =================================================================================================================
REM AUTOR: Carlos de Vera Sanz
REM FECHA: 20-06-2025
REM DESCRIPCIÓN: Script de Batch para ejecutar el script SQL de configuración de Saiku (setup_saiku_cdb.sql)
REM              usando 'docker exec' y conectándose como SYSDBA sin solicitar credenciales.
REM
REM USO:
REM 1. Asegúrate de que Docker está en ejecución y el contenedor de Oracle (ej. 'oracle-xe') está activo.
REM 2. Ejecuta este script haciendo doble clic o desde una ventana de comandos (cmd).
REM =================================================================================================================

set "CONTAINER_NAME=oracle_db"

ECHO.
ECHO Este script creara un usuario para Saiku y copiara las tablas necesarias usando Docker.
ECHO Se conectara como SYSDBA automaticamente.
ECHO.

ECHO Ejecutando el script setup_saiku_cdb.sql en el contenedor %CONTAINER_NAME% como SYSDBA...

REM Usar 'docker exec' para pasar el script a SQL*Plus dentro del contenedor, conectando como SYSDBA
(type setup_saiku_cdb.sql) | docker exec -i %CONTAINER_NAME% sqlplus -S / as sysdba

IF %ERRORLEVEL% NEQ 0 (
    ECHO.
    ECHO Hubo un error durante la ejecucion del script.
    ECHO Por favor, revisa el log anterior para identificar la causa.
) ELSE (
    ECHO.
    ECHO Script ejecutado correctamente.
)

ECHO.
ECHO Proceso finalizado.
pause
