-- ============================================
-- SCRIPT DE VERIFICACIÓN Y LIMPIEZA SAIKU CDB
-- ============================================
-- Este script permite verificar el estado actual de la configuración
-- y limpiar/resetear si es necesario
-- ============================================

-- Mostrar información del sistema
PROMPT ========================================
PROMPT VERIFICACIÓN DEL SISTEMA
PROMPT ========================================

-- Verificar que estamos en CDB
SELECT 'Conectado a: ' || SYS_CONTEXT('USERENV', 'DB_NAME') AS CONTEXTO FROM DUAL;
SELECT 'Container: ' || SYS_CONTEXT('USERENV', 'CON_NAME') AS CONTAINER FROM DUAL;

-- Verificar usuarios
PROMPT
PROMPT Usuarios comunes (C##) en el sistema:
SELECT USERNAME, ACCOUNT_STATUS, CREATED 
FROM DBA_USERS 
WHERE USERNAME LIKE 'C##%' 
ORDER BY USERNAME;

-- Conectar como el usuario de Saiku si existe
DECLARE
    user_exists NUMBER;
BEGIN
    SELECT COUNT(*) INTO user_exists 
    FROM DBA_USERS 
    WHERE USERNAME = 'C##DM_ACADEMICO';
    
    IF user_exists > 0 THEN
        DBMS_OUTPUT.PUT_LINE('Usuario C##DM_ACADEMICO encontrado');
    ELSE
        DBMS_OUTPUT.PUT_LINE('Usuario C##DM_ACADEMICO NO encontrado');
        DBMS_OUTPUT.PUT_LINE('Ejecute setup_saiku_cdb_links.sql primero');
    END IF;
END;
/

-- Si el usuario existe, mostrar su configuración
BEGIN
    EXECUTE IMMEDIATE 'ALTER SESSION SET CURRENT_SCHEMA = C##DM_ACADEMICO';
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('No se puede cambiar al schema C##DM_ACADEMICO');
        DBMS_OUTPUT.PUT_LINE('Termine aquí si el usuario no existe');
        RETURN;
END;
/

CONNECT C##DM_ACADEMICO/YourPassword123@@localhost:1521/XE;

PROMPT ========================================
PROMPT CONFIGURACIÓN ACTUAL C##DM_ACADEMICO
PROMPT ========================================

-- Mostrar database links
PROMPT Database Links configurados:
SELECT DB_LINK, USERNAME, HOST, CREATED 
FROM USER_DB_LINKS 
ORDER BY DB_LINK;

-- Mostrar vistas
PROMPT
PROMPT Vistas creadas:
SELECT VIEW_NAME, CREATED 
FROM USER_VIEWS 
ORDER BY VIEW_NAME;

-- Mostrar sinónimos
PROMPT
PROMPT Sinónimos creados:
SELECT SYNONYM_NAME, TABLE_NAME 
FROM USER_SYNONYMS 
ORDER BY SYNONYM_NAME;

-- Probar conectividad con XEPDB1
PROMPT ========================================
PROMPT PRUEBAS DE CONECTIVIDAD
PROMPT ========================================

PROMPT Probando database link XEPDB1_LINK...
BEGIN
    EXECUTE IMMEDIATE 'SELECT ''Database Link OK'' FROM DUAL@XEPDB1_LINK';
    DBMS_OUTPUT.PUT_LINE('✓ Database link funciona correctamente');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✗ Error en database link: ' || SQLERRM);
END;
/

-- Probar acceso a las vistas
PROMPT
PROMPT Probando acceso a vistas...

DECLARE
    cnt NUMBER;
BEGIN
    -- Probar cada vista
    SELECT COUNT(*) INTO cnt FROM D_CURSO_ACADEMICO WHERE ROWNUM <= 1;
    DBMS_OUTPUT.PUT_LINE('✓ D_CURSO_ACADEMICO: ' || cnt || ' registros visibles');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✗ D_CURSO_ACADEMICO: ' || SQLERRM);
END;
/

DECLARE
    cnt NUMBER;
BEGIN
    SELECT COUNT(*) INTO cnt FROM D_CENTRO WHERE ROWNUM <= 1;
    DBMS_OUTPUT.PUT_LINE('✓ D_CENTRO: ' || cnt || ' registros visibles');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✗ D_CENTRO: ' || SQLERRM);
END;
/

DECLARE
    cnt NUMBER;
BEGIN
    SELECT COUNT(*) INTO cnt FROM D_ASIGNATURA WHERE ROWNUM <= 1;
    DBMS_OUTPUT.PUT_LINE('✓ D_ASIGNATURA: ' || cnt || ' registros visibles');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✗ D_ASIGNATURA: ' || SQLERRM);
END;
/

DECLARE
    cnt NUMBER;
BEGIN
    SELECT COUNT(*) INTO cnt FROM D_SEXO WHERE ROWNUM <= 1;
    DBMS_OUTPUT.PUT_LINE('✓ D_SEXO: ' || cnt || ' registros visibles');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✗ D_SEXO: ' || SQLERRM);
END;
/

DECLARE
    cnt NUMBER;
BEGIN
    SELECT COUNT(*) INTO cnt FROM F_MATRICULA WHERE ROWNUM <= 1;
    DBMS_OUTPUT.PUT_LINE('✓ F_MATRICULA: ' || cnt || ' registros visibles');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✗ F_MATRICULA: ' || SQLERRM);
END;
/

-- Estadísticas finales
PROMPT ========================================
PROMPT ESTADÍSTICAS DE DATOS
PROMPT ========================================

SELECT 'D_CURSO_ACADEMICO' AS TABLA, COUNT(*) AS REGISTROS FROM D_CURSO_ACADEMICO
UNION ALL
SELECT 'D_CENTRO' AS TABLA, COUNT(*) AS REGISTROS FROM D_CENTRO
UNION ALL
SELECT 'D_ASIGNATURA' AS TABLA, COUNT(*) AS REGISTROS FROM D_ASIGNATURA
UNION ALL
SELECT 'D_SEXO' AS TABLA, COUNT(*) AS REGISTROS FROM D_SEXO
UNION ALL
SELECT 'F_MATRICULA' AS TABLA, COUNT(*) AS REGISTROS FROM F_MATRICULA
ORDER BY TABLA;

PROMPT ========================================
PROMPT RESUMEN DE CONFIGURACIÓN
PROMPT ========================================
PROMPT Configuración para Saiku:
PROMPT Driver: Oracle JDBC Thin
PROMPT URL: jdbc:oracle:thin:@localhost:1521:XE
PROMPT Username: C##DM_ACADEMICO
PROMPT Password: YourPassword123@
PROMPT ========================================
