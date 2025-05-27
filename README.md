# MDX LEARN - Proyecto de Aprendizaje MDX y Análisis Multidimensional

Proyecto integral para el aprendizaje de consultas MDX, análisis multidimensional y generación de datos sintéticos para un Data Mart Académico.

## Descripción

Este proyecto combina múltiples herramientas y enfoques para el análisis de datos académicos:

1. **Generador de datos sintéticos** (`dm_academico_faker/`) - Utiliza la librería Faker para generar datos coherentes
2. **Notebooks educativos** (`notebooks/`) - Tutoriales progresivos de MDX y análisis multidimensional  
3. **Infraestructura Docker** - Base de datos Oracle para análisis OLAP
4. **Scripts de automatización** - Herramientas para gestión de datos y análisis

## Estructura del proyecto

```
MDX_LEARN/
├── dm_academico_faker/           # Generador de datos sintéticos
│   ├── config/                   # Configuración de conexiones
│   │   └── connection.py
│   ├── generators/               # Generadores especializados
│   │   ├── dimension_generators.py
│   │   ├── fact_generators.py
│   │   ├── fact_generators_acuerdos.py
│   │   ├── fact_generators_doctorado.py
│   │   ├── fact_generators_extended.py
│   │   ├── fact_generators_fusion.py
│   │   ├── fact_generators_mobility.py
│   │   └── fact_generators_priority.py
│   ├── models/                   # Modelos de datos
│   │   ├── dimensions.py
│   │   └── facts.py
│   ├── output/                   # Datos generados
│   │   ├── dimensions/           # Tablas de dimensión (.csv)
│   │   └── facts/                # Tablas de hechos (.csv)
│   ├── utils/                    # Utilidades
│   │   └── helpers.py
│   ├── main.py                   # Script principal de generación
│   ├── upload_to_oracle.py       # Carga de datos a Oracle
│   └── requirements.txt          # Dependencias específicas
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
│   ├── analyze_tables.py         # Análisis de tablas
│   ├── import_tables.bat         # Importación automática
│   ├── clean_database.bat        # Limpieza de BD
│   └── unlock_account.bat        # Gestión de cuentas
├── generators/                   # Generadores adicionales
│   └── fact_generators_fusion.py
├── docker-compose.yml            # Infraestructura Oracle
├── docker-oracle-config.md       # Configuración Docker
├── schema.dbml                   # Modelo de datos
└── requirements.txt              # Dependencias del proyecto
```

## Componentes del proyecto

### 🎲 Generador de datos sintéticos (dm_academico_faker/)

Genera datos sintéticos coherentes para todas las tablas del Data Mart Académico:

**Tablas de dimensión implementadas (81 tablas):**
- Básicas: D_SEXO, D_PAIS, D_TIEMPO, D_CURSO_ACADEMICO, D_CURSO_COHORTE
- Académicas: D_TIPO_ESTUDIO, D_RAMA_CONOCIMIENTO, D_ESTUDIO, D_PLAN_ESTUDIO
- Institucionales: D_CENTRO, D_CAMPUS, D_POBLACION, D_UNIVERSIDAD
- Personas: D_PERSONA, D_CATEGORIA_CUERPO_PDI, D_DEDICACION_PROFESOR
- Evaluación: D_CALIFICACION, D_CONVOCATORIA, D_TIPO_ACCESO
- Movilidad: D_PROGRAMA_MOVILIDAD, D_IDIOMA_MOVILIDAD, D_ACUERDO_BILATERAL
- Y muchas más...

**Tablas de hechos implementadas (16 tablas):**
- F_MATRICULA - Datos de matriculación
- F_RENDIMIENTO - Rendimiento académico
- F_COHORTE - Seguimiento de cohortes
- F_DOCTORADO - Programas de doctorado
- F_EGRESADO - Datos de egresados
- F_ESTUDIANTES_MOVILIDAD_IN/OUT - Movilidad estudiantil
- F_OFERTA_ADMISION - Procesos de admisión
- F_TABLA_FUSION - Datos consolidados
- Y más...

### 📚 Notebooks educativos

Secuencia progresiva de aprendizaje:

1. **01_introduccion_atoti.ipynb** - Fundamentos de Atoti y OLAP
2. **02_consultas_mdx_basicas.ipynb** - Sintaxis básica MDX
3. **03_cubos_multidimensionales.ipynb** - Construcción y análisis de cubos
4. **04_consultas_mdx_avanzadas.ipynb** - Consultas complejas y optimización
5. **05_consultas_sql_analiticas.ipynb** - SQL analítico vs MDX

### 🐳 Infraestructura

- **Oracle Database XE** en Docker para análisis OLAP
- **Esquemas XML** para configuración de cubos
- **Scripts automatizados** para gestión de datos

## Uso

### 🚀 Inicio rápido

1. **Configurar infraestructura:**
   ```bash
   # Levantar Oracle Database
   docker-compose up -d
   ```

2. **Generar datos sintéticos:**
   ```bash
   cd dm_academico_faker
   python main.py
   ```

3. **Cargar datos a Oracle:**
   ```bash
   python upload_to_oracle.py
   ```

4. **Explorar con notebooks:**
   ```bash
   jupyter notebook notebooks/
   ```

### 📊 Generación de datos específica

Para generar solo ciertos tipos de datos:

```python
from dm_academico_faker.generators.dimension_generators import *
from dm_academico_faker.generators.fact_generators import *

# Generar solo dimensiones básicas
d_sexo = generate_d_sexo()
d_pais = generate_d_pais()

# Generar tabla de hechos específica
f_matricula = generate_f_matricula(d_personas, d_estudios, d_tiempo)
```

### 🔧 Scripts de utilidad

```bash
# Limpiar base de datos
scripts/clean_database.bat

# Importar tablas específicas
scripts/import_tables.bat

# Analizar estructura de tablas
python scripts/analyze_tables.py
```

## Requisitos

### Sistema base
- Python 3.8+
- Docker y Docker Compose
- Jupyter Notebook

### Dependencias Python
```bash
pip install -r requirements.txt
```

Principales librerías:
- **pandas** - Manipulación de datos
- **faker** - Generación de datos sintéticos
- **atoti** - Análisis OLAP y MDX
- **cx_Oracle** - Conexión a Oracle Database
- **tqdm** - Barras de progreso

## Configuración avanzada

### 🔧 Variables de entorno

```bash
# Configuración Oracle
ORACLE_USER=C##DM_ACADEMICO
ORACLE_PASSWORD=YourPassword123
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE=XEPDB1

# Configuración Atoti
ATOTI_MAXMEMORY=4G
ATOTI_PORT=9090
```

### 📊 Análisis de cubos OLAP

El proyecto incluye esquemas XML configurados para diferentes áreas de análisis:

- **Academico.xml** - Cubo principal con matriculas, rendimiento, cohortes
- **Movilidad.xml** - Análisis de movilidad estudiantil internacional
- **EstudioPropio.xml** - Estudios propios y formación continua
- **Admision.xml** - Procesos de admisión y preinscripción

### 🎯 Casos de uso

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


*Proyecto desarrollado como parte del Trabajo de Fin de Grado en Ingeniería Informática*
