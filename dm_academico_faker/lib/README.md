# Drivers JDBC

Este directorio contiene los drivers JDBC necesarios para conectar con diferentes bases de datos.

## Drivers incluidos

### Oracle Database
- **ojdbc8.jar** - Driver JDBC para Oracle (Java 8+)
- **ojdbc11.jar** - Driver JDBC para Oracle (Java 11+)
- **ojdbc17.jar** - Driver JDBC para Oracle (Java 17+) (Recomendado para Oracle 21c)
### PostgreSQL  
- **postgresql-42.5.0.jar** - Driver JDBC para PostgreSQL

## Descarga automática

Para descargar automáticamente todos los drivers:

```bash
cd dm_academico_faker
python download_jdbc_drivers.py
```

El script descargará automáticamente:
- **ojdbc8.jar** desde Maven Central (Oracle JDBC para Java 8+)
- **ojdbc11.jar** desde Maven Central (Oracle JDBC para Java 11+)
- **ojdbc17.jar** desde Maven Central (Oracle JDBC para Java 17+)
- **postgresql-42.5.0.jar** desde Maven Central (PostgreSQL JDBC)

**Características del script:**
- ✅ Verifica archivos existentes antes de descargar
- ✅ Muestra progreso de descarga
- ✅ Permite sobrescribir archivos existentes
- ✅ Manejo de errores robusto
- ✅ Descarga desde repositorios oficiales

## Descarga manual

### Oracle
1. Visite: https://www.oracle.com/database/technologies/maven-central-guide.html
2. Descargue ojdbc8.jar u ojdbc11.jar según su versión de Java
3. Coloque el archivo en este directorio

### PostgreSQL
1. Visite: https://jdbc.postgresql.org/download.html
2. Descargue postgresql-42.5.0.jar o la versión más reciente
3. Coloque el archivo en este directorio

## Uso

Los scripts `upload_to_db.py` buscarán automáticamente los drivers en este directorio.

## Licencias

- **Oracle JDBC**: Sujeto a la licencia de Oracle. Consulte los términos en el sitio web de Oracle.
- **PostgreSQL JDBC**: Licencia BSD de código abierto.
