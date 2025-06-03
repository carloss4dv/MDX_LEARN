# Drivers JDBC

Este directorio contiene los drivers JDBC necesarios para conectar con diferentes bases de datos.

## Drivers incluidos

### Oracle Database
- **ojdbc8.jar** - Driver JDBC para Oracle (Java 8+)
- **ojdbc11.jar** - Driver JDBC para Oracle (Java 11+)

### PostgreSQL  
- **postgresql-42.5.0.jar** - Driver JDBC para PostgreSQL

## Descarga automática

Para descargar automáticamente los drivers:

```bash
python download_jdbc_drivers.py
```

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
