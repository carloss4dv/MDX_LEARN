-- =================================================================================================================
-- AUTOR: Copilot
-- FECHA: 20-06-2025
-- DESCRIPCIÓN: Script para crear un usuario común para Saiku y configurar el acceso a las tablas
--              del esquema C##DM_ACADEMICO en la PDB (XEPDB1) mediante un Database Link.
--              Esta solución es más robusta y eficiente que la copia de tablas.
--
-- PRE-REQUISITOS:
-- 1. Conectarse a la base de datos como SYSDBA.
-- 2. Conocer la contraseña del usuario C##DM_ACADEMICO.
--
-- USO:
-- 1. Reemplazar 'saiku_password' con una contraseña segura para el nuevo usuario C##SAIKU_USER.
-- 2. Reemplazar 'dm_academico_password' con la contraseña REAL del usuario C##DM_ACADEMICO.
-- 3. Ejecutar este script a través de los scripts de shell/batch proporcionados.
-- =================================================================================================================

-- Paso 1: Limpieza (opcional, para ejecuciones repetidas)
-- Si el script falla, puede que necesites ejecutar esto manualmente para limpiar antes de reintentar.
-- DROP USER C##SAIKU_USER CASCADE;

-- Paso 2: Crear un nuevo usuario común para Saiku
-- Se crea como "common user" (C##) para que sea visible desde el contenedor raíz (CDB).
CREATE USER C##SAIKU_USER IDENTIFIED BY saiku_password;

-- Paso 3: Otorgar los privilegios necesarios al nuevo usuario
-- Se le da permiso para conectarse, crear DB Links y Sinónimos.
GRANT CREATE SESSION, CREATE DATABASE LINK, CREATE SYNONYM TO C##SAIKU_USER;
GRANT UNLIMITED TABLESPACE TO C##SAIKU_USER;

-- Paso 4: Conectarse como el nuevo usuario para crear los objetos que le pertenecerán
CONNECT C##SAIKU_USER/saiku_password;

-- Paso 5: Crear un Database Link que apunta desde el CDB a la PDB donde están los datos
-- IMPORTANTE: Reemplaza 'dm_academico_password' por la contraseña correcta.
CREATE DATABASE LINK PDB_LINK
   CONNECT TO "C##DM_ACADEMICO" IDENTIFIED BY YourPassword123
   USING 'XEPDB1';

-- Paso 6: Crear sinónimos para las tablas remotas
-- Esto hace que las tablas de la PDB parezcan locales para el usuario C##SAIKU_USER.
-- Así, el esquema de Mondrian no necesita ninguna modificación.
CREATE SYNONYM F_MATRICULA FOR "F_MATRICULA"@"PDB_LINK";
CREATE SYNONYM D_CURSO_ACADEMICO FOR "D_CURSO_ACADEMICO"@"PDB_LINK";
CREATE SYNONYM D_CENTRO FOR "D_CENTRO"@"PDB_LINK";
CREATE SYNONYM D_SEXO FOR "D_SEXO"@"PDB_LINK";
CREATE SYNONYM D_ESTUDIO_JERARQ FOR "D_ESTUDIO_JERARQ"@"PDB_LINK";

-- Paso 7: Volver a conectar como SYS para que el script de shell pueda finalizar limpiamente
CONNECT / AS SYSDBA;

PROMPT 'Proceso finalizado con exito.';
PROMPT '================================================================================================';
PROMPT 'PASOS SIGUIENTES: ';
PROMPT '1. En Pentaho, actualiza la conexion a la base de datos para que use el usuario "C##SAIKU_USER" y su contrasena.';
PROMPT '2. En el esquema de Mondrian (dm_academico.xml), asegurate de que las tablas NO tengan el atributo "schema".';
PROMPT '   Ejemplo: <Table name="F_MATRICULA"/> en lugar de <Table name="F_MATRICULA" schema="..."/>';
PROMPT '================================================================================================';
