#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de carga de datos usando JDBC
Soporte para Oracle Database y PostgreSQL
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from tqdm import tqdm
import time
import logging
from datetime import datetime
from dotenv import load_dotenv
import configparser

# Verificar si JayDeBeApi está disponible
try:
    import jaydebeapi as jdbc
    JDBC_AVAILABLE = True
except ImportError:
    JDBC_AVAILABLE = False

# Cargar variables de entorno
load_dotenv()

def setup_logging(log_level='INFO', log_file='upload_db.log'):
    """
    Configura el sistema de logging compacto y eficiente
    """
    # Limpiar handlers existentes
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # Configurar formato compacto
    log_format = '%(asctime)s [%(levelname)s] %(message)s'
    date_format = '%H:%M:%S'
    
    # Logger principal
    logger = logging.getLogger('upload_db')
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Handler para archivo - formato detallado
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Handler para consola - formato compacto
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_formatter = logging.Formatter(log_format, datefmt=date_format)
    console_handler.setFormatter(console_formatter)
    
    # Añadir handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Configurar logger global
logger = setup_logging()

class DatabaseUploader:
    """Clase para cargar datos a diferentes bases de datos usando JDBC"""
    
    def __init__(self, db_type='oracle', log_level='INFO'):
        """
        Inicializa el uploader con el tipo de base de datos
        
        Args:
            db_type (str): Tipo de base de datos ('oracle' o 'postgresql')
            log_level (str): Nivel de logging
        """
        self.db_type = db_type.lower()
        self.connection = None
        self.cursor = None
        self.driver_path = None
        self.stats = {
            'start_time': datetime.now(),
            'tables_processed': 0,
            'tables_success': 0,
            'tables_failed': 0,
            'total_rows': 0,
            'errors': []
        }
        
        logger.info(f"🚀 Iniciando DatabaseUploader para {db_type.upper()}")
        
        # Configurar rutas de drivers JDBC
        self._setup_jdbc_drivers()
        
    def _setup_jdbc_drivers(self):
        """Configura las rutas de los drivers JDBC"""
        lib_dir = Path(__file__).parent / 'lib'
        logger.debug(f"Buscando drivers JDBC en: {lib_dir}")
        
        if self.db_type == 'oracle':
            possible_paths = [
                lib_dir / 'ojdbc8.jar',
                lib_dir / 'ojdbc11.jar',
                lib_dir / 'ojdbc17.jar',
                Path.home() / '.m2' / 'repository' / 'com' / 'oracle' / 'database' / 'jdbc' / 'ojdbc8' / '21.7.0.0' / 'ojdbc8-21.7.0.0.jar',
                Path('C:/oracle/instantclient_19_11/ojdbc8.jar'),
                Path('/opt/oracle/instantclient/ojdbc8.jar')
            ]
            
            for path in possible_paths:
                if path.exists():
                    self.driver_path = str(path)
                    logger.debug(f"Driver Oracle encontrado: {path}")
                    break
                    
            if not self.driver_path:
                error_msg = "Driver Oracle JDBC no encontrado"
                logger.error(error_msg)
                logger.info("💡 Ejecute: python download_jdbc_drivers.py")
                
        elif self.db_type == 'postgresql':
            possible_paths = [
                lib_dir / 'postgresql.jar',
                lib_dir / 'postgresql-42.5.0.jar',
                Path.home() / '.m2' / 'repository' / 'org' / 'postgresql' / 'postgresql' / '42.5.0' / 'postgresql-42.5.0.jar'
            ]
            
            for path in possible_paths:
                if path.exists():
                    self.driver_path = str(path)
                    logger.debug(f"Driver PostgreSQL encontrado: {path}")
                    break
                    
            if not self.driver_path:
                error_msg = "Driver PostgreSQL JDBC no encontrado"
                logger.error(error_msg)
                logger.info("💡 Ejecute: python download_jdbc_drivers.py")
                
    def connect(self):
        """Establece conexión con la base de datos"""
        if not JDBC_AVAILABLE:
            error_msg = "JayDeBeApi no está disponible"
            logger.error(error_msg)
            logger.info("💡 pip install JayDeBeApi>=1.2.3")
            raise ImportError(error_msg)
            
        if not self.driver_path:
            error_msg = f"Driver JDBC para {self.db_type} no encontrado"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
            
        try:
            logger.info(f"🔌 Conectando a {self.db_type.upper()}...")
            start_time = time.time()
            
            if self.db_type == 'oracle':
                self._connect_oracle()
            elif self.db_type == 'postgresql':
                self._connect_postgresql()
            else:
                raise ValueError(f"Tipo de base de datos no soportado: {self.db_type}")
                
            connect_time = time.time() - start_time
            logger.info(f"✅ Conexión establecida en {connect_time:.2f}s")
            
        except Exception as e:
            error_msg = f"Error al conectar con {self.db_type}: {e}"
            logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            raise
            
    def _connect_oracle(self):
        """Conecta a Oracle Database usando JDBC"""
        host = os.getenv('ORACLE_HOST', 'localhost')
        port = os.getenv('ORACLE_PORT', '1521')
        service = os.getenv('ORACLE_SERVICE', 'XEPDB1')
        user = os.getenv('ORACLE_USER', 'C##DM_ACADEMICO')
        password = os.getenv('ORACLE_PASSWORD', 'YourPassword123')
        
        logger.debug(f"Oracle config: {user}@{host}:{port}/{service}")
        
        # URL de conexión Oracle
        jdbc_url = f"jdbc:oracle:thin:@{host}:{port}:{service}"
        
        try:
            self.connection = jdbc.connect(
                "oracle.jdbc.driver.OracleDriver",
                jdbc_url,
                [user, password],
                self.driver_path
            )
            connection.setAutoCommit(False)
        except:
            # Intentar con service_name
            jdbc_url = f"jdbc:oracle:thin:@//{host}:{port}/{service}"
            logger.debug(f"Reintentando con service_name: {jdbc_url}")
            self.connection = jdbc.connect(
                "oracle.jdbc.driver.OracleDriver",
                jdbc_url,
                [user, password],
                self.driver_path
            )
            
        self.cursor = self.connection.cursor()
        
        # 🔧 CONFIGURAR ORACLE AUTOMÁTICAMENTE
        try:
            logger.info("🔧 Configurando Oracle para formato de fechas...")
            
            # Configurar formato de fecha compatible
            oracle_config_commands = [
                "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD'",
                "ALTER SESSION SET NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS'",
                "ALTER SESSION SET NLS_NUMERIC_CHARACTERS = '.,'",
                "ALTER SESSION SET NLS_LANGUAGE = 'AMERICAN'"
            ]
            
            for cmd in oracle_config_commands:
                try:
                    self.cursor.execute(cmd)
                    logger.debug(f"✅ Oracle config: {cmd}")
                except Exception as e:
                    logger.warning(f"⚠️  No se pudo ejecutar: {cmd} - {e}")
            
            # Commit la configuración
            self.connection.commit()
            logger.info("✅ Oracle configurado correctamente")
            
        except Exception as e:
            logger.warning(f"⚠️  Error configurando Oracle (continuando): {e}")
            # No es crítico, continuar sin esta configuración
        
    def _connect_postgresql(self):
        """Conecta a PostgreSQL usando JDBC"""
        host = os.getenv('POSTGRES_HOST', 'localhost')
        port = os.getenv('POSTGRES_PORT', '5432')
        database = os.getenv('POSTGRES_DB', 'dm_academico')
        user = os.getenv('POSTGRES_USER', 'postgres')
        password = os.getenv('POSTGRES_PASSWORD', 'postgres')
        
        logger.debug(f"PostgreSQL config: {user}@{host}:{port}/{database}")
        
        jdbc_url = f"jdbc:postgresql://{host}:{port}/{database}"
        
        self.connection = jdbc.connect(
            "org.postgresql.Driver",
            jdbc_url,
            [user, password],
            self.driver_path
        )
        self.cursor = self.connection.cursor()
        
    def get_table_columns(self, table_name):
        """Obtiene información de columnas de una tabla"""
        try:
            if self.db_type == 'oracle':
                query = """
                    SELECT column_name, data_type, data_length, data_precision, data_scale, nullable
                    FROM all_tab_columns 
                    WHERE table_name = ? AND owner = ?
                    ORDER BY column_id
                """
                user = os.getenv('ORACLE_USER', 'C##DM_ACADEMICO')
                self.cursor.execute(query, [table_name.upper(), user.upper()])
                
            elif self.db_type == 'postgresql':
                query = """
                    SELECT column_name, data_type, character_maximum_length, 
                           numeric_precision, numeric_scale, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = ? AND table_schema = 'public'
                    ORDER BY ordinal_position
                """
                self.cursor.execute(query, [table_name.lower()])
                
            columns = self.cursor.fetchall()
            logger.debug(f"Tabla {table_name}: {len(columns)} columnas")
            return columns
            
        except Exception as e:
            logger.warning(f"No se pudo obtener columnas de {table_name}: {e}")
            return []
        
    def preprocess_dataframe(self, df, table_name):
        """Preprocesa el DataFrame según el tipo de base de datos con manejo robusto de errores"""
        if df.empty:
            return df
            
        original_size = len(df)
        df = df.copy()
        
        # Obtener información de columnas
        columns_info = self.get_table_columns(table_name)
        
        if not columns_info:
            logger.warning(f"Usando DataFrame sin validación para {table_name}")
            # Preprocessing básico sin metadatos de columnas
            df = self._basic_preprocessing(df)
            return df
            
        # Crear diccionario de metadatos por columna
        column_metadata = {}
        for col_info in columns_info:
            col_name = col_info[0].upper()
            column_metadata[col_name] = {
                'data_type': col_info[1],
                'max_length': col_info[2] if len(col_info) > 2 else None,
                'precision': col_info[3] if len(col_info) > 3 else None,
                'scale': col_info[4] if len(col_info) > 4 else None,
                'nullable': col_info[5] if len(col_info) > 5 else 'Y'
            }
            
        # Procesar cada columna del DataFrame
        for df_column in df.columns:
            # Buscar metadatos de la columna (case-insensitive)
            col_meta = None
            for meta_col, meta_data in column_metadata.items():
                if df_column.upper() == meta_col:
                    col_meta = meta_data
                    break
                    
            if col_meta is None:
                logger.debug(f"No se encontraron metadatos para columna {df_column}")
                # Aplicar limpieza básica si no hay metadatos
                df[df_column] = self._clean_column_basic(df[df_column])
                continue
                
            data_type = col_meta['data_type']
            max_length = col_meta['max_length']
            precision = col_meta['precision']
            scale = col_meta['scale']
            nullable = col_meta['nullable']
            
            # APLICAR LIMPIEZA ROBUSTA POR TIPO DE DATOS
            if self.db_type == 'oracle':
                df[df_column] = self._clean_column_oracle(
                    df[df_column], df_column, data_type, max_length, 
                    precision, scale, nullable
                )
            else:
                df[df_column] = self._clean_column_postgresql(
                    df[df_column], df_column, data_type, max_length, 
                    precision, scale, nullable
                )
                        
        processed_size = len(df)
        if processed_size != original_size:
            logger.warning(f"Filas perdidas en {table_name}: {original_size} → {processed_size}")
            
        return df
        
    def _clean_column_basic(self, series):
        """Limpieza básica cuando no hay metadatos"""
        # Reemplazar valores problemáticos
        series = series.replace({
            np.nan: None, 'nan': None, 'NaN': None, 'NaT': None,
            'null': None, 'NULL': None, 'None': None,
            '': None, ' ': None, 'undefined': None
        })
        
        # Para Oracle, convertir timestamps a string
        if self.db_type == 'oracle':
            if series.dtype == 'datetime64[ns]' or 'datetime' in str(series.dtype):
                series = pd.to_datetime(series, errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S').replace('NaT', None)
            elif series.dtype in ['float64', 'float32'] or 'float' in str(series.dtype):
                # Convertir NaN numéricos a None
                series = series.replace({np.nan: None})
                
        return series
        
    def _clean_column_oracle(self, series, column_name, data_type, max_length, precision, scale, nullable):
        """Limpieza específica para Oracle con manejo robusto de todos los errores comunes"""
        
        # 1. LIMPIEZA INICIAL: Reemplazar todos los valores problemáticos
        problematic_values = {
            np.nan: None, 'nan': None, 'NaN': None, 'NaT': None,
            'null': None, 'NULL': None, 'None': None,
            '': None, ' ': None, 'undefined': None, 'inf': None, 
            '-inf': None, np.inf: None, -np.inf: None
        }
        series = series.replace(problematic_values)
        
        # 2. PROCESAR SEGÚN TIPO DE DATOS
        data_type_upper = data_type.upper()
        
        if 'NUMBER' in data_type_upper or 'INTEGER' in data_type_upper or 'DECIMAL' in data_type_upper:
            # MANEJO DE NÚMEROS - Prevenir ORA-01858 y IllegalArgumentException: NaN
            series = self._clean_numeric_oracle(series, column_name, precision, scale, nullable)
            
        elif 'VARCHAR' in data_type_upper or 'CHAR' in data_type_upper or 'CLOB' in data_type_upper:
            # MANEJO DE TEXTO - Prevenir ORA-12899
            series = self._clean_text_oracle(series, column_name, max_length, nullable)
            
        elif 'DATE' in data_type_upper or 'TIMESTAMP' in data_type_upper:
            # MANEJO DE FECHAS - Prevenir ORA-01858
            series = self._clean_date_oracle(series, column_name, nullable)
            
        else:
            # Tipo desconocido, limpieza básica
            logger.debug(f"Tipo de datos desconocido para {column_name}: {data_type}")
            if nullable in ('Y', 'YES'):
                series = series.replace(problematic_values)
            else:
                series = series.fillna('')
                
        return series
        
    def _clean_numeric_oracle(self, series, column_name, precision, scale, nullable):
        """Limpieza robusta de columnas numéricas para Oracle"""
        try:
            # Convertir a string primero para limpiar
            series_str = series.astype(str)
            
            # Limpiar caracteres no numéricos problemáticos
            series_str = series_str.replace({
                'nan': None, 'NaN': None, 'NaT': None, 'None': None,
                'null': None, 'NULL': None, '': None, ' ': None,
                'inf': None, '-inf': None, 'undefined': None
            })
            
            # Convertir a numérico
            series_numeric = pd.to_numeric(series_str, errors='coerce')
            
            # Manejar valores nulos
            if nullable in ('Y', 'YES'):
                series_numeric = series_numeric.replace({np.nan: None})
            else:
                # Para NOT NULL, usar 0 como valor por defecto
                series_numeric = series_numeric.fillna(0)
                
            # Aplicar límites de precisión si están definidos
            if precision and pd.notna(precision):
                try:
                    max_digits = int(precision)
                    if scale and pd.notna(scale):
                        scale_digits = int(scale)
                        # Para NUMBER(p,s), el máximo valor es 10^(p-s) - 1
                        max_value = 10**(max_digits - scale_digits) - 1
                        series_numeric = series_numeric.clip(upper=max_value, lower=-max_value)
                    else:
                        # Para INTEGER o NUMBER sin escala
                        max_value = 10**max_digits - 1
                        series_numeric = series_numeric.clip(upper=max_value, lower=-max_value)
                        # Convertir a entero si no hay decimales
                        if pd.isna(scale) or scale == 0:
                            series_numeric = series_numeric.round().astype('Int64')
                except Exception as e:
                    logger.debug(f"Error aplicando límites de precisión en {column_name}: {e}")
                    
            logger.debug(f"Columna numérica {column_name} limpiada: {series_numeric.isna().sum()} nulos")
            return series_numeric
            
        except Exception as e:
            logger.warning(f"Error procesando columna numérica {column_name}: {e}")
            # Fallback: usar 0 para NOT NULL, None para nullable
            if nullable in ('Y', 'YES'):
                return pd.Series([None] * len(series), dtype=object)
            else:
                return pd.Series([0] * len(series), dtype='int64')
                
    def _clean_text_oracle(self, series, column_name, max_length, nullable):
        """Limpieza robusta de columnas de texto para Oracle"""
        try:
            # Convertir todo a string primero
            series_str = series.astype(str)
            
            # Reemplazar valores nulos representados como string
            null_representations = ['nan', 'NaN', 'NaT', 'None', 'null', 'NULL', 'undefined']
            for null_repr in null_representations:
                series_str = series_str.replace(null_repr, None)
                
            # Manejar valores nulos
            if nullable in ('Y', 'YES'):
                series_str = series_str.replace('', None)
            else:
                # Para NOT NULL, usar string vacío
                series_str = series_str.fillna('')
                series_str = series_str.replace('', '')
                
            # Mapeo específico de columnas problemáticas conocidas
            known_column_limits = {
                'NOMBRE_CCAA': 30,
                'ID_SITUACION_ADVA_NK': 2,
                'ID_DETALLE_CUPO_GENERAL_NK': 3,
                'ID_PROYECTO_INVESTIGACION_NK': 30,
                'ID_ESTUDIO_OTRA_UNIV_DEST_NK': 11,
                'ID_CENTRO_OTRA_UNIV_DEST_NK': 11,
                'ID_UNIVERSIDAD_ORIGEN_NK': 11,
                'ID_ACUERDO_BILATERAL_NK': 11,
                'ID_PLAN_ESTUDIO_NK': 11,
                'ID_ASIGNATURA_NK': 11,
                'ID_PERSONA_NIP_NK': 11,
                'ID_CENTRO_NK': 11
            }
            
            # Determinar límite de longitud efectivo
            effective_max_length = max_length
            
            # Si tenemos mapeo específico, usar ese límite
            if column_name in known_column_limits:
                effective_max_length = known_column_limits[column_name]
                logger.debug(f"Aplicando límite específico para {column_name}: {effective_max_length} caracteres")
            elif max_length and pd.notna(max_length):
                effective_max_length = int(max_length)
            elif column_name.endswith('_NK'):
                # Para claves naturales sin límite definido, usar conservador
                effective_max_length = 20
            elif 'NOMBRE' in column_name.upper():
                # Para nombres sin límite definido
                effective_max_length = 200
            elif 'DESCRIPCION' in column_name.upper() or 'DESC' in column_name.upper():
                # Para descripciones sin límite definido
                effective_max_length = 500
            
            # Truncar según longitud máxima efectiva
            if effective_max_length and pd.notna(effective_max_length):
                max_len = int(effective_max_length)
                # Identificar valores que serán truncados
                mask_too_long = series_str.notna() & (series_str.str.len() > max_len)
                if mask_too_long.any():
                    count_truncated = mask_too_long.sum()
                    logger.info(f"🔧 Truncando {count_truncated} valores en {column_name} a {max_len} caracteres (preprocesamiento)")
                    series_str = series_str.str[:max_len]
                    
            logger.debug(f"Columna texto {column_name} limpiada: {series_str.isna().sum()} nulos")
            return series_str
            
        except Exception as e:
            logger.warning(f"Error procesando columna texto {column_name}: {e}")
            # Fallback: string vacío para NOT NULL, None para nullable
            if nullable in ('Y', 'YES'):
                return pd.Series([None] * len(series), dtype=object)
            else:
                return pd.Series([''] * len(series), dtype=str)
                
    def _clean_date_oracle(self, series, column_name, nullable):
        """Limpieza robusta de columnas de fecha para Oracle"""
        try:
            # Primero, detectar si ya son strings con formato de fecha
            if series.dtype == 'object':
                # Intentar parsear como fechas existentes en string
                sample_non_null = series.dropna().head(3)
                if not sample_non_null.empty:
                    sample_value = str(sample_non_null.iloc[0])
                    # Si ya tiene formato timestamp, solo limpiar
                    if ' ' in sample_value and ':' in sample_value and len(sample_value) > 15:
                        # Ya parece timestamp, limpiar valores problemáticos y convertir a formato Oracle simple
                        series_cleaned = series.replace({
                            'NaT': None, 'NaN': None, 'nan': None, 'null': None, 'NULL': None
                        })
                        
                        # Para Oracle, usar formato DATE simple sin hora para evitar problemas
                        # Convertir "YYYY-MM-DD HH:MM:SS" a "YYYY-MM-DD"
                        def clean_oracle_date(date_str):
                            if pd.isna(date_str) or date_str is None:
                                return None
                            try:
                                date_str = str(date_str)
                                if ' ' in date_str:
                                    # Extraer solo la parte de fecha
                                    return date_str.split(' ')[0]
                                return date_str
                            except:
                                return None
                        
                        series_cleaned = series_cleaned.apply(clean_oracle_date)
                        
                        if nullable in ('Y', 'YES'):
                            return series_cleaned
                        else:
                            return series_cleaned.fillna('2023-01-01')
            
            # Convertir a datetime con múltiples formatos
            series_dt = None
            
            # Intentar formatos comunes
            date_formats = [
                '%Y-%m-%d',           # 2023-01-15
                '%Y-%m-%d %H:%M:%S',  # 2023-01-15 10:30:00
                '%d/%m/%Y',           # 15/01/2023
                '%d-%m-%Y',           # 15-01-2023
                '%Y/%m/%d',           # 2023/01/15
            ]
            
            # Si es object, intentar diferentes formatos
            if series.dtype == 'object':
                for fmt in date_formats:
                    try:
                        series_dt = pd.to_datetime(series, format=fmt, errors='coerce')
                        if series_dt.notna().sum() > len(series) * 0.5:  # Si más del 50% se convierte bien
                            break
                    except:
                        continue
                        
            # Si no funcionó ningún formato específico, usar parsing automático
            if series_dt is None or series_dt.notna().sum() == 0:
                series_dt = pd.to_datetime(series, errors='coerce')
            
            # Manejar valores nulos y formatear para Oracle (solo fecha, sin hora)
            if nullable in ('Y', 'YES'):
                # Para columnas nullable, formatear fechas válidas y dejar None para inválidas
                series_formatted = series_dt.dt.strftime('%Y-%m-%d')
                series_formatted = series_formatted.replace('NaT', None)
                # Asegurar que los None se mantengan como None
                series_formatted = series_formatted.where(pd.notna(series_dt), None)
            else:
                # Para NOT NULL, usar fecha por defecto para valores inválidos
                default_date = pd.Timestamp('2023-01-01')
                series_dt = series_dt.fillna(default_date)
                series_formatted = series_dt.dt.strftime('%Y-%m-%d')
                
            logger.debug(f"Columna fecha {column_name} limpiada: {series_formatted.isna().sum() if hasattr(series_formatted, 'isna') else 0} nulos")
            return series_formatted
            
        except Exception as e:
            logger.warning(f"Error procesando columna fecha {column_name}: {e}")
            # Fallback robusto: fecha por defecto para NOT NULL, None para nullable
            fallback_date = '2023-01-01'
            if nullable in ('Y', 'YES'):
                return pd.Series([None] * len(series), dtype=object)
            else:
                return pd.Series([fallback_date] * len(series), dtype=str)
                
    def _clean_column_postgresql(self, series, column_name, data_type, max_length, precision, scale, nullable):
        """Limpieza específica para PostgreSQL (más permisivo que Oracle)"""
        # PostgreSQL es generalmente más permisivo, pero aplicamos limpieza básica
        series = self._clean_column_basic(series)
        
        data_type_upper = data_type.upper()
        
        if 'INTEGER' in data_type_upper or 'BIGINT' in data_type_upper or 'SMALLINT' in data_type_upper:
            series = pd.to_numeric(series, errors='coerce')
            if nullable not in ('Y', 'YES'):
                series = series.fillna(0)
                
        elif 'NUMERIC' in data_type_upper or 'DECIMAL' in data_type_upper:
            series = pd.to_numeric(series, errors='coerce')
            if nullable not in ('Y', 'YES'):
                series = series.fillna(0.0)
                
        elif 'VARCHAR' in data_type_upper or 'TEXT' in data_type_upper:
            series = series.astype(str)
            if max_length and pd.notna(max_length):
                max_len = int(max_length)
                series = series.str[:max_len]
            if nullable not in ('Y', 'YES'):
                series = series.fillna('')
                
        elif 'TIMESTAMP' in data_type_upper or 'DATE' in data_type_upper:
            series = pd.to_datetime(series, errors='coerce')
            if nullable not in ('Y', 'YES'):
                series = series.fillna(pd.Timestamp('2023-01-01'))
                
        return series
        
    def _basic_preprocessing(self, df):
        """Preprocessing básico y robusto cuando no hay metadatos de columnas"""
        df = df.copy()
        
        for col in df.columns:
            # 1. LIMPIEZA EXHAUSTIVA DE VALORES PROBLEMÁTICOS
            problematic_values = {
                np.nan: None, 'nan': None, 'NaN': None, 'NaT': None,
                'null': None, 'NULL': None, 'None': None,
                '': None, ' ': None, 'undefined': None,
                np.inf: None, -np.inf: None, 'inf': None, '-inf': None
            }
            df[col] = df[col].replace(problematic_values)
            
            # 2. PROCESAMIENTO POR TIPO DE DATOS DETECTADO
            col_dtype = str(df[col].dtype).lower()
            
            if 'datetime' in col_dtype or df[col].dtype == 'datetime64[ns]':
                # FECHAS: Convertir a formato Oracle/PostgreSQL
                if self.db_type == 'oracle':
                    df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S').replace('NaT', None)
                else:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    
            elif 'float' in col_dtype or 'int' in col_dtype:
                # NÚMEROS: Limpiar NaN y valores infinitos
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col] = df[col].replace({np.nan: None, np.inf: None, -np.inf: None})
                
                # Para Oracle, convertir enteros explícitamente
                if self.db_type == 'oracle' and 'int' in col_dtype:
                    df[col] = df[col].astype('Int64', errors='ignore')  # Permite nulos
                    
            elif 'object' in col_dtype or 'string' in col_dtype:
                # TEXTO: Limpieza de strings
                df[col] = df[col].astype(str)
                
                # Reemplazar representaciones de nulos como string
                null_strings = ['nan', 'NaN', 'NaT', 'None', 'null', 'NULL', 'undefined']
                for null_str in null_strings:
                    df[col] = df[col].replace(null_str, None)
                
                # Para Oracle, limitar longitud conservadoramente
                if self.db_type == 'oracle':
                    # Truncar strings muy largos para evitar ORA-12899
                    mask_too_long = df[col].notna() & (df[col].str.len() > 200)
                    if mask_too_long.any():
                        logger.info(f"Truncando {mask_too_long.sum()} valores largos en {col} (max: 200)")
                        df[col] = df[col].str[:200]
                        
            elif 'bool' in col_dtype:
                # BOOLEANOS: Convertir a 0/1 para Oracle
                if self.db_type == 'oracle':
                    df[col] = df[col].astype(int, errors='ignore')
                    
            else:
                # TIPO DESCONOCIDO: Intentar conversión a string segura
                logger.debug(f"Tipo desconocido para columna {col}: {col_dtype}")
                try:
                    df[col] = df[col].astype(str)
                    df[col] = df[col].replace('nan', None)
                except Exception as e:
                    logger.warning(f"No se pudo convertir columna {col}: {e}")
                    df[col] = None  # Última opción: toda la columna a None
                    
        logger.debug(f"Preprocessing básico completado: {len(df)} filas, {len(df.columns)} columnas")
        return df
        
    def upload_dataframe(self, df, table_name, batch_size=1000):
        """Carga un DataFrame a la base de datos con manejo robusto de errores"""
        if df.empty:
            logger.warning(f"DataFrame vacío para {table_name}")
            return True
            
        start_time = time.time()
        total_rows = len(df)
        self.stats['tables_processed'] += 1
        self.stats['total_rows'] += total_rows
        
        logger.info(f"📊 {table_name}: {total_rows} filas, batch={batch_size}")
        
        # Preprocesar DataFrame con manejo robusto
        try:
            df = self.preprocess_dataframe(df, table_name)
            logger.debug(f"DataFrame preprocesado para {table_name}: {len(df)} filas")
        except Exception as e:
            logger.error(f"Error en preprocesamiento de {table_name}: {e}")
            self.stats['tables_failed'] += 1
            return False
        
        # Preparar query de inserción
        columns = ', '.join(df.columns)
        placeholders = ', '.join(['?' for _ in df.columns])
        
        if self.db_type == 'oracle':
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        else:
            query = f"""
                INSERT INTO {table_name} ({columns}) 
                VALUES ({placeholders})
                ON CONFLICT DO NOTHING
            """
            
        # Configurar transacciones para Oracle
        if self.db_type == 'oracle':
            try:
                self.connection.jconn.setAutoCommit(False)
            except Exception as e:
                logger.debug(f"No se pudo desactivar autocommit: {e}")
        
        # Variables de control de errores mejoradas
        rows_processed = 0
        batch_errors = 0
        consecutive_errors = 0
        last_successful_batch = -1
        max_batch_errors = min(10, max(3, total_rows // batch_size // 4))  # Límite dinámico
        
        try:
            for i in range(0, total_rows, batch_size):
                batch_num = i // batch_size + 1
                batch = df.iloc[i:i+batch_size]
                
                try:
                    # Intentar inserción del batch
                    values = [tuple(row) for row in batch.values]
                    self.cursor.executemany(query, values)
                    
                    # Commit según tipo de BD
                    if self.db_type == 'oracle':
                        self.connection.jconn.commit()
                    else:
                        self.connection.commit()
                        
                    rows_processed += len(batch)
                    last_successful_batch = batch_num
                    consecutive_errors = 0  # Reset contador de errores consecutivos
                    
                    # Log progreso para tablas grandes
                    if total_rows > 1000 and batch_num % 5 == 0:
                        progress = (rows_processed / total_rows) * 100
                        logger.debug(f"{table_name} progreso: {progress:.1f}% ({rows_processed}/{total_rows})")
                    
                except Exception as e:
                    batch_errors += 1
                    consecutive_errors += 1
                    error_msg = str(e)
                    
                    # Diagnóstico detallado del error
                    error_type = self._diagnose_error(error_msg)
                    logger.error(f"Error batch {batch_num}/{(total_rows-1)//batch_size + 1} en {table_name} [{error_type}]: {error_msg}")
                    
                    # Intentar recovery según el tipo de error
                    recovery_attempted = False
                    if error_type in ['DATA_TYPE', 'LENGTH', 'NULL_CONSTRAINT', 'NAN_VALUE'] and not recovery_attempted:
                        recovery_success = self._attempt_batch_recovery(
                            batch, table_name, query, batch_num, error_type
                        )
                        if recovery_success:
                            rows_processed += len(batch)
                            last_successful_batch = batch_num
                            consecutive_errors = 0
                            logger.info(f"✅ Recovery exitoso para batch {batch_num} en {table_name}")
                            continue
                        else:
                            recovery_attempted = True
                    
                    # Rollback
                    try:
                        if self.db_type == 'oracle':
                            self.connection.jconn.rollback()
                        else:
                            self.connection.rollback()
                    except Exception as rollback_error:
                        logger.debug(f"Error en rollback: {rollback_error}")
                    
                    # Decidir si continuar o abortar
                    if consecutive_errors >= 3:
                        logger.error(f"Demasiados errores consecutivos en {table_name}, abortando")
                        break
                    elif batch_errors > max_batch_errors:
                        logger.error(f"Demasiados errores totales en {table_name} ({batch_errors}>{max_batch_errors}), abortando")
                        break
                        
            # Resultado final con estadísticas mejoradas
            elapsed = time.time() - start_time
            success_rate = (rows_processed / total_rows) * 100 if total_rows > 0 else 0
            success = batch_errors == 0 and rows_processed == total_rows
            
            if success:
                self.stats['tables_success'] += 1
                speed = rows_processed / elapsed if elapsed > 0 else 0
                logger.info(f"✅ {table_name}: {rows_processed} filas en {elapsed:.1f}s ({speed:.0f} filas/s)")
            else:
                self.stats['tables_failed'] += 1
                if rows_processed > 0:
                    logger.warning(f"⚠️  {table_name}: {batch_errors} errores, {rows_processed}/{total_rows} filas ({success_rate:.1f}%)")
                else:
                    logger.error(f"❌ {table_name}: {batch_errors} errores, {rows_processed}/{total_rows} filas")
                
            return success
            
        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = f"Error general en {table_name}: {e}"
            logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            self.stats['tables_failed'] += 1
            return False
            
        finally:
            # Reactivar autocommit para Oracle
            if self.db_type == 'oracle':
                try:
                    self.connection.jconn.setAutoCommit(True)
                except Exception as e:
                    logger.debug(f"No se pudo reactivar autocommit: {e}")
                    
    def _diagnose_error(self, error_msg):
        """Diagnostica el tipo de error para determinar estrategia de recovery"""
        error_msg_upper = error_msg.upper()
        
        if ('ORA-01858' in error_msg or 'SE HA ENCONTRADO UN CARÁCTER NO NUMÉRICO' in error_msg_upper or
            'ORA-01861' in error_msg or 'EL LITERAL NO COINCIDE CON LA CADENA DE FORMATO' in error_msg_upper):
            return 'DATA_TYPE'
        elif 'ORA-12899' in error_msg or 'EL VALOR ES DEMASIADO GRANDE' in error_msg_upper:
            return 'LENGTH'
        elif 'ORA-01400' in error_msg or 'NOT NULL' in error_msg_upper:
            return 'NULL_CONSTRAINT'
        elif 'NaN' in error_msg or 'ILLEGALARGUMENTEXCEPTION' in error_msg_upper:
            return 'NAN_VALUE'
        elif 'ORA-00001' in error_msg or 'UNIQUE CONSTRAINT' in error_msg_upper:
            return 'UNIQUE_CONSTRAINT'
        elif ('ORA-00904' in error_msg or 'IDENTIFICADOR NO VÁLIDO' in error_msg_upper or 
              'TABLE OR VIEW DOES NOT EXIST' in error_msg_upper or 'ORA-00942' in error_msg):
            return 'MISSING_COLUMN'
        else:
            return 'UNKNOWN'
            
    def _attempt_batch_recovery(self, batch, table_name, query, batch_num, error_type):
        """Intenta recuperar un batch con errores aplicando limpieza adicional"""
        try:
            logger.debug(f"Intentando recovery de batch {batch_num} en {table_name} por error {error_type}")
            
            # Clonar el batch para no modificar el original
            recovery_batch = batch.copy()
            
            # Aplicar limpieza adicional según el tipo de error
            if error_type == 'DATA_TYPE':
                # Limpieza robusta para problemas de tipos de datos y fechas
                for col in recovery_batch.columns:
                    # Limpiar valores problemáticos
                    recovery_batch[col] = recovery_batch[col].replace({
                        np.nan: None, np.inf: None, -np.inf: None,
                        'nan': None, 'NaN': None, 'inf': None, '-inf': None,
                        'NaT': None, 'undefined': None
                    })
                    
                    # Si parece ser una fecha, convertir conservadoramente
                    if recovery_batch[col].dtype == 'object':
                        # Intentar detectar si son fechas
                        sample_values = recovery_batch[col].dropna().head()
                        if not sample_values.empty:
                            first_value = str(sample_values.iloc[0])
                            if any(char in first_value for char in ['-', '/', ':', ' ']) and len(first_value) > 8:
                                # Parece fecha, convertir a formato estándar
                                try:
                                    recovery_batch[col] = pd.to_datetime(recovery_batch[col], errors='coerce')
                                    recovery_batch[col] = recovery_batch[col].dt.strftime('%Y-%m-%d %H:%M:%S')
                                    recovery_batch[col] = recovery_batch[col].replace('NaT', None)
                                    logger.debug(f"Columna {col} convertida a formato fecha estándar")
                                except:
                                    recovery_batch[col] = recovery_batch[col].astype(str).replace('nan', None)
                    
                    # Si es numérico, limpiar más agresivamente
                    elif recovery_batch[col].dtype in ['float64', 'float32']:
                        recovery_batch[col] = pd.to_numeric(recovery_batch[col], errors='coerce').replace({np.nan: None})
                        
            elif error_type == 'LENGTH':
                # Mapeo específico de columnas problemáticas conocidas y sus límites
                column_limits = {
                    'NOMBRE_CCAA': 30,
                    'ID_SITUACION_ADVA_NK': 2, 
                    'ID_DETALLE_CUPO_GENERAL_NK': 3,
                    'ID_PROYECTO_INVESTIGACION_NK': 30,
                    'ID_ESTUDIO_OTRA_UNIV_DEST_NK': 11,
                    'ID_CENTRO_OTRA_UNIV_DEST_NK': 11,
                    'ID_UNIVERSIDAD_ORIGEN_NK': 11,
                    'ID_ACUERDO_BILATERAL_NK': 11,
                    'ID_PLAN_ESTUDIO_NK': 11,
                    'ID_ASIGNATURA_NK': 11,
                    'ID_PERSONA_NIP_NK': 11,
                    'ID_CENTRO_NK': 11
                }
                
                # Truncar strings según límites conocidos o genéricos
                for col in recovery_batch.columns:
                    if recovery_batch[col].dtype == 'object':
                        # Obtener límite específico o usar genérico según patrón
                        max_length = None
                        
                        if col in column_limits:
                            max_length = column_limits[col]
                        elif col.endswith('_NK'):
                            # Para claves naturales, limitar a 20 caracteres por defecto
                            max_length = 20
                        elif 'NOMBRE' in col.upper():
                            # Para nombres, limitar a 200 caracteres por defecto
                            max_length = 200
                        elif 'DESCRIPCION' in col.upper() or 'DESC' in col.upper():
                            # Para descripciones, limitar a 500 caracteres
                            max_length = 500
                        else:
                            # Truncamiento conservador genérico
                            max_length = 50
                        
                        # Aplicar truncamiento
                        original_values = recovery_batch[col].astype(str)
                        mask_too_long = original_values.str.len() > max_length
                        if mask_too_long.any():
                            count_truncated = mask_too_long.sum()
                            logger.info(f"🔧 Truncando {count_truncated} valores en {col} a {max_length} caracteres")
                            recovery_batch[col] = original_values.str[:max_length]
                        
                        # Limpiar valores None/nan como string
                        recovery_batch[col] = recovery_batch[col].replace({
                            'None': None, 'nan': None, 'NaT': None, 'null': None, 'NULL': None
                        })
                        
            elif error_type == 'NULL_CONSTRAINT':
                # Rellenar valores nulos con defaults apropiados
                for col in recovery_batch.columns:
                    if recovery_batch[col].isna().any():
                        if recovery_batch[col].dtype in ['float64', 'int64', 'float32', 'int32']:
                            recovery_batch[col] = recovery_batch[col].fillna(0)
                        else:
                            recovery_batch[col] = recovery_batch[col].fillna('')
                            
            elif error_type == 'NAN_VALUE':
                # Limpieza exhaustiva para valores NaN
                for col in recovery_batch.columns:
                    # Reemplazar absolutamente todos los NaN y valores problemáticos
                    recovery_batch[col] = recovery_batch[col].replace({
                        np.nan: None, np.inf: None, -np.inf: None,
                        'nan': None, 'NaN': None, 'inf': None, '-inf': None,
                        'NaT': None, 'undefined': None, '': None
                    })
                    
                    # Para columnas numéricas, asegurar que no hay NaN residuales
                    if recovery_batch[col].dtype in ['float64', 'int64', 'float32', 'int32']:
                        # Convertir a nullable integer si es entero
                        if recovery_batch[col].dtype in ['int64', 'int32']:
                            recovery_batch[col] = recovery_batch[col].astype('Int64')
                        else:
                            # Para float, convertir NaN a None explícitamente
                            recovery_batch[col] = recovery_batch[col].where(pd.notna(recovery_batch[col]), None)
                    
                    # Para objetos, asegurar que no quedan strings 'nan'
                    elif recovery_batch[col].dtype == 'object':
                        mask_nan_strings = recovery_batch[col].astype(str).str.lower().isin(['nan', 'none', 'nat'])
                        recovery_batch.loc[mask_nan_strings, col] = None
                        
            elif error_type == 'MISSING_COLUMN':
                # Para columnas faltantes, intentar eliminar columnas problemáticas
                logger.warning(f"Detectado problema de columnas en {table_name}")
                # Este tipo de error generalmente requiere intervención manual
                # Por ahora, intentamos continuar sin hacer cambios
                pass
            
            # Validación final: asegurar que no hay NaN en ningún lugar
            for col in recovery_batch.columns:
                if recovery_batch[col].dtype in ['float64', 'float32']:
                    nan_count = recovery_batch[col].isna().sum()
                    if nan_count > 0:
                        recovery_batch[col] = recovery_batch[col].fillna(None)
                        logger.debug(f"Eliminados {nan_count} NaN residuales en {col}")
            
            # Intentar la inserción con los datos limpiados
            values = [tuple(row) for row in recovery_batch.values]
            self.cursor.executemany(query, values)
            
            if self.db_type == 'oracle':
                self.connection.jconn.commit()
            else:
                self.connection.commit()
                
            return True
            
        except Exception as recovery_error:
            logger.debug(f"Recovery falló para batch {batch_num}: {recovery_error}")
            try:
                if self.db_type == 'oracle':
                    self.connection.jconn.rollback()
                else:
                    self.connection.rollback()
            except:
                pass
            return False
        
    def upload_csv_file(self, csv_path, table_name, batch_size=1000):
        """Carga un archivo CSV a la base de datos"""
        try:
            logger.debug(f"Leyendo CSV: {csv_path}")
            df = pd.read_csv(csv_path)
            return self.upload_dataframe(df, table_name, batch_size)
        except Exception as e:
            error_msg = f"Error al leer {csv_path}: {e}"
            logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            return False
            
    def truncate_table(self, table_name):
        """Vacía una tabla"""
        try:
            # Desactivar autocommit para Oracle
            if self.db_type == 'oracle':
                self.connection.jconn.setAutoCommit(False)
            
            if self.db_type == 'oracle':
                # Para Oracle, usar DELETE si TRUNCATE falla
                try:
                    self.cursor.execute(f"TRUNCATE TABLE {table_name}")
                    self.connection.commit()
                except Exception as truncate_error:
                    logger.debug(f"TRUNCATE falló para {table_name}, intentando DELETE: {truncate_error}")
                    try:
                        self.cursor.execute(f"DELETE FROM {table_name}")
                        self.connection.commit()
                        logger.info(f"🗑️  {table_name} vaciada (DELETE)")
                        return
                    except Exception as delete_error:
                        logger.error(f"DELETE también falló para {table_name}: {delete_error}")
                        self.connection.rollback()
                        raise delete_error
            else:
                # PostgreSQL
                self.cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE")
                self.connection.commit()
                
            logger.info(f"🗑️  {table_name} vaciada (TRUNCATE)")
            
        except Exception as e:
            error_msg = str(e)
            if "ORA-00942" in error_msg or "no existe" in error_msg:
                logger.warning(f"Tabla {table_name} no existe, saltando...")
            else:
                logger.error(f"Error al vaciar {table_name}: {e}")
                try:
                    self.connection.rollback()
                except:
                    pass
            raise e
        finally:
            # Reactivar autocommit
            if self.db_type == 'oracle':
                try:
                    self.connection.jconn.setAutoCommit(True)
                except:
                    pass
            
    def truncate_all_tables(self, upload_order):
        """Trunca todas las tablas del DM en orden inverso (facts primero, luego dimensions)"""
        logger.info("🗑️  Iniciando truncado de todas las tablas del DM...")
        
        # Procesar en orden inverso: facts primero, luego dimensions
        categories_order = ['facts', 'dimensions_dependent', 'dimensions_basic']
        
        total_tables = sum(len(tables) for tables in upload_order.values())
        truncated = 0
        skipped = 0
        failed = 0
        
        for category in categories_order:
            if category not in upload_order:
                continue
                
            tables = upload_order[category]
            if not tables:
                continue
                
            logger.info(f"🗑️  Truncando {category.replace('_', ' ')}: {len(tables)} tablas")
            
            # Para facts y dimensions_dependent, truncar en orden inverso
            if category in ['facts', 'dimensions_dependent']:
                tables = list(reversed(tables))
            
            for table_name in tables:
                try:
                    self.truncate_table(table_name)
                    truncated += 1
                except Exception as e:
                    error_msg = str(e)
                    if "ORA-00942" in error_msg or "no existe" in error_msg:
                        skipped += 1
                        logger.debug(f"Tabla {table_name} no existe, continuando...")
                    else:
                        failed += 1
                        logger.error(f"Error crítico al truncar {table_name}: {e}")
                        
        # Resultado final más preciso
        logger.info(f"📊 Resultado del truncado:")
        logger.info(f"   ✅ Truncadas: {truncated}")
        logger.info(f"   ⏭️  Saltadas (no existen): {skipped}")
        logger.info(f"   ❌ Fallaron: {failed}")
        logger.info(f"   📈 Total procesadas: {truncated + skipped + failed}/{total_tables}")
        
        if failed > 0:
            logger.warning(f"⚠️  {failed} tablas no se pudieron truncar por errores")
            
        # Retornar true solo si no hubo errores críticos (fallos)
        return failed == 0
            
    def get_stats_summary(self):
        """Genera resumen compacto de estadísticas"""
        elapsed = datetime.now() - self.stats['start_time']
        
        summary = {
            'duration': f"{elapsed.total_seconds():.1f}s",
            'tables_total': self.stats['tables_processed'],
            'tables_success': self.stats['tables_success'],
            'tables_failed': self.stats['tables_failed'],
            'success_rate': f"{(self.stats['tables_success']/max(1,self.stats['tables_processed'])*100):.1f}%",
            'total_rows': self.stats['total_rows'],
            'avg_speed': f"{self.stats['total_rows']/max(1,elapsed.total_seconds()):.0f} filas/s",
            'errors_count': len(self.stats['errors'])
        }
        
        return summary
            
    def close(self):
        """Cierra la conexión y muestra estadísticas finales"""
        # Mostrar resumen compacto
        summary = self.get_stats_summary()
        
        logger.info("📈 Resumen final:")
        logger.info(f"   Duración: {summary['duration']}")
        logger.info(f"   Tablas: {summary['tables_success']}/{summary['tables_total']} ({summary['success_rate']})")
        logger.info(f"   Filas: {summary['total_rows']} ({summary['avg_speed']})")
        
        if summary['errors_count'] > 0:
            logger.warning(f"   Errores: {summary['errors_count']}")
            
        # Cerrar conexión
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("🔌 Conexión cerrada")

    def get_dm_tables_from_database(self):
        """Obtiene dinámicamente las tablas del DM académico desde la base de datos"""
        try:
            logger.info("🔍 Consultando tablas del DM académico en la base de datos...")
            
            if self.db_type == 'oracle':
                # Consultar tablas que empiecen con 'd_' o 'f_' del esquema actual
                user = os.getenv('ORACLE_USER', 'C##DM_ACADEMICO')
                query = """
                    SELECT table_name 
                    FROM all_tables 
                    WHERE owner = ? 
                    AND (table_name LIKE 'D_%' OR table_name LIKE 'F_%')
                    ORDER BY table_name
                """
                self.cursor.execute(query, [user.upper()])
                
            elif self.db_type == 'postgresql':
                # Consultar tablas que empiecen con 'd_' o 'f_' del esquema public
                query = """
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND (table_name LIKE 'd_%' OR table_name LIKE 'f_%')
                    ORDER BY table_name
                """
                self.cursor.execute(query)
                
            tables = [row[0].lower() for row in self.cursor.fetchall()]
            
            # Separar en categorías
            dimensions_basic = []
            dimensions_dependent = []
            facts = []
            
            # Tablas básicas (dimensiones que no dependen de otras)
            basic_patterns = [
                'd_sexo', 'd_pais', 'd_tiempo', 'd_curso_academico', 'd_curso_cohorte',
                'd_tipo_estudio', 'd_rama_conocimiento', 'd_calificacion', 'd_convocatoria',
                'd_tipo_acceso', 'd_categoria_cuerpo_pdi', 'd_dedicacion_profesor',
                'd_programa_movilidad', 'd_idioma_movilidad', 'd_tipo_beca', 'd_situacion_laboral'
            ]
            
            # Tablas dependientes (dimensiones que tienen FK a otras dimensiones)
            dependent_patterns = [
                'd_poblacion', 'd_campus', 'd_centro', 'd_universidad', 'd_estudio',
                'd_plan_estudio', 'd_asignatura', 'd_persona', 'd_profesor',
                'd_acuerdo_bilateral', 'd_empresa', 'd_proyecto_investigacion'
            ]
            
            for table in tables:
                if table.startswith('f_'):
                    facts.append(table)
                elif table in basic_patterns:
                    dimensions_basic.append(table)
                elif table in dependent_patterns:
                    dimensions_dependent.append(table)
                elif table.startswith('d_'):
                    # Si es una dimensión no clasificada, asumir que es básica
                    dimensions_basic.append(table)
            
            upload_order = {
                'dimensions_basic': dimensions_basic,
                'dimensions_dependent': dimensions_dependent,
                'facts': facts
            }
            
            # Log del resultado
            total_tables = len(tables)
            logger.info(f"📊 Tablas encontradas en el DM académico: {total_tables}")
            logger.info(f"   📋 Dimensiones básicas: {len(dimensions_basic)}")
            logger.info(f"   🔗 Dimensiones dependientes: {len(dimensions_dependent)}")
            logger.info(f"   📈 Tablas de hechos: {len(facts)}")
            
            if logger.isEnabledFor(logging.DEBUG):
                for category, tables_list in upload_order.items():
                    if tables_list:
                        logger.debug(f"{category}: {', '.join(tables_list)}")
            
            return upload_order
            
        except Exception as e:
            logger.error(f"Error al consultar tablas del DM: {e}")
            logger.warning("Usando configuración por defecto...")
            return get_default_upload_order()


def load_upload_config():
    """Carga la configuración de carga desde database.ini"""
    config_path = Path(__file__).parent / 'config' / 'database.ini'
    
    if not config_path.exists():
        logger.warning("database.ini no encontrado, usando configuración por defecto")
        return get_default_upload_order()
        
    try:
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        
        if 'upload_order' in config:
            upload_order = {}
            
            # Procesar cada categoría
            for key, value in config['upload_order'].items():
                # Dividir por comas y limpiar espacios/saltos de línea
                tables = [table.strip() for table in value.replace('\n', '').split(',') if table.strip()]
                upload_order[key] = tables
                logger.debug(f"Categoría {key}: {len(tables)} tablas")
                
            return upload_order
        else:
            logger.warning("Sección 'upload_order' no encontrada en database.ini")
            return get_default_upload_order()
            
    except Exception as e:
        logger.error(f"Error al leer database.ini: {e}")
        return get_default_upload_order()


def get_default_upload_order():
    """Retorna el orden por defecto de carga de tablas"""
    return {
        'dimensions_basic': [
            'd_sexo', 'd_pais', 'd_tiempo', 'd_curso_academico',
            'd_tipo_estudio', 'd_rama_conocimiento', 'd_calificacion'
        ],
        'dimensions_dependent': [
            'd_poblacion', 'd_centro', 'd_estudio', 'd_plan_estudio',
            'd_persona', 'd_asignatura'
        ],
        'facts': [
            'f_matricula', 'f_rendimiento', 'f_cohorte', 'f_egresado'
        ]
    }


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Carga datos usando JDBC')
    parser.add_argument('--db', choices=['oracle', 'postgresql'], 
                       default='oracle', help='Tipo de base de datos')
    parser.add_argument('--no-clean', action='store_true', 
                       help='NO vaciar tablas antes de cargar (por defecto sí se vacían)')
    parser.add_argument('--truncate-all', action='store_true',
                       help='Truncar TODAS las tablas del DM antes de cargar (alternativa a truncado individual)')
    parser.add_argument('--batch-size', type=int, default=1000,
                       help='Tamaño de lote para inserción')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO', help='Nivel de logging')
    parser.add_argument('--log-file', default='upload_db.log',
                       help='Archivo de log')
    
    args = parser.parse_args()
    
    # Configurar logging con parámetros
    global logger
    logger = setup_logging(args.log_level, args.log_file)
    
    if not JDBC_AVAILABLE:
        logger.error("JayDeBeApi no está disponible")
        logger.info("💡 pip install JayDeBeApi>=1.2.3")
        return 1
        
    # Validar directorio output
    output_dir = Path(__file__).parent / 'output'
    if not output_dir.exists():
        logger.error("Directorio output/ no encontrado")
        logger.info("💡 Ejecute primero: python main.py")
        return 1
        
    logger.info(f"🚀 Iniciando carga JDBC: {args.db.upper()}")
    logger.info(f"📂 Directorio: {output_dir}")
    logger.info(f"📝 Log: {args.log_file}")
    
    # Mostrar configuración de limpieza
    if args.no_clean:
        logger.info("🚫 Limpieza deshabilitada: se insertará sobre datos existentes")
    elif args.truncate_all:
        logger.info("🗑️  Se truncarán TODAS las tablas del DM antes de cargar")
    else:
        logger.info("🗑️  Se truncará cada tabla individualmente antes de cargar")
    
    # Inicializar uploader
    uploader = DatabaseUploader(args.db, args.log_level)
    
    try:
        # Conectar
        uploader.connect()
        
        # Obtener tablas dinámicamente desde la base de datos
        upload_order = uploader.get_dm_tables_from_database()
        
        # Truncar todas las tablas si se solicita
        if args.truncate_all:
            logger.info("🗑️  Truncando todas las tablas del DM...")
            if not uploader.truncate_all_tables(upload_order):
                logger.warning("⚠️  Algunas tablas no se pudieron truncar, continuando...")
        
        # Procesar cada categoría de tablas
        total_tables_to_process = 0
        for tables in upload_order.values():
            total_tables_to_process += len(tables)
        
        current_table = 0
        for category, tables in upload_order.items():
            if not tables:
                continue
                
            logger.info(f"📊 Procesando {category.replace('_', ' ')}: {len(tables)} tablas")
            
            for table_name in tables:
                current_table += 1
                
                # Determinar directorio según tipo de tabla
                if table_name.startswith('d_'):
                    csv_path = output_dir / 'dimensions' / f'{table_name}.csv'
                else:
                    csv_path = output_dir / 'facts' / f'{table_name}.csv'
                    
                if csv_path.exists():
                    logger.info(f"📋 [{current_table}/{total_tables_to_process}] Procesando {table_name}")
                    
                    # Truncar tabla individual si NO se usó --truncate-all Y NO se deshabilitó la limpieza
                    if not args.truncate_all and not args.no_clean:
                        try:
                            uploader.truncate_table(table_name)
                        except Exception as e:
                            logger.warning(f"No se pudo truncar {table_name}: {e}")
                    
                    # Cargar datos
                    uploader.upload_csv_file(csv_path, table_name, args.batch_size)
                else:
                    logger.warning(f"📋 [{current_table}/{total_tables_to_process}] Archivo no encontrado: {csv_path.name}")
                    
        # Mostrar estadísticas finales
        summary = uploader.get_stats_summary()
        
        if summary['tables_failed'] == 0:
            logger.info("🎉 ¡Carga completada exitosamente!")
            return 0
        else:
            logger.warning(f"⚠️  Carga completada con {summary['tables_failed']} fallos")
            return 1
            
    except Exception as e:
        logger.error(f"Error crítico: {e}")
        return 1
        
    finally:
        uploader.close()


if __name__ == "__main__":
    sys.exit(main()) 