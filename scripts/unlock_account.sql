-- Script para desbloquear la cuenta C##DM_ACADEMICO
ALTER USER C##DM_ACADEMICO ACCOUNT UNLOCK;
-- También cambiar la contraseña para asegurar que sea correcta
ALTER USER C##DM_ACADEMICO IDENTIFIED BY YourPassword123@; 