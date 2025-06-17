# MDX LEARN - Proyecto de Aprendizaje MDX y Análisis Multidimensional

Proyecto integral para el aprendizaje de consultas MDX, análisis multidimensional y generación de datos sintéticos para un Data Mart Académico.

## Descripción

Este proyecto combina múltiples herramientas y enfoques para el análisis de datos académicos:

1. **Generador de datos sintéticos** (`dm_academico_faker/`) - Utiliza la librería Faker para generar datos coherentes
2. **Notebooks educativos** (`notebooks/`) - Tutoriales progresivos de MDX y análisis multidimensional  
3. **Infraestructura Docker** - Base de datos Oracle para análisis OLAP
4. **Scripts de automatización** - Herramientas para gestión de datos y análisis

## 🚀 Inicio Rápido

### 1. Clonar el repositorio

```bash
git clone https://github.com/carloss4dv/MDX_LEARN.git
cd MDX_LEARN
```

### 2. Instalar dependencias

```bash
# Dependencias esenciales
pip install -r requirements.txt

# Para carga de datos con JDBC (recomendado)
pip install JayDeBeApi>=1.2.3

# Para Oracle con cliente nativo (opcional)
pip install cx_Oracle>=8.3.0

# Para PostgreSQL (opcional)
pip install psycopg2-binary>=2.9.0
```

### 3. Configurar infraestructura de base de datos

#### Opción A: Oracle con Docker - Configuración Automática

Para una configuración completamente automática de Oracle Database:

```bash
# Levantar Oracle Database
docker-compose up -d

# Ejecutar script de configuración automática
# En Windows (PowerShell):
.\setup_oracle.ps1

# En Linux/macOS (Bash):
chmod +x setup_oracle.sh
./setup_oracle.sh
```

Una vez se haya configurado la base de datos ejecuta:

```bash
.\scripts\import_tables.bat
```

El script automáticamente:
- ✅ Espera a que Oracle esté listo
- ✅ Crea el tablespace `DMACADEMICO_DAT`  
- ✅ Crea el usuario `C##DM_ACADEMICO` con permisos completos
- ✅ Configura las cuotas y privilegios necesarios
- ✅ Muestra las variables de entorno para el archivo `.env`

#### Opción B: Oracle con configuración manual
```bash
# Levantar Oracle Database
docker-compose up -d

# Configurar manualmente la base de datos
# Ver sección "Configuración manual de Oracle" más abajo
```

#### Opción C: PostgreSQL local
```bash
# Configurar PostgreSQL según sus preferencias
# Ver sección "Configuración de PostgreSQL" más abajo
```

### 4. Configurar variables de entorno

#### Configuración automática (recomendado)

Si has usado los scripts de configuración automática (`setup_oracle.ps1` o `setup_oracle.sh`), las variables de entorno se muestran al final de la ejecución.


#### Configuración manual

Crear archivo `.env` en `dm_academico_faker/`:

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

### 5. Descargar drivers JDBC (método recomendado)

```bash
cd dm_academico_faker
python download_jdbc_drivers.py
```

### 6. Generar y cargar datos

```bash
# Generar datos sintéticos
python main.py

# Cargar a Oracle usando JDBC (recomendado)
python upload_to_db.py --db oracle

# O cargar a PostgreSQL
python upload_to_db.py --db postgresql

# O usar método tradicional con cx_Oracle
python upload_to_oracle.py
```

### 7. Explorar con notebooks

```bash
# Desde el directorio raíz
jupyter notebook notebooks/
```

## Estructura del proyecto

```
MDX_LEARN/
├── dm_academico_faker/           # Generador de datos sintéticos
│   ├── config/                   # Configuración de conexiones
│   │   ├── connection.py
│   │   └── database.ini          # ⭐ Configuración multi-BD
│   ├── generators/               # Generadores especializados
│   │   ├── dimension_generators.py
│   │   ├── fact_generators.py
│   │   └── [otros generadores...]
│   ├── models/                   # Modelos de datos
│   │   ├── dimensions.py
│   │   └── facts.py
│   ├── output/                   # Datos generados
│   │   ├── dimensions/           # Tablas de dimensión (.csv)
│   │   └── facts/                # Tablas de hechos (.csv)
│   ├── utils/                    # Utilidades
│   │   └── helpers.py
│   ├── lib/                      # ⭐ Drivers JDBC
│   │   ├── README.md
│   │   ├── ojdbc8.jar           # Driver Oracle
│   │   └── postgresql-42.5.0.jar # Driver PostgreSQL
│   ├── main.py                   # Script principal de generación
│   ├── upload_to_db.py          # ⭐ Carga JDBC (Oracle/PostgreSQL)
│   ├── upload_to_oracle.py      # Carga tradicional Oracle
│   ├── download_jdbc_drivers.py # ⭐ Descarga automática drivers
│   ├── requirements.txt          # Dependencias específicas
│   └── README_UPLOAD.md         # ⭐ Guía completa de carga
├── notebooks/                    # Notebooks educativos
│   ├── 01_introduccion_atoti.ipynb
│   ├── 02_consultas_mdx_basicas.ipynb
│   ├── 03_cubos_multidimensionales.ipynb
│   ├── 04_consultas_mdx_avanzadas.ipynb
│   └── 05_consultas_sql_analiticas.ipynb
├── data/                         # Esquemas y configuraciones
│   ├── Academico.xml             # Esquema OLAP académico
│   ├── Admision.xml              # Esquema OLAP admisión
│   ├── EstudioPropio.xml         # Esquema OLAP estudios propios
│   ├── Movilidad.xml             # Esquema OLAP movilidad
│   ├── dm_academico.sql          # DDL base de datos
│   └── clean_database.sql        # Scripts de limpieza
├── scripts/                      # Scripts de automatización
├── init_scripts/                 # ⭐ Scripts SQL de configuración
│   ├── create_tablespace.sql     # Creación de tablespace
│   └── create_user.sql           # Creación de usuario Oracle
├── setup_oracle.ps1              # ⭐ Configuración automática (Windows)
├── setup_oracle.sh               # ⭐ Configuración automática (Linux/macOS)
├── setup_oracle.bat              # ⭐ Configuración simple (Windows)
├── .env.example                  # ⭐ Variables de entorno de ejemplo
├── docker-compose.yml            # Infraestructura Oracle
├── docker-oracle-config.md       # Configuración Docker
├── ORACLE_SETUP_README.md        # ⭐ Guía de configuración automática
├── requirements.txt              # ⭐ Dependencias del proyecto
└── README.md                     # Este archivo
```

## 📊 Métodos de Carga de Datos

### Método 1: JDBC (Recomendado) ⭐

**Ventajas:**
- ✅ No requiere clientes nativos de base de datos
- ✅ Multiplataforma (Windows, Linux, macOS)
- ✅ Soporte para Oracle y PostgreSQL
- ✅ Configuración flexible y automática

```bash
# Oracle
python upload_to_db.py --db oracle

# PostgreSQL
python upload_to_db.py --db postgresql

# Con opciones avanzadas
python upload_to_db.py --db oracle --clean --batch-size 500
```

### Método 2: Cliente Nativo Oracle

**Para máximo rendimiento con Oracle:**
```bash
python upload_to_oracle.py
```

**Requisitos adicionales:**
- Oracle Instant Client instalado
- cx_Oracle>=8.3.0

### Configuración de PostgreSQL

Si desea usar PostgreSQL en lugar de Oracle:

1. **Instalar PostgreSQL** (si no está instalado)
2. **Crear base de datos:**
   ```sql
   CREATE DATABASE dm_academico;
   ```
3. **Configurar variables de entorno** en `.env`
4. **Ejecutar scripts de creación** (adaptar DDL de Oracle a PostgreSQL)

## Componentes del proyecto

### 🎲 Generador de datos sintéticos (dm_academico_faker/)

Genera datos sintéticos coherentes para todas las tablas del Data Mart Académico:

**Estadísticas:**
- **86 tablas totales** (70 dimensiones + 16 hechos)
- **Integridad referencial completa**
- **Datos coherentes** usando Faker
- **Soporte para múltiples idiomas** y regiones

**Tablas principales:**
- **Dimensiones básicas:** D_SEXO, D_PAIS, D_TIEMPO, D_CURSO_ACADEMICO
- **Dimensiones académicas:** D_TIPO_ESTUDIO, D_RAMA_CONOCIMIENTO, D_ESTUDIO
- **Dimensiones institucionales:** D_CENTRO, D_CAMPUS, D_UNIVERSIDAD
- **Tablas de hechos:** F_MATRICULA, F_RENDIMIENTO, F_COHORTE, F_DOCTORADO

### 📚 Notebooks educativos

Secuencia progresiva de aprendizaje de MDX:

1. **01_introduccion_atoti.ipynb** - Fundamentos de Atoti y OLAP
2. **02_consultas_mdx_basicas.ipynb** - Sintaxis básica MDX
3. **03_cubos_multidimensionales.ipynb** - Construcción y análisis de cubos
4. **04_consultas_mdx_avanzadas.ipynb** - Consultas complejas y optimización
5. **05_consultas_sql_analiticas.ipynb** - SQL analítico vs MDX

### 🐳 Infraestructura

- **Oracle Database XE** en Docker para análisis OLAP
- **Esquemas XML** configurados para diferentes áreas de análisis
- **Scripts automatizados** para gestión de datos
- **Soporte multiplataforma** con drivers JDBC

## 📋 Configuración Avanzada

### Variables de entorno completas

```env
# Oracle Database
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE=XEPDB1           # O usar SID
ORACLE_USER=C##DM_ACADEMICO
ORACLE_PASSWORD=YourPassword123

# PostgreSQL (alternativa)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=dm_academico
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Configuración Atoti
ATOTI_MAXMEMORY=4G
ATOTI_PORT=9090
```

### Opciones de línea de comandos

```bash
# Ver ayuda completa
python upload_to_db.py --help

# Limpiar y recargar
python upload_to_db.py --db oracle --clean

# Ajustar rendimiento
python upload_to_db.py --batch-size 500

# Combinar opciones
python upload_to_db.py --db postgresql --clean --batch-size 2000
```

### Configuración en database.ini

El archivo `dm_academico_faker/config/database.ini` permite:
- Definir parámetros de conexión por tipo de BD
- Configurar orden de carga de tablas
- Ajustar tamaños de lote por tabla
- Opciones avanzadas de rendimiento

## 🛠️ Solución de Problemas

### Problemas comunes y soluciones

#### 1. Error: "No module named 'faker'"
```bash
pip install -r requirements.txt
```

#### 2. Error: "JayDeBeApi no está instalado"
```bash
pip install JayDeBeApi>=1.5.0
```

#### 3. Error: "Driver JDBC no encontrado"
```bash
cd dm_academico_faker
python download_jdbc_drivers.py
```

#### 4. Error de conexión Oracle
- Verificar que Docker esté ejecutándose: `docker ps`
- Revisar variables de entorno en `.env`
- Verificar puertos disponibles

#### 5. Problemas de rendimiento
- Reducir batch size: `--batch-size 500`
- Verificar memoria disponible
- Usar `--clean` solo cuando sea necesario

### Logs y monitoreo

- **Logs de carga:** `dm_academico_faker/upload.log`
- **Trazas de generación:** `dm_academico_faker/trazas.txt`
- **Progreso en tiempo real:** Barras de progreso durante la ejecución

## 📊 Análisis de cubos OLAP

### Esquemas XML configurados

- **Academico.xml** - Cubo principal con matriculas, rendimiento, cohortes
- **Movilidad.xml** - Análisis de movilidad estudiantil internacional  
- **EstudioPropio.xml** - Estudios propios y formación continua
- **Admision.xml** - Procesos de admisión y preinscripción

### Casos de uso implementados

1. **Análisis de rendimiento académico**
   - Evolución temporal de calificaciones
   - Análisis por rama de conocimiento
   - Drill-down desde centro hasta asignatura

2. **Seguimiento de cohortes**
   - Tasas de abandono y permanencia
   - Tiempo hasta graduación
   - Análisis demográfico

3. **Movilidad internacional**
   - Flujos de estudiantes entrantes/salientes
   - Acuerdos bilaterales más activos
   - Distribución geográfica

4. **Gestión institucional**
   - Ocupación por centros y campus
   - Planificación de recursos
   - Indicadores de calidad

## 📖 Documentación

### Guías específicas

- **[Carga de datos](dm_academico_faker/README_UPLOAD.md)** - Guía completa de carga con JDBC
- **[Drivers JDBC](dm_academico_faker/lib/README.md)** - Información sobre drivers
- **[Configuración Docker](docker-oracle-config.md)** - Configuración detallada de Oracle

### Scripts útiles

```bash
# Análisis de tablas generadas
python scripts/analyze_tables.py

# Limpieza de base de datos
scripts/clean_database.bat   # Windows
scripts/clean_database.sh    # Linux/macOS

# Importación específica
scripts/import_tables.bat
```

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Cree una rama para su funcionalidad: `git checkout -b nueva-funcionalidad`
3. Commit sus cambios: `git commit -am 'Añadir nueva funcionalidad'`
4. Push a la rama: `git push origin nueva-funcionalidad`
5. Envíe un Pull Request


## 🎯 Próximas mejoras

- [ ] Soporte para MySQL y SQL Server
- [ ] Interfaz web para configuración
- [ ] Métricas de calidad de datos
- [ ] Exportación a diferentes formatos
- [ ] Integración con herramientas BI adicionales

---

*Proyecto desarrollado para el aprendizaje de consultas MDX y análisis multidimensional en entornos educativos.*
*Desarrollado como parte del Trabajo de Fin de Grado en Ingeniería Informática.*
