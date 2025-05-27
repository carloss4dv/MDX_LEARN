# DM Académico Faker

Generador de datos sintéticos para un Data Mart Académico utilizando la librería Faker.

## Descripción

Este proyecto genera datos sintéticos para un Data Mart Académico, incluyendo tablas de dimensiones y hechos relacionados con el ámbito académico universitario. Los datos generados son ficticios pero coherentes entre sí, respetando las relaciones entre tablas.

## Estructura del proyecto

```
dm_academico_faker/
├── generators/
│   ├── __init__.py
│   ├── dimension_generators.py
│   └── fact_generators.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── __init__.py
└── main.py
```

## Tablas generadas

### Tablas de dimensión

- D_SEXO
- D_PAIS
- D_TIEMPO
- D_CURSO_ACADEMICO
- D_CURSO_COHORTE
- D_TIPO_ESTUDIO
- D_RAMA_CONOCIMIENTO
- D_CALIFICACION
- D_CONVOCATORIA
- D_TIPO_ACCESO
- D_CLASE_ASIGNATURA
- D_PERSONA
- D_POBLACION
- D_ASIGNATURA
- D_PLAN_ESTUDIO

### Tablas de hechos

- F_MATRICULA
- F_RENDIMIENTO

## Uso

Para generar los datos, ejecutar el script principal:

```bash
python -m dm_academico_faker.main
```

Los datos generados se guardarán en la carpeta `output/`, separados en subcarpetas para dimensiones y hechos.

## Requisitos

- Python 3.6+
- pandas
- numpy
- faker
- tqdm

## Instalación

```bash
pip install -r requirements.txt
```

## TODO

### Tablas de dimensión pendientes

- D_ACUERDO_BILATERAL
- D_AREA_ESTUDIOS_MOVILIDAD
- D_ARTICULO
- D_CAMPUS
- D_CATEGORIA_CUERPO_PDI
- D_CENTRO
- D_CENTRO_DESTINO
- D_CENTRO_ESTUDIO
- D_CENTRO_OTRA_UNIVERSIDAD
- D_CLASE_LIQUIDACION
- D_COLECTIVO_MOVILIDAD
- D_CONVOCATORIA_PREINSCRIPCION
- D_CUPO_ADJUDICACION
- D_DEDICACION
- D_DEDICACION_PROFESOR
- D_DETALLE_CUPO_GENERAL
- D_DOCTORADO_TIPO_BECA
- D_EDAD_EST
- D_ESTADO_ACUERDO_BILATERAL
- D_ESTADO_ADJUDICACION
- D_ESTADO_SOLICITUD_DOCTORADO
- D_ESTUDIO
- D_ESTUDIO_DESTINO
- D_ESTUDIO_JERARQ
- D_ESTUDIO_OTRA_UNIVERSIDAD
- D_ESTUDIO_PROPIO
- D_ESTUDIO_PROPIO_MODALIDAD
- D_ESTUDIO_PROPIO_ORGANO_GEST
- D_ESTUDIO_PROPIO_TIPO
- D_GRUPO
- D_IDIOMA_MOVILIDAD
- D_IDIOMA_NIVEL_MOVILIDAD
- D_MODALIDAD_PLAN_ESTUDIO
- D_NACIONALIDAD
- D_NIVEL_ESTUDIOS_MOVILIDAD
- D_PLAN_ESTUDIO_ANO_DATOS
- D_PLAN_ESTUDIO_ASIGNATURA
- D_POBLACION_CENTRO
- D_PROGRAMA_MOVILIDAD
- D_PROYECTO_INVESTIGACION
- D_RAMA_MACROAREA
- D_RANGO_CREDITO
- D_RANGO_CREDITO_MOVILIDAD
- D_RANGO_EDAD
- D_RANGO_NOTA_ADMISION
- D_RANGO_NOTA_CRUE
- D_RANGO_NOTA_EGRACONS
- D_RANGO_NOTA_NUMERICA
- D_TIPO_ABANDONO
- D_TIPO_ACCESO_PREINSCRIPCION
- D_TIPO_ASIGNATURA
- D_TIPO_CENTRO
- D_TIPO_DOCENCIA
- D_TIPO_EGRESO
- D_TIPO_PROCEDIMIENTO
- D_TITULACION
- D_UNIVERSIDAD

### Tablas de hechos pendientes

- F_COHORTE
- F_DOCTORADO
- F_DOCTORADO_ADMISION
- F_EGRACONS
- F_EGRESADO
- F_ESTUDIANTES_MOVILIDAD_IN
- F_ESTUDIANTES_MOVILIDAD_OUT
- F_ESTUDIO_PROPIO_MATRICULA
- F_OFERTA_ACUERDO_BILATERAL
- F_OFERTA_ADMISION
- F_SOLICITANTE_ADMISION
- F_SOLICITUDES_MOVILIDAD
- F_TABLA_FUSION
- F_TABLA_FUSION_ESTCEN 