#!/bin/bash
# =================================================================================================================
# AUTOR: Carlos de Vera Sanz
# FECHA: 20-06-2025
# DESCRIPCIÓN: Script de Shell para ejecutar el script SQL de configuración de Saiku (setup_saiku_cdb.sql)
#              usando 'docker exec' y conectándose como SYSDBA sin solicitar credenciales.
#
# USO:
# 1. Asegúrate de que Docker está en ejecución y el contenedor de Oracle (ej. 'oracle-xe') está activo.
# 2. Otorga permisos de ejecución al script: chmod +x setup_saiku_cdb.sh
# 3. Ejecuta el script: ./setup_saiku_cdb.sh
# =================================================================================================================

CONTAINER_NAME="oracle_db" # <-- ¡IMPORTANTE! Cambia esto si tu contenedor tiene otro nombre.

echo "Este script creará un usuario para Saiku y copiará las tablas necesarias usando Docker."
echo "Se conectará como SYSDBA automáticamente."
echo ""

echo "Ejecutando el script setup_saiku_cdb.sql en el contenedor $CONTAINER_NAME como SYSDBA..."

# Usar 'docker exec' para ejecutar el script SQL dentro del contenedor, conectando como SYSDBA
# Se pasa el contenido del script a través de la entrada estándar
cat setup_saiku_cdb.sql | docker exec -i $CONTAINER_NAME sqlplus -S / as sysdba

# Comprobar el resultado
if [ $? -eq 0 ]; then
    echo ""
    echo "Script ejecutado correctamente."
else
    echo ""
    echo "Hubo un error durante la ejecución del script."
    echo "Por favor, revisa la salida anterior para identificar la causa."
fi

echo ""
echo "Proceso finalizado."
