# Configuración de Oracle en Docker

## 1. Requisitos Previos
- Docker instalado
- Al menos 4GB de RAM disponible
- 10GB de espacio en disco

## 2. Configuración del Contenedor

### 2.1. Crear el archivo docker-compose.yml
```yaml
version: '3'
services:
  oracle:
    image: container-registry.oracle.com/database/express:latest
    container_name: oracle_db
    environment:
      - ORACLE_PWD=YourStrongPassword123
      - ORACLE_CHARACTERSET=AL32UTF8
    ports:
      - "1521:1521"
    volumes:
      - oracle_data:/opt/oracle/oradata
    shm_size: '2gb'
    restart: unless-stopped

volumes:
  oracle_data:
```

### 2.2. Variables de Entorno
- `ORACLE_PWD`: Contraseña para los usuarios SYS y SYSTEM
- `ORACLE_CHARACTERSET`: Juego de caracteres de la base de datos
- `shm_size`: Tamaño de la memoria compartida

## 3. Iniciar el Contenedor

```bash
docker-compose up -d
```

## 4. Configuración de la Base de Datos

### 4.1. Conectar a la Base de Datos
```bash
docker exec -it oracle_db sqlplus sys/YourStrongPassword123@//localhost:1521/XE as sysdba
```

### 4.2. Crear el Esquema DM_ACADEMICO
```sql
ALTER SESSION SET CONTAINER = XEPDB1;

CREATE USER C##dm_academico IDENTIFIED BY YourPassword123;
GRANT CONNECT, RESOURCE, DBA TO C##dm_academico;

ALTER USER C##dm_academico DEFAULT TABLESPACE DMACADEMICO_DAT;
ALTER USER C##dm_academico QUOTA UNLIMITED ON DMACADEMICO_DAT;
```

### 4.3. Configuración de JDBC
```properties
# Configuración de conexión JDBC para Atoti
jdbc.driver=oracle.jdbc.driver.OracleDriver
jdbc.url=jdbc:oracle:thin:@//localhost:1521/XE
jdbc.user=dm_academico
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