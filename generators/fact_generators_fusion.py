import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker('es_ES')

def generate_f_tabla_fusion(n=100, dimension_dfs=None):
    """
    Genera datos para la tabla de hechos F_TABLA_FUSION
    
    Args:
        n (int): Número de registros a generar
        dimension_dfs (dict): Diccionario con DataFrames de dimensiones
    
    Returns:
        DataFrame: Datos generados para F_TABLA_FUSION
    """
    print(f"Generando {n} registros para F_TABLA_FUSION...")
    
    # Obtener datos de dimensiones necesarias
    curso_academico_df = dimension_dfs.get('d_curso_academico')
    plan_estudio_df = dimension_dfs.get('d_plan_estudio')
    
    # Crear lista para almacenar los datos
    data = []
    
    # Generar registros
    for _ in range(n):
        # Seleccionar valores de dimensiones aleatoriamente
        curso_academico = curso_academico_df.sample(n=1).iloc[0]
        plan_estudio = plan_estudio_df.sample(n=1).iloc[0]
        
        # Generar métricas
        tasa_exito_ponderada = round(random.uniform(0.5, 1.0), 4)
        tasa_rendimiento_ponderada = round(random.uniform(0.4, 0.95), 4)
        base_ponderacion_tasas_exito = random.randint(100, 5000)
        base_ponderacion_tasas_rto = random.randint(100, 5000)
        tasa_eficiencia_ponderada = round(random.uniform(0.6, 0.98), 4)
        base_ponderacion_tasas_egre = random.randint(50, 2000)
        alumnos_graduados = random.randint(5, 300)
        duracion_ponderada = round(random.uniform(3.5, 8.0), 2)
        base_ponderacion_duracion = random.randint(20, 400)
        alumnos_matriculados = random.randint(20, 800)
        alumnos_matriculados_ning = random.randint(5, 300)
        
        # Crear registro
        record = {
            'ID_CURSO_ACADEMICO': curso_academico['ID_CURSO_ACADEMICO'],
            'ID_PLAN_ESTUDIO': plan_estudio['ID_PLAN_ESTUDIO'],
            'TASA_EXITO_PONDERADA': tasa_exito_ponderada,
            'TASA_RENDIMIENTO_PONDERADA': tasa_rendimiento_ponderada,
            'BASE_PONDERACION_TASAS_EXITO': base_ponderacion_tasas_exito,
            'BASE_PONDERACION_TASAS_RTO': base_ponderacion_tasas_rto,
            'TASA_EFICIENCIA_PONDERADA': tasa_eficiencia_ponderada,
            'BASE_PONDERACION_TASAS_EGRE': base_ponderacion_tasas_egre,
            'ALUMNOS_GRADUADOS': alumnos_graduados,
            'DURACION_PONDERADA': duracion_ponderada,
            'BASE_PONDERACION_DURACION': base_ponderacion_duracion,
            'ALUMNOS_MATRICULADOS': alumnos_matriculados,
            'ALUMNOS_MATRICULADOS_NING': alumnos_matriculados_ning
        }
        
        data.append(record)
    
    # Crear DataFrame
    df = pd.DataFrame(data)
    
    # Asegurar que no haya duplicados en la clave primaria (ID_CURSO_ACADEMICO, ID_PLAN_ESTUDIO)
    df = df.drop_duplicates(subset=['ID_CURSO_ACADEMICO', 'ID_PLAN_ESTUDIO'])
    
    print(f"Generados {len(df)} registros únicos para F_TABLA_FUSION")
    return df

def generate_f_tabla_fusion_estcen(n=100, dimension_dfs=None):
    """
    Genera datos para la tabla de hechos F_TABLA_FUSION_ESTCEN
    
    Args:
        n (int): Número de registros a generar
        dimension_dfs (dict): Diccionario con DataFrames de dimensiones
    
    Returns:
        DataFrame: Datos generados para F_TABLA_FUSION_ESTCEN
    """
    print(f"Generando {n} registros para F_TABLA_FUSION_ESTCEN...")
    
    # Obtener datos de dimensiones necesarias
    curso_academico_df = dimension_dfs.get('d_curso_academico')
    estudio_df = dimension_dfs.get('d_estudio')
    centro_df = dimension_dfs.get('d_centro')
    tipo_estudio_df = dimension_dfs.get('d_tipo_estudio')
    rama_conocimiento_df = dimension_dfs.get('d_rama_conocimiento')
    
    # Crear lista para almacenar los datos
    data = []
    
    # Generar registros
    for _ in range(n):
        # Seleccionar valores de dimensiones aleatoriamente
        curso_academico = curso_academico_df.sample(n=1).iloc[0]
        estudio = estudio_df.sample(n=1).iloc[0]
        centro = centro_df.sample(n=1).iloc[0]
        tipo_estudio = tipo_estudio_df.sample(n=1).iloc[0]
        rama_conocimiento = rama_conocimiento_df.sample(n=1).iloc[0]
        
        # Generar métricas
        tasa_exito_ponderada = round(random.uniform(0.5, 1.0), 4)
        tasa_rendimiento_ponderada = round(random.uniform(0.4, 0.95), 4)
        base_ponderacion_tasas_exito = random.randint(100, 5000)
        base_ponderacion_tasas_rto = random.randint(100, 5000)
        alumnos_matriculados = random.randint(20, 800)
        alumnos_matriculados_ning = random.randint(5, 300)
        tasa_eficiencia_ponderada = round(random.uniform(0.6, 0.98), 4)
        base_ponderacion_tasas_egre = random.randint(50, 2000)
        alumnos_graduados = random.randint(5, 300)
        duracion_ponderada = round(random.uniform(3.5, 8.0), 2)
        base_ponderacion_duracion = random.randint(20, 400)
        doctorado_vigente = random.choice(['S', 'N'])
        doc_alumnos_informe = random.randint(0, 100)
        valoracion_alumnos = round(random.uniform(3.0, 5.0), 2)
        valoracion_profesores = round(random.uniform(3.5, 5.0), 2)
        doc_alumnos_beca = random.randint(0, 50)
        
        # Crear registro
        record = {
            'ID_CURSO_ACADEMICO': curso_academico['ID_CURSO_ACADEMICO'],
            'ID_ESTUDIO': estudio['ID_ESTUDIO'],
            'ID_CENTRO': centro['ID_CENTRO'],
            'TASA_EXITO_PONDERADA': tasa_exito_ponderada,
            'TASA_RENDIMIENTO_PONDERADA': tasa_rendimiento_ponderada,
            'BASE_PONDERACION_TASAS_EXITO': base_ponderacion_tasas_exito,
            'BASE_PONDERACION_TASAS_RTO': base_ponderacion_tasas_rto,
            'ALUMNOS_MATRICULADOS': alumnos_matriculados,
            'ALUMNOS_MATRICULADOS_NING': alumnos_matriculados_ning,
            'TASA_EFICIENCIA_PONDERADA': tasa_eficiencia_ponderada,
            'BASE_PONDERACION_TASAS_EGRE': base_ponderacion_tasas_egre,
            'ALUMNOS_GRADUADOS': alumnos_graduados,
            'DURACION_PONDERADA': duracion_ponderada,
            'BASE_PONDERACION_DURACION': base_ponderacion_duracion,
            'ID_TIPO_ESTUDIO': tipo_estudio['ID_TIPO_ESTUDIO'],
            'SN_DOCTORADO_VIGENTE': doctorado_vigente,
            'DOC_ALUMNOS_INFORME': doc_alumnos_informe,
            'VALORACION_ALUMNOS': valoracion_alumnos,
            'VALORACION_PROFESORES': valoracion_profesores,
            'DOC_ALUMNOS_BECA': doc_alumnos_beca,
            'ID_RAMA_CONOCIMIENTO': rama_conocimiento['ID_RAMA_CONOCIMIENTO']
        }
        
        data.append(record)
    
    # Crear DataFrame
    df = pd.DataFrame(data)
    
    # Asegurar que no haya duplicados en la clave primaria (ID_CURSO_ACADEMICO, ID_ESTUDIO, ID_CENTRO)
    df = df.drop_duplicates(subset=['ID_CURSO_ACADEMICO', 'ID_ESTUDIO', 'ID_CENTRO'])
    
    print(f"Generados {len(df)} registros únicos para F_TABLA_FUSION_ESTCEN")
    return df 