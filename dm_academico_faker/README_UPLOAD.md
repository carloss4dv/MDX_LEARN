# Carga de Datos a Oracle

Este documento explica cómo cargar los datos generados en el Data Mart Académico a una base de datos Oracle.

## Requisitos previos

1. Oracle Database (cualquier versión compatible con cx_Oracle)
2. Oracle Instant Client instalado
3. Python 3.6 o superior
4. Las siguientes bibliotecas de Python:
   - cx_Oracle
   - pandas
   - tqdm
   - python-dotenv

## Configuración

1. Cree un archivo `.env` en el directorio raíz del proyecto con el siguiente contenido:

```
# Configuración de Oracle Instant Client
ORACLE_CLIENT_PATH=C:\ruta\a\instantclient

# Conexión a la base de datos Oracle
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=XEPDB1
ORACLE_USER=C##DM_ACADEMICO
ORACLE_PASSWORD=YourPassword123@
```

2. Actualice los valores con su configuración específica:
   - `ORACLE_CLIENT_PATH`: Ruta a su instalación de Oracle Instant Client
   - `ORACLE_HOST`: Servidor donde se encuentra la base de datos
   - `ORACLE_PORT`: Puerto (por defecto 1521)
   - `ORACLE_SERVICE_NAME`: Nombre del servicio o SID
   - `ORACLE_USER`: Usuario de la base de datos
   - `ORACLE_PASSWORD`: Contraseña del usuario

## Estructura de la base de datos

Asegúrese de que la base de datos tenga las tablas necesarias creadas antes de ejecutar el script de carga. 
Puede utilizar el script SQL proporcionado `data/dm_academico_modified.sql` para crear todas las tablas.

## Ejecución

1. Primero, genere los datos utilizando el script principal:

```bash
python main.py
```

2. Una vez generados todos los datos, ejecute el script de carga:

```bash
python upload_to_oracle.py
```

Este script seguirá el siguiente proceso:
- Conectará a la base de datos Oracle
- Cargará primero las tablas de dimensión sin dependencias
- Luego cargará las tablas de dimensión con dependencias
- Finalmente cargará las tablas de hechos

## Solución de problemas

### Error de conexión a Oracle
- Verifique que Oracle esté en ejecución
- Compruebe los datos de conexión en el archivo `.env`
- Asegúrese de que Oracle Instant Client esté correctamente instalado y configurado

### Errores durante la carga de datos
- El script intentará identificar filas específicas que causan errores
- Revise las restricciones de clave primaria y foránea
- Verifique que las tablas destino tengan la estructura correcta

## Orden de carga

El script respeta el siguiente orden para mantener la integridad referencial:

1. Tablas de dimensión sin dependencias (d_sexo, d_pais, etc.)
2. Tablas de dimensión con dependencias (d_poblacion, d_centro, etc.)
3. Tablas de hechos (f_matricula, f_rendimiento, etc.)

Este orden garantiza que todas las claves foráneas existan antes de cargar las tablas que las referencian. 