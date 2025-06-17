# Configuración de Saiku con Database Links

## Problema Original

Saiku (y muchas herramientas de BI) solo permite configurar datasources con los parámetros básicos de conexión (host, puerto, database, usuario, contraseña). Esto significa que solo puede conectarse al **Container Database (CDB)**, pero nuestros datos están en el **Pluggable Database (XEPDB1)**.

## Solución: Database Links Transparentes

En lugar de copiar físicamente los datos (que sería lento y consumiría espacio), utilizamos **database links** desde el CDB hacia XEPDB1 y creamos **vistas transparentes** que hacen que los datos parezcan estar en el CDB.

## Arquitectura de la Solución

```
Saiku → CDB (Usuario: C##DM_ACADEMICO) → Database Link → XEPDB1 (dm_academico)
                    ↓
              Vistas Transparentes
                    ↓  
            D_CURSO_ACADEMICO ────→ dm_academico.D_CURSO_ACADEMICO@XEPDB1_LINK
            D_CENTRO ─────────────→ dm_academico.D_CENTRO@XEPDB1_LINK
            D_ASIGNATURA ─────────→ dm_academico.D_ASIGNATURA@XEPDB1_LINK
            D_SEXO ───────────────→ dm_academico.D_SEXO@XEPDB1_LINK
            F_MATRICULA ──────────→ dm_academico.F_MATRICULA@XEPDB1_LINK
```

## Archivos de la Solución

### 1. `setup_saiku_cdb_links.sql`
Script principal que configura:
- Usuario común `C##DM_ACADEMICO` en CDB
- Database link `XEPDB1_LINK` hacia XEPDB1
- Vistas transparentes que apuntan a las tablas originales
- Sinónimos opcionales con nombres más descriptivos

### 2. `setup_saiku_cdb.ps1`
Script de PowerShell que automatiza todo el proceso:
- Verifica conectividad con Oracle
- Ejecuta el script SQL de configuración
- Valida que todo funcione correctamente
- Muestra los parámetros de conexión para Saiku

### 3. `verify_saiku_setup.sql`
Script de verificación que muestra:
- Estado actual de la configuración
- Database links creados
- Vistas y sinónimos disponibles
- Estadísticas de datos accesibles

### 4. `cleanup_saiku_setup.sql`
Script de limpieza que elimina toda la configuración para poder reinstalar desde cero.

## Instrucciones de Uso

### Configuración Inicial

1. **Ejecutar setup automático (recomendado):**
   ```powershell
   .\setup_saiku_cdb.ps1
   ```

2. **O ejecutar manualmente:**
   ```sql
   sqlplus system/password@localhost:1521/XE @setup_saiku_cdb_links.sql
   ```

### Configuración en Saiku

Una vez ejecutado el setup, configurar Saiku con:

- **Driver:** Oracle JDBC Thin
- **URL:** `jdbc:oracle:thin:@localhost:1521:XE`
- **Username:** `C##DM_ACADEMICO`
- **Password:** `YourPassword123@`

> **Nota:** Esta configuración es consistente con el contenedor Docker oracle_db del proyecto.

### Tablas Disponibles

En Saiku verás estas tablas/vistas:

| Nombre en Saiku | Descripción | Tabla Original |
|----------------|-------------|----------------|
| `D_CURSO_ACADEMICO` | Dimensión Cursos Académicos | `XEPDB1.dm_academico.D_CURSO_ACADEMICO` |
| `D_CENTRO` | Dimensión Centros | `XEPDB1.dm_academico.D_CENTRO` |
| `D_ASIGNATURA` | Dimensión Asignaturas | `XEPDB1.dm_academico.D_ASIGNATURA` |
| `D_SEXO` | Dimensión Sexo | `XEPDB1.dm_academico.D_SEXO` |
| `F_MATRICULA` | Tabla de Hechos Matrículas | `XEPDB1.dm_academico.F_MATRICULA` |
| `F_RENDIMIENTO` | Tabla de Hechos Rendimiento | `XEPDB1.dm_academico.F_RENDIMIENTO` |

También hay sinónimos disponibles con nombres más descriptivos:
- `DIM_CURSO_ACADEMICO`, `DIM_CENTRO`, `DIM_ASIGNATURA`, `DIM_SEXO`
- `FACT_MATRICULA`

## Verificación y Troubleshooting

### Verificar Configuración
```sql
sqlplus system/password@localhost:1521/XE @verify_saiku_setup.sql
```

### Limpiar y Reinstalar
```sql
sqlplus system/password@localhost:1521/XE @cleanup_saiku_setup.sql
.\setup_saiku_cdb.ps1
```

### Problemas Comunes

1. **Error "ORA-12541: TNS:no listener"**
   - Verificar que el contenedor Docker oracle_db esté ejecutándose
   - Comprobar puerto 1521 mapeado correctamente

2. **Error "ORA-01017: invalid username/password"**
   - Verificar contraseña SYS: YourStrongPassword123
   - Verificar contraseña C##DM_ACADEMICO: YourPassword123@
   - Asegurar que XEPDB1 esté abierto

3. **Error "ORA-02019: connection description for remote database not found"**
   - Verificar que XEPDB1 esté disponible en el contenedor
   - Comprobar servicios de Oracle en Docker

4. **Tablas no aparecen en Saiku**
   - Ejecutar `verify_saiku_setup.sql` para verificar vistas
   - Comprobar permisos del usuario C##DM_ACADEMICO

## Ventajas de esta Solución

✅ **Sin duplicación de datos:** Los datos permanecen en XEPDB1
✅ **Tiempo real:** Los cambios en XEPDB1 se reflejan inmediatamente
✅ **Eficiente:** No consume espacio adicional
✅ **Transparente:** Para Saiku parece que los datos están en CDB
✅ **Mantenible:** Fácil de configurar, verificar y limpiar

## Integración con el Proyecto

Esta solución se integra perfectamente con:
- Los notebooks de aprendizaje MDX
- El servidor Pentaho existente
- Los scripts de generación de datos faker
- La estructura general del proyecto TFG
