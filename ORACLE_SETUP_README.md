# Scripts de Configuración Automática de Oracle

Este directorio contiene scripts que automatizan completamente la configuración de Oracle Database para el proyecto MDX_LEARN.

## 📁 Archivos Incluidos

### Scripts Principales
- `setup_oracle.ps1` - Script de PowerShell para Windows
- `setup_oracle.sh` - Script de Bash para Linux/macOS
- `setup_oracle.bat` - Script por lotes para Windows (simple)

### Scripts SQL
- `init_scripts/create_tablespace.sql` - Creación del tablespace DMACADEMICO_DAT
- `init_scripts/create_user.sql` - Creación del usuario C##DM_ACADEMICO

### Archivos de Configuración
- `.env.example` - Ejemplo de variables de entorno

## 🚀 Uso Rápido

### Windows
```cmd
# Opción 1: Script por lotes (más simple)
setup_oracle.bat

# Opción 2: PowerShell (más control)
powershell -ExecutionPolicy Bypass -File setup_oracle.ps1
```

### Linux/macOS
```bash
chmod +x setup_oracle.sh
./setup_oracle.sh
```

## ⚙️ ¿Qué Hacen los Scripts?

1. **Verificación de Docker**: Comprueban que Docker esté ejecutándose
2. **Inicio del Contenedor**: Inician el contenedor Oracle si no está corriendo
3. **Espera de Inicialización**: Esperan hasta que Oracle esté completamente listo
4. **Creación de Tablespace**: Crean automáticamente el tablespace `DMACADEMICO_DAT`
5. **Creación de Usuario**: Crean el usuario `C##DM_ACADEMICO` con todos los permisos
6. **Configuración Completa**: Establecen cuotas y privilegios necesarios
7. **Información de Conexión**: Muestran las variables de entorno para usar

## 📋 Salida del Script

Al completarse exitosamente, verás:

```
=== Oracle Database Setup Complete ===
You can now use the following connection details:
Host: localhost
Port: 1521
Service: XEPDB1
User: C##DM_ACADEMICO
Password: YourPassword123

Environment variables for .env file:
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE=XEPDB1
ORACLE_USER=C##DM_ACADEMICO
ORACLE_PASSWORD=YourPassword123
```

## 🔧 Personalización

### Parámetros del Script PowerShell
```powershell
.\setup_oracle.ps1 -OracleHost "localhost" -OraclePort "1521" -OracleService "XEPDB1" -OraclePassword "YourStrongPassword123"
```

### Variables de Entorno del Script Bash
```bash
ORACLE_HOST=localhost ORACLE_PORT=1521 ORACLE_SERVICE=XEPDB1 ORACLE_PASSWORD=YourStrongPassword123 ./setup_oracle.sh
```

## 🐛 Solución de Problemas

### Error: "Docker is not running"
**Solución**: Inicia Docker Desktop o el daemon de Docker

### Error: "Oracle container is not running"
**Solución**: El script automáticamente intenta iniciar el contenedor. Si falla, revisa:
- Que el archivo `docker-compose.yml` esté presente
- Que tengas suficiente memoria disponible (4GB+)
- Que el puerto 1521 no esté ocupado

### Error: "Timeout waiting for Oracle Database"
**Solución**: Oracle puede tardar varios minutos en inicializarse completamente:
- Espera más tiempo (especialmente en el primer inicio)
- Verifica los logs: `docker logs oracle_db`
- Asegúrate de tener suficientes recursos del sistema

### Error: "User C##DM_ACADEMICO already exists"
**Solución**: Esto es normal si ejecutas el script múltiples veces. El usuario ya está configurado.

## 📚 Archivos de Configuración Generados

### Tablespace DMACADEMICO_DAT
- **Ubicación**: `/opt/oracle/oradata/XE/XEPDB1/dmacademico_dat01.dbf`
- **Tamaño inicial**: 100MB
- **Autoextend**: Habilitado
- **Crecimiento**: 10MB por vez
- **Tamaño máximo**: Ilimitado

### Usuario C##DM_ACADEMICO
- **Privilegios**: CONNECT, RESOURCE, DBA
- **Tablespace por defecto**: DMACADEMICO_DAT
- **Cuota**: Ilimitada
- **Permisos adicionales**: CREATE SESSION, CREATE TABLE, CREATE VIEW, etc.

## 🔒 Seguridad

- **Contraseñas**: Cambia las contraseñas por defecto en producción
- **Permisos**: Los scripts otorgan permisos DBA para facilitar el desarrollo
- **Red**: Configura el firewall apropiadamente en entornos productivos

## 📞 Soporte

Si tienes problemas con estos scripts:
1. Verifica que Docker esté funcionando correctamente
2. Revisa los logs de Oracle: `docker logs oracle_db`
3. Asegúrate de tener suficientes recursos del sistema
4. Consulta la documentación completa en `docker-oracle-config.md`
