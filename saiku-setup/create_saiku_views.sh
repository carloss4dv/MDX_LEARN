#!/bin/bash

# =================================================================================================================
# AUTOR: Assistant
# FECHA: 26-06-2025
# DESCRIPCION: Script de Bash para ejecutar create_saiku_views.sql
#              Crea vistas optimizadas para mejorar el analisis en Saiku Analytics
#
# PRE-REQUISITOS:
# 1. Docker en ejecucion con contenedor Oracle activo
# 2. Script setup_saiku_cdb.sql ejecutado previamente
# 3. Usuario C##SAIKU_USER debe existir
#
# USO:
# 1. Dar permisos de ejecucion: chmod +x create_saiku_views.sh
# 2. Desde bash: ./create_saiku_views.sh
# 3. Desde el directorio root: ./saiku-setup/create_saiku_views.sh
# =================================================================================================================

# Configuracion
CONTAINER_NAME="oracle_db" # Cambiar si tu contenedor tiene otro nombre
SQL_SCRIPT_PATH="create_saiku_views.sql"

# Detectar si estamos en el directorio root o en saiku-setup
if [ -f "$SQL_SCRIPT_PATH" ]; then
    # Estamos en saiku-setup
    SCRIPT_FULL_PATH="$SQL_SCRIPT_PATH"
elif [ -f "saiku-setup/$SQL_SCRIPT_PATH" ]; then
    # Estamos en el directorio root
    SCRIPT_FULL_PATH="saiku-setup/$SQL_SCRIPT_PATH"
else
    echo -e "\033[1;31mError: No se encuentra el archivo '$SQL_SCRIPT_PATH'\033[0m"
    echo -e "\033[1;33m   Ejecuta este script desde:\033[0m"
    echo -e "\033[1;33m   - El directorio raiz del proyecto, o\033[0m"
    echo -e "\033[1;33m   - La carpeta saiku-setup/\033[0m"
    exit 1
fi

# Funcion para mostrar mensaje con colores
write_colored_message() {
    local message="$1"
    local color="$2"
    
    case $color in
        "red")     echo -e "\033[1;31m$message\033[0m" ;;
        "green")   echo -e "\033[1;32m$message\033[0m" ;;
        "yellow")  echo -e "\033[1;33m$message\033[0m" ;;
        "cyan")    echo -e "\033[1;36m$message\033[0m" ;;
        "magenta") echo -e "\033[1;35m$message\033[0m" ;;
        "gray")    echo -e "\033[0;37m$message\033[0m" ;;
        *)         echo -e "\033[1;37m$message\033[0m" ;;
    esac
}

# Verificar que Docker este disponible
write_colored_message "Verificando Docker..." "cyan"
if ! command -v docker &> /dev/null; then
    write_colored_message "Error: Docker no esta instalado o no esta en el PATH" "red"
    write_colored_message "   Instala Docker y vuelve a intentar" "yellow"
    exit 1
fi

if ! docker ps &> /dev/null; then
    write_colored_message "Error: Docker no esta ejecutandose o no tienes permisos" "red"
    write_colored_message "   Inicia Docker y vuelve a intentar" "yellow"
    write_colored_message "   Comandos utiles:" "yellow"
    write_colored_message "   sudo systemctl start docker" "gray"
    write_colored_message "   sudo usermod -aG docker \$USER" "gray"
    exit 1
fi
write_colored_message "Docker esta disponible" "green"

# Verificar que el contenedor Oracle este ejecutandose
write_colored_message "Verificando contenedor Oracle '$CONTAINER_NAME'..." "cyan"
CONTAINER_STATUS=$(docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}" | grep -i "$CONTAINER_NAME")
if [ -z "$CONTAINER_STATUS" ]; then
    write_colored_message "Error: El contenedor '$CONTAINER_NAME' no esta ejecutandose" "red"
    write_colored_message "   Comandos disponibles:" "yellow"
    write_colored_message "   docker start $CONTAINER_NAME" "gray"
    write_colored_message "   docker-compose up -d" "gray"
    exit 1
fi
write_colored_message "Contenedor Oracle esta activo" "green"

# Mostrar informacion del script
echo ""
write_colored_message "CREACION DE VISTAS OPTIMIZADAS PARA SAIKU" "magenta"
write_colored_message "================================================" "magenta"
write_colored_message "Script SQL: $SCRIPT_FULL_PATH" "white"
write_colored_message "Contenedor: $CONTAINER_NAME" "white"
write_colored_message "================================================" "magenta"
echo ""

# Preguntar confirmacion
write_colored_message "Este script creara las siguientes vistas optimizadas:" "yellow"
write_colored_message "- V_HECHOS_MATRICULA - Tabla de hechos con campos calculados" "white"
write_colored_message "- V_DIM_CENTRO - Dimension de centros con jerarquias" "white"
write_colored_message "- V_DIM_PLAN_ESTUDIO - Dimension academica optimizada" "white"
write_colored_message "- V_DIM_CURSO_ACADEMICO - Dimension temporal" "white"
write_colored_message "- V_DIM_SEXO - Dimension demografica normalizada" "white"
write_colored_message "- V_RESUMEN_EJECUTIVO - Vista agregada para dashboards" "white"
echo ""

read -p "Deseas continuar? (s/N): " confirmacion
if [[ ! "$confirmacion" =~ ^[sS]([iI])?$ ]]; then
    write_colored_message "Operacion cancelada por el usuario" "yellow"
    exit 0
fi

# Ejecutar el script SQL
write_colored_message "Ejecutando script de creacion de vistas..." "cyan"
write_colored_message "Esto puede tardar unos minutos..." "yellow"

# Ejecutar el script SQL en el contenedor
if cat "$SCRIPT_FULL_PATH" | docker exec -i "$CONTAINER_NAME" sqlplus -S "/ as sysdba"; then
    write_colored_message "VISTAS CREADAS EXITOSAMENTE!" "green"
    write_colored_message "================================================" "green"
    write_colored_message "PROXIMOS PASOS:" "cyan"
    write_colored_message "1. Actualizar el esquema Mondrian (dm_academico.xml)" "white"
    write_colored_message "2. Reiniciar Pentaho Server" "white"
    write_colored_message "3. Probar las nuevas funcionalidades en Saiku" "white"
    write_colored_message "================================================" "green"
    echo ""
    
    write_colored_message "COMANDOS UTILES:" "magenta"
    write_colored_message "- Reiniciar Pentaho: ./pentaho-server/stop-pentaho.sh && ./pentaho-server/start-pentaho.sh" "gray"
    write_colored_message "- Acceder a Saiku: http://localhost:8080/pentaho" "gray"
    write_colored_message "- Ver logs: tail -f ./pentaho-server/tomcat/logs/pentaho.log" "gray"
    
else
    write_colored_message "ERROR AL EJECUTAR EL SCRIPT" "red"
    write_colored_message "Codigo de salida: $?" "red"
    write_colored_message "Posibles soluciones:" "yellow"
    write_colored_message "- Verificar que el usuario C##SAIKU_USER existe" "white"
    write_colored_message "- Ejecutar primero: ./setup_saiku_cdb.sh" "white"
    write_colored_message "- Verificar conectividad con Oracle" "white"
    exit 1
fi

write_colored_message "PROCESO COMPLETADO!" "green" 