-- =================================================================================================================
-- AUTOR: Assistant
-- FECHA: 26-06-2025
-- DESCRIPCION: Script para crear vistas optimizadas para Saiku Analytics
--              Mejora el rendimiento y funcionalidad OLAP con campos calculados y jerarquias optimizadas
--
-- PRE-REQUISITOS:
-- 1. El usuario C##SAIKU_USER debe existir (ejecutar setup_saiku_cdb.sql primero)
-- 2. Los sinonimos para las tablas base deben estar creados
-- 3. Conexion como SYSDBA
--
-- USO:
-- 1. Ejecutar este script despues de setup_saiku_cdb.sql
-- 2. Actualizar el esquema Mondrian para usar estas vistas
-- =================================================================================================================

-- Conectarse como SYSDBA para crear las vistas
CONNECT / AS SYSDBA;

-- Configurar SQLPlus
SET PAGESIZE 0;
SET FEEDBACK ON;
SET VERIFY OFF;
SET HEADING OFF;
SET ECHO OFF;

-- =================================================================================================================
-- PASO 1: ELIMINAR VISTAS EXISTENTES (SI EXISTEN)
-- =================================================================================================================

BEGIN
  EXECUTE IMMEDIATE 'DROP VIEW C##SAIKU_USER.V_HECHOS_MATRICULA';
EXCEPTION
  WHEN OTHERS THEN NULL;
END;
/

BEGIN
  EXECUTE IMMEDIATE 'DROP VIEW C##SAIKU_USER.V_DIM_CENTRO';
EXCEPTION
  WHEN OTHERS THEN NULL;
END;
/

BEGIN
  EXECUTE IMMEDIATE 'DROP VIEW C##SAIKU_USER.V_DIM_PLAN_ESTUDIO';
EXCEPTION
  WHEN OTHERS THEN NULL;
END;
/

BEGIN
  EXECUTE IMMEDIATE 'DROP VIEW C##SAIKU_USER.V_DIM_CURSO_ACADEMICO';
EXCEPTION
  WHEN OTHERS THEN NULL;
END;
/

BEGIN
  EXECUTE IMMEDIATE 'DROP VIEW C##SAIKU_USER.V_DIM_SEXO';
EXCEPTION
  WHEN OTHERS THEN NULL;
END;
/

BEGIN
  EXECUTE IMMEDIATE 'DROP VIEW C##SAIKU_USER.V_RESUMEN_EJECUTIVO';
EXCEPTION
  WHEN OTHERS THEN NULL;
END;
/

-- =================================================================================================================
-- PASO 2: CREAR VISTA PRINCIPAL DE HECHOS OPTIMIZADA
-- =================================================================================================================

CREATE OR REPLACE VIEW C##SAIKU_USER.V_HECHOS_MATRICULA AS
SELECT 
    m.ID_EXPEDIENTE_ACADEMICO_NK,
    m.ID_CURSO_ACADEMICO,
    m.ID_CENTRO,
    m.ID_SEXO,
    m.ID_PLAN_ESTUDIO,
    m.ID_ALUMNO,
    m.CREDITOS,
    m.EDAD,
    DECODE(
        SIGN(m.EDAD - 20), -1, '1. Menor 20',
        DECODE(SIGN(m.EDAD - 25), -1, '2. 20-24 años',
        DECODE(SIGN(m.EDAD - 30), -1, '3. 25-29 años',
        DECODE(SIGN(m.EDAD - 35), -1, '4. 30-34 años',
        '5. 35+ años')))) as GRUPO_EDAD,
    DECODE(
        SIGN(NVL(m.CREDITOS,0) - 1), -1, '0. Sin creditos',
        DECODE(SIGN(m.CREDITOS - 30), -1, '1. Tiempo Parcial (<30)',
        DECODE(SIGN(m.CREDITOS - 60), -1, '2. Medio Tiempo (30-59)',
        DECODE(SIGN(m.CREDITOS - 90), -1, '3. Tiempo Completo (60-89)',
        '4. Sobrecarga (90+)')))) as TIPO_DEDICACION,
    DECODE(
        NVL(m.CREDITOS,0), 0, '0',
        DECODE(SIGN(m.CREDITOS - 15), -1, '1-15',
        DECODE(SIGN(m.CREDITOS - 30), -1, '16-30',
        DECODE(SIGN(m.CREDITOS - 45), -1, '31-45',
        DECODE(SIGN(m.CREDITOS - 60), -1, '46-60',
        DECODE(SIGN(m.CREDITOS - 75), -1, '61-75',
        '76+')))))) as RANGO_CREDITOS,
    2020 + NVL(m.ID_CURSO_ACADEMICO, 1) - 1 as ANNO_MATRICULA,
    DECODE(SIGN(m.EDAD - 25), -1, 1, 0) as ES_JOVEN,
    DECODE(SIGN(NVL(m.CREDITOS,0) - 60), -1, 0, 1) as ES_TIEMPO_COMPLETO,
    1 as CONTADOR_MATRICULAS,
    DECODE(SIGN(NVL(m.CREDITOS,0) - 1), -1, 0, 1) as TIENE_CREDITOS
FROM C##SAIKU_USER.F_MATRICULA m;
/

-- =================================================================================================================
-- PASO 3: CREAR VISTAS DE DIMENSIONES OPTIMIZADAS
-- =================================================================================================================

CREATE OR REPLACE VIEW C##SAIKU_USER.V_DIM_CENTRO AS
SELECT 
    c.ID_CENTRO,
    c.NOMBRE_CENTRO,
    c.NOMBRE_CAMPUS,
    c.NOMBRE_TIPO_CENTRO,
    c.NOMBRE_TIPO_CENTRO as NIVEL_1_TIPO,
    c.NOMBRE_CAMPUS as NIVEL_2_CAMPUS,
    c.NOMBRE_CENTRO as NIVEL_3_CENTRO,
    c.NOMBRE_TIPO_CENTRO || ' - ' || c.NOMBRE_CAMPUS as TIPO_CAMPUS,
    c.NOMBRE_CAMPUS || ' - ' || c.NOMBRE_CENTRO as CAMPUS_CENTRO,
    ROW_NUMBER() OVER (ORDER BY c.NOMBRE_TIPO_CENTRO, c.NOMBRE_CAMPUS, c.NOMBRE_CENTRO) as ORDEN_CENTRO
FROM C##SAIKU_USER.D_CENTRO c;
/

CREATE OR REPLACE VIEW C##SAIKU_USER.V_DIM_PLAN_ESTUDIO AS
SELECT 
    ej.ID_PLAN_ESTUDIO,
    ej.NOMBRE_PLAN_ESTUDIO,
    ej.NOMBRE_ESTUDIO,
    ej.NOMBRE_TIPO_ESTUDIO,
    ej.NOMBRE_RAMA_CONOCIMIENTO,
    ej.NOMBRE_TIPO_ESTUDIO as NIVEL_1_TIPO_ESTUDIO,
    ej.NOMBRE_RAMA_CONOCIMIENTO as NIVEL_2_RAMA,
    ej.NOMBRE_ESTUDIO as NIVEL_3_ESTUDIO,
    ej.NOMBRE_PLAN_ESTUDIO as NIVEL_4_PLAN,
    ej.NOMBRE_TIPO_ESTUDIO || ' - ' || ej.NOMBRE_RAMA_CONOCIMIENTO as TIPO_RAMA,
    ej.NOMBRE_RAMA_CONOCIMIENTO || ' - ' || ej.NOMBRE_ESTUDIO as RAMA_ESTUDIO,
    DECODE(
        INSTR(UPPER(ej.NOMBRE_TIPO_ESTUDIO), 'GRADO'), 0,
        DECODE(INSTR(UPPER(ej.NOMBRE_TIPO_ESTUDIO), 'MASTER'), 0,
        DECODE(INSTR(UPPER(ej.NOMBRE_TIPO_ESTUDIO), 'DOCTOR'), 0, 'Otro', 'Doctorado'),
        'Master'), 'Grado') as CATEGORIA_ESTUDIO
FROM C##SAIKU_USER.D_ESTUDIO_JERARQ ej;
/

CREATE OR REPLACE VIEW C##SAIKU_USER.V_DIM_CURSO_ACADEMICO AS
SELECT 
    ca.ID_CURSO_ACADEMICO,
    ca.NOMBRE_CURSO_ACADEMICO,
    DECODE(
        INSTR(ca.NOMBRE_CURSO_ACADEMICO, '2020'), 0,
        DECODE(INSTR(ca.NOMBRE_CURSO_ACADEMICO, '2021'), 0,
        DECODE(INSTR(ca.NOMBRE_CURSO_ACADEMICO, '2022'), 0,
        DECODE(INSTR(ca.NOMBRE_CURSO_ACADEMICO, '2023'), 0,
        DECODE(INSTR(ca.NOMBRE_CURSO_ACADEMICO, '2024'), 0,
        DECODE(INSTR(ca.NOMBRE_CURSO_ACADEMICO, '2025'), 0,
        2020 + ca.ID_CURSO_ACADEMICO, 2025), 2024), 2023), 2022), 2021), 2020) as ANNO_INICIO,
    DECODE(
        GREATEST(INSTR(ca.NOMBRE_CURSO_ACADEMICO, '2024'), INSTR(ca.NOMBRE_CURSO_ACADEMICO, '2025')), 0,
        DECODE(INSTR(ca.NOMBRE_CURSO_ACADEMICO, '2023'), 0,
        DECODE(INSTR(ca.NOMBRE_CURSO_ACADEMICO, '2022'), 0, 'Historico', 'Anterior'),
        'Reciente'), 'Actual') as PERIODO_CLASIFICACION
FROM C##SAIKU_USER.D_CURSO_ACADEMICO ca;
/

CREATE OR REPLACE VIEW C##SAIKU_USER.V_DIM_SEXO AS
SELECT 
    s.ID_SEXO,
    s.NOMBRE_SEXO,
    DECODE(
        UPPER(s.NOMBRE_SEXO), 'M', 'Masculino',
        'MASCULINO', 'Masculino',
        'HOMBRE', 'Masculino',
        'F', 'Femenino',
        'FEMENINO', 'Femenino',
        'MUJER', 'Femenino',
        'No especificado') as GENERO_NORMALIZADO
FROM C##SAIKU_USER.D_SEXO s;
/

-- =================================================================================================================
-- PASO 4: CREAR VISTA AGREGADA PARA DASHBOARDS EJECUTIVOS
-- =================================================================================================================

CREATE OR REPLACE VIEW C##SAIKU_USER.V_RESUMEN_EJECUTIVO AS
SELECT 
    ca.NOMBRE_CURSO_ACADEMICO as CURSO,
    c.NOMBRE_TIPO_CENTRO as TIPO_CENTRO,
    c.NOMBRE_CAMPUS as CAMPUS,
    ej.NOMBRE_TIPO_ESTUDIO as TIPO_ESTUDIO,
    s.NOMBRE_SEXO as SEXO,
    COUNT(*) as TOTAL_MATRICULAS,
    COUNT(DISTINCT m.ID_ALUMNO) as ALUMNOS_UNICOS,
    SUM(NVL(m.CREDITOS,0)) as TOTAL_CREDITOS,
    ROUND(AVG(NVL(m.CREDITOS,0)), 2) as PROMEDIO_CREDITOS,
    ROUND(AVG(NVL(m.EDAD,0)), 2) as PROMEDIO_EDAD,
    MIN(NVL(m.EDAD,0)) as EDAD_MINIMA,
    MAX(NVL(m.EDAD,0)) as EDAD_MAXIMA,
    COUNT(DECODE(SIGN(m.EDAD - 25), -1, 1, NULL)) as JOVENES,
    COUNT(DECODE(SIGN(NVL(m.CREDITOS,0) - 60), -1, NULL, 1)) as TIEMPO_COMPLETO,
    COUNT(DECODE(UPPER(s.NOMBRE_SEXO), 'FEMENINO', 1, 'F', 1, 'MUJER', 1, NULL)) as MUJERES,
    COUNT(DECODE(UPPER(s.NOMBRE_SEXO), 'MASCULINO', 1, 'M', 1, 'HOMBRE', 1, NULL)) as HOMBRES
FROM C##SAIKU_USER.F_MATRICULA m
JOIN C##SAIKU_USER.D_CURSO_ACADEMICO ca ON m.ID_CURSO_ACADEMICO = ca.ID_CURSO_ACADEMICO
JOIN C##SAIKU_USER.D_CENTRO c ON m.ID_CENTRO = c.ID_CENTRO
JOIN C##SAIKU_USER.D_ESTUDIO_JERARQ ej ON m.ID_PLAN_ESTUDIO = ej.ID_PLAN_ESTUDIO
JOIN C##SAIKU_USER.D_SEXO s ON m.ID_SEXO = s.ID_SEXO
GROUP BY 
    ca.NOMBRE_CURSO_ACADEMICO,
    c.NOMBRE_TIPO_CENTRO,
    c.NOMBRE_CAMPUS,
    ej.NOMBRE_TIPO_ESTUDIO,
    s.NOMBRE_SEXO;
/

-- =================================================================================================================
-- PASO 5: CONCEDER PERMISOS AL USUARIO SAIKU
-- =================================================================================================================

GRANT SELECT ON C##SAIKU_USER.V_HECHOS_MATRICULA TO C##SAIKU_USER;
GRANT SELECT ON C##SAIKU_USER.V_DIM_CENTRO TO C##SAIKU_USER;
GRANT SELECT ON C##SAIKU_USER.V_DIM_PLAN_ESTUDIO TO C##SAIKU_USER;
GRANT SELECT ON C##SAIKU_USER.V_DIM_CURSO_ACADEMICO TO C##SAIKU_USER;
GRANT SELECT ON C##SAIKU_USER.V_DIM_SEXO TO C##SAIKU_USER;
GRANT SELECT ON C##SAIKU_USER.V_RESUMEN_EJECUTIVO TO C##SAIKU_USER;

-- =================================================================================================================
-- PASO 6: MOSTRAR CONFIRMACION
-- =================================================================================================================

SELECT 'Vistas optimizadas para Saiku creadas con exito!' FROM DUAL;
SELECT '==========================================' FROM DUAL;
SELECT 'VISTAS CREADAS:' FROM DUAL;
SELECT '- C##SAIKU_USER.V_HECHOS_MATRICULA (tabla de hechos optimizada)' FROM DUAL;
SELECT '- C##SAIKU_USER.V_DIM_CENTRO (dimension centro con jerarquias)' FROM DUAL;
SELECT '- C##SAIKU_USER.V_DIM_PLAN_ESTUDIO (dimension academica optimizada)' FROM DUAL;
SELECT '- C##SAIKU_USER.V_DIM_CURSO_ACADEMICO (dimension temporal)' FROM DUAL;
SELECT '- C##SAIKU_USER.V_DIM_SEXO (dimension demografica)' FROM DUAL;
SELECT '- C##SAIKU_USER.V_RESUMEN_EJECUTIVO (vista agregada para dashboards)' FROM DUAL;
SELECT '==========================================' FROM DUAL;
SELECT 'PASOS SIGUIENTES:' FROM DUAL;
SELECT '1. Actualizar esquema Mondrian para usar las nuevas vistas' FROM DUAL;
SELECT '2. Reiniciar Pentaho Server' FROM DUAL;
SELECT '3. Probar las nuevas funcionalidades en Saiku' FROM DUAL;
SELECT '==========================================' FROM DUAL;

-- Salir
EXIT; 