# =================================================================================================================
# AUTOR: Assistant
# FECHA: 26-06-2025
# DESCRIPCION: Script de PowerShell para ejecutar create_saiku_views.sql
#              Crea vistas optimizadas para mejorar el analisis en Saiku Analytics
#
# PRE-REQUISITOS:
# 1. Docker en ejecucion con contenedor Oracle activo
# 2. Script setup_saiku_cdb.sql ejecutado previamente
# 3. Usuario C##SAIKU_USER debe existir
#
# USO:
# 1. Desde PowerShell: .\create_saiku_views.ps1
# 2. Desde el directorio root: .\saiku-setup\create_saiku_views.ps1
# =================================================================================================================

# Configuracion
$containerName = "oracle_db" # Cambiar si tu contenedor tiene otro nombre
$sqlScriptPath = "create_saiku_views.sql"

# Detectar si estamos en el directorio root o en saiku-setup
if (Test-Path $sqlScriptPath) {
    # Estamos en saiku-setup
    $scriptFullPath = $sqlScriptPath
} elseif (Test-Path "saiku-setup\$sqlScriptPath") {
    # Estamos en el directorio root
    $scriptFullPath = "saiku-setup\$sqlScriptPath"
} else {
    Write-Host "Error: No se encuentra el archivo '$sqlScriptPath'" -ForegroundColor Red
    Write-Host "   Ejecuta este script desde:" -ForegroundColor Yellow
    Write-Host "   - El directorio raiz del proyecto, o" -ForegroundColor Yellow
    Write-Host "   - La carpeta saiku-setup\" -ForegroundColor Yellow
    exit 1
}

# Funcion para mostrar mensaje con colores
function Write-ColoredMessage {
    param($Message, $Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

# Verificar que Docker este disponible
Write-ColoredMessage "Verificando Docker..." "Cyan"
try {
    docker ps | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker no esta ejecutandose"
    }
    Write-ColoredMessage "Docker esta disponible" "Green"
} catch {
    Write-ColoredMessage "Error: Docker no esta disponible o no esta ejecutandose" "Red"
    Write-ColoredMessage "   Inicia Docker Desktop y vuelve a intentar" "Yellow"
    exit 1
}

# Verificar que el contenedor Oracle este ejecutandose
Write-ColoredMessage "Verificando contenedor Oracle '$containerName'..." "Cyan"
$containerStatus = docker ps --filter "name=$containerName" --format "table {{.Names}}\t{{.Status}}" | Select-String $containerName
if (-not $containerStatus) {
    Write-ColoredMessage "Error: El contenedor '$containerName' no esta ejecutandose" "Red"
    Write-ColoredMessage "   Comandos disponibles:" "Yellow"
    Write-ColoredMessage "   docker start $containerName" "Gray"
    Write-ColoredMessage "   docker-compose up -d" "Gray"
    exit 1
}
Write-ColoredMessage "Contenedor Oracle esta activo" "Green"

# Mostrar informacion del script
Write-ColoredMessage "`nCREACION DE VISTAS OPTIMIZADAS PARA SAIKU" "Magenta"
Write-ColoredMessage "================================================" "Magenta"
Write-ColoredMessage "Script SQL: $scriptFullPath" "White"
Write-ColoredMessage "Contenedor: $containerName" "White"
Write-ColoredMessage "================================================`n" "Magenta"

# Preguntar confirmacion
Write-ColoredMessage "Este script creara las siguientes vistas optimizadas:" "Yellow"
Write-ColoredMessage "- V_HECHOS_MATRICULA - Tabla de hechos con campos calculados" "White"
Write-ColoredMessage "- V_DIM_CENTRO - Dimension de centros con jerarquias" "White"
Write-ColoredMessage "- V_DIM_PLAN_ESTUDIO - Dimension academica optimizada" "White"
Write-ColoredMessage "- V_DIM_CURSO_ACADEMICO - Dimension temporal" "White"
Write-ColoredMessage "- V_DIM_SEXO - Dimension demografica normalizada" "White"
Write-ColoredMessage "- V_RESUMEN_EJECUTIVO - Vista agregada para dashboards" "White"

$confirmacion = Read-Host "Deseas continuar? (s/N)"
if ($confirmacion -ne "s" -and $confirmacion -ne "S" -and $confirmacion -ne "si" -and $confirmacion -ne "SI") {
    Write-ColoredMessage "Operacion cancelada por el usuario" "Yellow"
    exit 0
}

# Ejecutar el script SQL
Write-ColoredMessage "Ejecutando script de creacion de vistas..." "Cyan"
Write-ColoredMessage "Esto puede tardar unos minutos..." "Yellow"

try {
    # Ejecutar el script SQL en el contenedor
    Get-Content $scriptFullPath | docker exec -i $containerName sqlplus -S "/ as sysdba"
    
    # Verificar el resultado
    if ($LASTEXITCODE -eq 0) {
        Write-ColoredMessage "VISTAS CREADAS EXITOSAMENTE!" "Green"
        Write-ColoredMessage "================================================" "Green"
        Write-ColoredMessage "PROXIMOS PASOS:" "Cyan"
        Write-ColoredMessage "1. Actualizar el esquema Mondrian (dm_academico.xml)" "White"
        Write-ColoredMessage "2. Reiniciar Pentaho Server" "White"
        Write-ColoredMessage "3. Probar las nuevas funcionalidades en Saiku" "White"
        Write-ColoredMessage "================================================" "Green"
        
        Write-ColoredMessage "COMANDOS UTILES:" "Magenta"
        Write-ColoredMessage "- Reiniciar Pentaho: .\pentaho-server\stop-pentaho.bat; .\pentaho-server\start-pentaho.bat" "Gray"
        Write-ColoredMessage "- Acceder a Saiku: http://localhost:8080/pentaho" "Gray"
        Write-ColoredMessage "- Ver logs: Get-Content .\pentaho-server\tomcat\logs\pentaho.log -Tail 20" "Gray"
        
    } else {
        Write-ColoredMessage "ERROR AL EJECUTAR EL SCRIPT" "Red"
        Write-ColoredMessage "Codigo de salida: $LASTEXITCODE" "Red"
        Write-ColoredMessage "Posibles soluciones:" "Yellow"
        Write-ColoredMessage "- Verificar que el usuario C##SAIKU_USER existe" "White"
        Write-ColoredMessage "- Ejecutar primero: .\setup_saiku_cdb.ps1" "White"
        Write-ColoredMessage "- Verificar conectividad con Oracle" "White"
        exit 1
    }
    
} catch {
    Write-ColoredMessage "ERROR INESPERADO: $($_.Exception.Message)" "Red"
    exit 1
}

Write-ColoredMessage "PROCESO COMPLETADO!" "Green" 