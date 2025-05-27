# Análisis Detallado de Tablas DM_ACADEMICO

## Resumen

- Número total de tablas: 89
- Tablas D_ (Dimensiones): 73
- Tablas F_ (Hechos): 16

## Tablas de Dimensión


### D_ACUERDO_BILATERAL

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_ACUERDO_BILATERAL | NUMBER(*) | ✓ |  |  |
| ID_ACUERDO_BILATERAL_NK | NUMBER(*) |  |  |  |
| NOMBRE_ACUERDO_BILATERAL | VARCHAR2(220 CHAR) |  |  |  |
| ID_ACUERDO_BILATERAL_DESCR | NUMBER(*) |  |  |  |

### D_AREA_ESTUDIOS_MOVILIDAD

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_AREA_ESTUDIOS_MOVILIDAD | NUMBER(*) | ✓ |  |  |
| NOMBRE_AREA_ESTUDIOS_MOV | VARCHAR2(850 CHAR) |  |  |  |
| ID_AREA_ESTUDIOS_MOVILIDAD_NK | NUMBER(*) |  |  |  |

### D_ARTICULO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_ARTICULO | NUMBER(*) | ✓ |  |  |
| NOMBRE_ARTICULO | VARCHAR2(300 CHAR) |  |  |  |

### D_ASIGNATURA

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_ASIGNATURA | NUMBER(*) | ✓ | ✓ | D_ASIGNATURA(ID_ASIGNATURA) |
| NOMBRE_ASIGNATURA | VARCHAR2(200 CHAR) |  |  |  |
| ID_ASIGNATURA_NK | NUMBER(*) |  | ✓ | D_ASIGNATURA(ID_ASIGNATURA) |

### D_CALIFICACION

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CALIFICACION | NUMBER(*) | ✓ | ✓ | D_CALIFICACION(ID_CALIFICACION) |
| NOMBRE_CALIFICACION | VARCHAR2(50 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |
| ID_CALIFICACION_NK | VARCHAR2(2 CHAR) |  | ✓ | D_CALIFICACION(ID_CALIFICACION) |

### D_CAMPUS

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CAMPUS | NUMBER(*) | ✓ |  |  |
| NOMBRE_CAMPUS | VARCHAR2(30 CHAR) |  |  |  |

### D_CATEGORIA_CUERPO_PDI

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CATEGORIA_CUERPO_ESCALA | NUMBER(*) |  |  |  |
| NOMBRE_CATEGORIA_CUERPO_ESCALA | VARCHAR2(70 CHAR) |  |  |  |
| ID_CAT_CPO_ESC_DESCR | NUMBER(*) |  |  |  |

### D_CENTRO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CENTRO | NUMBER(*) | ✓ | ✓ | D_CENTRO(ID_CENTRO) |
| ID_CAMPUS | NUMBER(*) |  |  |  |
| NOMBRE_CAMPUS | VARCHAR2(30 CHAR) |  |  |  |
| ID_TIPO_CENTRO | NUMBER(*) |  |  |  |
| NOMBRE_TIPO_CENTRO | VARCHAR2(30 CHAR) |  |  |  |
| ID_POBLACION | NUMBER(*) |  | ✓ | D_POBLACION(ID_POBLACION) |
| NOMBRE_POBLACION | VARCHAR2(50 CHAR) |  |  |  |
| ID_CENTRO_NK | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_CENTRO_DESCR | NUMBER(*) |  |  |  |
| NOMBRE_CENTRO | VARCHAR2(295 CHAR) |  |  |  |
| ORD_NOMBRE_CENTRO | VARCHAR2(254 CHAR) |  |  |  |
| NOMBRE_CENTRO_EXT | VARCHAR2(150 CHAR) |  |  |  |

### D_CENTRO_DESTINO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CENTRO_OTRA_UNIVERSIDAD | NUMBER(*) | ✓ |  |  |
| NOMBRE_CENTRO_OTRA_UNIVERSIDAD | VARCHAR2(100 CHAR) |  |  |  |
| ID_UNIVERSIDAD | NUMBER(*) |  | ✓ | D_UNIVERSIDAD(ID_UNIVERSIDAD) |
| NOMBRE_UNIVERSIDAD | VARCHAR2(80 CHAR) |  |  |  |
| ID_CENTRO_OTRA_UNIVERSIDAD_NK | VARCHAR2(8 CHAR) |  | ✓ | D_CENTRO_DESTINO(ID_CENTRO_OTRA_UNIVERSIDAD) |
| ID_UNIVERSIDAD_NK | VARCHAR2(3 CHAR) |  | ✓ | D_UNIVERSIDAD(ID_UNIVERSIDAD) |

### D_CENTRO_ESTUDIO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_UNIVERSIDAD | NUMBER(*) |  | ✓ | D_UNIVERSIDAD(ID_UNIVERSIDAD) |
| NOMBRE_UNIVERSIDAD | VARCHAR2(80 CHAR) |  |  |  |
| ID_CENTRO | NUMBER(*) | ✓ | ✓ | D_CENTRO(ID_CENTRO) |
| ID_PLAN_ESTUDIO | NUMBER(*) |  |  |  |
| NOMBRE_CENTRO_EXT | VARCHAR2(150 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |
| NOMBRE_CENTRO | VARCHAR2(254 CHAR) |  |  |  |
| NOMBRE_PLAN_ESTUDIO | VARCHAR2(350 CHAR) |  |  |  |
| NOMBRE_PLAN_ESTUDIO_EXT | VARCHAR2(350 CHAR) |  |  |  |

### D_CENTRO_OTRA_UNIVERSIDAD

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CENTRO_OTRA_UNIVERSIDAD | NUMBER(*) | ✓ |  |  |
| ID_CENTRO_OTRA_UNIVERSIDAD_NK | VARCHAR2(8 CHAR) |  | ✓ | D_CENTRO_DESTINO(ID_CENTRO_OTRA_UNIVERSIDAD) |
| NOMBRE_CENTRO_OTRA_UNIVERSIDAD | VARCHAR2(600 CHAR) |  |  |  |
| ID_UNIVERSIDAD | NUMBER(*) |  | ✓ | D_UNIVERSIDAD(ID_UNIVERSIDAD) |
| ID_UNIVERSIDAD_NK | VARCHAR2(3 CHAR) |  | ✓ | D_UNIVERSIDAD(ID_UNIVERSIDAD) |
| NOMBRE_UNIVERSIDAD | VARCHAR2(80 CHAR) |  |  |  |

### D_CLASE_ASIGNATURA

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CLASE_ASIGNATURA | NUMBER(*) | ✓ | ✓ | D_CLASE_ASIGNATURA(ID_CLASE_ASIGNATURA) |
| NOMBRE_CLASE_ASIGNATURA | VARCHAR2(240 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |
| ID_CLASE_ASIGNATURA_NK | CHAR(1 CHAR) |  | ✓ | D_CLASE_ASIGNATURA(ID_CLASE_ASIGNATURA) |

### D_CLASE_LIQUIDACION

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CLASE_LIQUIDACION | NUMBER(*) | ✓ |  |  |
| ID_CURSO_ACADEMICO_NK | NUMBER(*) |  | ✓ | D_CURSO_COHORTE(ID_CURSO_ACADEMICO) |
| ID_CLASE_LIQUIDACION_NK | NUMBER(*) |  |  |  |
| NOMBRE_CLASE_LIQUIDACION | VARCHAR2(240 CHAR) |  |  |  |
| ID_CLASE_LIQUIDACION_DESCR | NUMBER(*) |  |  |  |

### D_COLECTIVO_MOVILIDAD

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_COLECTIVO_MOVILIDAD | NUMBER(*) | ✓ |  |  |
| ID_COLECTIVO_MOVILIDAD_NK | VARCHAR2(2 BYTE) |  |  |  |
| NOMBRE_COLECTIVO_MOVILIDAD | VARCHAR2(50 BYTE) |  |  |  |

### D_CONVOCATORIA

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CONVOCATORIA | NUMBER(*) | ✓ | ✓ | D_CONVOCATORIA(ID_CONVOCATORIA) |
| NOMBRE_CONVOCATORIA | VARCHAR2(100 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |

### D_CONVOCATORIA_PREINSCRIPCION

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CONVOCATORIA | NUMBER(*) | ✓ | ✓ | D_CONVOCATORIA(ID_CONVOCATORIA) |
| NOMBRE_CONVOCATORIA | VARCHAR2(100 CHAR) |  |  |  |
| ID_CONVOCATORIA_NK | NUMBER(*) |  | ✓ | D_CONVOCATORIA_PREINSCRIPCION(ID_CONVOCATORIA) |

### D_CUPO_ADJUDICACION

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CUPO_ADJUDICACION | NUMBER(*) | ✓ | ✓ | D_CUPO_ADJUDICACION(ID_CUPO_ADJUDICACION) |
| NOMBRE_CUPO_ADJUDICACION | VARCHAR2(100 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |
| ID_CUPO_ADJUDICACION_NK | VARCHAR2(4 CHAR) |  | ✓ | D_CUPO_ADJUDICACION(ID_CUPO_ADJUDICACION) |

### D_CURSO_ACADEMICO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CURSO_ACADEMICO | NUMBER(*) | ✓ | ✓ | D_CURSO_ACADEMICO(ID_CURSO_ACADEMICO) |
| NOMBRE_CURSO_ACADEMICO | VARCHAR2(12 CHAR) |  |  |  |
| ID_CURSO_ACADEMICO_NK | NUMBER(*) |  | ✓ | D_CURSO_COHORTE(ID_CURSO_ACADEMICO) |

### D_CURSO_COHORTE

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CURSO_ACADEMICO | NUMBER(*) | ✓ | ✓ | D_CURSO_ACADEMICO(ID_CURSO_ACADEMICO) |
| NOMBRE_CURSO_ACADEMICO | VARCHAR2(12 CHAR) |  |  |  |
| ID_CURSO_ACADEMICO_NK | NUMBER(*) |  | ✓ | D_CURSO_COHORTE(ID_CURSO_ACADEMICO) |

### D_DEDICACION

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_DEDICACION | NUMBER(*) | ✓ |  |  |
| ID_DEDICACION_NK | NUMBER(*) |  |  |  |
| NOMBRE_DEDICACION | VARCHAR2(50 CHAR) |  |  |  |

### D_DEDICACION_PROFESOR

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_DEDICACION | NUMBER(*) | ✓ |  |  |
| ID_DEDICACION_NK | VARCHAR2(10 CHAR) |  |  |  |
| NOMBRE_DEDICACION | VARCHAR2(35 CHAR) |  |  |  |

### D_DETALLE_CUPO_GENERAL

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_DETALLE_CUPO_GENERAL | NUMBER(*) | ✓ |  |  |
| ID_DETALLE_CUPO_GENERAL_NK | VARCHAR2(4 CHAR) |  |  |  |
| NOMBRE_DETALLE_CUPO_GENERAL | VARCHAR2(100 CHAR) |  |  |  |

### D_DOCTORADO_TIPO_BECA

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_TIPO_BECA | NUMBER(*) |  |  |  |
| ID_CURSO_ACADEMICO_NK | NUMBER(*) |  | ✓ | D_CURSO_COHORTE(ID_CURSO_ACADEMICO) |
| ID_TIPO_BECA_NK | VARCHAR2(2 CHAR) |  |  |  |
| ID_TIPO_BECA_DESCR | NUMBER(*) |  |  |  |
| NOMBRE_TIPO_BECA | VARCHAR2(240 CHAR) |  |  |  |

### D_EDAD_EST

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_EDAD_EST | NUMBER(*) | ✓ |  |  |
| ID_EDAD_EST_NK | VARCHAR2(10 BYTE) |  |  |  |
| NOMBRE_EDAD_EST | VARCHAR2(20 BYTE) |  |  |  |

### D_ESTADO_ACUERDO_BILATERAL

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_ESTADO_ACUERDO | NUMBER(*) | ✓ |  |  |
| ID_ESTADO_ACUERDO_NK | VARCHAR2(5 CHAR) |  |  |  |
| NOMBRE_ESTADO_ACUERDO | VARCHAR2(100 CHAR) |  |  |  |

### D_ESTADO_ADJUDICACION

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_ESTADO_ADJUDICACION | NUMBER(*) | ✓ | ✓ | D_ESTADO_ADJUDICACION(ID_ESTADO_ADJUDICACION) |
| NOMBRE_ESTADO_ADJUDICACION | VARCHAR2(100 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |

### D_ESTADO_SOLICITUD_DOCTORADO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_ESTADO_SOL_DOCTORADO | NUMBER(*) |  |  |  |
| ID_ESTADO_SOL_DOCTORADO_NK | VARCHAR2(2 CHAR) |  |  |  |
| NOMBRE_ESTADO_SOL_DOCTORADO | VARCHAR2(800 CHAR) |  |  |  |

### D_ESTUDIO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_ESTUDIO | NUMBER(*) | ✓ |  |  |
| ID_ESTUDIO_NK | NUMBER(*) |  |  |  |
| NOMBRE_ESTUDIO | VARCHAR2(350 CHAR) |  |  |  |
| ORD_NOMBRE_ESTUDIO | VARCHAR2(350 CHAR) |  |  |  |

### D_ESTUDIO_DESTINO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_ESTUDIO_OTRA_UNIVERSIDAD | NUMBER(*) | ✓ |  |  |
| NOMBRE_ESTUDIO_OTRA_UNIVERSIDA | VARCHAR2(250 CHAR) |  |  |  |
| ID_ESTUDIO_OTRA_UNIV_DESCR | NUMBER(*) |  |  |  |
| ID_ESTUDIO_OTRA_UNIVERSIDAD_NK | VARCHAR2(11 CHAR) |  | ✓ | D_ESTUDIO_DESTINO(ID_ESTUDIO_OTRA_UNIVERSIDAD) |

### D_ESTUDIO_JERARQ

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_PLAN_ESTUDIO | NUMBER(*) |  |  |  |
| ID_PLAN_ESTUDIO_NK | NUMBER(*) |  |  |  |
| ID_ESTUDIO | NUMBER(*) | ✓ |  |  |
| ID_ESTUDIO_NK | NUMBER(*) |  |  |  |
| ID_TIPO_ESTUDIO | NUMBER(*) |  |  |  |
| NOMBRE_TIPO_ESTUDIO | VARCHAR2(30 CHAR) |  |  |  |
| ID_RAMA_CONOCIMIENTO | NUMBER(*) |  |  |  |
| NOMBRE_RAMA_CONOCIMIENTO | VARCHAR2(200 CHAR) |  |  |  |
| ID_TIPO_ESTUDIO_DESCR | NUMBER(*) |  |  |  |
| NOMBRE_PLAN_ESTUDIO | VARCHAR2(350 CHAR) |  |  |  |
| ORD_NOMBRE_ESTUDIO | VARCHAR2(350 CHAR) |  |  |  |
| NOMBRE_ESTUDIO | VARCHAR2(350 CHAR) |  |  |  |
| ORD_NOMBRE_PLAN_ESTUDIO | VARCHAR2(350 CHAR) |  |  |  |
| NOMBRE_PLAN_ESTUDIO_LOCALIDAD | VARCHAR2(350 CHAR) |  |  |  |
| ID_TIPO_ESTUDIO_NK | NUMBER(*) |  |  |  |
| ID_RAMA_CONOCIMIENTO_NK | CHAR(1 CHAR) |  |  |  |
| FLG_INTERUNIVERSITARIO | NUMBER(*) |  |  |  |
| FLG_COORDINADOR | NUMBER(*) |  |  |  |
| NOMBRE_PLAN_ESTUDIO_SC | VARCHAR2(350 CHAR) |  |  |  |
| NOMBRE_ESTUDIO_SC | VARCHAR2(350 CHAR) |  |  |  |

### D_ESTUDIO_OTRA_UNIVERSIDAD

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_ESTUDIO_OTRA_UNIVERSIDAD | NUMBER(*) | ✓ |  |  |
| ID_ESTUDIO_OTRA_UNIVERSIDAD_NK | VARCHAR2(11 CHAR) |  | ✓ | D_ESTUDIO_DESTINO(ID_ESTUDIO_OTRA_UNIVERSIDAD) |
| NOMBRE_ESTUDIO_OTRA_UNIVERSIDA | VARCHAR2(250 CHAR) |  |  |  |
| ID_ESTUDIO_OTRA_UNIV_DESCR | NUMBER(*) |  |  |  |

### D_ESTUDIO_PREVIO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_ESTUDIO_PREVIO | NUMBER(*) | ✓ | ✓ | D_ESTUDIO_PREVIO(ID_ESTUDIO_PREVIO) |
| NOMBRE_ESTUDIO_PREVIO | VARCHAR2(100 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |
| ID_ESTUDIO_PREVIO_NK | VARCHAR2(4 CHAR) |  | ✓ | D_ESTUDIO_PREVIO(ID_ESTUDIO_PREVIO) |

### D_ESTUDIO_PROPIO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_ESTUDIO_PROPIO | NUMBER(*) | ✓ |  |  |
| ID_ESTUDIO_PROPIO_NK | NUMBER(*) |  |  |  |
| ID_ESTUDIO_PROPIO_EDICION_NK | NUMBER(*) |  |  |  |
| NOMBRE_ESTUDIO_PROPIO | VARCHAR2(500 CHAR) |  |  |  |
| NOMBRE_ESTUDIO_PROPIO_EXT | VARCHAR2(1000 CHAR) |  |  |  |
| ID_ESTUDIO_PROPIO_DESCR | NUMBER(*) |  |  |  |

### D_ESTUDIO_PROPIO_MODALIDAD

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_ESTUDIO_PROPIO_MODALIDAD | NUMBER(*) | ✓ |  |  |
| ID_ESTUDIO_PROPIO_MODALIDAD_NK | VARCHAR2(20 CHAR) |  |  |  |
| NOMBRE_ESTUDIO_PROPIO_MODALID | VARCHAR2(500 CHAR) |  |  |  |

### D_ESTUDIO_PROPIO_ORGANO_GEST

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_ORGANO_GESTION_EP | NUMBER(*) |  |  |  |
| ID_ORGANO_GESTION_EP_NK | VARCHAR2(10 CHAR) |  |  |  |
| NOMBRE_ORGANO_GESTION_EP | VARCHAR2(500 CHAR) |  |  |  |
| ORD_NOMBRE_ORGANO_GESTION_EP | VARCHAR2(500 CHAR) |  |  |  |
| ID_ORGANO_GESTION_EP_DESCR | NUMBER(*) |  |  |  |

### D_ESTUDIO_PROPIO_TIPO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_ESTUDIO_PROPIO_TIPO | NUMBER(*) | ✓ |  |  |
| ID_ESTUDIO_PROPIO_TIPO_NK | VARCHAR2(20 CHAR) |  |  |  |
| NOMBRE_ESTUDIO_PROPIO_TIPO | VARCHAR2(500 CHAR) |  |  |  |

### D_GRUPO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_GRUPO | NUMBER(*) | ✓ | ✓ | D_GRUPO(ID_GRUPO) |
| NOMBRE_GRUPO | VARCHAR2(50 CHAR) |  |  |  |
| ID_CURSO_ACADEMICO_NK | NUMBER(*) |  | ✓ | D_CURSO_COHORTE(ID_CURSO_ACADEMICO) |
| ID_CENTRO_NK | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_ASIGNATURA_NK | NUMBER(*) |  | ✓ | D_ASIGNATURA(ID_ASIGNATURA) |
| ID_GRUPO_NK | NUMBER(*) |  | ✓ | D_GRUPO(ID_GRUPO) |
| ID_GRUPO_DESCR | NUMBER(*) |  |  |  |
| ID_TIPO_PERIODO_LECTIVO_NK | CHAR(1 CHAR) |  |  |  |
| ID_VALOR_PERIODO_LECTIVO_NK | CHAR(1 CHAR) |  |  |  |

### D_IDIOMA_MOVILIDAD

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_IDIOMA_MOVILIDAD | NUMBER(*) | ✓ |  |  |
| NOMBRE_IDIOMA_MOVILIDAD | VARCHAR2(50 CHAR) |  |  |  |
| ID_IDIOMA_MOVILIDAD_NK | NUMBER(*) |  |  |  |

### D_IDIOMA_NIVEL_MOVILIDAD

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_IDIOMA_NIVEL_MOVILIDAD | NUMBER(*) | ✓ | ✓ | D_IDIOMA_NIVEL_MOVILIDAD(ID_IDIOMA_NIVEL_MOVILIDAD) |
| ID_IDIOMA_MOVILIDAD_NK | NUMBER(*) |  |  |  |
| ID_NIVEL_IDIOMA_MOVILIDAD_NK | NUMBER(*) |  |  |  |
| NOMBRE_IDIOMA_NIVEL_MOVILIDAD | VARCHAR2(100 CHAR) |  |  |  |

### D_MODALIDAD_PLAN_ESTUDIO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_MODALIDAD_PLAN_ESTUDIO | NUMBER(*) | ✓ |  |  |
| NOMBRE_MODALIDAD_PLAN | VARCHAR2(60 CHAR) |  |  |  |
| ID_MODALIDAD_PLAN_ESTUDIO_NK | VARCHAR2(3 CHAR) |  |  |  |

### D_NACIONALIDAD

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_NACIONALIDAD | NUMBER(*) | ✓ | ✓ | D_NACIONALIDAD(ID_NACIONALIDAD) |
| NOMBRE_NACIONALIDAD | VARCHAR2(45 CHAR) |  |  |  |
| NOMBRE_PAIS | VARCHAR2(45 CHAR) |  |  |  |

### D_NIVEL_ESTUDIOS_MOVILIDAD

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_NIVEL_ESTUDIOS_MOVILIDAD | NUMBER(*) | ✓ |  |  |
| NOMBRE_NIVEL_ESTUDIOS_MOV | VARCHAR2(100 CHAR) |  |  |  |
| ID_NIVEL_ESTUDIOS_MOVILIDAD_NK | VARCHAR2(20 CHAR) |  |  |  |

### D_PAIS

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_PAIS | NUMBER(*) | ✓ | ✓ | D_PAIS(ID_PAIS) |
| NOMBRE_PAIS | VARCHAR2(45 CHAR) |  |  |  |
| ID_PAIS_NK | VARCHAR2(3 CHAR) |  | ✓ | D_UNIVERSIDAD(ID_PAIS) |
| NOMBRE_NACIONALIDAD | VARCHAR2(45 CHAR) |  |  |  |
| ID_PAIS_DESCR | NUMBER(*) |  |  |  |
| SN_PERTENECE_EEES | CHAR(1 CHAR) |  |  |  |
| FLG_EXTRANJERO | NUMBER(*) |  |  |  |
| SN_EXTRANJERO | CHAR(1 CHAR) |  |  |  |

### D_PERSONA

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_PERSONA | NUMBER(*) | ✓ | ✓ | D_PERSONA(ID_PERSONA) |
| ID_PERSONA_NIP_NK | NUMBER(*) |  |  |  |
| DOCUMENTO_IDENTIDAD | VARCHAR2(16 CHAR) |  |  |  |
| APELLIDO1 | VARCHAR2(32 CHAR) |  |  |  |
| APELLIDO2 | VARCHAR2(32 CHAR) |  |  |  |
| NOMBRE | VARCHAR2(32 CHAR) |  |  |  |
| APELLIDOS_NOMBRE | VARCHAR2(99 CHAR) |  |  |  |
| ID_OFUSCADO | VARCHAR2(100 CHAR) |  |  |  |
| SEXO | CHAR(1 CHAR) |  |  |  |
| ID_PAIS_NACIONALIDAD_NK | VARCHAR2(3 CHAR) |  |  |  |
| EMAIL | VARCHAR2(254 BYTE) |  |  |  |
| FECHA_NACIMIENTO_TXT | VARCHAR2(10 CHAR) |  |  |  |
| ANYO_NACIMIENTO | NUMBER(*) |  |  |  |

### D_PLAN_ESTUDIO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_PLAN_ESTUDIO | NUMBER(*) | ✓ |  |  |
| ID_PLAN_ESTUDIO_NK | NUMBER(*) |  |  |  |
| ORD_NOMBRE_PLAN_ESTUDIO | VARCHAR2(350 CHAR) |  |  |  |
| NOMBRE_PLAN_ESTUDIO | VARCHAR2(350 CHAR) |  |  |  |

### D_PLAN_ESTUDIO_ANO_DATOS

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_PLAN_ESTUDIO_ANO_DATOS | NUMBER(*) | ✓ |  |  |
| ID_CURSO_ACADEMICO_NK | NUMBER(*) |  | ✓ | D_CURSO_COHORTE(ID_CURSO_ACADEMICO) |
| ID_PLAN_ESTUDIO_NK | NUMBER(*) |  |  |  |
| ID_TIPO_ESTUDIO_NK | NUMBER(*) |  |  |  |
| ID_MODALIDAD_PLAN_NK | VARCHAR2(3 CHAR) |  |  |  |
| EXPERIMENTALIDAD | NUMBER(14) |  |  |  |
| CREDITOS_OFERTADOS | NUMBER(14) |  |  |  |
| ID_CENTRO_OFERTA_NK | NUMBER(*) |  |  |  |
| NUM_PLAZAS_OFERTADAS | NUMBER(*) |  |  |  |
| FLG_OFERTA | NUMBER(*) |  |  |  |
| ID_CENTRO_MATRICULA_NK | NUMBER(*) |  |  |  |
| NUM_EXPEDIENTES_MATRI | NUMBER(*) |  |  |  |
| FLG_MATRICULA | NUMBER(*) |  |  |  |
| ID_CENTRO_CENT_PLAN_NK | NUMBER(*) |  |  |  |
| FLG_CENT_PLAN | NUMBER(*) |  |  |  |
| ID_AMBITO_CONOCIMIENTO | NUMBER(*) |  |  |  |
| ID_AMBITO_CONOCIMIENTO_NK | VARCHAR2(5 CHAR) |  |  |  |
| NOMBRE_AMBITO_CONOCIMIENTO | VARCHAR2(350 CHAR) |  |  |  |

### D_PLAN_ESTUDIO_ASIGNATURA

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_PLAN_ESTUDIO_ASIGNATURA | NUMBER(*) | ✓ |  |  |
| ID_ASIGNATURA | NUMBER(*) |  | ✓ | D_ASIGNATURA(ID_ASIGNATURA) |
| ID_ASIGNATURA_NK | NUMBER(*) |  | ✓ | D_ASIGNATURA(ID_ASIGNATURA) |
| ID_PLAN_ESTUDIO | NUMBER(*) |  |  |  |
| ID_PLAN_ESTUDIO_NK | NUMBER(*) |  |  |  |
| ID_CLASE_ASIGNATURA | NUMBER(*) |  | ✓ | D_CLASE_ASIGNATURA(ID_CLASE_ASIGNATURA) |
| ID_CLASE_ASIGNATURA_NK | CHAR(1 CHAR) |  | ✓ | D_CLASE_ASIGNATURA(ID_CLASE_ASIGNATURA) |
| CURSO_ORDEN | VARCHAR2(2 CHAR) |  |  |  |
| TIPO_PERIODO | CHAR(1 CHAR) |  |  |  |
| VALOR_PERIODO | VARCHAR2(2 CHAR) |  |  |  |

### D_POBLACION

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_POBLACION | NUMBER(*) | ✓ | ✓ | D_POBLACION(ID_POBLACION) |
| NOMBRE_POBLACION | VARCHAR2(50 CHAR) |  |  |  |
| ID_PROVINCIA | NUMBER(*) |  |  |  |
| NOMBRE_PROVINCIA | VARCHAR2(30 CHAR) |  |  |  |
| ID_CCAA | NUMBER(*) |  |  |  |
| NOMBRE_CCAA | VARCHAR2(30 CHAR) |  |  |  |
| ID_PAIS | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| NOMBRE_PAIS | VARCHAR2(45 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |

### D_POBLACION_CENTRO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_POBLACION | NUMBER(*) | ✓ | ✓ | D_POBLACION(ID_POBLACION) |
| NOMBRE_POBLACION | VARCHAR2(50 CHAR) |  |  |  |

### D_PROGRAMA_MOVILIDAD

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_PROGRAMA_MOVILIDAD | NUMBER(*) | ✓ |  |  |
| NOMBRE_PROGRAMA_MOVILIDAD | VARCHAR2(100 CHAR) |  |  |  |
| COD_PROGRAMA_INT | VARCHAR2(10 CHAR) |  |  |  |
| ID_TIPO_PROGRAMA_MOVILIDAD | NUMBER(*) |  |  |  |
| NOMBRE_TIPO_PROGRAMA_MOV | VARCHAR2(100 CHAR) |  |  |  |
| ID_PROGRAMA_MOVILIDAD_NK | NUMBER(*) |  |  |  |
| SN_PROGRAMA_INTERNACIONAL | VARCHAR2(1 CHAR) |  |  |  |

### D_PROYECTO_INVESTIGACION

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_PROYECTO_INVESTIGACION | NUMBER(*) | ✓ |  |  |
| ID_PROYECTO_INVESTIGACION_NK | VARCHAR2(30 CHAR) |  |  |  |

### D_RAMA_MACROAREA

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_RAMA_MACROAREA | NUMBER(*) | ✓ |  |  |
| NOMBRE_RAMA_MACROAREA | VARCHAR2(200 CHAR) |  |  |  |
| ID_RAMA_CONOCIMIENTO_NK | CHAR(1 CHAR) |  |  |  |
| ID_MACROAREA_NK | CHAR(1 CHAR) |  |  |  |
| ID_MACROAREA_AREA_NK | VARCHAR2(3 CHAR) |  |  |  |

### D_RANGO_CREDITO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_RANGO_CREDITO | NUMBER(*) | ✓ | ✓ | D_RANGO_CREDITO(ID_RANGO_CREDITO) |
| ID_RANGO_CREDITO_NK | VARCHAR2(10 CHAR) |  | ✓ | D_RANGO_CREDITO(ID_RANGO_CREDITO) |
| NOMBRE_RANGO_CREDITO | VARCHAR2(20 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |

### D_RANGO_CREDITO_MOVILIDAD

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CREDITO | NUMBER(16) |  |  |  |
| ID_RANGO_CREDITO | NUMBER(*) | ✓ | ✓ | D_RANGO_CREDITO(ID_RANGO_CREDITO) |
| NOMBRE_RANGO_CREDITO | VARCHAR2(80 CHAR) |  |  |  |

### D_RANGO_EDAD

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_RANGO_EDAD | NUMBER(*) | ✓ | ✓ | D_RANGO_EDAD(ID_RANGO_EDAD) |
| ID_RANGO_EDAD_NK | VARCHAR2(10 CHAR) |  | ✓ | D_RANGO_EDAD(ID_RANGO_EDAD) |
| NOMBRE_RANGO_EDAD | VARCHAR2(20 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |

### D_RANGO_NOTA_ADMISION

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_RANGO_NOTA_ADMISION | NUMBER(*) | ✓ | ✓ | D_RANGO_NOTA_ADMISION(ID_RANGO_NOTA_ADMISION) |
| ID_RANGO_NOTA_ADMISION_NK | NUMBER |  | ✓ | D_RANGO_NOTA_ADMISION(ID_RANGO_NOTA_ADMISION) |
| NOMBRE_RANGO_NOTA_ADMISION | VARCHAR2(20 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |

### D_RANGO_NOTA_CRUE

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| FECHA_CARGA | DATE |  |  |  |
| ID_RANGO_NOTA_CRUE | NUMBER(*) | ✓ |  |  |
| ID_RANGO_NOTA_CRUE_NK | VARCHAR2(10 CHAR) |  |  |  |
| NOMBRE_RANGO_NOTA_CRUE | VARCHAR2(20 CHAR) |  |  |  |

### D_RANGO_NOTA_EGRACONS

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_RANGO_NOTA_EGRACONS | NUMBER(*) | ✓ |  |  |
| ID_RANGO_NOTA_EGRACONS_NK | VARCHAR2(10 CHAR) |  |  |  |
| NOMBRE_RANGO_NOTA_EGRACONS | VARCHAR2(20 CHAR) |  |  |  |
| NOTA_REFERENCIA | NUMBER(16) |  |  |  |

### D_RANGO_NOTA_NUMERICA

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_RANGO_NOTA_NUMERICA | NUMBER(*) | ✓ | ✓ | D_RANGO_NOTA_NUMERICA(ID_RANGO_NOTA_NUMERICA) |
| ID_RANGO_NOTA_NUMERICA_NK | VARCHAR2(10 CHAR) |  | ✓ | D_RANGO_NOTA_NUMERICA(ID_RANGO_NOTA_NUMERICA) |
| NOMBRE_RANGO_NOTA_NUMERICA | VARCHAR2(20 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |

### D_SEXO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_SEXO | NUMBER(*) | ✓ | ✓ | D_SEXO(ID_SEXO) |
| ID_SEXO_NK | CHAR(1 CHAR) |  | ✓ | D_SEXO(ID_SEXO) |
| NOMBRE_SEXO | VARCHAR2(20 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |

### D_TIEMPO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_DIA | NUMBER(*) |  |  |  |
| NOMBRE_DIA | VARCHAR2(20 CHAR) |  |  |  |
| ID_MES | NUMBER(*) |  |  |  |
| NOMBRE_MES | VARCHAR2(10 CHAR) |  |  |  |
| ID_TRIMESTRE | NUMBER(*) |  |  |  |
| NOMBRE_TRIMESTRE | VARCHAR2(10 CHAR) |  |  |  |
| ID_ANYO | NUMBER(*) |  |  |  |
| NOMBRE_ANYO | VARCHAR2(4 CHAR) |  |  |  |

### D_TIPO_ABANDONO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_TIPO_ABANDONO | NUMBER(*) | ✓ | ✓ | D_TIPO_ABANDONO(ID_TIPO_ABANDONO) |
| NOMBRE_TIPO_ABANDONO | VARCHAR2(100 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |

### D_TIPO_ACCESO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_TIPO_ACCESO | NUMBER(*) | ✓ | ✓ | D_TIPO_ACCESO(ID_TIPO_ACCESO) |
| NOMBRE_TIPO_ACCESO | VARCHAR2(50 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |

### D_TIPO_ACCESO_PREINSCRIPCION

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_TIPO_ACCESO_PREINS | NUMBER(*) | ✓ | ✓ | D_TIPO_ACCESO_PREINSCRIPCION(ID_TIPO_ACCESO_PREINS) |
| NOMBRE_TIPO_ACCESO_PREINS | VARCHAR2(100 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |

### D_TIPO_ASIGNATURA

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_TIPO_ASIGNATURA | NUMBER(*) | ✓ |  |  |
| NOMBRE_TIPO_ASIGNATURA | VARCHAR2(42 CHAR) |  |  |  |
| ID_TIPO_ASIGNATURA_DESCR | NUMBER(*) |  |  |  |
| ID_TIPO_ASIGNATURA_NK | NUMBER(*) |  |  |  |

### D_TIPO_CENTRO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_TIPO_CENTRO | NUMBER(*) | ✓ |  |  |
| NOMBRE_TIPO_CENTRO | VARCHAR2(30 CHAR) |  |  |  |
| ID_TIPO_CENTRO_DESCR | NUMBER(*) |  |  |  |

### D_TIPO_DOCENCIA

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_TIPO_DOCENCIA | NUMBER(*) | ✓ | ✓ | D_TIPO_DOCENCIA(ID_TIPO_DOCENCIA) |
| NOMBRE_TIPO_DOCENCIA | VARCHAR2(128 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |

### D_TIPO_EGRESO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_TIPO_EGRESO | NUMBER(*) | ✓ | ✓ | D_TIPO_EGRESO(ID_TIPO_EGRESO) |
| NOMBRE_TIPO_EGRESO | VARCHAR2(100 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |

### D_TIPO_ESTUDIO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_TIPO_ESTUDIO | NUMBER(*) | ✓ |  |  |
| NOMBRE_TIPO_ESTUDIO | VARCHAR2(30 CHAR) |  |  |  |
| ID_TIPO_ESTUDIO_NK | NUMBER(*) |  |  |  |
| ID_TIPO_ESTUDIO_DESCR | NUMBER(*) |  |  |  |
| ORD_TIPO_ESTUDIO | VARCHAR2(100 CHAR) |  |  |  |

### D_TIPO_PROCEDIMIENTO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_TIPO_PROCEDIMIENTO | NUMBER(*) | ✓ | ✓ | D_TIPO_PROCEDIMIENTO(ID_TIPO_PROCEDIMIENTO) |
| NOMBRE_TIPO_PROCEDIMIENTO | VARCHAR2(100 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |

### D_TIPO_RECONOCIMIENTO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_TIPO_RECONOCIMIENTO | NUMBER(*) | ✓ | ✓ | D_TIPO_RECONOCIMIENTO(ID_TIPO_RECONOCIMIENTO) |
| NOMBRE_TIPO_RECONOCIMIENTO | VARCHAR2(80 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |
| ID_TIPO_RECONOCIMIENTO_NK | CHAR(1 CHAR) |  | ✓ | D_TIPO_RECONOCIMIENTO(ID_TIPO_RECONOCIMIENTO) |

### D_TITULACION

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_TITULACION | NUMBER(*) | ✓ | ✓ | D_TITULACION(ID_TITULACION) |
| NOMBRE_TITULACION | VARCHAR2(350 CHAR) |  |  |  |
| ID_TIPO_TITULACION | NUMBER(*) |  |  |  |
| NOMBRE_TIPO_TITULACION | VARCHAR2(100 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |

### D_UNIVERSIDAD

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_UNIVERSIDAD | NUMBER(*) | ✓ | ✓ | D_UNIVERSIDAD(ID_UNIVERSIDAD) |
| ID_UNIVERSIDAD_NK | NUMBER(*) |  | ✓ | D_UNIVERSIDAD(ID_UNIVERSIDAD) |
| ID_UNIVERSIDAD_DESCR | NUMBER(*) |  |  |  |
| NOMBRE_UNIVERSIDAD | VARCHAR2(500 CHAR) |  |  |  |
| NOMBRE_UNIVERSIDAD_SIN_PAIS | VARCHAR2(80 CHAR) |  |  |  |
| ID_PAIS_NK | VARCHAR2(3 CHAR) |  | ✓ | D_UNIVERSIDAD(ID_PAIS) |
| ID_UNIVERSIDAD_PIC_NK | VARCHAR2(30 CHAR) |  |  |  |
| ID_PAIS | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| NOMBRE_PAIS | VARCHAR2(45 CHAR) |  |  |  |
| SN_UNIVERSIDAD_UNITA | CHAR(1 CHAR) |  |  |  |
| SN_UNIVERSIDAD_UNITA_GEMINAE | CHAR(1 CHAR) |  |  |  |

## Tablas de Hechos


### F_COHORTE

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CURSO_ACADEMICO_COHORTE_NK | NUMBER(*) |  |  |  |
| ID_EXPEDIENTE_ACADEMICO_NK | NUMBER(*) |  |  |  |
| ID_CURSO_ACADEMICO_COHORTE | NUMBER(*) |  |  |  |
| ID_EXPEDIENTE_ACADEMICO | NUMBER(*) |  |  |  |
| ID_PLAN_ESTUDIO | NUMBER(*) |  | ✓ | F_TABLA_FUSION(ID_PLAN_ESTUDIO) |
| ID_CENTRO | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_ALUMNO | NUMBER(*) |  |  |  |
| ID_TIPO_ACCESO | NUMBER(*) |  | ✓ | D_TIPO_ACCESO(ID_TIPO_ACCESO) |
| ID_SEXO | NUMBER(*) |  | ✓ | D_SEXO(ID_SEXO) |
| ID_RANGO_CREDITOS_MATRICULADOS | NUMBER(*) |  |  |  |
| ID_RANGO_CREDITOS_SUPERADOS | NUMBER(*) |  |  |  |
| ID_CURSO_ACAD_GRADUACION | NUMBER(*) |  |  |  |
| ID_CURSO_ACAD_ABANDONO | NUMBER(*) |  |  |  |
| ID_CURSO_ACAD_TRASLADO | NUMBER(*) |  |  |  |
| ID_RANGO_CALIFICACION_FINAL | NUMBER(*) |  |  |  |
| ID_TIPO_ABANDONO | NUMBER(*) |  | ✓ | D_TIPO_ABANDONO(ID_TIPO_ABANDONO) |
| EDAD_INGRESO | NUMBER |  |  |  |
| DURACION | NUMBER(*) |  |  |  |
| CREDITOS_NECESARIOS | NUMBER |  |  |  |
| CREDITOS_MATRICULADOS | NUMBER |  |  |  |
| CREDITOS_SUPERADOS | NUMBER |  |  |  |
| CREDITOS_PRESENTADOS | NUMBER |  |  |  |
| CREDITOS_SUSPENDIDOS | NUMBER |  |  |  |
| CREDITOS_RECONOCIDOS | NUMBER |  |  |  |
| CREDITOS_TRANSFERIDOS | NUMBER |  |  |  |
| GRADUADO | NUMBER(*) |  |  |  |
| TRASLADO | NUMBER(*) |  |  |  |
| INGRESO | NUMBER(*) |  |  |  |
| FLG_NUEVO_INGRESO | NUMBER(*) |  |  |  |
| FLG_ABANDONO_INICIAL | NUMBER(*) |  |  |  |
| FLG_GRADUADO_EN_TIEMPO | NUMBER(*) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |
| SN_GRADUADO_EN_TIEMPO | CHAR(1 CHAR) |  |  |  |
| NOTA_ADMISION | NUMBER(10) |  |  |  |
| ABANDONO_GENERICO | NUMBER(*) |  |  |  |
| ABANDONO_OFICIAL | NUMBER(*) |  |  |  |
| FLG_PLAN_OFICIAL | NUMBER(*) |  |  |  |
| FLG_TASA_ABANDONO | NUMBER(*) |  |  |  |
| FLG_TASA_GRADUACION | NUMBER(*) |  |  |  |
| FLG_CALCULO_TASA | NUMBER(*) |  |  |  |
| ID_ESTUDIO_PREVIO | NUMBER(*) |  | ✓ | D_ESTUDIO_PREVIO(ID_ESTUDIO_PREVIO) |
| ID_PAIS_NACIONALIDAD | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| ID_POBLACION_FAMILIAR | NUMBER(*) |  | ✓ | D_POBLACION(ID_POBLACION) |
| ID_ESTUDIO | NUMBER(*) |  |  |  |
| ID_CENTRO_INICIO | NUMBER(*) |  |  |  |
| FLG_TRASLADO_MISMO_ESTUDIO | NUMBER(*) |  |  |  |
| ID_FECHA_CARGA | NUMBER(*) |  |  |  |
| ID_TIPO_ESTUDIO | NUMBER(*) |  |  |  |
| ID_TIPO_CENTRO | NUMBER(*) |  |  |  |
| ID_CAMPUS_CENTRO | NUMBER(*) |  |  |  |
| ID_RAMA_CONOCIMIENTO | NUMBER(*) |  |  |  |
| ID_POBLACION_CENTRO | NUMBER(*) |  | ✓ | D_POBLACION(ID_POBLACION) |
| ID_PERSONA_NIP_NK | NUMBER(*) |  |  |  |
| CURSOS_MATRICULADOS | NUMBER(*) |  |  |  |
| CURSO_MAS_ALTO_MATRICULADO | NUMBER(*) |  |  |  |
| CURSOS_EXTRA_GRADUACION | NUMBER(*) |  |  |  |
| CALIFICACION_FINAL | NUMBER |  |  |  |
| SN_ABANDONO_INICIAL | CHAR(1 CHAR) |  |  |  |
| SN_GRADUADO | CHAR(1 CHAR) |  |  |  |
| SN_ABANDONO_OFICIAL | CHAR(1 CHAR) |  |  |  |
| ID_PAIS_FAMILIAR | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| ID_PAIS_FAMILIAR_NK | VARCHAR2(3 CHAR) |  |  |  |
| ID_EDAD_EST | NUMBER(*) |  |  |  |
| FLG_GRADUADO_IDONEO | NUMBER(*) |  |  |  |
| SN_GRADUADO_IDONEO | CHAR(1 CHAR) |  |  |  |
| FLG_MULTIPLE_TITULACION | NUMBER(*) |  |  |  |
| SN_MULTIPLE_TITULACION | CHAR(1 CHAR) |  |  |  |
| FLG_C_ABANDONOINI | NUMBER(*) |  |  |  |
| FLG_C_ABANDONO | NUMBER(*) |  |  |  |
| FLG_C_IDONEIDAD | NUMBER(*) |  |  |  |
| FLG_C_GRADUACION | NUMBER(*) |  |  |  |
| FE_C_ABANDONOINI | DATE |  |  |  |
| FE_C_ABANDONO | DATE |  |  |  |
| FE_C_IDONEIDAD | DATE |  |  |  |
| FE_C_GRADUACION | DATE |  |  |  |
| FECHA_ACTUAL | DATE |  |  |  |

### F_DOCTORADO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CURSO_INFORME_NK | NUMBER(*) |  |  |  |
| ID_CURSO_MATRICULA_NK | NUMBER(*) |  |  |  |
| ID_PERSONA_NIP_NK | NUMBER(*) |  |  |  |
| ID_CENTRO_NK | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_PLAN_ESTUDIO_NK | NUMBER(*) |  |  |  |
| ID_EXPEDIENTE_ACADEMICO_NK | NUMBER(*) |  |  |  |
| ID_DEDICACION_ALUMNO_NK | NUMBER(*) |  |  |  |
| FLG_NUEVO_INGRESO | NUMBER(*) |  |  |  |
| FLG_EN_PROGRAMA_MOVILIDAD | NUMBER(*) |  |  |  |
| FECHA_LECTURA_TESIS | DATE |  |  |  |
| SN_COTUTELA_TESIS | CHAR(1 CHAR) |  |  |  |
| SN_MENCION_INTERNAC_TESIS | CHAR(1 CHAR) |  |  |  |
| FECHA_MATRICULA | DATE |  |  |  |
| ID_ASIGNATURA_NK | NUMBER(*) |  | ✓ | D_ASIGNATURA(ID_ASIGNATURA) |
| CALIFICACION | VARCHAR2(2 CHAR) |  |  |  |
| FLG_SUPERADA | NUMBER(*) |  |  |  |
| FLG_PRESENTADA | NUMBER(*) |  |  |  |
| FLG_RECONOCIDA | NUMBER(*) |  |  |  |
| FLG_TRANSFERIDA | NUMBER(*) |  |  |  |
| FLG_SUSPENDIDA | NUMBER(*) |  |  |  |
| FECHA_CALIFICACION | DATE |  |  |  |
| ID_PROFESOR_NIP_NK | NUMBER(*) |  |  |  |
| ID_DEDICACION_PROFESOR_NK | VARCHAR2(2 CHAR) |  |  |  |
| FLG_TUTOR | NUMBER(*) |  |  |  |
| FLG_DIRECTOR | NUMBER(*) |  |  |  |
| FECHA_REFERENCIA | DATE |  |  |  |
| ID_CURSO_INFORME | NUMBER(*) |  |  |  |
| ID_CURSO_MATRICULA | NUMBER(*) |  |  |  |
| ID_ALUMNO | NUMBER(*) |  |  |  |
| SEXO_ALUMNO | CHAR(1 CHAR) |  |  |  |
| ID_PAIS_NACIONALIDAD_ALUMNO | NUMBER(*) |  |  |  |
| ID_DEDICACION_ALUMNO | NUMBER(*) |  |  |  |
| ID_PROFESOR | NUMBER(*) |  |  |  |
| SEXO_PROFESOR | CHAR(1 CHAR) |  |  |  |
| ID_PAIS_NACIONALIDAD_PROF | NUMBER(*) |  |  |  |
| ID_PLAN_ESTUDIO | NUMBER(*) |  | ✓ | F_TABLA_FUSION(ID_PLAN_ESTUDIO) |
| ID_ESTUDIO | NUMBER(*) |  |  |  |
| ID_RAMA_CONOCIMIENTO | NUMBER(*) |  |  |  |
| ID_ASIGNATURA | NUMBER(*) |  | ✓ | D_ASIGNATURA(ID_ASIGNATURA) |
| ID_TIPO_ASIGNATURA | NUMBER(*) |  |  |  |
| ID_CALIFICACION | NUMBER(*) |  | ✓ | D_CALIFICACION(ID_CALIFICACION) |
| FLG_SEXENIO_VIVO | NUMBER(*) |  |  |  |
| ID_DEDICACION_PROFESOR | NUMBER(*) |  |  |  |
| ID_FECHA_CARGA | NUMBER(*) |  |  |  |
| ID_CENTRO | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| SN_NUEVO_INGRESO | CHAR(1 CHAR) |  |  |  |
| SN_EN_PROGRAMA_MOVILIDAD | CHAR(1 CHAR) |  |  |  |
| SN_TUTOR | CHAR(1 CHAR) |  |  |  |
| SN_DIRECTOR | CHAR(1 CHAR) |  |  |  |
| NUM_SEXENIOS | NUMBER(*) |  |  |  |
| FLG_TIEMPO_PARCIAL | NUMBER(*) |  |  |  |
| ID_PAIS_NACIONALIDAD_ALUMNO_NK | VARCHAR2(3 CHAR) |  |  |  |
| FLG_EXTRANJERO | NUMBER(*) |  |  |  |
| ID_FECHA_LECTURA_TESIS | NUMBER(*) |  |  |  |
| ID_FECHA_MATRICULA | NUMBER(*) |  |  |  |
| FLG_PROFESOR | NUMBER(*) |  |  |  |
| FLG_TESIS_LEIDA | NUMBER(*) |  |  |  |
| NUM_DIRECTORES_TESIS | NUMBER(*) |  |  |  |
| ID_ESTUDIO_NK | NUMBER(*) |  |  |  |
| ID_TIPO_BECA_NK | VARCHAR2(2 CHAR) |  |  |  |
| ID_TIPO_BECA | NUMBER(*) |  |  |  |
| ID_TIPO_CONTRATO_NK | VARCHAR2(11 CHAR) |  |  |  |
| FLG_PROFESOR_UZ | NUMBER(*) |  |  |  |
| FLG_PROFESOR_TIEMPO_COMPLETO | NUMBER(*) |  |  |  |
| FLG_COTUTELA_TESIS | NUMBER(*) |  |  |  |
| FLG_MENCION_INTERNAC_TESIS | NUMBER(*) |  |  |  |
| FLG_BECADO | NUMBER(*) |  |  |  |
| SN_TESIS_LEIDA | CHAR(1 CHAR) |  |  |  |
| FLG_ABANDONO | NUMBER(*) |  |  |  |
| SN_ABANDONO | CHAR(1 CHAR) |  |  |  |
| FLG_ABANDONO_DENOMINADOR | NUMBER(*) |  |  |  |
| DURACION_NETA_TESIS | NUMBER |  |  |  |
| FLG_TESIS_CUM_LAUDE | NUMBER(*) |  |  |  |
| SN_PROFESOR_UZ | CHAR(1 CHAR) |  |  |  |
| ID_SITUACION_ADVA | NUMBER(*) |  |  |  |
| ID_SITUACION_ADVA_NK | VARCHAR2(2 CHAR) |  |  |  |
| ID_CATEGORIA_CUERPO_ESCALA | NUMBER(*) |  |  |  |
| ID_CATEGORIA_CUERPO_ESCALA_NK | VARCHAR2(5 CHAR) |  |  |  |
| NUM_REGS_TESIS | NUMBER(*) |  |  |  |
| DURACION_BRUTA_TESIS | NUMBER(*) |  |  |  |
| DIAS_BAJA | NUMBER(*) |  |  |  |
| FECHA_DEPOSITO_TESIS | DATE |  |  |  |
| FECHA_INSCRI_SOLICITUD_TESIS | DATE |  |  |  |
| NUM_SEXENIO_ESTATAL | NUMBER(*) |  |  |  |
| NUM_SEXENIO_AUTONOMICO | NUMBER(*) |  |  |  |
| NUM_SEXENIO_CNEAI | NUMBER(*) |  |  |  |
| FECHA_RECON_SEXENIO_ESTATAL | DATE |  |  |  |
| FECHA_RECON_SEXENIO_AUTONOMICO | DATE |  |  |  |
| FECHA_RECON_SEXENIO_CNEAI | DATE |  |  |  |
| FLG_SEXENIO_VIVO_ESTATAL | NUMBER(*) |  |  |  |
| FLG_SEXENIO_VIVO_AUTONOMICO | NUMBER(*) |  |  |  |
| FLG_SEXENIO_VIVO_CNEAI | NUMBER(*) |  |  |  |
| ID_SEXO_ALUMNO | NUMBER(*) |  |  |  |
| NUM_QUINQUENIOS | NUMBER(*) |  |  |  |
| SN_MENCION_INDUSTRIAL | CHAR(1 CHAR) |  |  |  |
| FLG_MENCION_INDUSTRIAL | NUMBER(*) |  |  |  |
| SN_COMPENDIO_PUBLICACIONES | CHAR(1 CHAR) |  |  |  |
| FLG_COMPENDIO_PUBLICACIONES | NUMBER(*) |  |  |  |
| ID_PROYECTO_INVESTIGACION | NUMBER(*) |  |  |  |
| ID_PROYECTO_INVESTIGACION_NK | VARCHAR2(30 CHAR) |  |  |  |
| AMBITO_PROYECTO | VARCHAR2(13 CHAR) |  |  |  |
| AUT_AMPLIACION_TESIS | NUMBER(*) |  |  |  |
| SN_PRORROGA_1 | CHAR(1 CHAR) |  |  |  |
| SN_PRORROGA_2 | CHAR(1 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |
| NUMERO_ALU_ENCUESTA_GLOBAL_1 | NUMBER(*) |  |  |  |
| NUMERO_ALU_ENCUESTA_GLOBAL_2 | NUMBER(*) |  |  |  |
| NUMERO_ALU_ENCUESTA_GLOBAL_3 | NUMBER(*) |  |  |  |
| NUMERO_ALU_ENCUESTA_GLOBAL_4 | NUMBER(*) |  |  |  |
| NUMERO_ALU_ENCUESTA_GLOBAL_5 | NUMBER(*) |  |  |  |
| NUMERO_PROF_ENCUESTA_GLOBAL_1 | NUMBER(*) |  |  |  |
| NUMERO_PROF_ENCUESTA_GLOBAL_2 | NUMBER(*) |  |  |  |
| NUMERO_PROF_ENCUESTA_GLOBAL_3 | NUMBER(*) |  |  |  |
| NUMERO_PROF_ENCUESTA_GLOBAL_4 | NUMBER(*) |  |  |  |
| NUMERO_PROF_ENCUESTA_GLOBAL_5 | NUMBER(*) |  |  |  |
| NUMERO_ALU_ENCUESTA_GLOBAL_0 | NUMBER(*) |  |  |  |
| NUMERO_PROF_ENCUESTA_GLOBAL_0 | NUMBER(*) |  |  |  |
| ID_UNIVERSIDAD_ORIGEN | NUMBER(*) |  |  |  |
| ID_UNIVERSIDAD_ORIGEN_NK | NUMBER(*) |  |  |  |
| FLG_OTRA_UNIVERSIDAD | NUMBER(*) |  |  |  |
| FLG_OTRA_UNIVERSIDAD_DENOM | NUMBER(*) |  |  |  |
| ID_SEXO_PROFESOR | NUMBER(*) |  |  |  |
| NUM_SEXENIOS_TRANSF | NUMBER(*) |  |  |  |
| NUM_ART_IDX_ANO_CURSO_UZ | NUMBER(*) |  |  |  |
| NUM_ART_NO_IDX_ANO_CURSO_UZ | NUMBER(*) |  |  |  |
| NUM_ART_IDX_ANO_SIG_UZ | NUMBER(*) |  |  |  |
| NUM_ART_NO_IDX_ANO_SIG_UZ | NUMBER(*) |  |  |  |
| TOT_ARTICULOS_INDEX_UZ | NUMBER(16) |  |  |  |
| TOT_ARTICULOS_NO_INDEX_UZ | NUMBER(16) |  |  |  |
| NUM_ART_IDX_ANO_CURSO_RAMA | NUMBER(*) |  |  |  |
| NUM_ART_NO_IDX_ANO_CURSO_RAMA | NUMBER(*) |  |  |  |
| NUM_ART_IDX_ANO_SIG_RAMA | NUMBER(*) |  |  |  |
| NUM_ART_NO_IDX_ANO_SIG_RAMA | NUMBER(*) |  |  |  |
| TOT_ARTICULOS_INDEX_RAMA | NUMBER(16) |  |  |  |
| TOT_ARTICULOS_NO_INDEX_RAMA | NUMBER(16) |  |  |  |
| NUM_ART_IDX_ANO_CURSO_PLAN | NUMBER(*) |  |  |  |
| NUM_ART_NO_IDX_ANO_CURSO_PLAN | NUMBER(*) |  |  |  |
| NUM_ART_IDX_ANO_SIG_PLAN | NUMBER(*) |  |  |  |
| NUM_ART_NO_IDX_ANO_SIG_PLAN | NUMBER(*) |  |  |  |
| TOT_ARTICULOS_INDEX_PLAN | NUMBER(16) |  |  |  |
| TOT_ARTICULOS_NO_INDEX_PLAN | NUMBER(16) |  |  |  |

### F_DOCTORADO_ADMISION

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CURSO_ACADEMICO_NK | NUMBER(*) |  | ✓ | D_CURSO_COHORTE(ID_CURSO_ACADEMICO) |
| ESTADO_INSCRIPCION | VARCHAR2(2 CHAR) |  |  |  |
| ID_SOLICITUD_NK | NUMBER(*) |  |  |  |
| ID_EXPEDIENTE_ACADEMICO_NK | NUMBER(*) |  |  |  |
| SN_MATRICULADO | CHAR(1 CHAR) |  |  |  |
| FECHA_REFERENCIA | DATE |  |  |  |
| ID_CURSO_ACADEMICO | NUMBER(*) |  | ✓ | D_CURSO_ACADEMICO(ID_CURSO_ACADEMICO) |
| ID_PLAN_ESTUDIO | NUMBER(*) |  | ✓ | F_TABLA_FUSION(ID_PLAN_ESTUDIO) |
| ID_ESTUDIO | NUMBER(*) |  |  |  |
| ID_RAMA_CONOCIMIENTO | NUMBER(*) |  |  |  |
| ID_CENTRO | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_ALUMNO | NUMBER(*) |  |  |  |
| SEXO_ALUMNO | CHAR(1 CHAR) |  |  |  |
| ID_PAIS_NACIONALIDAD_ALUMNO | NUMBER(*) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |
| ID_FECHA_CARGA | NUMBER(*) |  |  |  |
| ID_PERSONA_NIP_NK | NUMBER(*) |  |  |  |
| ID_CENTRO_NK | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_PLAN_ESTUDIO_NK | NUMBER(*) |  |  |  |
| SN_NUEVO_INGRESO | CHAR(1 CHAR) |  |  |  |
| ID_ESTADO_SOL_DOCTORADO | NUMBER(*) |  |  |  |
| SN_COMPLEMENTO_FORMACION | CHAR(1 CHAR) |  |  |  |
| FLG_MATRICULADO | NUMBER |  |  |  |
| FLG_NUEVO_INGRESO | NUMBER(*) |  |  |  |
| FLG_COMPLEMENTO_FORMACION | NUMBER(*) |  |  |  |
| FLG_TIEMPO_PARCIAL | NUMBER(*) |  |  |  |
| ID_DEDICACION_NK | NUMBER(*) |  |  |  |
| ID_DEDICACION | NUMBER(*) |  |  |  |
| FLG_EXTRANJERO | NUMBER(*) |  |  |  |
| ID_PAIS_NACIONALIDAD_ALUMNO_NK | VARCHAR2(3 CHAR) |  |  |  |
| FLG_OTRA_UNIVERSIDAD | NUMBER(*) |  |  |  |
| ID_UNIVERSIDAD_ORIGEN | NUMBER(*) |  |  |  |
| FLG_OTRA_UNIVERSIDAD_DENOM | NUMBER(*) |  |  |  |
| ID_ESTUDIO_NK | NUMBER(*) |  |  |  |
| ID_UNIVERSIDAD_ORIGEN_NK | NUMBER(*) |  |  |  |
| ID_SEXO_ALUMNO | NUMBER(*) |  |  |  |

### F_EGRACONS

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CURSO_EGRACONS | NUMBER(*) |  |  |  |
| ID_CURSO_EGRACONS_NK | NUMBER(*) |  |  |  |
| ID_CURSO_ACADEMICO_CALIFIC | NUMBER(*) |  |  |  |
| ID_CURSO_ACADEMICO_CALIFIC_NK | NUMBER(*) |  |  |  |
| ID_ALUMNO | NUMBER(*) |  |  |  |
| ID_EXPEDIENTE_ACADEMICO | NUMBER(*) |  |  |  |
| ID_EXPEDIENTE_ACADEMICO_NK | NUMBER(*) |  |  |  |
| EXPEDIENTE_ASIGNATURA | NUMBER |  |  |  |
| ID_TIPO_ESTUDIO | NUMBER(*) |  |  |  |
| ID_ESTUDIO | NUMBER(*) |  |  |  |
| ID_PLAN_ESTUDIO | NUMBER(*) |  | ✓ | F_TABLA_FUSION(ID_PLAN_ESTUDIO) |
| ID_RAMA_CONOCIMIENTO | NUMBER(*) |  |  |  |
| ID_CENTRO | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_CENTRO_NK | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_POBLACION_CENTRO | NUMBER(*) |  | ✓ | D_POBLACION(ID_POBLACION) |
| ID_ASIGNATURA | NUMBER(*) |  | ✓ | D_ASIGNATURA(ID_ASIGNATURA) |
| ID_ASIGNATURA_NK | NUMBER(*) |  | ✓ | D_ASIGNATURA(ID_ASIGNATURA) |
| ID_TIPO_ASIGNATURA | NUMBER(*) |  |  |  |
| ID_CLASE_ASIGNATURA | NUMBER(*) |  | ✓ | D_CLASE_ASIGNATURA(ID_CLASE_ASIGNATURA) |
| CREDITOS | NUMBER(16) |  |  |  |
| NOTA_NUMERICA | NUMBER(16) |  |  |  |
| ID_CALIFICACION | NUMBER(*) |  | ✓ | D_CALIFICACION(ID_CALIFICACION) |
| ID_CALIFICACION_NK | VARCHAR2(2 CHAR) |  | ✓ | D_CALIFICACION(ID_CALIFICACION) |
| ID_RANGO_NOTA_NUMERICA | NUMBER(*) |  | ✓ | D_RANGO_NOTA_NUMERICA(ID_RANGO_NOTA_NUMERICA) |
| ID_RANGO_NOTA_EGRACONS | NUMBER(*) |  |  |  |
| ID_PLAN_GRUPO_MATRICULA | NUMBER(*) |  |  |  |
| ID_PLAN_GRUPO_MATRICULA_NK | NUMBER(*) |  |  |  |
| ID_CENTRO_IMPARTICION | NUMBER(*) |  |  |  |
| ID_CENTRO_IMPARTICION_NK | NUMBER(*) |  |  |  |
| ID_ESTUDIO_ASIGNATURA | NUMBER(*) |  |  |  |
| ID_ESTUDIO_ASIGNATURA_NK | NUMBER(*) |  |  |  |
| ID_TIPO_ESTUDIO_ASIGNATURA | NUMBER(*) |  |  |  |
| ID_TIPO_ESTUDIO_ASIGNATURA_NK | NUMBER(*) |  |  |  |
| ID_RAMA_CONOCIMIENTO_ASIG | NUMBER(*) |  |  |  |
| ID_RAMA_CONOCIMIENTO_ASIG_NK | CHAR(1 CHAR) |  |  |  |
| ID_ESTUDIO_NK | NUMBER(*) |  |  |  |
| ID_PROGRAMA_MOVILIDAD | NUMBER(*) |  |  |  |
| ID_PROGRAMA_MOVILIDAD_NK | NUMBER(*) |  |  |  |
| FLG_ENTRADA | CHAR(1 CHAR) |  |  |  |
| SN_PROGRAMA_INTERNACIONAL | CHAR(1 CHAR) |  |  |  |

### F_EGRESADO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CURSO_ACADEMICO_NK | NUMBER(*) |  | ✓ | D_CURSO_COHORTE(ID_CURSO_ACADEMICO) |
| ID_EXPEDIENTE_ACADEMICO_NK | NUMBER(*) |  |  |  |
| ID_CURSO_ACADEMICO | NUMBER(*) |  | ✓ | D_CURSO_ACADEMICO(ID_CURSO_ACADEMICO) |
| ID_ALUMNO | NUMBER(*) |  |  |  |
| ID_EXPEDIENTE_ACADEMICO | NUMBER(*) |  |  |  |
| ID_TIPO_ABANDONO | NUMBER(*) |  | ✓ | D_TIPO_ABANDONO(ID_TIPO_ABANDONO) |
| ID_TIPO_EGRESO | NUMBER(*) |  | ✓ | D_TIPO_EGRESO(ID_TIPO_EGRESO) |
| ID_PLAN_ESTUDIO | NUMBER(*) |  | ✓ | F_TABLA_FUSION(ID_PLAN_ESTUDIO) |
| ID_CENTRO | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_CURSO_ACADEMICO_COHORTE | NUMBER(*) |  |  |  |
| ID_TIPO_ACCESO | NUMBER(*) |  | ✓ | D_TIPO_ACCESO(ID_TIPO_ACCESO) |
| ID_TITULACION | NUMBER(*) |  | ✓ | D_TITULACION(ID_TITULACION) |
| ID_POBLACION_FAMILIAR | NUMBER(*) |  | ✓ | D_POBLACION(ID_POBLACION) |
| CURSOS_MATRICULADOS | NUMBER(*) |  |  |  |
| CURSO_MAS_ALTO_MATRICULADO | NUMBER(*) |  |  |  |
| CURSOS_EXTRA_GRADUACION | NUMBER |  |  |  |
| DURACION | NUMBER(*) |  |  |  |
| CREDITOS_MATRICULADOS | NUMBER |  |  |  |
| ID_RANGO_CREDITOS_MATRICULADOS | NUMBER(*) |  |  |  |
| CREDITOS_SUPERADOS | NUMBER |  |  |  |
| ID_RANGO_CREDITOS_SUPERADOS | NUMBER(*) |  |  |  |
| CREDITOS_NECESARIOS | NUMBER |  |  |  |
| ID_RANGO_CREDITOS_NECESARIOS | NUMBER(*) |  |  |  |
| CALIFICACION_FINAL | FLOAT(63) |  |  |  |
| ID_RANGO_CALIFICACION_FINAL | NUMBER(*) |  |  |  |
| SEXO | CHAR(1 CHAR) |  |  |  |
| ID_SEXO | NUMBER(*) |  | ✓ | D_SEXO(ID_SEXO) |
| EDAD | NUMBER |  |  |  |
| ID_FECHA_SOLICITUD_TITULO | NUMBER(*) |  |  |  |
| ID_FECHA_EGRESO | NUMBER(*) |  |  |  |
| GRADUADO | NUMBER(*) |  |  |  |
| TRASLADO | NUMBER(*) |  |  |  |
| SN_SOLICITA_TITULO | CHAR(1 CHAR) |  |  |  |
| SN_ABANDONO_INICIAL | CHAR(1 CHAR) |  |  |  |
| FLG_SOLICITUD_TITULO | NUMBER(*) |  |  |  |
| FLG_ABANDONO_INICIAL | NUMBER(*) |  |  |  |
| FLG_CALCULO_TASA | NUMBER(*) |  |  |  |
| FLG_GRADUADO_EN_TIEMPO | NUMBER(*) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |
| SN_GRADUADO_EN_TIEMPO | CHAR(1 CHAR) |  |  |  |
| ABANDONO_GENERICO | NUMBER(*) |  |  |  |
| ABANDONO_OFICIAL | NUMBER(*) |  |  |  |
| FLG_PLAN_OFICIAL | NUMBER(*) |  |  |  |
| CREDITOS_RECONOCIDOS | NUMBER |  |  |  |
| ID_RANGO_CREDITOS_RECONOCIDOS | NUMBER(*) |  |  |  |
| SN_CAMBIO_CICLO_GRADO | CHAR(1 CHAR) |  |  |  |
| FLG_DURACION_MEDIA | NUMBER(*) |  |  |  |
| ID_ESTUDIO_PREVIO | NUMBER(*) |  | ✓ | D_ESTUDIO_PREVIO(ID_ESTUDIO_PREVIO) |
| ID_PAIS_NACIONALIDAD | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| ID_CENTRO_ORIGEN | NUMBER(*) |  |  |  |
| SN_MULTIPLE_TITULACION | CHAR(1 CHAR) |  |  |  |
| SN_MOVILIDAD_IN | CHAR(1 CHAR) |  |  |  |
| FLG_MULTIPLE_TITULACION | NUMBER(*) |  |  |  |
| FLG_MOVILIDAD_IN | NUMBER(*) |  |  |  |
| ID_FECHA_CARGA | NUMBER(*) |  |  |  |
| ID_TIPO_TITULACION | NUMBER(*) |  |  |  |
| ID_TIPO_ESTUDIO | NUMBER(*) |  |  |  |
| ID_ESTUDIO | NUMBER(*) |  |  |  |
| ID_TIPO_CENTRO | NUMBER(*) |  |  |  |
| ID_CAMPUS_CENTRO | NUMBER(*) |  |  |  |
| ID_POBLACION_CENTRO | NUMBER(*) |  | ✓ | D_POBLACION(ID_POBLACION) |
| ID_TIPO_CENTRO_ORI | NUMBER(*) |  |  |  |
| ID_CAMPUS_CENTRO_ORI | NUMBER(*) |  |  |  |
| ID_POBLACION_CENTRO_ORI | NUMBER(*) |  |  |  |
| ID_RAMA_CONOCIMIENTO | NUMBER(*) |  |  |  |
| ID_PERSONA_NIP_NK | NUMBER(*) |  |  |  |
| ORDEN_BOE_PLAN | VARCHAR2(16 CHAR) |  |  |  |
| SN_DOCTORADO_VIGENTE | CHAR(1 CHAR) |  |  |  |
| SN_MOVILIDAD_OUT_INTERNACIONAL | CHAR(1 CHAR) |  |  |  |
| DURACION_REAL | NUMBER(9) |  |  |  |
| ID_PAIS_FAMILIAR | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| ID_PAIS_FAMILIAR_NK | VARCHAR2(3 CHAR) |  |  |  |
| ID_EDAD_EST | NUMBER(*) |  |  |  |
| ID_ESTUDIO_OTRA_UNIV_DEST | NUMBER(*) |  |  |  |
| ID_CENTRO_OTRA_UNIV_DEST | NUMBER(*) |  |  |  |
| SN_MOVILIDAD_OUT_NACIONAL | CHAR(1 CHAR) |  |  |  |
| SN_UNITA | CHAR(1 CHAR) |  |  |  |
| SN_UNITA_GEMINAE | CHAR(1 CHAR) |  |  |  |

### F_ESTUDIANTES_MOVILIDAD_IN

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CURSO_ACADEMICO_NK | NUMBER(*) |  | ✓ | D_CURSO_COHORTE(ID_CURSO_ACADEMICO) |
| ID_EXPEDIENTE_ACADEMICO_NK | NUMBER(*) |  |  |  |
| ID_ALUMNO_NIP_NK | NUMBER(*) |  |  |  |
| ID_CURSO_ACADEMICO | NUMBER(*) |  | ✓ | D_CURSO_ACADEMICO(ID_CURSO_ACADEMICO) |
| ID_EXPEDIENTE_ACADEMICO | NUMBER(*) |  |  |  |
| ID_ALUMNO | NUMBER(*) |  |  |  |
| ID_CENTRO | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_PLAN_ESTUDIO | NUMBER(*) |  | ✓ | F_TABLA_FUSION(ID_PLAN_ESTUDIO) |
| ID_TIPO_ESTUDIO | NUMBER(*) |  |  |  |
| ID_UNIVERSIDAD_ORIGEN | NUMBER(*) |  |  |  |
| ID_PAIS_UNIVERSIDAD_ORIGEN | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| ID_TUTOR | NUMBER(*) |  |  |  |
| ID_RANGO_CRED_SUPERADOS | NUMBER(*) |  | ✓ | D_RANGO_CREDITO(ID_RANGO_CREDITO) |
| ID_FECHA_INICIO_ESTANCIA | NUMBER(*) |  |  |  |
| ID_FECHA_FIN_ESTANCIA | NUMBER(*) |  |  |  |
| ID_SEXO | NUMBER(*) |  | ✓ | D_SEXO(ID_SEXO) |
| ID_PAIS_NACIONALIDAD | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| EDAD | NUMBER(*) |  |  |  |
| CREDITOS_SUPERA_DESTINO | NUMBER(5) |  |  |  |
| DURACION_ESTANCIA | NUMBER(*) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |
| ID_PROGRAMA_MOVILIDAD_NK | NUMBER(*) |  |  |  |
| ID_PROGRAMA_MOVILIDAD | NUMBER(*) |  |  |  |
| ID_ESTUDIO | NUMBER(*) |  |  |  |
| ID_RAMA_CONOCIMIENTO | NUMBER(*) |  |  |  |
| ID_FECHA_CARGA | NUMBER(*) |  |  |  |
| CREDITOS_MATRICULADOS | NUMBER(5) |  |  |  |
| ID_CENTRO_NK | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_CENTRO_IMPARTICION | NUMBER(*) |  |  |  |
| ID_CENTRO_IMPARTICION_NK | NUMBER(*) |  |  |  |
| ID_EDAD_EST | NUMBER(*) |  |  |  |
| ID_PLAN_ESTUDIO_MAX | NUMBER(*) |  |  |  |

### F_ESTUDIANTES_MOVILIDAD_OUT

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CURSO_ACADEMICO_NK | NUMBER(*) |  | ✓ | D_CURSO_COHORTE(ID_CURSO_ACADEMICO) |
| ID_EXPEDIENTE_ACADEMICO_NK | NUMBER(*) |  |  |  |
| ID_ALUMNO_NIP_NK | NUMBER(*) |  |  |  |
| ID_SOLICITUD_MOVILIDAD_NK | NUMBER(*) |  |  |  |
| ID_CURSO_ACADEMICO | NUMBER(*) |  | ✓ | D_CURSO_ACADEMICO(ID_CURSO_ACADEMICO) |
| ID_EXPEDIENTE_ACADEMICO | NUMBER(*) |  |  |  |
| ID_ALUMNO | NUMBER(*) |  |  |  |
| ID_CENTRO | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_PLAN_ESTUDIO | NUMBER(*) |  | ✓ | F_TABLA_FUSION(ID_PLAN_ESTUDIO) |
| ID_TIPO_ESTUDIO | NUMBER(*) |  |  |  |
| ID_UNIVERSIDAD_DESTINO | NUMBER(*) |  |  |  |
| ID_PAIS_UNIVERSIDAD_DESTINO | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| ID_TUTOR | NUMBER(*) |  |  |  |
| ID_AREA_ESTUDIOS_MOVILIDAD | NUMBER(*) |  |  |  |
| ID_NIVEL_ESTUDIOS_MOVILIDAD | NUMBER(*) |  |  |  |
| ID_TIPO_ACCESO | NUMBER(*) |  | ✓ | D_TIPO_ACCESO(ID_TIPO_ACCESO) |
| ID_RANGO_CRED_SUPERADOS | NUMBER(*) |  | ✓ | D_RANGO_CREDITO(ID_RANGO_CREDITO) |
| ID_RANGO_CRED_SUPERADOS_PREVIO | NUMBER(*) |  | ✓ | D_RANGO_CREDITO(ID_RANGO_CREDITO) |
| ID_FECHA_INICIO_ESTANCIA | NUMBER(*) |  |  |  |
| ID_FECHA_FIN_ESTANCIA | NUMBER(*) |  |  |  |
| ID_SEXO | NUMBER(*) |  | ✓ | D_SEXO(ID_SEXO) |
| ID_PAIS_NACIONALIDAD | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| ID_RANGO_NOTA_ADMISION | NUMBER(*) |  | ✓ | D_RANGO_NOTA_ADMISION(ID_RANGO_NOTA_ADMISION) |
| EDAD | NUMBER(3) |  |  |  |
| ORDEN_PREFERENCIA | NUMBER(*) |  |  |  |
| FLG_ACCESO_DIRECTO_MOVILIDAD | CHAR(1 CHAR) |  |  |  |
| DURACION_ESTANCIA | NUMBER(*) |  |  |  |
| ANOS_CURSADOS | NUMBER(*) |  |  |  |
| CURSO_MAS_ALTO_MATRICULADO | NUMBER(*) |  |  |  |
| CREDITOS_SUPERADOS_PREVIO | NUMBER(5) |  |  |  |
| CREDITOS_SUPERA_DESTINO | NUMBER(5) |  |  |  |
| NOTA_ADMISION | NUMBER(10) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |
| ID_POBLACION_FAMILIAR | NUMBER(*) |  | ✓ | D_POBLACION(ID_POBLACION) |
| ID_PROGRAMA_MOVILIDAD_NK | NUMBER(*) |  |  |  |
| ID_PROGRAMA_MOVILIDAD | NUMBER(*) |  |  |  |
| ID_ESTUDIO | NUMBER(*) |  |  |  |
| ID_RAMA_CONOCIMIENTO | NUMBER(*) |  |  |  |
| ID_FECHA_CARGA | NUMBER(*) |  |  |  |
| FLG_NUM_ACCESO_DIRECTO_MOVI | NUMBER(*) |  |  |  |
| ID_EDAD_EST | NUMBER(*) |  |  |  |

### F_ESTUDIO_PROPIO_MATRICULA

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CURSO_ACADEMICO_NK | NUMBER(*) |  | ✓ | D_CURSO_COHORTE(ID_CURSO_ACADEMICO) |
| ID_CURSO_ACADEMICO | NUMBER(*) |  | ✓ | D_CURSO_ACADEMICO(ID_CURSO_ACADEMICO) |
| ID_EXPEDIENTE_EST_PROPIO_NK | NUMBER(*) |  |  |  |
| ID_EXPEDIENTE_EST_PROPIO | NUMBER(*) |  |  |  |
| ID_PERSONA_NIP_NK | NUMBER(*) |  |  |  |
| ID_PERSONA | NUMBER(*) |  | ✓ | D_PERSONA(ID_PERSONA) |
| ID_ESTUDIO_PROPIO_NK | NUMBER(*) |  |  |  |
| ID_ESTUDIO_PROPIO_EDICION_NK | NUMBER(*) |  |  |  |
| ID_ESTUDIO_PROPIO | NUMBER(*) |  |  |  |
| ID_ESTUDIO_PROPIO_TIPO_NK | NUMBER(*) |  |  |  |
| ID_ESTUDIO_PROPIO_TIPO | NUMBER(*) |  |  |  |
| ID_ESTUDIO_PROPIO_MODALIDAD_NK | NUMBER(*) |  |  |  |
| ID_ESTUDIO_PROPIO_MODALIDAD | NUMBER(*) |  |  |  |
| TOTAL_CREDITOS_EP | NUMBER |  |  |  |
| NUMERO_CURSOS_EP | NUMBER(*) |  |  |  |
| ID_CENTRO_DEPT_GESTION_EP_NK | NUMBER(*) |  |  |  |
| ID_CENTRO_DEPT_GESTION_EP | NUMBER(*) |  |  |  |
| ID_RAMA_CONOCIMIENTO_EP_NK | NUMBER(*) |  |  |  |
| ID_RAMA_ESTUDIO_PROPIO | NUMBER(*) |  |  |  |
| ANO_ACAD_APERTURA | NUMBER(*) |  |  |  |
| CREDITOS_MATRICULADOS | NUMBER |  |  |  |
| FECHA_MATRICULA | DATE |  |  |  |
| ID_FECHA_MATRICULA | NUMBER(*) |  |  |  |
| FLG_NUEVO_INGRESO | NUMBER(*) |  |  |  |
| SN_NUEVO_INGRESO | CHAR(1 CHAR) |  |  |  |
| FLG_ESTUDIANTE_INTERNACIONAL | NUMBER(*) |  |  |  |
| SN_ESTUDIANTE_INTERNACIONAL | CHAR(1 CHAR) |  |  |  |
| ID_PAIS_NACIONALIDAD | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| ID_PAIS_NACIONALIDAD_NK | VARCHAR2(3 CHAR) |  |  |  |
| DOCUMENTO_IDENTIDAD | VARCHAR2(16 CHAR) |  |  |  |
| FECHA_NACIMIENTO | DATE |  |  |  |
| ID_PAIS_PROCEDENCIA | NUMBER(*) |  |  |  |
| ID_PAIS_PROCEDENCIA_NK | VARCHAR2(3 CHAR) |  |  |  |
| ID_POBLACION_FAMILIAR | NUMBER(*) |  | ✓ | D_POBLACION(ID_POBLACION) |
| COD_POSTAL_FAMILIAR | VARCHAR2(30 CHAR) |  |  |  |
| ID_POBLACION_CURSO | NUMBER(*) |  | ✓ | D_POBLACION(ID_POBLACION) |
| ID_PAIS_CURSO | NUMBER(*) |  |  |  |
| COD_POSTAL_CURSO | VARCHAR2(5 CHAR) |  |  |  |
| SEXO | CHAR(1 CHAR) |  |  |  |
| ID_SEXO | NUMBER(*) |  | ✓ | D_SEXO(ID_SEXO) |
| EDAD | NUMBER |  |  |  |
| FECHA_CARGA | DATE |  |  |  |
| ID_FECHA_CARGA | NUMBER(*) |  |  |  |
| ID_ORGANO_PROPONENTE_EP_NK | VARCHAR2(10 CHAR) |  |  |  |
| ID_ORGANO_PROPONENTE_EP | NUMBER(*) |  |  |  |
| EDAD_EST | VARCHAR2(10 CHAR) |  |  |  |
| ID_EDAD_EST | NUMBER(*) |  |  |  |

### F_MATRICULA

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CURSO_ACADEMICO_NK | NUMBER(*) |  | ✓ | D_CURSO_COHORTE(ID_CURSO_ACADEMICO) |
| ID_EXPEDIENTE_ACADEMICO_NK | NUMBER(*) |  |  |  |
| ID_CURSO_ACADEMICO | NUMBER(*) |  | ✓ | D_CURSO_ACADEMICO(ID_CURSO_ACADEMICO) |
| ID_ALUMNO | NUMBER(*) |  |  |  |
| ID_EXPEDIENTE_ACADEMICO | NUMBER(*) |  |  |  |
| ID_PLAN_ESTUDIO | NUMBER(*) |  | ✓ | F_TABLA_FUSION(ID_PLAN_ESTUDIO) |
| ID_CENTRO | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_PAIS_NACIONALIDAD | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| ID_ASIGNATURA | NUMBER(*) |  | ✓ | D_ASIGNATURA(ID_ASIGNATURA) |
| ID_CLASE_ASIGNATURA | NUMBER(*) |  | ✓ | D_CLASE_ASIGNATURA(ID_CLASE_ASIGNATURA) |
| ID_TIPO_ACCESO | NUMBER(*) |  | ✓ | D_TIPO_ACCESO(ID_TIPO_ACCESO) |
| ID_CURSO_ACADEMICO_COHORTE | NUMBER(*) |  |  |  |
| ID_POBLACION_FAMILIAR | NUMBER(*) |  | ✓ | D_POBLACION(ID_POBLACION) |
| ID_FECHA_MATRICULA | NUMBER(*) |  |  |  |
| SEXO | CHAR(1 CHAR) |  |  |  |
| ID_SEXO | NUMBER(*) |  | ✓ | D_SEXO(ID_SEXO) |
| EDAD | NUMBER |  |  |  |
| CREDITOS | NUMBER |  |  |  |
| CURSO_ORDEN | VARCHAR2(2 CHAR) |  |  |  |
| CURSO_MAS_ALTO_MATRICULADO | NUMBER(*) |  |  |  |
| NUMERO_MATRICULAS | NUMBER(*) |  |  |  |
| RANGO_NUM_MATRICULAS | VARCHAR2(10 CHAR) |  |  |  |
| FLG_NUEVO_INGRESO | NUMBER(*) |  |  |  |
| SN_NUEVO_INGRESO | CHAR(1 CHAR) |  |  |  |
| FLG_EN_PROGRAMA_MOVILIDAD | NUMBER(*) |  |  |  |
| SN_PROG_MOVILIDAD | CHAR(1 CHAR) |  |  |  |
| ANYO_ACCESO_SUE | NUMBER(*) |  |  |  |
| FLG_NUEVO_ACCESO_SUE | NUMBER(*) |  |  |  |
| SN_NUEVO_ACCESO_SUE | CHAR(1 CHAR) |  |  |  |
| FLG_CAMBIO_CICLO_GRADO | NUMBER(*) |  |  |  |
| SN_CAMBIO_CICLO_GRADO | CHAR(1 CHAR) |  |  |  |
| FLG_TRASLADO_MISMO_ESTUDIO | NUMBER(*) |  |  |  |
| SN_TRASLADO_MISMO_ESTUDIO | CHAR(1 CHAR) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |
| ID_ESTUDIO_PREVIO | NUMBER(*) |  | ✓ | D_ESTUDIO_PREVIO(ID_ESTUDIO_PREVIO) |
| ID_RANGO_NOTA_CRUE | NUMBER(*) |  |  |  |
| SN_CAMBIO_CICLO_GRADO_NUEVO | CHAR(1 CHAR) |  |  |  |
| ID_DEDICACION | NUMBER(*) |  |  |  |
| ID_PLAN_GRUPO_MATRICULA | NUMBER(*) |  |  |  |
| FLG_MOVILIDAD_IN | NUMBER(*) |  |  |  |
| SN_MOVILIDAD_IN | CHAR(1 CHAR) |  |  |  |
| ID_GRUPO | NUMBER(*) |  | ✓ | D_GRUPO(ID_GRUPO) |
| ID_FECHA_CARGA | NUMBER(*) |  |  |  |
| ID_TIPO_ASIGNATURA | NUMBER(*) |  |  |  |
| ID_TIPO_ESTUDIO | NUMBER(*) |  |  |  |
| ID_ESTUDIO | NUMBER(*) |  |  |  |
| ID_TIPO_CENTRO | NUMBER(*) |  |  |  |
| ID_CAMPUS_CENTRO | NUMBER(*) |  |  |  |
| ID_POBLACION_CENTRO | NUMBER(*) |  | ✓ | D_POBLACION(ID_POBLACION) |
| ID_RAMA_CONOCIMIENTO | NUMBER(*) |  |  |  |
| ID_PLAN_GRUPO_MATRICULA_NK | NUMBER(*) |  |  |  |
| ID_CENTRO_IMPARTICION_NK | NUMBER(*) |  |  |  |
| COD_POSTAL_CURSO | VARCHAR2(5 CHAR) |  |  |  |
| ID_DETALLE_CUPO_GENERAL | NUMBER(*) |  |  |  |
| ID_DETALLE_CUPO_GENERAL_NK | VARCHAR2(3 CHAR) |  |  |  |
| ID_UNIVERSIDAD_ORIGEN | NUMBER(*) |  |  |  |
| ID_UNIVERSIDAD_ORIGEN_NK | NUMBER(*) |  |  |  |
| ID_PAIS_UNIVERSIDAD_ORIGEN | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| ID_PAIS_UNIVERSIDAD_ORIGEN_NK | VARCHAR2(3 CHAR) |  |  |  |
| FLG_ESTUDIANTE_INTERNACIONAL | NUMBER(*) |  |  |  |
| SN_ESTUDIANTE_INTERNACIONAL | CHAR(1 CHAR) |  |  |  |
| ID_PERSONA_NIP_NK | NUMBER(*) |  |  |  |
| SUPER_EXPEDIENTE | NUMBER(*) |  |  |  |
| ID_ASIGNATURA_NK | NUMBER(*) |  | ✓ | D_ASIGNATURA(ID_ASIGNATURA) |
| ID_PLAN_ESTUDIO_NK | NUMBER(*) |  |  |  |
| ID_TIPO_ESTUDIO_NK | NUMBER(*) |  |  |  |
| ID_TIPO_ACCESO_NK | VARCHAR2(3 CHAR) |  | ✓ | D_TIPO_ACCESO(ID_TIPO_ACCESO) |
| ID_CENTRO_NK | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_ESTUDIO_NK | NUMBER(*) |  |  |  |
| ID_DEDICACION_NK | NUMBER(*) |  |  |  |
| NUM_REGS_GRANO | NUMBER(*) |  |  |  |
| ID_PAIS_BACH_PROCEDENCIA | NUMBER(*) |  |  |  |
| ID_PAIS_BACH_PROCEDENCIA_NK | VARCHAR2(5 CHAR) |  |  |  |
| ORDEN_BOE_PLAN | VARCHAR2(16 CHAR) |  |  |  |
| SN_DOCTORADO_VIGENTE | CHAR(1 CHAR) |  |  |  |
| COD_POSTAL_FAMILIAR | VARCHAR2(30 CHAR) |  |  |  |
| CURSO_IMPARTICION_ASIG | VARCHAR2(2 CHAR) |  |  |  |
| ID_MODALIDAD_PLAN_NK | VARCHAR2(3 CHAR) |  |  |  |
| ID_MODALIDAD_PLAN | NUMBER(*) |  |  |  |
| ID_PAIS_FAMILIAR | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| ID_PAIS_FAMILIAR_NK | VARCHAR2(3 CHAR) |  |  |  |
| FLG_EQUIVALENTE_TC_SIIU | NUMBER(16) |  |  |  |
| NUM_REGS_GRANO_MOV | NUMBER(*) |  |  |  |
| FLG_EQUIVALENTE_TC_SIIU_MOV | NUMBER(16) |  |  |  |
| ID_PROGRAMA_MOVILIDAD_NK | NUMBER(*) |  |  |  |
| SN_PROGRAMA_INTERNACIONAL | CHAR(1 CHAR) |  |  |  |
| SN_MASTER_HABILITANTE | CHAR(1 CHAR) |  |  |  |
| FLG_MULTIPLE_TITULACION | NUMBER(*) |  |  |  |
| SN_MULTIPLE_TITULACION | CHAR(1 CHAR) |  |  |  |
| FLG_DISCAPACIDAD | NUMBER(*) |  |  |  |
| SN_DISCAPACIDAD | CHAR(1 BYTE) |  |  |  |
| FLG_INTERUNIVERSITARIO | NUMBER(*) |  |  |  |
| SN_INTERUNIVERSITARIO | CHAR(1 BYTE) |  |  |  |
| FLG_COORDINADOR | NUMBER(*) |  |  |  |
| SN_COORDINADOR | CHAR(1 BYTE) |  |  |  |
| ID_EDAD_EST | NUMBER(*) |  |  |  |
| ID_TITULO_PREVIO_MASTER_NK | VARCHAR2(11 CHAR) |  |  |  |
| ID_TITULO_PREVIO_MASTER | NUMBER(*) |  |  |  |
| ID_PLAN_ESTUDIO_ANO_DATOS | NUMBER(*) |  |  |  |

### F_OFERTA_ACUERDO_BILATERAL

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CURSO_ACADEMICO_NK | NUMBER(*) |  | ✓ | D_CURSO_COHORTE(ID_CURSO_ACADEMICO) |
| ID_ACUERDO_BILATERAL_NK | NUMBER(*) |  |  |  |
| ID_AREA_ESTUDIOS_NK | NUMBER(*) |  |  |  |
| ID_NIVEL_ESTUDIOS_NK | NUMBER(*) |  |  |  |
| ID_CURSO_ACADEMICO | NUMBER(*) |  | ✓ | D_CURSO_ACADEMICO(ID_CURSO_ACADEMICO) |
| ID_ACUERDO_BILATERAL | NUMBER(*) |  |  |  |
| ID_AREA_ESTUDIOS_MOVILIDAD | NUMBER(*) |  |  |  |
| ID_NIVEL_ESTUDIOS_MOVILIDAD | NUMBER(*) |  |  |  |
| IN_OUT | VARCHAR2(5 CHAR) |  |  |  |
| ID_UNIVERSIDAD_ACUERDO | NUMBER(*) |  |  |  |
| ID_PAIS_UNIVERSIDAD_ACUERDO | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| ID_COLECTIVO_MOVILIDAD | NUMBER(*) |  |  |  |
| ID_CURSO_INICIO_VIGENCIA | NUMBER(*) |  |  |  |
| ID_CURSO_FIN_VIGENCIA | NUMBER(*) |  |  |  |
| ID_FECHA_REFERENCIA | NUMBER(*) |  |  |  |
| DURACION_ESTANCIA_ALUMNOS | NUMBER(*) |  |  |  |
| DURACION_ESTANCIA_DOCENTES | NUMBER(*) |  |  |  |
| HORAS_CLASE_SEMANA | NUMBER(*) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |
| ID_PROGRAMA_MOVILIDAD | NUMBER(*) |  |  |  |
| ID_IDIOMA_NIVEL_PRINCIPAL | NUMBER(*) |  |  |  |
| ID_IDIOMA_NIVEL_SECUNDARIO | NUMBER(*) |  |  |  |
| ID_CENTRO | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_FECHA_CARGA | NUMBER(*) |  |  |  |
| ID_COLECTIVO_NK | VARCHAR2(4 CHAR) |  |  |  |
| ID_PROGRAMA_MOVILIDAD_NK | NUMBER(*) |  |  |  |
| ID_UNIVERSIDAD_DESTINO_NK | NUMBER(*) |  |  |  |
| ID_CURSO_ACADEMICO_INICIO_NK | NUMBER(*) |  |  |  |
| ID_CURSO_ACADEMICO_FIN_NK | NUMBER(*) |  |  |  |
| ENTRADA_SALIDA | CHAR(1 CHAR) |  |  |  |
| COD_PLAZA_OFERTADA | VARCHAR2(90 CHAR) |  |  |  |
| COLECTIVO_OFERTA | VARCHAR2(20 CHAR) |  |  |  |
| ID_CENTRO_NK | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_IDIOMA_1_NK | NUMBER(*) |  |  |  |
| ID_NIVEL_IDIOMA_1_NK | NUMBER(*) |  |  |  |
| ID_IDIOMA_2_NK | NUMBER(*) |  |  |  |
| ID_NIVEL_IDIOMA_2_NK | NUMBER(*) |  |  |  |
| ID_ALUMNO | NUMBER(*) |  |  |  |
| ID_ALUMNO_NIP_NK | NUMBER(*) |  |  |  |
| FLG_OFERTA_ALUMNOS | NUMBER(*) |  |  |  |
| FLG_OFERTA_DOCENTES | NUMBER(*) |  |  |  |
| FECHA_REFERENCIA | DATE |  |  |  |
| FLG_PLAZA_FICTICIA | NUMBER(*) |  |  |  |

### F_OFERTA_ADMISION

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CURSO_ACADEMICO | NUMBER(*) |  | ✓ | D_CURSO_ACADEMICO(ID_CURSO_ACADEMICO) |
| ID_PLAN_ESTUDIO | NUMBER(*) |  | ✓ | F_TABLA_FUSION(ID_PLAN_ESTUDIO) |
| ID_TIPO_ESTUDIO | NUMBER(*) |  |  |  |
| ID_CENTRO | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_TIPO_ACCESO | NUMBER(*) |  | ✓ | D_TIPO_ACCESO(ID_TIPO_ACCESO) |
| ID_ESTUDIO_PREVIO | NUMBER(*) |  | ✓ | D_ESTUDIO_PREVIO(ID_ESTUDIO_PREVIO) |
| ID_CUPO_ADJUDICACION | NUMBER(*) |  | ✓ | D_CUPO_ADJUDICACION(ID_CUPO_ADJUDICACION) |
| PLAZAS_OFERTADAS | NUMBER(*) |  |  |  |
| PLAZAS_ASIGNADAS | NUMBER(*) |  |  |  |
| PLAZAS_SOLICITADAS | NUMBER(*) |  |  |  |
| NOTA_AGREGADA | NUMBER(10) |  |  |  |
| NOTA_CORTE_ADJUDICACION_1 | NUMBER(10) |  |  |  |
| NOTA_CORTE_ADJUDICACION_2 | NUMBER(10) |  |  |  |
| NOTA_CORTE_DEFINITIVA_1 | NUMBER(10) |  |  |  |
| NOTA_CORTE_DEFINITIVA_2 | NUMBER(10) |  |  |  |
| FLG_ADMITIDOS_TODOS_1 | CHAR(1 CHAR) |  |  |  |
| FLG_ADMITIDOS_TODOS_2 | CHAR(1 CHAR) |  |  |  |
| PARTICIPA_1 | NUMBER(*) |  |  |  |
| PARTICIPA_2 | NUMBER(*) |  |  |  |
| ID_CURSO_ACADEMICO_NK | NUMBER(*) |  | ✓ | D_CURSO_COHORTE(ID_CURSO_ACADEMICO) |
| FECHA_CARGA | DATE |  |  |  |
| NOTA_MEDIA_ADMISION | NUMBER(10) |  |  |  |
| PRELA_CONVO_NOTA_DEF | CHAR(1 CHAR) |  |  |  |
| PRELA_CONVO_NOTA_DEF_1 | CHAR(1 CHAR) |  |  |  |
| PRELA_CONVO_NOTA_DEF_2 | CHAR(1 CHAR) |  |  |  |
| NUM_CREDENCIAL_UNED | NUMBER(*) |  |  |  |
| PLAZAS_SOLICITADAS_PREF_1 | NUMBER(*) |  |  |  |
| ID_FECHA_CARGA | NUMBER(*) |  |  |  |
| ID_TIPO_CENTRO | NUMBER(*) |  |  |  |
| ID_CAMPUS | NUMBER(*) |  |  |  |
| ID_POBLACION_CENTRO | NUMBER(*) |  | ✓ | D_POBLACION(ID_POBLACION) |
| ID_ESTUDIO | NUMBER(*) |  |  |  |
| ID_RAMA_CONOCIMIENTO | NUMBER(*) |  |  |  |
| ORDEN_BOE_PLAN | VARCHAR2(16 CHAR) |  |  |  |
| SN_DOCTORADO_VIGENTE | CHAR(1 CHAR) |  |  |  |
| ID_PERSONA_NIP_COORD_NK | NUMBER(*) |  |  |  |
| CORREO_COORD | VARCHAR2(100 CHAR) |  |  |  |
| ID_PERSONA_COORD | NUMBER(*) |  |  |  |
| FLG_INTERUNIVERSITARIO | NUMBER(*) |  |  |  |
| FLG_COORDINADOR | NUMBER(*) |  |  |  |
| FLG_MULTIPLE_TITULACION | NUMBER(*) |  |  |  |
| FLG_MASTER_HAB | NUMBER(*) |  |  |  |
| SN_MASTER_HABILITANTE | CHAR(1 CHAR) |  |  |  |
| SN_MULTIPLE_TITULACION | CHAR(1 CHAR) |  |  |  |
| SN_INTERUNIVERSITARIO | CHAR(1 CHAR) |  |  |  |
| SN_COORDINADOR | CHAR(1 CHAR) |  |  |  |

### F_RENDIMIENTO

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CURSO_ACADEMICO_NK | NUMBER(*) |  | ✓ | D_CURSO_COHORTE(ID_CURSO_ACADEMICO) |
| ID_EXPEDIENTE_ACADEMICO_NK | NUMBER(*) |  |  |  |
| ID_CURSO_ACADEMICO | NUMBER(*) |  | ✓ | D_CURSO_ACADEMICO(ID_CURSO_ACADEMICO) |
| ID_EXPEDIENTE_ACADEMICO | NUMBER(*) |  |  |  |
| ID_ASIGNATURA | NUMBER(*) |  | ✓ | D_ASIGNATURA(ID_ASIGNATURA) |
| ID_CONVOCATORIA | NUMBER(*) |  | ✓ | D_CONVOCATORIA(ID_CONVOCATORIA) |
| ID_PLAN_ESTUDIO | NUMBER(*) |  | ✓ | F_TABLA_FUSION(ID_PLAN_ESTUDIO) |
| ID_CENTRO | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_TIPO_ACCESO | NUMBER(*) |  | ✓ | D_TIPO_ACCESO(ID_TIPO_ACCESO) |
| ID_GRUPO | NUMBER(*) |  | ✓ | D_GRUPO(ID_GRUPO) |
| ID_TIPO_DOCENCIA | NUMBER(*) |  | ✓ | D_TIPO_DOCENCIA(ID_TIPO_DOCENCIA) |
| ID_CLASE_ASIGNATURA | NUMBER(*) |  | ✓ | D_CLASE_ASIGNATURA(ID_CLASE_ASIGNATURA) |
| ID_TIPO_RECONOCIMIENTO | NUMBER(*) |  | ✓ | D_TIPO_RECONOCIMIENTO(ID_TIPO_RECONOCIMIENTO) |
| ID_CALIFICACION | NUMBER(*) |  | ✓ | D_CALIFICACION(ID_CALIFICACION) |
| ID_RANGO_NOTA_NUMERICA | NUMBER(*) |  | ✓ | D_RANGO_NOTA_NUMERICA(ID_RANGO_NOTA_NUMERICA) |
| ID_ALUMNO | NUMBER(*) |  |  |  |
| ID_SEXO | NUMBER(*) |  | ✓ | D_SEXO(ID_SEXO) |
| ID_CURSO_ACADEMICO_COHORTE | NUMBER(*) |  |  |  |
| ID_PAIS_NACIONALIDAD | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| ID_POBLACION_FAMILIAR | NUMBER(*) |  | ✓ | D_POBLACION(ID_POBLACION) |
| ID_FECHA_CALIFICACION | NUMBER(*) |  |  |  |
| EDAD | NUMBER |  |  |  |
| NOTA_NUMERICA | FLOAT(63) |  |  |  |
| CREDITOS | NUMBER |  |  |  |
| ORDEN_CONVOCATORIA | NUMBER(*) |  |  |  |
| CONVOCATORIAS_CONSUMIDAS | NUMBER(*) |  |  |  |
| NUMERO_MATRICULAS | NUMBER(*) |  |  |  |
| RANGO_NUM_MATRICULAS | VARCHAR2(10 CHAR) |  |  |  |
| CURSO_MAS_ALTO_MATRICULADO | NUMBER(*) |  |  |  |
| ANYO_ACCESO_SUE | NUMBER(*) |  |  |  |
| FLG_SUPERADA | NUMBER(*) |  |  |  |
| FLG_PRESENTADA | NUMBER(*) |  |  |  |
| FLG_SUSPENDIDA | NUMBER(*) |  |  |  |
| FLG_RECONOCIDA | NUMBER(*) |  |  |  |
| FLG_MATRICULADA | NUMBER(*) |  |  |  |
| FLG_TRANSFERIDA | NUMBER(*) |  |  |  |
| FLG_ULTIMA_CONVOCATORIA | NUMBER(*) |  |  |  |
| FLG_CALCULO_TASAS | NUMBER(*) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |
| NOTA_ADMISION | NUMBER(10) |  |  |  |
| ID_RANGO_NOTA_ADMISION | NUMBER(*) |  | ✓ | D_RANGO_NOTA_ADMISION(ID_RANGO_NOTA_ADMISION) |
| ID_ESTUDIO_PREVIO | NUMBER(*) |  | ✓ | D_ESTUDIO_PREVIO(ID_ESTUDIO_PREVIO) |
| SN_CAMBIO_CICLO_GRADO | CHAR(1 CHAR) |  |  |  |
| FLG_NUEVO_INGRESO | NUMBER(*) |  |  |  |
| SN_NUEVO_INGRESO | CHAR(1 CHAR) |  |  |  |
| ID_DEDICACION | NUMBER(*) |  |  |  |
| ID_FECHA_CARGA | NUMBER(*) |  |  |  |
| ID_TIPO_ESTUDIO | NUMBER(*) |  |  |  |
| ID_ESTUDIO | NUMBER(*) |  |  |  |
| ID_RAMA_CONOCIMIENTO | NUMBER(*) |  |  |  |
| ID_CENTRO_NK | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_TIPO_CENTRO | NUMBER(*) |  |  |  |
| ID_CAMPUS_CENTRO | NUMBER(*) |  |  |  |
| ID_POBLACION_CENTRO | NUMBER(*) |  | ✓ | D_POBLACION(ID_POBLACION) |
| ID_TIPO_ASIGNATURA | NUMBER(*) |  |  |  |
| ORDEN_BOE_PLAN | VARCHAR2(16 CHAR) |  |  |  |
| SN_DOCTORADO_VIGENTE | CHAR(1 CHAR) |  |  |  |
| CURSO_IMPARTICION_ASIG | VARCHAR2(2 CHAR) |  |  |  |
| ID_RANGO_NOTA_EGRACONS | NUMBER(*) |  |  |  |
| ID_PAIS_FAMILIAR | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| ID_PAIS_FAMILIAR_NK | VARCHAR2(3 CHAR) |  |  |  |
| FLG_EN_PROGRAMA_MOVILIDAD | NUMBER(*) |  |  |  |
| ID_PLAN_GRUPO_MATRICULA | NUMBER(*) |  |  |  |
| ID_PLAN_GRUPO_MATRICULA_NK | NUMBER(*) |  |  |  |
| ID_CENTRO_IMPARTICION | NUMBER(*) |  |  |  |
| ID_CENTRO_IMPARTICION_NK | NUMBER(*) |  |  |  |
| SN_MOVILIDAD_IN | CHAR(1 CHAR) |  |  |  |
| FLG_MOVILIDAD_IN | NUMBER(*) |  |  |  |
| ID_ESTUDIO_NK | NUMBER(*) |  |  |  |
| FLG_COMPENSADA | NUMBER(*) |  |  |  |
| SN_COMPENSADA | CHAR(1 CHAR) |  |  |  |
| ID_EDAD_EST | NUMBER(*) |  |  |  |
| ID_ASIGNATURA_NK | NUMBER(*) |  | ✓ | D_ASIGNATURA(ID_ASIGNATURA) |
| ID_PLAN_ESTUDIO_NK | NUMBER(*) |  |  |  |
| SN_PROG_MOVILIDAD | CHAR(1 CHAR) |  |  |  |

### F_SOLICITANTE_ADMISION

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_PREINSCRIPCION | NUMBER(*) |  |  |  |
| ID_CURSO_ACADEMICO | NUMBER(*) |  | ✓ | D_CURSO_ACADEMICO(ID_CURSO_ACADEMICO) |
| ID_CONVOCATORIA | NUMBER(*) |  | ✓ | D_CONVOCATORIA(ID_CONVOCATORIA) |
| ID_TIPO_ACCESO_PREINS | NUMBER(*) |  | ✓ | D_TIPO_ACCESO_PREINSCRIPCION(ID_TIPO_ACCESO_PREINS) |
| ID_TIPO_PROCEDIMIENTO | NUMBER(*) |  | ✓ | D_TIPO_PROCEDIMIENTO(ID_TIPO_PROCEDIMIENTO) |
| ID_ESTUDIO_PREVIO | NUMBER(*) |  | ✓ | D_ESTUDIO_PREVIO(ID_ESTUDIO_PREVIO) |
| ID_UNIVERSIDAD | NUMBER(*) |  | ✓ | D_UNIVERSIDAD(ID_UNIVERSIDAD) |
| ID_CUPO_ADJUDICACION | NUMBER(*) |  | ✓ | D_CUPO_ADJUDICACION(ID_CUPO_ADJUDICACION) |
| NOTA_ADMISION | NUMBER(10) |  |  |  |
| ID_PLAN_ESTUDIO | NUMBER(*) |  | ✓ | F_TABLA_FUSION(ID_PLAN_ESTUDIO) |
| ORDEN_PREFERENCIA | NUMBER(*) |  |  |  |
| RESOLUCION_SOLICITUD | CHAR(1 CHAR) |  |  |  |
| SN_ADMITIDO | CHAR(1 CHAR) |  |  |  |
| ORDEN_ADJUDICACION | NUMBER(*) |  |  |  |
| FECHA_PREINSCRIPCION | DATE |  |  |  |
| ID_PERSONA | NUMBER(*) |  | ✓ | D_PERSONA(ID_PERSONA) |
| FECHA_NACIMIENTO | DATE |  |  |  |
| ID_SEXO | NUMBER(*) |  | ✓ | D_SEXO(ID_SEXO) |
| SEXO | CHAR(1 CHAR) |  |  |  |
| ID_POBLACION_NACIMIENTO | NUMBER(*) |  | ✓ | D_POBLACION(ID_POBLACION) |
| ID_PAIS_NACIMIENTO | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| ID_PAIS_NACIONALIDAD | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| EDAD | NUMBER |  |  |  |
| FECHA_CARGA | DATE |  |  |  |
| ID_CENTRO | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_PAIS_UNIVERSIDAD_ORIGEN | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| RESOLUCION_LLAMAMIENTO | VARCHAR2(2 CHAR) |  |  |  |
| NUM_LLAMAMIENTO | CHAR(1 CHAR) |  |  |  |
| RESOLUCION_FINAL | VARCHAR2(2000 CHAR) |  |  |  |
| ID_ESTADO_ADJUDICACION | NUMBER(*) |  | ✓ | D_ESTADO_ADJUDICACION(ID_ESTADO_ADJUDICACION) |
| ID_CURSO_ACADEMICO_NK | NUMBER(*) |  | ✓ | D_CURSO_COHORTE(ID_CURSO_ACADEMICO) |
| ID_RANGO_NOTA_ADMISION | NUMBER(*) |  | ✓ | D_RANGO_NOTA_ADMISION(ID_RANGO_NOTA_ADMISION) |
| SN_MATRICULADO | CHAR(1 CHAR) |  |  |  |
| SN_PARTICIPA_ADJUDICACION | CHAR(1 CHAR) |  |  |  |
| ID_POBLACION_FAMILIAR | NUMBER(*) |  | ✓ | D_POBLACION(ID_POBLACION) |
| SN_CREDENCIAL_UNED | CHAR(1 CHAR) |  |  |  |
| FLG_CREDENCIAL_UNED | NUMBER(*) |  |  |  |
| NOTA_ACCESO | NUMBER(10) |  |  |  |
| ID_FECHA_CARGA | NUMBER(*) |  |  |  |
| ID_TIPO_CENTRO | NUMBER(*) |  |  |  |
| ID_CAMPUS | NUMBER(*) |  |  |  |
| ID_POBLACION_CENTRO | NUMBER(*) |  | ✓ | D_POBLACION(ID_POBLACION) |
| ID_TIPO_ESTUDIO | NUMBER(*) |  |  |  |
| ID_ESTUDIO | NUMBER(*) |  |  |  |
| ID_RAMA_CONOCIMIENTO | NUMBER(*) |  |  |  |
| ID_DETALLE_CUPO_GENERAL | NUMBER(*) |  |  |  |
| ID_DETALLE_CUPO_GENERAL_NK | VARCHAR2(3 CHAR) |  |  |  |
| ID_PAIS_FAMILIAR | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| ID_PAIS_FAMILIAR_NK | VARCHAR2(3 CHAR) |  |  |  |
| EDAD_EST | VARCHAR2(10 CHAR) |  |  |  |
| ID_EDAD_EST | NUMBER(*) |  |  |  |

### F_SOLICITUDES_MOVILIDAD

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_SOLICITUD_MOVILIDAD_NK | NUMBER(*) |  |  |  |
| ID_CURSO_ACADEMICO_NK | NUMBER(*) |  | ✓ | D_CURSO_COHORTE(ID_CURSO_ACADEMICO) |
| ID_EXPEDIENTE_ACADEMICO_NK | NUMBER(*) |  |  |  |
| ID_ALUMNO_NIP_NK | NUMBER(*) |  |  |  |
| ID_CURSO_ACADEMICO | NUMBER(*) |  | ✓ | D_CURSO_ACADEMICO(ID_CURSO_ACADEMICO) |
| ID_EXPEDIENTE_ACADEMICO | NUMBER(*) |  |  |  |
| ID_ALUMNO | NUMBER(*) |  |  |  |
| ID_PAIS_NACIONALIDAD | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |
| ID_SEXO | NUMBER(*) |  | ✓ | D_SEXO(ID_SEXO) |
| ID_PLAN_ESTUDIO | NUMBER(*) |  | ✓ | F_TABLA_FUSION(ID_PLAN_ESTUDIO) |
| ID_TIPO_ESTUDIO | NUMBER(*) |  |  |  |
| ID_CENTRO | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| ID_TIPO_ACCESO | NUMBER(*) |  | ✓ | D_TIPO_ACCESO(ID_TIPO_ACCESO) |
| ID_AREA_ESTUDIOS_MOVILIDAD | NUMBER(*) |  |  |  |
| ID_NIVEL_ESTUDIOS_MOVILIDAD | NUMBER(*) |  |  |  |
| ID_IDIOMA_MOVILIDAD | NUMBER(*) |  |  |  |
| ID_FECHA_SOLICITUD | NUMBER(*) |  |  |  |
| ID_RANGO_NOTA_ADMISION | NUMBER(*) |  | ✓ | D_RANGO_NOTA_ADMISION(ID_RANGO_NOTA_ADMISION) |
| ID_RANGO_CRED_SUPERADOS_PREVIO | NUMBER(*) |  | ✓ | D_RANGO_CREDITO(ID_RANGO_CREDITO) |
| ORDEN_PREFERENCIA | NUMBER(*) |  |  |  |
| FLG_ACEPTADA | CHAR(1 CHAR) |  |  |  |
| FLG_RENUNCIA | CHAR(1 CHAR) |  |  |  |
| ACEPTADA | NUMBER(*) |  |  |  |
| RENUNCIA | NUMBER(*) |  |  |  |
| EDAD | NUMBER(3) |  |  |  |
| DURACION_ESTANCIA | NUMBER(*) |  |  |  |
| ANOS_CURSADOS | NUMBER(*) |  |  |  |
| CREDITOS_SUPERADOS | NUMBER(5) |  |  |  |
| NOTA_ADMISION | NUMBER(10) |  |  |  |
| FECHA_CARGA | DATE |  |  |  |
| ID_POBLACION_FAMILIAR | NUMBER(*) |  | ✓ | D_POBLACION(ID_POBLACION) |
| ID_PROGRAMA_MOVILIDAD | NUMBER(*) |  |  |  |
| ID_ESTUDIO | NUMBER(*) |  |  |  |
| ID_RAMA_CONOCIMIENTO | NUMBER(*) |  |  |  |
| ID_FECHA_CARGA | NUMBER(*) |  |  |  |
| ID_EDAD_EST | NUMBER(*) |  |  |  |
| ID_UNIVERSIDAD_DESTINO | NUMBER(*) |  |  |  |
| ID_PAIS_UNIVERSIDAD_DESTINO | NUMBER(*) |  | ✓ | D_PAIS(ID_PAIS) |

### F_TABLA_FUSION

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CURSO_ACADEMICO | NUMBER(*) | ✓ | ✓ | D_CURSO_ACADEMICO(ID_CURSO_ACADEMICO) |
| ID_PLAN_ESTUDIO | NUMBER(*) | ✓ | ✓ | F_TABLA_FUSION(ID_PLAN_ESTUDIO) |
| TASA_EXITO_PONDERADA | NUMBER |  |  |  |
| TASA_RENDIMIENTO_PONDERADA | NUMBER |  |  |  |
| BASE_PONDERACION_TASAS_EXITO | NUMBER |  |  |  |
| BASE_PONDERACION_TASAS_RTO | NUMBER |  |  |  |
| TASA_EFICIENCIA_PONDERADA | NUMBER |  |  |  |
| BASE_PONDERACION_TASAS_EGRE | NUMBER |  |  |  |
| ALUMNOS_GRADUADOS | NUMBER |  |  |  |
| DURACION_PONDERADA | NUMBER |  |  |  |
| BASE_PONDERACION_DURACION | NUMBER |  |  |  |
| ALUMNOS_MATRICULADOS | NUMBER |  |  |  |
| ALUMNOS_MATRICULADOS_NING | NUMBER |  |  |  |

### F_TABLA_FUSION_ESTCEN

| Columna | Tipo | PK | FK | Referencia |
|---------|------|----|----|------------|
| ID_CURSO_ACADEMICO | NUMBER(*) |  | ✓ | D_CURSO_ACADEMICO(ID_CURSO_ACADEMICO) |
| ID_ESTUDIO | NUMBER(*) |  |  |  |
| ID_CENTRO | NUMBER(*) |  | ✓ | D_CENTRO(ID_CENTRO) |
| TASA_EXITO_PONDERADA | NUMBER |  |  |  |
| TASA_RENDIMIENTO_PONDERADA | NUMBER |  |  |  |
| BASE_PONDERACION_TASAS_EXITO | NUMBER |  |  |  |
| BASE_PONDERACION_TASAS_RTO | NUMBER |  |  |  |
| ALUMNOS_MATRICULADOS | NUMBER |  |  |  |
| ALUMNOS_MATRICULADOS_NING | NUMBER |  |  |  |
| TASA_EFICIENCIA_PONDERADA | NUMBER |  |  |  |
| BASE_PONDERACION_TASAS_EGRE | NUMBER |  |  |  |
| ALUMNOS_GRADUADOS | NUMBER |  |  |  |
| DURACION_PONDERADA | NUMBER |  |  |  |
| BASE_PONDERACION_DURACION | NUMBER |  |  |  |
| ID_TIPO_ESTUDIO | NUMBER(*) |  |  |  |
| SN_DOCTORADO_VIGENTE | CHAR(1 CHAR) |  |  |  |
| DOC_ALUMNOS_INFORME | NUMBER(*) |  |  |  |
| VALORACION_ALUMNOS | NUMBER(9) |  |  |  |
| VALORACION_PROFESORES | NUMBER(9) |  |  |  |
| DOC_ALUMNOS_BECA | NUMBER(*) |  |  |  |
| ID_RAMA_CONOCIMIENTO | NUMBER(*) |  |  |  |