-- ============================================
-- SCRIPT DE LIMPIEZA SAIKU CDB SETUP
-- ============================================
-- Este script elimina completamente la configuración de Saiku
-- para permitir reinstalar desde cero si es necesario
-- ============================================

PROMPT ========================================
PROMPT LIMPIANDO CONFIGURACIÓN SAIKU CDB
PROMPT ========================================

-- Conectar como SYS para eliminar el usuario
CONNECT sys/YourStrongPassword123@localhost:1521/XE AS SYSDBA;

-- Verificar si el usuario existe
DECLARE
    user_exists NUMBER;
BEGIN
    SELECT COUNT(*) INTO user_exists 
    FROM DBA_USERS 
    WHERE USERNAME = 'C##DM_ACADEMICO';
    
    IF user_exists > 0 THEN
        DBMS_OUTPUT.PUT_LINE('Usuario C##DM_ACADEMICO encontrado, procediendo a eliminar...');
        
        -- Desconectar todas las sesiones del usuario
        FOR sess IN (SELECT SID, SERIAL# FROM V$SESSION WHERE USERNAME = 'C##DM_ACADEMICO') LOOP
            BEGIN
                EXECUTE IMMEDIATE 'ALTER SYSTEM KILL SESSION ''' || sess.SID || ',' || sess.SERIAL# || ''' IMMEDIATE';
            EXCEPTION
                WHEN OTHERS THEN NULL;
            END;
        END LOOP;
        
        -- Eliminar el usuario y todos sus objetos
        EXECUTE IMMEDIATE 'DROP USER C##DM_ACADEMICO CASCADE';
        DBMS_OUTPUT.PUT_LINE('✓ Usuario C##DM_ACADEMICO eliminado exitosamente');
        
    ELSE
        DBMS_OUTPUT.PUT_LINE('Usuario C##DM_ACADEMICO no encontrado, no hay nada que limpiar');
    END IF;
END;
/

-- Limpiar database links públicos relacionados (si existen)
BEGIN
    EXECUTE IMMEDIATE 'DROP PUBLIC DATABASE LINK XEPDB1_LINK';
    DBMS_OUTPUT.PUT_LINE('✓ Database link público eliminado');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('No hay database links públicos que eliminar');
END;
/

-- Verificar limpieza
PROMPT ========================================
PROMPT VERIFICANDO LIMPIEZA
PROMPT ========================================

SELECT 'Usuarios C## restantes: ' || COUNT(*) AS RESULTADO
FROM DBA_USERS 
WHERE USERNAME LIKE 'C##%';

SELECT 'Database links públicos restantes: ' || COUNT(*) AS RESULTADO
FROM DBA_DB_LINKS 
WHERE DB_LINK LIKE 'XEPDB1%';

PROMPT ========================================
PROMPT LIMPIEZA COMPLETADA
PROMPT ========================================
PROMPT La configuración de Saiku ha sido eliminada completamente.
PROMPT Ahora puede ejecutar setup_saiku_cdb_links.sql para 
PROMPT reinstalar desde cero.
PROMPT ========================================
