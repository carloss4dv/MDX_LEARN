import os
import pandas as pd
import cx_Oracle
import numpy as np
from config.connection import get_connection
from tqdm import tqdm
import time
from datetime import datetime

# Función para establecer conexión directamente sin depender del archivo .env
def get_direct_connection():
    """
    Establece y retorna una conexión directa a la base de datos Oracle
    usando los valores hardcodeados que funcionan con clean_database.bat
    
    Returns:
        cx_Oracle.Connection: Objeto de conexión a Oracle
    """
    try:
        # Verificar versión de cx_Oracle
        print(f"Versión de cx_Oracle: {cx_Oracle.version}")
        
        # Configuración de Oracle Instant Client si es necesario
        oracle_client_path = 'C:\\oracle\\instantclient_19_11'
        if oracle_client_path:
            print(f"Añadiendo Oracle Instant Client al PATH: {oracle_client_path}")
            os.environ["PATH"] = os.environ["PATH"] + ";" + oracle_client_path
        
        # Datos de conexión para Docker (los mismos del script bat)
        # Cambiamos localhost a la dirección IP del contenedor Docker
        # Este es un posible problema si Docker está usando su propia red interna
        host = 'localhost'  # Cambia esto si es necesario a la IP de Docker
        port = '1521'
        service_name = 'XEPDB1'
        user = 'C##DM_ACADEMICO'
        password = 'YourPassword123'  # Quitamos el @ al final que puede causar problemas
        
        print(f"Intentando conectar a: {user}@{host}:{port}/{service_name}")
        
        # Intentar diferentes formas de conexión
        connection = None
        error_messages = []
        
        # Intento 1: DSN con service_name
        try:
            print("Intento 1: Usando service_name en DSN")
            dsn = cx_Oracle.makedsn(host=host, port=port, service_name=service_name)
            print(f"DSN creado: {dsn}")
            connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
        except cx_Oracle.Error as e:
            error_obj, = e.args
            error_messages.append(f"Error 1: {error_obj.message} (código {error_obj.code})")
        
        # Intento 2: DSN con SID
        if not connection:
            try:
                print("Intento 2: Usando SID en DSN")
                dsn = cx_Oracle.makedsn(host=host, port=port, sid=service_name)
                print(f"DSN creado: {dsn}")
                connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
            except cx_Oracle.Error as e:
                error_obj, = e.args
                error_messages.append(f"Error 2: {error_obj.message} (código {error_obj.code})")
        
        # Intento 3: Cadena de conexión completa
        if not connection:
            try:
                print("Intento 3: Usando cadena de conexión Easy Connect")
                conn_str = f"{user}/{password}@{host}:{port}/{service_name}"
                print(f"Cadena de conexión: {user}@{host}:{port}/{service_name}")
                connection = cx_Oracle.connect(conn_str)
            except cx_Oracle.Error as e:
                error_obj, = e.args
                error_messages.append(f"Error 3: {error_obj.message} (código {error_obj.code})")
                
        # Intento 4: Usando la cadena exacta del script batch
        if not connection:
            try:
                print("Intento 4: Usando la cadena exacta de clean_database.bat")
                conn_str = f"{user}/{password}@//{host}:{port}/{service_name}"
                print(f"Cadena de conexión: {user}@//{host}:{port}/{service_name}")
                connection = cx_Oracle.connect(conn_str)
            except cx_Oracle.Error as e:
                error_obj, = e.args
                error_messages.append(f"Error 4: {error_obj.message} (código {error_obj.code})")
        
        if connection:
            print(f"Conexión establecida con éxito a {user}@{host}:{port}/{service_name}")
            return connection
        else:
            print("No se pudo establecer la conexión. Errores:")
            for msg in error_messages:
                print(f"  - {msg}")
            raise Exception("No se pudo establecer conexión con Oracle")
            
    except cx_Oracle.Error as error:
        error_obj, = error.args
        print(f"Error de Oracle al conectar: {error_obj.message}")
        print(f"Código de error: {error_obj.code}")
        raise
    except Exception as e:
        print(f"Error general al conectar: {str(e)}")
        print(f"Tipo de error: {type(e)}")
        raise

def get_column_names_and_types(table_name, connection):
    """Obtiene los nombres de las columnas y sus tipos de datos de una tabla en Oracle"""
    cursor = connection.cursor()
    try:
        cursor.execute(f"""
            SELECT column_name, data_type, data_length, data_precision, data_scale, nullable
            FROM all_tab_columns 
            WHERE table_name = '{table_name.upper()}'
            ORDER BY column_id
        """)
        columns_info = [(row[0], row[1], row[2], row[3], row[4], row[5]) 
                        for row in cursor]
        return columns_info
    except cx_Oracle.Error as error:
        print(f"Error al obtener columnas de {table_name}: {error}")
        return []
    finally:
        cursor.close()

def preprocess_dataframe(df, columns_info):
    """
    Preprocesa el DataFrame para que coincida con los tipos de datos en Oracle
    
    Args:
        df (DataFrame): DataFrame a preprocesar
        columns_info (list): Lista de tuplas con información de columnas de Oracle
        
    Returns:
        DataFrame: DataFrame procesado
    """
    if df.empty:
        return df
    
    # Crear una copia del DataFrame para evitar warnings de SettingWithCopyWarning
    df = df.copy()
    
    # Crear un diccionario con la información de columnas de Oracle
    oracle_columns = {col_name.upper(): (data_type, data_length, data_precision, data_scale, nullable) 
                     for col_name, data_type, data_length, data_precision, data_scale, nullable in columns_info}
    
    # Convertir nombres de columnas del DataFrame a mayúsculas para comparación
    df_columns_upper = {col: col.upper() for col in df.columns}
    
    # Convertir los tipos de datos según corresponda
    for col in df.columns:
        col_upper = df_columns_upper[col]
        if col_upper in oracle_columns:
            data_type, data_length, data_precision, data_scale, nullable = oracle_columns[col_upper]
            
            # Manejar valores nulos primero
            if nullable == 'Y':
                # Reemplazar varios tipos de valores nulos con None
                df[col] = df[col].replace({
                    np.nan: None, 
                    'nan': None, 
                    'NaN': None,
                    'null': None,
                    'NULL': None,
                    'None': None,
                    '': None,
                    ' ': None
                })
            else:
                # Para columnas NOT NULL, reemplazar nulos con valores por defecto según el tipo
                if data_type in ('NUMBER', 'FLOAT'):
                    df[col] = df[col].fillna(0)
                elif data_type.startswith(('VARCHAR', 'CHAR')):
                    df[col] = df[col].fillna('')
                elif data_type in ('DATE', 'TIMESTAMP'):
                    df[col] = df[col].fillna(pd.Timestamp.now())
            
            # Convertir tipos de datos según el tipo en Oracle
            if data_type in ('NUMBER', 'FLOAT'):
                # Para columnas numéricas
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    if data_precision is not None:
                        # Redondear a la precisión especificada
                        df[col] = df[col].round(data_scale if data_scale is not None else 0)
                except Exception as e:
                    print(f"Error al convertir columna numérica {col}: {e}")
            
            elif data_type in ('DATE', 'TIMESTAMP'):
                # Para columnas de fecha
                try:
                    # Intentar diferentes formatos de fecha
                    for date_format in ['%Y-%m-%d', '%d/%m/%Y', '%Y%m%d']:
                        mask = df[col].notna() & df[col].astype(str).str.match(r'^\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|\d{8}$')
                        try:
                            df.loc[mask, col] = pd.to_datetime(df.loc[mask, col], format=date_format, errors='coerce')
                        except:
                            continue
                    
                    # Los demás a nulo si se permite
                    if nullable == 'Y':
                        df.loc[df[col].notna() & ~df[col].apply(lambda x: isinstance(x, pd.Timestamp)), col] = None
                    else:
                        df.loc[df[col].notna() & ~df[col].apply(lambda x: isinstance(x, pd.Timestamp)), col] = pd.Timestamp.now()
                except Exception as e:
                    print(f"Error al convertir fechas en columna {col}: {e}")
                    
            elif data_type.startswith('VARCHAR') or data_type.startswith('CHAR'):
                # Para columnas de texto
                try:
                    # Convertir a string y limpiar
                    df[col] = df[col].astype(str)
                    df[col] = df[col].replace({
                        'nan': None, 
                        'None': None, 
                        'NULL': None,
                        'null': None
                    })
                    
                    # Truncar si es necesario y no es None
                    if data_length and data_length > 0:
                        df[col] = df[col].apply(lambda x: str(x)[:data_length] if x is not None else x)
                        
                    # Eliminar espacios en blanco al inicio y final
                    df[col] = df[col].apply(lambda x: x.strip() if x is not None else x)
                except Exception as e:
                    print(f"Error al procesar texto en columna {col}: {e}")
    
    return df

def upload_csv_to_oracle(csv_path, table_name, connection, batch_size=1000):
    """
    Carga un archivo CSV a una tabla de Oracle
    
    Args:
        csv_path (str): Ruta al archivo CSV
        table_name (str): Nombre de la tabla en Oracle
        connection (cx_Oracle.Connection): Conexión a Oracle
        batch_size (int): Tamaño del lote para inserciones
    """
    try:
        # Verificar si la tabla existe
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                SELECT COUNT(*) 
                FROM all_tables 
                WHERE table_name = '{table_name}' 
                AND owner = '{connection.username}'
            """)
            if cursor.fetchone()[0] == 0:
                print(f"La tabla {table_name} no existe en el esquema {connection.username}.")
                print("Tablas disponibles:")
                cursor.execute(f"""
                    SELECT table_name 
                    FROM all_tables 
                    WHERE owner = '{connection.username}'
                    ORDER BY table_name
                """)
                tables = cursor.fetchall()
                for table in tables:
                    print(f"  - {table[0]}")
                return
        except cx_Oracle.Error as e:
            print(f"Error al verificar la existencia de la tabla {table_name}: {e}")
            return
            
        # Leer el CSV con manejo de valores nulos
        try:
            df = pd.read_csv(csv_path, na_values=['', 'NULL', 'null', 'NaN', 'nan'], keep_default_na=True)
        except Exception as e:
            print(f"Error al leer el archivo CSV {csv_path}: {e}")
            return
        
        # Si el DataFrame está vacío, no hacer nada
        if df.empty:
            print(f"El archivo {csv_path} está vacío. No se cargará nada.")
            return
        
        # Obtener las columnas y tipos de datos de la tabla de Oracle
        columns_info = get_column_names_and_types(table_name, connection)
        if not columns_info:
            print(f"No se pudieron obtener las columnas para {table_name}. Omitiendo tabla.")
            return
        
        # Nombres de columnas en Oracle
        oracle_column_names = [col[0] for col in columns_info]
        
        # Filtrar el DataFrame para incluir solo las columnas que existen en Oracle
        # y convertir nombres a mayúsculas para comparar
        df_columns_upper = [col.upper() for col in df.columns]
        matching_columns = []
        
        for i, col in enumerate(df.columns):
            if df_columns_upper[i] in oracle_column_names:
                matching_columns.append(col)
            else:
                print(f"Advertencia: La columna {col} no existe en la tabla {table_name}")
        
        # Si no hay columnas coincidentes, salir
        if not matching_columns:
            print(f"No hay columnas coincidentes entre el CSV y la tabla {table_name}. Omitiendo tabla.")
            return
        
        # Seleccionar solo las columnas que existen en Oracle
        df_filtered = df[matching_columns]
        
        # Preprocesar DataFrame para coincidencia de tipos
        df_filtered = preprocess_dataframe(df_filtered, columns_info)
        
        # Verificar si hay claves primarias
        try:
            cursor.execute(f"""
                SELECT cols.column_name
                FROM all_constraints cons, all_cons_columns cols
                WHERE cons.constraint_type = 'P'
                AND cons.constraint_name = cols.constraint_name
                AND cons.owner = cols.owner
                AND cols.table_name = '{table_name}'
            """)
            pk_columns = [row[0] for row in cursor.fetchall()]
        except cx_Oracle.Error as e:
            print(f"Error al obtener información de clave primaria: {e}")
            pk_columns = []
        
        # Si hay claves primarias, eliminar duplicados
        if pk_columns:
            print(f"Eliminando duplicados basados en la clave primaria: {', '.join(pk_columns)}")
            df_filtered = df_filtered.drop_duplicates(subset=[col for col in pk_columns if col in df_filtered.columns])
        
        # Crear la sentencia SQL para la inserción
        oracle_matching_columns = [col.upper() for col in matching_columns]
        placeholders = ':' + ', :'.join(str(i+1) for i in range(len(matching_columns)))
        insert_sql = f"INSERT INTO {table_name} ({', '.join(oracle_matching_columns)}) VALUES ({placeholders})"
        
        # Insertar los datos en lotes
        cursor = connection.cursor()
        total_rows = len(df_filtered)
        rows_inserted = 0
        errors = 0
        error_rows = []
        
        try:
            # Procesar en lotes con barra de progreso
            for i in tqdm(range(0, total_rows, batch_size), desc=f"Cargando {table_name}"):
                batch = df_filtered.iloc[i:i+batch_size]
                batch_data = [tuple(None if pd.isna(x) else x for x in row) for row in batch.values]
                
                try:
                    cursor.executemany(insert_sql, batch_data)
                    connection.commit()
                    rows_inserted += len(batch)
                except cx_Oracle.Error as error:
                    print(f"\nError al insertar lote en {table_name}: {error}")
                    connection.rollback()
                    errors += 1
                    
                    # Si hay demasiados errores, detener
                    if errors > 10:
                        print(f"Demasiados errores en {table_name}. Deteniendo carga.")
                        break
                    
                    # Intentar insertar fila por fila para identificar la problemática
                    for j, row in batch.iterrows():
                        try:
                            row_data = tuple(None if pd.isna(x) else x for x in row)
                            cursor.execute(insert_sql, row_data)
                            connection.commit()
                            rows_inserted += 1
                        except cx_Oracle.Error as row_error:
                            error_obj, = row_error.args
                            error_rows.append({
                                'row_index': j,
                                'error_code': error_obj.code,
                                'error_message': error_obj.message,
                                'data': dict(zip(matching_columns, row_data))
                            })
                            connection.rollback()
                            errors += 1
            
            # Resumen de errores
            if error_rows:
                print("\nResumen de errores:")
                error_types = {}
                for error in error_rows:
                    error_key = f"ORA-{error['error_code']}"
                    if error_key not in error_types:
                        error_types[error_key] = {
                            'count': 0,
                            'message': error['error_message'],
                            'example_row': error['data']
                        }
                    error_types[error_key]['count'] += 1
                
                for error_code, details in error_types.items():
                    print(f"\n{error_code} ({details['count']} ocurrencias):")
                    print(f"Mensaje: {details['message']}")
                    print("Ejemplo de fila problemática:")
                    for col, val in details['example_row'].items():
                        print(f"  {col}: {val}")
            
            print(f"\nCarga de {table_name} completada. {rows_inserted}/{total_rows} filas procesadas con {errors} errores.")
        
        finally:
            cursor.close()
    
    except Exception as e:
        print(f"Error al cargar {csv_path} en {table_name}: {e}")
        raise

def truncate_table(table_name, connection):
    """Vacía una tabla para reiniciar la carga"""
    cursor = connection.cursor()
    try:
        cursor.execute(f"TRUNCATE TABLE {table_name}")
        connection.commit()
        print(f"Tabla {table_name} vaciada correctamente.")
    except cx_Oracle.Error as error:
        print(f"Error al vaciar tabla {table_name}: {error}")
        connection.rollback()
    finally:
        cursor.close()

def check_and_create_missing_tables(connection):
    """
    Verifica y crea las tablas faltantes en el esquema
    
    Args:
        connection (cx_Oracle.Connection): Conexión a Oracle
    """
    expected_tables = {
        'D_AREA_CONOCIMIENTO': """
            CREATE TABLE D_AREA_CONOCIMIENTO (
                ID_AREA_CONOCIMIENTO NUMBER(10) PRIMARY KEY,
                NOMBRE_AREA_CONOCIMIENTO VARCHAR2(100),
                DESCRIPCION VARCHAR2(500)
            )
        """,
        'D_TERRITORIO': """
            CREATE TABLE D_TERRITORIO (
                ID_TERRITORIO NUMBER(10) PRIMARY KEY,
                NOMBRE_TERRITORIO VARCHAR2(100),
                TIPO_TERRITORIO VARCHAR2(50),
                ID_TERRITORIO_PADRE NUMBER(10),
                NIVEL_TERRITORIAL NUMBER(2)
            )
        """
    }
    
    # Modificar longitudes de columnas en tablas existentes
    column_fixes = {
        'D_POBLACION': [
            "ALTER TABLE D_POBLACION MODIFY NOMBRE_PROVINCIA VARCHAR2(50)",
            "ALTER TABLE D_POBLACION MODIFY NOMBRE_CCAA VARCHAR2(50)"
        ],
        'D_NACIONALIDAD': [
            "ALTER TABLE D_NACIONALIDAD MODIFY NOMBRE_NACIONALIDAD VARCHAR2(100)"
        ],
        'D_UNIVERSIDAD': [
            "ALTER TABLE D_UNIVERSIDAD MODIFY NOMBRE_PAIS VARCHAR2(100)",
            "ALTER TABLE D_UNIVERSIDAD MODIFY NOMBRE_UNIVERSIDAD VARCHAR2(200)"
        ],
        'D_CENTRO_DESTINO': [
            "ALTER TABLE D_CENTRO_DESTINO MODIFY NOMBRE_UNIVERSIDAD VARCHAR2(200)"
        ],
        'D_CENTRO_OTRA_UNIVERSIDAD': [
            "ALTER TABLE D_CENTRO_OTRA_UNIVERSIDAD MODIFY NOMBRE_UNIVERSIDAD VARCHAR2(200)"
        ],
        'D_CENTRO_ESTUDIO': [
            "ALTER TABLE D_CENTRO_ESTUDIO MODIFY NOMBRE_UNIVERSIDAD VARCHAR2(200)"
        ],
        'F_MATRICULA': [
            "ALTER TABLE F_MATRICULA MODIFY ID_DETALLE_CUPO_GENERAL_NK VARCHAR2(10)"
        ],
        'F_SOLICITANTE_ADMISION': [
            "ALTER TABLE F_SOLICITANTE_ADMISION MODIFY ID_DETALLE_CUPO_GENERAL_NK VARCHAR2(10)"
        ],
        'F_DOCTORADO': [
            "ALTER TABLE F_DOCTORADO MODIFY ID_SITUACION_ADVA_NK VARCHAR2(10)"
        ]
    }
    
    cursor = connection.cursor()
    try:
        # Obtener tablas existentes
        cursor.execute(f"""
            SELECT table_name 
            FROM all_tables 
            WHERE owner = '{connection.username}'
        """)
        existing_tables = {row[0] for row in cursor.fetchall()}
        
        # Verificar y crear tablas faltantes
        for table_name, create_sql in expected_tables.items():
            if table_name not in existing_tables:
                print(f"Creando tabla faltante: {table_name}")
                try:
                    cursor.execute(create_sql)
                    connection.commit()
                    print(f"Tabla {table_name} creada exitosamente")
                except cx_Oracle.Error as e:
                    print(f"Error al crear tabla {table_name}: {e}")
                    connection.rollback()
        
        # Aplicar correcciones de longitud de columnas
        for table_name, alter_statements in column_fixes.items():
            if table_name in existing_tables:
                print(f"\nAjustando columnas en tabla {table_name}...")
                for alter_sql in alter_statements:
                    try:
                        cursor.execute(alter_sql)
                        connection.commit()
                        print(f"Columna modificada exitosamente: {alter_sql}")
                    except cx_Oracle.Error as e:
                        if "ORA-01442" in str(e):  # Column already has desired properties
                            print(f"La columna ya tiene las propiedades deseadas: {alter_sql}")
                        else:
                            print(f"Error al modificar columna: {e}")
                            connection.rollback()
    
    except cx_Oracle.Error as e:
        print(f"Error al verificar tablas: {e}")
    finally:
        cursor.close()

def main():
    # Establecer conexión
    print("Conectando a Oracle...")
    connection = None
    try:
        connection = get_direct_connection()
        
        # Verificar y crear tablas faltantes
        check_and_create_missing_tables(connection)
        
        # Definir el orden de carga para respetar las dependencias
        # Primero las tablas de dimensión (sin dependencias)
        dimension_tables_base = [
            'd_sexo', 'd_pais', 'd_tiempo', 'd_curso_academico', 'd_curso_cohorte',
            'd_tipo_estudio', 'd_rama_conocimiento', 'd_calificacion', 'd_convocatoria',
            'd_tipo_acceso', 'd_tipo_acceso_preinscripcion', 'd_clase_asignatura',
            'd_tipo_docencia', 'd_tipo_egreso', 'd_tipo_abandono', 'd_tipo_procedimiento',
            'd_tipo_reconocimiento', 'd_cupo_adjudicacion', 'd_rango_credito',
            'd_rango_edad', 'd_rango_nota_admision', 'd_rango_nota_numerica',
            'd_rango_nota_crue', 'd_rango_nota_egracons', 'd_estudio_previo',
            'd_campus', 'd_articulo', 'd_edad_est', 'd_dedicacion', 'd_dedicacion_profesor',
            'd_dedicacion_alumno', 'd_categoria_cuerpo_pdi', 'd_tipo_asignatura',
            'd_tipo_centro', 'd_modalidad_plan_estudio', 'd_estado_adjudicacion',
            'd_idioma_movilidad', 'd_nivel_estudios_movilidad', 'd_area_estudios_movilidad',
            'd_colectivo_movilidad', 'd_estado_acuerdo_bilateral', 'd_acuerdo_bilateral',
            'd_proyecto_investigacion', 'd_rama_macroarea', 'd_detalle_cupo_general',
            'd_clase_liquidacion', 'd_estudio_propio_tipo', 'd_estudio_propio_modalidad',
            'd_estudio_propio_organo_gest', 'd_doctorado_tipo_beca', 'd_estado_solicitud_doctorado',
            'd_estado_credencial_acceso', 'd_nivel_idioma', 'd_situacion_administrativa',
            'd_tipo_contrato', 'd_modalidad_asignatura', 'd_periodo_lectivo', 'd_area_conocimiento'
        ]
        
        # Tablas de dimensión con dependencias
        dimension_tables_dependent = [
            'd_poblacion', 'd_nacionalidad', 'd_poblacion_centro',
            'd_centro', 'd_universidad', 'd_centro_destino', 'd_centro_otra_universidad',
            'd_persona', 'd_asignatura', 'd_plan_estudio', 'd_estudio',
            'd_centro_estudio', 'd_estudio_jerarq', 'd_estudio_destino',
            'd_estudio_otra_universidad', 'd_plan_estudio_asignatura',
            'd_programa_movilidad', 'd_idioma_nivel_movilidad', 'd_titulacion',
            'd_grupo', 'd_plan_estudio_ano_datos', 'd_estudio_propio',
            'd_rango_credito_movilidad', 'd_convocatoria_preinscripcion', 'd_territorio'
        ]
        
        # Tablas de hechos
        fact_tables = [
            'f_matricula', 'f_rendimiento', 'f_oferta_admision', 'f_solicitante_admision',
            'f_egresado', 'f_cohorte', 'f_estudiantes_movilidad_in', 'f_estudiantes_movilidad_out',
            'f_solicitudes_movilidad', 'f_doctorado_admision', 'f_egracons',
            'f_estudio_propio_matricula', 'f_oferta_acuerdo_bilateral', 'f_doctorado',
            'f_tabla_fusion', 'f_tabla_fusion_estcen'
        ]
        
        # Directorio de archivos generados
        dimensions_dir = 'output/dimensions'
        facts_dir = 'output/facts'
        
        # Preguntar si desea vaciar las tablas antes de cargar
        truncate_tables = 's'
        
        if truncate_tables:
            print("\nVaciando tablas de hechos...")
            for table in reversed(fact_tables):
                truncate_table(table.upper(), connection)
            
            print("\nVaciando tablas de dimensión con dependencias...")
            for table in reversed(dimension_tables_dependent):
                truncate_table(table.upper(), connection)
            
            print("\nVaciando tablas de dimensión base...")
            for table in reversed(dimension_tables_base):
                truncate_table(table.upper(), connection)
        
        print("\nCargando tablas de dimensión (sin dependencias)...")
        for table in dimension_tables_base:
            csv_path = os.path.join(dimensions_dir, f"{table}.csv")
            if os.path.exists(csv_path):
                upload_csv_to_oracle(csv_path, table.upper(), connection)
            else:
                print(f"Archivo no encontrado: {csv_path}")
        
        print("\nCargando tablas de dimensión (con dependencias)...")
        for table in dimension_tables_dependent:
            csv_path = os.path.join(dimensions_dir, f"{table}.csv")
            if os.path.exists(csv_path):
                upload_csv_to_oracle(csv_path, table.upper(), connection)
            else:
                print(f"Archivo no encontrado: {csv_path}")
        
        print("\nCargando tablas de hechos...")
        for table in fact_tables:
            csv_path = os.path.join(facts_dir, f"{table}.csv")
            if os.path.exists(csv_path):
                upload_csv_to_oracle(csv_path, table.upper(), connection)
            else:
                print(f"Archivo no encontrado: {csv_path}")
        
        print("\n¡Carga completada con éxito!")
        
    except Exception as e:
        print(f"Error durante la carga: {e}")
    
    finally:
        # Cerrar conexión
        if connection:
            connection.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    start_time = time.time()
    main()
    elapsed_time = time.time() - start_time
    print(f"\nTiempo total de ejecución: {elapsed_time:.2f} segundos") 