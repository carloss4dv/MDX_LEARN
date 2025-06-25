# =================================================================================================================
# AUTOR: Carlos de Vera Sanz
# FECHA: 20-06-2025
# DESCRIPCIÓN: Script de PowerShell para ejecutar el script SQL de configuración de Saiku (setup_saiku_cdb.sql)
#              usando 'docker exec' y conectándose como SYSDBA sin solicitar credenciales.
#
# USO:
# 1. Asegúrate de que Docker está en ejecución y el contenedor de Oracle (ej. 'oracle-xe') está activo.
# 2. Ejecuta este script desde una terminal de PowerShell.
# =================================================================================================================

# Configuración
$containerName = "oracle_db" # <-- ¡IMPORTANTE! Cambia esto si tu contenedor tiene otro nombre.

# Definir la cadena de conexión y el script a ejecutar
$sqlScriptPath = "setup_saiku_cdb.sql"
$connectionString = "/ as sysdba"

# Mensaje informativo
Write-Host "Intentando ejecutar '$sqlScriptPath' en el contenedor Docker '$containerName' como SYSDBA..."

# Verificar si el script SQL existe
if (-not (Test-Path $sqlScriptPath)) {
    Write-Host "Error: No se encuentra el fichero '$sqlScriptPath'. Asegúrate de que estás en el directorio correcto."
    exit 1
}

# Usar 'docker exec' para ejecutar el script SQL dentro del contenedor
# Get-Content lee el script y lo pasa por la entrada estándar a sqlplus
Get-Content $sqlScriptPath | docker exec -i $containerName sqlplus -S $connectionString

# Comprobar el resultado
if ($LASTEXITCODE -eq 0) {
    Write-Host "Script '$sqlScriptPath' ejecutado con éxito en el contenedor '$containerName'."
} else {
    Write-Host "Error al ejecutar el script '$sqlScriptPath'. Código de salida: $LASTEXITCODE"
    Write-Host "Por favor, revisa la salida de Docker/SQL*Plus para más detalles."
}
