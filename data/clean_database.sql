-- Script para eliminar y recrear todas las tablas del esquema DM_ACADEMICO
-- Primero eliminamos todas las tablas existentes
BEGIN
  FOR r IN (SELECT table_name FROM user_tables WHERE table_name LIKE 'D_%' OR table_name LIKE 'F_%') LOOP
    EXECUTE IMMEDIATE 'DROP TABLE C##DM_ACADEMICO.' || r.table_name || ' CASCADE CONSTRAINTS';
  END LOOP;
END;
/

-- Reiniciamos las secuencias si existen
BEGIN
  FOR r IN (SELECT sequence_name FROM user_sequences) LOOP
    EXECUTE IMMEDIATE 'DROP SEQUENCE ' || r.sequence_name;
  END LOOP;
END;
/

