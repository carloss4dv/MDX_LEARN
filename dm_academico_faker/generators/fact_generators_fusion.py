import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker(['es_ES'])
Faker.seed(42)
random.seed(42)
np.random.seed(42)

def generate_f_tabla_fusion(n=100, dimension_dfs=None):
    """
    Genera datos para la tabla F_TABLA_FUSION con todos sus atributos
    
    Args:
        n (int): Número de filas a generar
        dimension_dfs (dict): Diccionario con DataFrames de dimensiones necesarias
        
    Returns:
        DataFrame: DataFrame con los datos generados para la tabla F_TABLA_FUSION
    """
    data = []
    
    # Verificar que se proporcionaron los DataFrames de dimensiones necesarias
    if dimension_dfs is None or not all(key in dimension_dfs for key in ['d_curso_academico', 'd_plan_estudio']):
        raise ValueError("Se requieren los DataFrames de las dimensiones: d_curso_academico, d_plan_estudio")
    
    # Obtener datos de las dimensiones
    curso_academico_df = dimension_dfs['d_curso_academico']
    plan_estudio_df = dimension_dfs['d_plan_estudio']
    
    # Crear combinaciones de curso académico y plan de estudio
    combinaciones = []
    cursos_id = curso_academico_df['ID_CURSO_ACADEMICO'].tolist()
    planes_id = plan_estudio_df['ID_PLAN_ESTUDIO'].tolist()
    
    # Asegurar que no hay más combinaciones que las solicitadas
    max_combinaciones = min(n, len(cursos_id) * len(planes_id))
    
    for _ in range(max_combinaciones):
        curso_id = np.random.choice(cursos_id)
        plan_id = np.random.choice(planes_id)
        combinacion = (curso_id, plan_id)
        
        # Evitar combinaciones duplicadas
        if combinacion not in combinaciones:
            combinaciones.append(combinacion)
    
    # Generar datos para cada combinación
    for curso_id, plan_id in combinaciones:
        # Generar valores base para las tasas y ponderaciones
        tasa_exito = round(random.uniform(0.60, 0.95), 4)
        tasa_rendimiento = round(random.uniform(0.55, 0.90), 4)
        tasa_eficiencia = round(random.uniform(0.70, 0.98), 4)
        
        base_ponderacion_exito = random.randint(100, 1000)
        base_ponderacion_rto = random.randint(100, 1000)
        base_ponderacion_egre = random.randint(50, 500)
        
        alumnos_graduados = random.randint(10, 200)
        alumnos_matriculados = random.randint(50, 500)
        alumnos_matriculados_ning = random.randint(10, 100)
        
        duracion_ponderada = round(random.uniform(3.5, 6.0), 2)
        base_ponderacion_duracion = alumnos_graduados
        
        # Crear registro
        registro = {
            'ID_CURSO_ACADEMICO': curso_id,
            'ID_PLAN_ESTUDIO': plan_id,
            'TASA_EXITO_PONDERADA': tasa_exito,
            'TASA_RENDIMIENTO_PONDERADA': tasa_rendimiento,
            'BASE_PONDERACION_TASAS_EXITO': base_ponderacion_exito,
            'BASE_PONDERACION_TASAS_RTO': base_ponderacion_rto,
            'TASA_EFICIENCIA_PONDERADA': tasa_eficiencia,
            'BASE_PONDERACION_TASAS_EGRE': base_ponderacion_egre,
            'ALUMNOS_GRADUADOS': alumnos_graduados,
            'DURACION_PONDERADA': duracion_ponderada,
            'BASE_PONDERACION_DURACION': base_ponderacion_duracion,
            'ALUMNOS_MATRICULADOS': alumnos_matriculados,
            'ALUMNOS_MATRICULADOS_NING': random.randint(0, 100),
        }
        
        data.append(registro)
    
    # Crear DataFrame
    df = pd.DataFrame(data)
    
    return df

def generate_f_tabla_fusion_estcen(n=100, dimension_dfs=None):
    """
    Genera datos para la tabla F_TABLA_FUSION_ESTCEN con todos sus atributos
    
    Args:
        n (int): Número de filas a generar
        dimension_dfs (dict): Diccionario con DataFrames de dimensiones necesarias
        
    Returns:
        DataFrame: DataFrame con los datos generados para la tabla F_TABLA_FUSION_ESTCEN
    """
    data = []
    
    # Verificar que se proporcionaron los DataFrames de dimensiones necesarias
    if dimension_dfs is None or not all(key in dimension_dfs for key in [
        'd_curso_academico', 'd_centro', 'd_estudio', 'd_tipo_estudio']):
        raise ValueError("Se requieren los DataFrames de las dimensiones: d_curso_academico, d_centro, d_estudio, d_tipo_estudio")
    
    # Obtener datos de las dimensiones
    curso_academico_df = dimension_dfs['d_curso_academico']
    centro_df = dimension_dfs['d_centro']
    estudio_df = dimension_dfs['d_estudio']
    tipo_estudio_df = dimension_dfs['d_tipo_estudio']
    
    # Crear combinaciones de curso académico, estudio y centro
    combinaciones = []
    cursos_id = curso_academico_df['ID_CURSO_ACADEMICO'].tolist()
    centros_id = centro_df['ID_CENTRO'].tolist()
    estudios_id = estudio_df['ID_ESTUDIO'].tolist()
    tipos_estudio_id = tipo_estudio_df['ID_TIPO_ESTUDIO'].tolist() if 'ID_TIPO_ESTUDIO' in tipo_estudio_df.columns else [1, 2, 3, 4, 5]
    
    # Asegurar que no hay más combinaciones que las solicitadas
    max_combinaciones = min(n, len(cursos_id) * len(centros_id) * len(estudios_id))
    
    for _ in range(max_combinaciones):
        curso_id = np.random.choice(cursos_id)
        centro_id = np.random.choice(centros_id)
        estudio_id = np.random.choice(estudios_id)
        combinacion = (curso_id, estudio_id, centro_id)
        
        # Evitar combinaciones duplicadas
        if combinacion not in combinaciones:
            combinaciones.append(combinacion)
    
    # Generar datos para cada combinación
    for curso_id, estudio_id, centro_id in combinaciones:
        # Generar valores base para las tasas y ponderaciones
        tasa_exito = round(random.uniform(0.60, 0.95), 4)
        tasa_rendimiento = round(random.uniform(0.55, 0.90), 4)
        tasa_eficiencia = round(random.uniform(0.70, 0.98), 4)
        
        base_ponderacion_exito = random.randint(100, 1000)
        base_ponderacion_rto = random.randint(100, 1000)
        base_ponderacion_egre = random.randint(50, 500)
        
        alumnos_graduados = random.randint(10, 200)
        alumnos_matriculados = random.randint(50, 500)
        alumnos_matriculados_ning = random.randint(10, 100)
        
        duracion_ponderada = round(random.uniform(3.5, 6.0), 2)
        base_ponderacion_duracion = alumnos_graduados
        
        tipo_estudio_id = np.random.choice(tipos_estudio_id)
        
        # Generar valores para doctorado (solo si es tipo estudio 3 - doctorado)
        sn_doctorado_vigente = 'S' if tipo_estudio_id == 3 else 'N'
        doc_alumnos_informe = random.randint(5, 50) if tipo_estudio_id == 3 else 0
        valoracion_alumnos = round(random.uniform(3.0, 5.0), 2) if tipo_estudio_id == 3 else 0
        valoracion_profesores = round(random.uniform(3.5, 5.0), 2) if tipo_estudio_id == 3 else 0
        doc_alumnos_beca = random.randint(1, 20) if tipo_estudio_id == 3 else 0
        
        # Crear registro
        registro = {
            'ID_CURSO_ACADEMICO': curso_id,
            'ID_ESTUDIO': estudio_id,
            'ID_CENTRO': centro_id,
            'TASA_EXITO_PONDERADA': tasa_exito,
            'TASA_RENDIMIENTO_PONDERADA': tasa_rendimiento,
            'BASE_PONDERACION_TASAS_EXITO': base_ponderacion_exito,
            'BASE_PONDERACION_TASAS_RTO': base_ponderacion_rto,
            'ALUMNOS_MATRICULADOS': alumnos_matriculados,
            'ALUMNOS_MATRICULADOS_NING': alumnos_matriculados_ning,
            'TASA_EFICIENCIA_PONDERADA': tasa_eficiencia,
            'BASE_PONDERACION_TASAS_EGRE': base_ponderacion_egre,
            'ALUMNOS_GRADUADOS': alumnos_graduados,
            'DURACION_PONDERADA': duracion_ponderada,
            'BASE_PONDERACION_DURACION': base_ponderacion_duracion,
            'ID_TIPO_ESTUDIO': tipo_estudio_id,
            'SN_DOCTORADO_VIGENTE': sn_doctorado_vigente,
            'DOC_ALUMNOS_INFORME': doc_alumnos_informe,
            'VALORACION_ALUMNOS': valoracion_alumnos,
            'VALORACION_PROFESORES': valoracion_profesores,
            'DOC_ALUMNOS_BECA': doc_alumnos_beca,
            'ID_RAMA_CONOCIMIENTO': random.randint(1, 5)
        }
        
        data.append(registro)
    
    # Crear DataFrame
    df = pd.DataFrame(data)
    
    return df 