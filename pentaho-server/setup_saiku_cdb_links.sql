-- ============================================
-- CONFIGURACIÓN PARA SAIKU CON DATABASE LINKS
-- ============================================
-- Este script configura database links desde CDB hacia XEPDB1
-- para que Saiku pueda acceder a los datos del Data Mart sin
-- necesidad de copiar las tablas físicamente.
-- ============================================

-- PASO 1: Crear usuario común en CDB (ejecutar como SYS con SYSDBA)
PROMPT ========================================
PROMPT PASO 1: Configurando usuario en CDB
PROMPT ========================================

-- Conexión se maneja externamente por docker exec

-- Eliminar usuario si existe
BEGIN
    EXECUTE IMMEDIATE 'DROP USER C##DM_ACADEMICO CASCADE';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

-- Crear usuario común (prefijo C## obligatorio para CDB)
-- Usar la contraseña del proyecto Docker
CREATE USER C##DM_ACADEMICO IDENTIFIED BY YourPassword123@ CONTAINER=ALL;

-- Otorgar permisos necesarios
GRANT CONNECT, RESOURCE TO C##DM_ACADEMICO CONTAINER=ALL;
GRANT CREATE DATABASE LINK TO C##DM_ACADEMICO CONTAINER=ALL;
GRANT CREATE VIEW TO C##DM_ACADEMICO CONTAINER=ALL;
GRANT CREATE SYNONYM TO C##DM_ACADEMICO CONTAINER=ALL;
GRANT UNLIMITED TABLESPACE TO C##DM_ACADEMICO CONTAINER=ALL;

-- Permitir al usuario crear database links públicos
GRANT CREATE PUBLIC DATABASE LINK TO C##DM_ACADEMICO;

PROMPT Usuario C##DM_ACADEMICO creado exitosamente en CDB

-- PASO 2: Conectar como el nuevo usuario y crear database link
PROMPT ========================================
PROMPT PASO 2: Creando Database Link
PROMPT ========================================

CONNECT C##DM_ACADEMICO/YourPassword123@@XE;

-- Crear database link hacia XEPDB1 usando credenciales del proyecto
-- Desde dentro del contenedor, usamos localhost
CREATE DATABASE LINK XEPDB1_LINK 
CONNECT TO dm_academico IDENTIFIED BY YourPassword123@
USING 'localhost:1521/XEPDB1';

-- Probar conexión del link
PROMPT Probando conexión del database link...
SELECT 'Database Link OK' AS STATUS FROM DUAL@XEPDB1_LINK;

-- PASO 3: Crear vistas que apunten a las tablas en XEPDB1
PROMPT ========================================
PROMPT PASO 3: Creando vistas transparentes
PROMPT ========================================

-- Eliminar vistas si existen
BEGIN
    EXECUTE IMMEDIATE 'DROP VIEW D_CURSO_ACADEMICO';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP VIEW D_CENTRO';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP VIEW D_ASIGNATURA';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP VIEW D_SEXO';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP VIEW F_MATRICULA';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP VIEW F_RENDIMIENTO';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

-- Crear vistas que apunten a las tablas en XEPDB1
CREATE VIEW D_CURSO_ACADEMICO AS 
SELECT * FROM dm_academico.D_CURSO_ACADEMICO@XEPDB1_LINK;

CREATE VIEW D_CENTRO AS 
SELECT * FROM dm_academico.D_CENTRO@XEPDB1_LINK;  

CREATE VIEW D_ASIGNATURA AS 
SELECT * FROM dm_academico.D_ASIGNATURA@XEPDB1_LINK;

CREATE VIEW D_SEXO AS 
SELECT * FROM dm_academico.D_SEXO@XEPDB1_LINK;

CREATE VIEW F_MATRICULA AS 
SELECT * FROM dm_academico.F_MATRICULA@XEPDB1_LINK;

-- Crear vista F_RENDIMIENTO si la tabla existe
DECLARE
    table_exists NUMBER;
BEGIN
    SELECT COUNT(*) INTO table_exists 
    FROM ALL_TABLES@XEPDB1_LINK 
    WHERE OWNER = 'DM_ACADEMICO' AND TABLE_NAME = 'F_RENDIMIENTO';

    IF table_exists > 0 THEN
        EXECUTE IMMEDIATE 'CREATE VIEW F_RENDIMIENTO AS SELECT * FROM dm_academico.F_RENDIMIENTO@XEPDB1_LINK';
        DBMS_OUTPUT.PUT_LINE('Vista F_RENDIMIENTO creada exitosamente');
    ELSE
        DBMS_OUTPUT.PUT_LINE('Tabla F_RENDIMIENTO no existe en XEPDB1, vista no creada');
    END IF;
END;
/

-- PASO 4: Crear sinónimos públicos (opcional, para mayor transparencia)
PROMPT ========================================
PROMPT PASO 4: Creando sinónimos (opcional)
PROMPT ========================================

-- Eliminar sinónimos si existen
BEGIN
    EXECUTE IMMEDIATE 'DROP SYNONYM DIM_CURSO_ACADEMICO';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP SYNONYM DIM_CENTRO';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP SYNONYM DIM_ASIGNATURA';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP SYNONYM DIM_SEXO';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP SYNONYM FACT_MATRICULA';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

-- Crear sinónimos más descriptivos
CREATE SYNONYM DIM_CURSO_ACADEMICO FOR D_CURSO_ACADEMICO;
CREATE SYNONYM DIM_CENTRO FOR D_CENTRO;
CREATE SYNONYM DIM_ASIGNATURA FOR D_ASIGNATURA;  
CREATE SYNONYM DIM_SEXO FOR D_SEXO;
CREATE SYNONYM FACT_MATRICULA FOR F_MATRICULA;

-- PASO 5: Verificar configuración
PROMPT ========================================
PROMPT PASO 5: Verificando configuración
PROMPT ========================================

PROMPT Verificando acceso a las vistas...
SELECT 'D_CURSO_ACADEMICO' AS VISTA, COUNT(*) AS REGISTROS FROM D_CURSO_ACADEMICO
UNION ALL
SELECT 'D_CENTRO' AS VISTA, COUNT(*) AS REGISTROS FROM D_CENTRO
UNION ALL
SELECT 'D_ASIGNATURA' AS VISTA, COUNT(*) AS REGISTROS FROM D_ASIGNATURA
UNION ALL
SELECT 'D_SEXO' AS VISTA, COUNT(*) AS REGISTROS FROM D_SEXO
UNION ALL
SELECT 'F_MATRICULA' AS VISTA, COUNT(*) AS REGISTROS FROM F_MATRICULA;

PROMPT Verificando database links...
SELECT DB_LINK, USERNAME, HOST FROM USER_DB_LINKS;

PROMPT Verificando vistas creadas...
SELECT VIEW_NAME FROM USER_VIEWS ORDER BY VIEW_NAME;

-- PASO 6: Información de conexión para Saiku
PROMPT ========================================
PROMPT CONFIGURACIÓN COMPLETADA
PROMPT ========================================
PROMPT
PROMPT Configuración para Saiku:
PROMPT --------------------------
PROMPT Driver: Oracle JDBC Thin
PROMPT URL: jdbc:oracle:thin:@localhost:1521:XE
PROMPT Username: C##DM_ACADEMICO  
PROMPT Password: YourPassword123@
PROMPT
PROMPT Las tablas están disponibles como vistas:
PROMPT - D_CURSO_ACADEMICO (dimensión cursos académicos)
PROMPT - D_CENTRO (dimensión centros)
PROMPT - D_ASIGNATURA (dimensión asignaturas)
PROMPT - D_SEXO (dimensión sexo)
PROMPT - F_MATRICULA (tabla de hechos matrículas)
PROMPT - F_RENDIMIENTO (tabla de hechos rendimiento, si existe)
PROMPT
PROMPT También están disponibles como sinónimos:
PROMPT - DIM_CURSO_ACADEMICO, DIM_CENTRO, DIM_ASIGNATURA, DIM_SEXO
PROMPT - FACT_MATRICULA
PROMPT ========================================
