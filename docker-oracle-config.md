# Configuración de Oracle en Docker

## 1. Requisitos Previos
- Docker instalado
- Al menos 4GB de RAM disponible
- 10GB de espacio en disco

## 2. Configuración del Contenedor

### 2.1. Usar el archivo docker-compose.yml existente
El proyecto incluye un archivo `docker-compose.yml` preconfigurado que puedes usar directamente:

```bash
docker-compose up -d
```

## 3. Configuración de la Base de Datos

### 3.1. Configuración Automática (Recomendado)

Usa los scripts de configuración automática incluidos:

#### En Windows (PowerShell):
```powershell
.\setup_oracle.ps1
```

#### En Linux/macOS (Bash):
```bash
chmod +x setup_oracle.sh
./setup_oracle.sh
```

**¿Qué hace el script automático?**
- ✅ Espera a que Oracle esté completamente inicializado
- ✅ Crea el tablespace `DMACADEMICO_DAT` automáticamente
- ✅ Crea el usuario `C##DM_ACADEMICO` con todos los permisos necesarios
- ✅ Configura cuotas y privilegios
- ✅ Muestra las variables de entorno para usar en tu aplicación

### 3.2. Configuración Manual (Avanzado)

Si prefieres configurar manualmente o entender el proceso:

#### 3.2.1. Conectar a la Base de Datos
```bash
docker exec -it oracle_db sqlplus sys/YourStrongPassword123@//localhost:1521/XE as sysdba
```

#### 3.2.2. Crear el Tablespace
```sql
CREATE TABLESPACE DMACADEMICO_DAT
DATAFILE '/opt/oracle/oradata/XE/XEPDB1/dmacademico_dat01.dbf'
SIZE 100M
AUTOEXTEND ON
NEXT 10M
MAXSIZE UNLIMITED
EXTENT MANAGEMENT LOCAL
AUTOALLOCATE
SEGMENT SPACE MANAGEMENT AUTO;
```

#### 3.2.3. Crear el Usuario DM_ACADEMICO
```sql
ALTER SESSION SET CONTAINER = XEPDB1;

CREATE USER C##DM_ACADEMICO IDENTIFIED BY YourPassword123;
GRANT CONNECT, RESOURCE, DBA TO C##DM_ACADEMICO;

ALTER USER C##DM_ACADEMICO DEFAULT TABLESPACE DMACADEMICO_DAT;
ALTER USER C##DM_ACADEMICO QUOTA UNLIMITED ON DMACADEMICO_DAT;

-- Permisos adicionales
GRANT CREATE SESSION TO C##DM_ACADEMICO;
GRANT CREATE TABLE TO C##DM_ACADEMICO;
GRANT CREATE VIEW TO C##DM_ACADEMICO;
GRANT CREATE PROCEDURE TO C##DM_ACADEMICO;
GRANT CREATE SEQUENCE TO C##DM_ACADEMICO;
```

## 4. Variables de Entorno y Configuración

### 4.1. Variables para la aplicación
Después de ejecutar el script de configuración automática, usa estas variables:

```env
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE=XEPDB1
ORACLE_USER=C##DM_ACADEMICO
ORACLE_PASSWORD=YourPassword123
```

### 4.2. Configuración de JDBC
```properties
# Configuración de conexión JDBC
jdbc.driver=oracle.jdbc.driver.OracleDriver
jdbc.url=jdbc:oracle:thin:@//localhost:1521/XEPDB1
jdbc.user=C##DM_ACADEMICO
jdbc.password=YourPassword123
```

## 5. Verificar la Instalación

### 5.1. Comprobar el Estado del Contenedor
```bash
docker ps
```

### 5.2. Ver Logs
```bash
docker logs oracle_db
```

## 6. Consideraciones de Seguridad

1. Cambiar las contraseñas por defecto
2. Configurar el firewall para limitar el acceso
3. Realizar copias de seguridad regulares
4. Mantener el sistema actualizado

## 7. Solución de Problemas

### 7.1. Problemas de Memoria
Si el contenedor falla por problemas de memoria:
- Aumentar el `shm_size` en docker-compose.yml
- Ajustar los parámetros de memoria de Oracle

### 7.2. Problemas de Conexión
- Verificar que el puerto 1521 está abierto
- Comprobar las credenciales de conexión
- Verificar que el servicio está en ejecución

## 8. Mantenimiento

### 8.1. Backup
```bash
docker exec oracle_db expdp dm_academico/YourPassword123 DIRECTORY=DATA_PUMP_DIR DUMPFILE=backup.dmp SCHEMAS=dm_academico
```

### 8.2. Restore
```bash
docker exec oracle_db impdp dm_academico/YourPassword123 DIRECTORY=DATA_PUMP_DIR DUMPFILE=backup.dmp SCHEMAS=dm_academico
``` 