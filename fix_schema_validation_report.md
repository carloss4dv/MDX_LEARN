# Informe de Corrección de Esquema

**Fecha:** 2025-06-03 13:04:00

**Respaldo creado en:** backup_generators_20250603_130359

## Resumen de Cambios

- function_commented: 18
- columns_removed: 26
- columns_added: 5

## Detalle de Cambios

### generate_random_date (RANDOM_DATE)

**Tipo:** function_commented

**Razón:** Tabla no existe en esquema

### generate_random_date_datetime (RANDOM_DATE_DATETIME)

**Tipo:** function_commented

**Razón:** Tabla no existe en esquema

### generate_random_date (RANDOM_DATE)

**Tipo:** function_commented

**Razón:** Tabla no existe en esquema

### generate_random_date_datetime (RANDOM_DATE_DATETIME)

**Tipo:** function_commented

**Razón:** Tabla no existe en esquema

### generate_d_pais (D_PAIS)

**Tipo:** columns_removed

**Columnas afectadas:**
- FECHA_CARGA

### generate_d_curso_academico (D_CURSO_ACADEMICO)

**Tipo:** columns_removed

**Columnas afectadas:**
- FECHA_CARGA

### generate_d_curso_cohorte (D_CURSO_COHORTE)

**Tipo:** columns_removed

**Columnas afectadas:**
- FECHA_CARGA

### generate_d_tipo_estudio (D_TIPO_ESTUDIO)

**Tipo:** columns_removed

**Columnas afectadas:**
- FECHA_CARGA

### generate_d_convocatoria (D_CONVOCATORIA)

**Tipo:** columns_removed

**Columnas afectadas:**
- ORDEN_CONVOCATORIA

### generate_d_tipo_acceso (D_TIPO_ACCESO)

**Tipo:** columns_removed

**Columnas afectadas:**
- ID_TIPO_ACCESO_NK

### generate_d_persona (D_PERSONA)

**Tipo:** columns_added

**Columnas afectadas:**
- APELLIDO1
- APELLIDO2

### generate_dni (DNI)

**Tipo:** function_commented

**Razón:** Tabla no existe en esquema

### generate_d_tipo_acceso_preinscripcion (D_TIPO_ACCESO_PREINSCRIPCION)

**Tipo:** columns_removed

**Columnas afectadas:**
- ID_TIPO_ACCESO_PREINS_NK

### generate_d_edad_est (D_EDAD_EST)

**Tipo:** columns_removed

**Columnas afectadas:**
- DESCRIPCION_EDAD_EST
- EDAD_MAXIMA
- EDAD_MINIMA

### generate_d_dedicacion (D_DEDICACION)

**Tipo:** columns_removed

**Columnas afectadas:**
- DESCRIPCION_DEDICACION
- ES_ACTIVO
- FECHA_CARGA
- FECHA_FIN_VIGENCIA
- FLG_TIEMPO_COMPLETO
- FLG_TIEMPO_PARCIAL
- HORAS_SEMANALES
- ORDEN_VISUALIZACION
- PORCENTAJE_DEDICACION
- SN_ACTIVO
- SN_TIEMPO_COMPLETO
- SN_TIEMPO_PARCIAL

### generate_d_dedicacion_profesor (D_DEDICACION_PROFESOR)

**Tipo:** columns_removed

**Columnas afectadas:**
- DESCRIPCION_DEDICACION
- ES_ACTIVO
- FECHA_CARGA
- FECHA_FIN_VIGENCIA
- FLG_TIEMPO_COMPLETO
- FLG_TIEMPO_PARCIAL
- HORAS_SEMANALES
- ORDEN_VISUALIZACION
- PORCENTAJE_DEDICACION
- SN_ACTIVO
- SN_TIEMPO_COMPLETO
- SN_TIEMPO_PARCIAL

### generate_d_estado_adjudicacion (D_ESTADO_ADJUDICACION)

**Tipo:** columns_removed

**Columnas afectadas:**
- ID_ESTADO_ADJUDICACION_NK

### generate_d_rango_nota_egracons (D_RANGO_NOTA_EGRACONS)

**Tipo:** columns_removed

**Columnas afectadas:**
- CODIGO_TIPO_EGRACONS
- DESCRIPCION_EGRACONS
- EQUIVALENCIA_ECTS
- EQUIVALENCIA_ESP
- ES_APROBADO
- FECHA_CARGA
- LIMITE_INFERIOR
- LIMITE_SUPERIOR
- ORDEN_VISUALIZACION
- SN_APROBADO

### generate_d_idioma_movilidad (D_IDIOMA_MOVILIDAD)

**Tipo:** columns_removed

**Columnas afectadas:**
- FECHA_CARGA

### generate_d_nivel_estudios_movilidad (D_NIVEL_ESTUDIOS_MOVILIDAD)

**Tipo:** columns_removed

**Columnas afectadas:**
- FECHA_CARGA

### generate_d_estado_acuerdo_bilateral (D_ESTADO_ACUERDO_BILATERAL)

**Tipo:** columns_removed

**Columnas afectadas:**
- FECHA_CARGA

### generate_d_estudio (D_ESTUDIO)

**Tipo:** columns_removed

**Columnas afectadas:**
- CODIGO_ESTUDIO
- ES_INTERUNIVERSITARIO
- ES_OFICIAL
- FECHA_CARGA
- FECHA_CREACION
- IDIOMA_IMPARTICION
- MODALIDAD_ESTUDIO
- SN_OFICIAL

### generate_d_proyecto_investigacion (D_PROYECTO_INVESTIGACION)

**Tipo:** columns_removed

**Columnas afectadas:**
- AEI
- CTR
- EUR
- FECHA_FIN
- FECHA_INICIO
- IMPORTE_CONCEDIDO
- MIN
- NOMBRE_PROYECTO
- PID
- REG
- TIPO_PROYECTO

### generate_d_rama_macroarea (D_RAMA_MACROAREA)

**Tipo:** columns_removed

**Columnas afectadas:**
- ID_RAMA_CONOCIMIENTO
- NOMBRE_RAMA_CONOCIMIENTO

### generate_d_estado_solicitud_doctorado (D_ESTADO_SOLICITUD_DOCTORADO)

**Tipo:** columns_removed

**Columnas afectadas:**
- DESCRIPCION_ESTADO
- FECHA_ALTA
- FLG_ESTADO_APROBADO
- FLG_ESTADO_RECHAZADO
- FLG_REQUIERE_ACCION

### generate_d_categoria_cuerpo_pdi (D_CATEGORIA_CUERPO_PDI)

**Tipo:** columns_removed

**Columnas afectadas:**
- SN_REQUIERE_DOCTORADO

### generate_d_tipo_asignatura (D_TIPO_ASIGNATURA)

**Tipo:** columns_removed

**Columnas afectadas:**
- CODIGO_TIPO_ASIGNATURA
- DESCRIPCION_TIPO_ASIGNATURA
- FECHA_CARGA
- FLG_COMPUTO_ACADEMICO
- FLG_FORMACION_BASICA
- FLG_PROYECTO_FIN_CARRERA
- ORDEN_VISUALIZACION
- SN_COMPUTO_ACADEMICO
- SN_FORMACION_BASICA
- SN_PROYECTO_FIN_CARRERA

### generate_d_modalidad_asignatura (D_MODALIDAD_ASIGNATURA)

**Tipo:** function_commented

**Razón:** Tabla no existe en esquema

### generate_d_tipo_centro (D_TIPO_CENTRO)

**Tipo:** columns_removed

**Columnas afectadas:**
- DESCRIPCION_TIPO_CENTRO
- FECHA_CARGA
- FLG_DOCENCIA
- FLG_TITULACION_OFICIAL
- ID_TIPO_CENTRO_NK
- ORDEN_TIPO_CENTRO
- SN_DOCENCIA
- SN_TITULACION_OFICIAL

### generate_d_poblacion_centro (D_POBLACION_CENTRO)

**Tipo:** columns_removed

**Columnas afectadas:**
- COD_POSTAL
- ID_CCAA
- ID_PROVINCIA
- NOMBRE_CCAA
- NOMBRE_PROVINCIA

### generate_d_estado_credencial_acceso (D_ESTADO_CREDENCIAL_ACCESO)

**Tipo:** function_commented

**Razón:** Tabla no existe en esquema

### generate_d_territorio (D_TERRITORIO)

**Tipo:** function_commented

**Razón:** Tabla no existe en esquema

### generate_d_nivel_idioma (D_NIVEL_IDIOMA)

**Tipo:** function_commented

**Razón:** Tabla no existe en esquema

### generate_d_situacion_administrativa (D_SITUACION_ADMINISTRATIVA)

**Tipo:** function_commented

**Razón:** Tabla no existe en esquema

### generate_d_tipo_contrato (D_TIPO_CONTRATO)

**Tipo:** function_commented

**Razón:** Tabla no existe en esquema

### generate_d_periodo_lectivo (D_PERIODO_LECTIVO)

**Tipo:** function_commented

**Razón:** Tabla no existe en esquema

### generate_d_modalidad_plan_estudio (D_MODALIDAD_PLAN_ESTUDIO)

**Tipo:** columns_removed

**Columnas afectadas:**
- DESCRIPCION_MODALIDAD
- ES_PRESENCIAL
- ES_VIRTUAL
- FECHA_CARGA
- ORDEN_VISUALIZACION
- SN_PRESENCIAL
- SN_VIRTUAL

### generate_d_asignatura_origen (D_ASIGNATURA_ORIGEN)

**Tipo:** function_commented

**Razón:** Tabla no existe en esquema

### generate_d_tipo_inscripcion (D_TIPO_INSCRIPCION)

**Tipo:** function_commented

**Razón:** Tabla no existe en esquema

### generate_d_ambito_conocimiento (D_AMBITO_CONOCIMIENTO)

**Tipo:** function_commented

**Razón:** Tabla no existe en esquema

### generate_d_evento_academico (D_EVENTO_ACADEMICO)

**Tipo:** function_commented

**Razón:** Tabla no existe en esquema

### generate_d_dedicacion_alumno (D_DEDICACION_ALUMNO)

**Tipo:** function_commented

**Razón:** Tabla no existe en esquema

### generate_random_date (RANDOM_DATE)

**Tipo:** function_commented

**Razón:** Tabla no existe en esquema

### generate_f_rendimiento (F_RENDIMIENTO)

**Tipo:** columns_added

**Columnas afectadas:**
- CURSO_IMPARTICION_ASIG
- FLG_COMPENSADA
- FLG_EN_PROGRAMA_MOVILIDAD
- FLG_MOVILIDAD_IN
- FLG_NUEVO_INGRESO
- ID_ASIGNATURA_NK
- ID_CAMPUS_CENTRO
- ID_CENTRO_IMPARTICION
- ID_CENTRO_IMPARTICION_NK
- ID_CENTRO_NK
- ID_DEDICACION
- ID_EDAD_EST
- ID_ESTUDIO
- ID_ESTUDIO_NK
- ID_ESTUDIO_PREVIO
- ID_FECHA_CARGA
- ID_PAIS_FAMILIAR
- ID_PAIS_FAMILIAR_NK
- ID_PLAN_ESTUDIO_NK
- ID_PLAN_GRUPO_MATRICULA
- ID_PLAN_GRUPO_MATRICULA_NK
- ID_POBLACION_CENTRO
- ID_RAMA_CONOCIMIENTO
- ID_RANGO_NOTA_ADMISION
- ID_RANGO_NOTA_EGRACONS
- ID_TIPO_ASIGNATURA
- ID_TIPO_CENTRO
- ID_TIPO_ESTUDIO
- NOTA_ADMISION
- ORDEN_BOE_PLAN
- SN_CAMBIO_CICLO_GRADO
- SN_COMPENSADA
- SN_DOCTORADO_VIGENTE
- SN_MOVILIDAD_IN
- SN_NUEVO_INGRESO
- SN_PROG_MOVILIDAD

### generate_f_oferta_acuerdo_bilateral (F_OFERTA_ACUERDO_BILATERAL)

**Tipo:** columns_added

**Columnas afectadas:**
- ID_IDIOMA_1_NK
- ID_IDIOMA_2_NK
- ID_NIVEL_IDIOMA_1_NK
- ID_NIVEL_IDIOMA_2_NK

### generate_f_doctorado_admision (F_DOCTORADO_ADMISION)

**Tipo:** columns_removed

**Columnas afectadas:**
- H

### generate_f_estudio_propio_matricula (F_ESTUDIO_PROPIO_MATRICULA)

**Tipo:** columns_removed

**Columnas afectadas:**
- H

### generate_f_doctorado (F_DOCTORADO)

**Tipo:** columns_added

**Columnas afectadas:**
- NUMERO_ALU_ENCUESTA_GLOBAL_0
- NUMERO_ALU_ENCUESTA_GLOBAL_1
- NUMERO_ALU_ENCUESTA_GLOBAL_2
- NUMERO_ALU_ENCUESTA_GLOBAL_3
- NUMERO_ALU_ENCUESTA_GLOBAL_4
- NUMERO_ALU_ENCUESTA_GLOBAL_5
- NUMERO_PROF_ENCUESTA_GLOBAL_0
- NUMERO_PROF_ENCUESTA_GLOBAL_1
- NUMERO_PROF_ENCUESTA_GLOBAL_2
- NUMERO_PROF_ENCUESTA_GLOBAL_3
- NUMERO_PROF_ENCUESTA_GLOBAL_4
- NUMERO_PROF_ENCUESTA_GLOBAL_5
- SN_PRORROGA_1
- SN_PRORROGA_2

### generate_f_oferta_admision (F_OFERTA_ADMISION)

**Tipo:** columns_added

**Columnas afectadas:**
- FLG_ADMITIDOS_TODOS_1
- FLG_ADMITIDOS_TODOS_2
- NOTA_CORTE_ADJUDICACION_1
- NOTA_CORTE_ADJUDICACION_2
- NOTA_CORTE_DEFINITIVA_1
- NOTA_CORTE_DEFINITIVA_2
- PARTICIPA_1
- PARTICIPA_2
- PLAZAS_SOLICITADAS_PREF_1
- PRELA_CONVO_NOTA_DEF_1
- PRELA_CONVO_NOTA_DEF_2

