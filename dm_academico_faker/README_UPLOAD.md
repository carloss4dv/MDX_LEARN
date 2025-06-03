# Carga de Datos del Data Mart Académico

Esta guía detalla cómo cargar los datos generados sintéticamente en diferentes sistemas de bases de datos, incluyendo Oracle Database y PostgreSQL.

## 🚀 Inicio Rápido

### 1. Instalar dependencias

```bash
# Dependencias básicas (siempre necesarias)
pip install -r requirements.txt

# Para Oracle con JDBC (recomendado)
pip install JayDeBeApi>=1.2.3

# Para Oracle con cliente nativo (opcional)
pip install cx_Oracle>=8.3.0

# Para PostgreSQL
pip install psycopg2-binary>=2.9.0
# O para JDBC con PostgreSQL
pip install JayDeBeApi>=1.2.3
```

### 2. Descargar drivers JDBC (método recomendado)

```bash
# Descarga automática de drivers
python download_jdbc_drivers.py
```

### 3. Configurar variables de entorno

Cree un archivo `.env` en el directorio `dm_academico_faker/`:

```env
# Para Oracle Database
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE=XEPDB1
ORACLE_USER=C##DM_ACADEMICO
ORACLE_PASSWORD=YourPassword123

# Para PostgreSQL (opcional)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=dm_academico
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

### 4. Generar y cargar datos

```bash
# 1. Generar datos sintéticos
python main.py

# 2. Cargar a Oracle usando JDBC (recomendado)
python upload_to_db.py --db oracle

# O cargar a PostgreSQL
python upload_to_db.py --db postgresql

# O usar el método tradicional con cx_Oracle
python upload_to_oracle.py
```

## 📊 Métodos de Carga Disponibles

### Método 1: JDBC (Recomendado) ⭐

**Ventajas:**
- ✅ No requiere instalar clientes nativos de base de datos
- ✅ Funciona en cualquier sistema operativo
- ✅ Soporte para Oracle y PostgreSQL
- ✅ Detección automática de drivers
- ✅ Configuración flexible

**Uso:**
```bash
# Oracle
python upload_to_db.py --db oracle

# PostgreSQL  
python upload_to_db.py --db postgresql

# Con opciones avanzadas
python upload_to_db.py --db oracle --clean --batch-size 500
```

**Requisitos:**
- Python package: `JayDeBeApi>=1.2.3`
- Drivers JDBC (se descargan automáticamente)

### Método 2: Cliente Nativo Oracle (cx_Oracle)

**Ventajas:**
- ✅ Máximo rendimiento para Oracle
- ✅ Soporte completo de características Oracle

**Desventajas:**
- ❌ Requiere Oracle Instant Client
- ❌ Configuración específica del sistema
- ❌ Solo funciona con Oracle

**Uso:**
```bash
python upload_to_oracle.py
```

**Requisitos:**
- Oracle Instant Client
- Python package: `cx_Oracle>=8.3.0`
- Variables de entorno configuradas

### Método 3: Cliente Nativo PostgreSQL

**Para PostgreSQL con cliente nativo:**
```bash
# Instalar psycopg2
pip install psycopg2-binary>=2.9.0

# Usar upload_to_db.py con PostgreSQL
python upload_to_db.py --db postgresql
```

## 🔧 Configuración Avanzada

### Archivo de configuración

El archivo `config/database.ini` permite configurar:

- Parámetros de conexión por tipo de base de datos
- Orden de carga de tablas
- Configuración de lotes
- Opciones avanzadas de rendimiento

### Variables de entorno soportadas

#### Oracle Database
```env
ORACLE_HOST=localhost          # Servidor Oracle
ORACLE_PORT=1521              # Puerto (por defecto 1521)
ORACLE_SERVICE=XEPDB1         # Nombre del servicio/SID
ORACLE_USER=C##DM_ACADEMICO   # Usuario de base de datos
ORACLE_PASSWORD=YourPassword123 # Contraseña
```

#### PostgreSQL
```env
POSTGRES_HOST=localhost       # Servidor PostgreSQL
POSTGRES_PORT=5432           # Puerto (por defecto 5432)
POSTGRES_DB=dm_academico     # Nombre de la base de datos
POSTGRES_USER=postgres       # Usuario
POSTGRES_PASSWORD=postgres   # Contraseña
```

### Opciones de línea de comandos

```bash
# Mostrar ayuda
python upload_to_db.py --help

# Especificar tipo de base de datos
python upload_to_db.py --db [oracle|postgresql]

# Limpiar tablas antes de cargar
python upload_to_db.py --clean

# Configurar tamaño de lote
python upload_to_db.py --batch-size 1000

# Combinar opciones
python upload_to_db.py --db oracle --clean --batch-size 500
```

## 📋 Estructura de Datos

### Orden de carga

El sistema respeta automáticamente las dependencias entre tablas:

1. **Dimensiones básicas** (sin dependencias)
   - d_sexo, d_pais, d_tiempo, d_curso_academico
   - d_tipo_estudio, d_rama_conocimiento, d_calificacion
   - Y otras dimensiones independientes

2. **Dimensiones dependientes**
   - d_poblacion (requiere d_pais)
   - d_centro (requiere d_poblacion, d_campus)
   - d_estudio (requiere d_tipo_estudio, d_rama_conocimiento)
   - Y otras con dependencias

3. **Tablas de hechos**
   - f_matricula, f_rendimiento, f_cohorte
   - f_doctorado, f_egresado, f_movilidad
   - Y todas las demás tablas de hechos

### Estadísticas del Data Mart

- **86 tablas totales**
  - 70 tablas de dimensión
  - 16 tablas de hechos
- **Integridad referencial completa**
- **Datos sintéticos coherentes** generados con Faker

## 🛠️ Solución de Problemas

### Error: "JayDeBeApi no está instalado"

```bash
pip install JayDeBeApi>=1.2.3
```

### Error: "Driver JDBC no encontrado"

```bash
# Descargar drivers automáticamente
python download_jdbc_drivers.py

# O descargar manualmente:
# Oracle: https://www.oracle.com/database/technologies/maven-central-guide.html
# PostgreSQL: https://jdbc.postgresql.org/download.html
```

### Error de conexión a Oracle

1. Verificar que Oracle esté ejecutándose:
   ```bash
   docker ps  # Si usa Docker
   ```

2. Verificar variables de entorno en `.env`

3. Probar diferentes formatos de conexión:
   - SID: `jdbc:oracle:thin:@host:port:service`
   - Service name: `jdbc:oracle:thin:@//host:port/service`

### Error de conexión a PostgreSQL

1. Verificar que PostgreSQL esté ejecutándose
2. Confirmar que la base de datos existe
3. Verificar permisos de usuario

### Problemas de rendimiento

1. Reducir tamaño de lote:
   ```bash
   python upload_to_db.py --batch-size 500
   ```

2. Usar configuración específica en `database.ini`

3. Para tablas muy grandes, considerar:
   - Dividir la carga en múltiples ejecuciones
   - Usar `--clean` solo cuando sea necesario
   - Optimizar índices en la base de datos

## 📈 Monitoreo y Logs

### Información durante la carga

El script muestra información detallada:
- ✅ Conexión establecida
- 🔄 Progreso de carga por tabla
- 📊 Estadísticas finales
- ⚠️ Advertencias y errores

### Archivos de log

Los logs se guardan en:
- `upload.log` - Log general de la aplicación
- `trazas.txt` - Trazas detalladas de la generación

### Verificación post-carga

```sql
-- Verificar conteos de filas
SELECT table_name, num_rows 
FROM user_tables 
WHERE table_name LIKE 'D_%' OR table_name LIKE 'F_%'
ORDER BY table_name;

-- Verificar integridad referencial
SELECT constraint_name, status 
FROM user_constraints 
WHERE constraint_type = 'R' AND status = 'DISABLED';
```

## 🔗 Recursos Adicionales

### Documentación relacionada

- [README principal](../README.md) - Documentación completa del proyecto
- [Generación de datos](README.md) - Guía del generador de datos sintéticos
- [Drivers JDBC](lib/README.md) - Información sobre drivers JDBC

### Enlaces útiles

- [Oracle JDBC Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/21/jjdbc/)
- [PostgreSQL JDBC Documentation](https://jdbc.postgresql.org/documentation/)
- [JayDeBeApi Documentation](https://github.com/baztian/jaydebeapi)

---

*Esta guía es parte del proyecto MDX_LEARN para el aprendizaje de consultas MDX y análisis multidimensional.* 