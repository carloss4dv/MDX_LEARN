"""
Generadores extendidos de tablas de hechos principales

Este módulo contiene versiones extendidas de los generadores principales:
- extended_generate_f_matricula
- extended_generate_f_rendimiento
"""

import pandas as pd
import numpy as np
from tqdm import tqdm
import random
import datetime
from faker import Faker
from .date_helpers import generate_random_date
from generators.fact_generators import generate_f_matricula, generate_f_rendimiento

# Inicializar Faker con locale español
fake = Faker('es_ES')

def extended_generate_f_matricula(n=10000, dimension_dfs=None):
    """
    Versión extendida del generador de F_MATRICULA que incluye todos los campos faltantes
    
    Campos faltantes implementados:
    - FLG_EQUIVALENTE_TC_SIIU: Flag para equivalente a tiempo completo SIIU
    - ID_MODALIDAD_PLAN: ID de la modalidad del plan de estudios (presencial, semipresencial, etc)
    - FLG_MULTIPLE_TITULACION: Flag para titulaciones múltiples
    - FLG_DISCAPACIDAD: Flag para estudiantes con discapacidad
    - FLG_INTERUNIVERSITARIO: Flag para planes interuniversitarios
    - FLG_COORDINADOR: Flag para universidad coordinadora
    - ID_EDAD_EST: ID del rango de edad estandarizado
    - ID_TITULO_PREVIO_MASTER: ID del título previo para estudios de máster
    - ID_PLAN_ESTUDIO_ANO_DATOS: ID del plan de estudio para el año académico
    - SN_MASTER_HABILITANTE: Indicador S/N para máster habilitante
    - SN_MULTIPLE_TITULACION: Indicador S/N para titulación múltiple
    - SN_INTERUNIVERSITARIO: Indicador S/N para interuniversitario
    - SN_COORDINADOR: Indicador S/N para coordinador
    - ID_DETALLE_CUPO_GENERAL: ID del detalle del cupo general
    - ID_UNIVERSIDAD_ORIGEN: ID de la universidad de origen
    - ID_UNIVERSIDAD_ORIGEN_NK: NK de la universidad de origen
    - ID_PAIS_UNIVERSIDAD_ORIGEN: ID del país de la universidad de origen
    - ID_PAIS_UNIVERSIDAD_ORIGEN_NK: NK del país de la universidad de origen
    - FLG_ESTUDIANTE_INTERNACIONAL: Flag para estudiante internacional
    - SN_ESTUDIANTE_INTERNACIONAL: Indicador S/N para estudiante internacional
    - ID_PROGRAMA_MOVILIDAD_NK: NK del programa de movilidad
    - SN_PROGRAMA_INTERNACIONAL: Indicador S/N para programa internacional
    - COD_POSTAL_CURSO: Código postal durante el curso
    - COD_POSTAL_FAMILIAR: Código postal familiar
    - ID_PAIS_FAMILIAR: ID del país familiar
    - ID_PAIS_FAMILIAR_NK: NK del país familiar
    
    Args:
        n (int): Número de registros a generar
        dimension_dfs (dict): Diccionario con DataFrames de dimensiones
        
    Returns:
        DataFrame: DataFrame con los datos generados
    """
    # Generar el DataFrame base con la función original
    df_base = generate_f_matricula(n, dimension_dfs)
    
    # Verificar que se proporcionaron todos los DataFrames de dimensiones necesarios
    required_dims = [
        'd_modalidad_plan_estudio', 'd_edad_est', 'd_plan_estudio_ano_datos', 
        'd_detalle_cupo_general', 'd_universidad', 'd_programa_movilidad'
    ]
    
    if dimension_dfs is None or not all(key in dimension_dfs for key in required_dims):
        raise ValueError(f"Se deben proporcionar todos los DataFrames de dimensiones adicionales necesarios: {required_dims}")
    
    # Obtener datos de dimensiones adicionales
    d_modalidad_plan = dimension_dfs['d_modalidad_plan_estudio']
    d_edad_est = dimension_dfs['d_edad_est']
    d_plan_estudio_ano_datos = dimension_dfs['d_plan_estudio_ano_datos']
    d_detalle_cupo_general = dimension_dfs['d_detalle_cupo_general']
    d_universidad = dimension_dfs['d_universidad']
    d_programa_movilidad = dimension_dfs['d_programa_movilidad']
    
    # Para cada registro, añadir los campos faltantes
    for index, row in tqdm(df_base.iterrows(), total=len(df_base), desc="Añadiendo campos faltantes a F_MATRICULA"):
        # 1. Campos relacionados con flags y características del plan
        df_base.at[index, 'FLG_EQUIVALENTE_TC_SIIU'] = random.choice([0, 1])
        
        # 2. Modalidad del plan
        modalidad_plan = random.choice(d_modalidad_plan.to_dict('records'))
        df_base.at[index, 'ID_MODALIDAD_PLAN'] = modalidad_plan['ID_MODALIDAD_PLAN_ESTUDIO']
        df_base.at[index, 'ID_MODALIDAD_PLAN_NK'] = modalidad_plan['ID_MODALIDAD_PLAN_ESTUDIO_NK']
        
        # 3. Flags varios con sus correspondientes SN
        flg_multiple_titulacion = random.choice([0, 1])
        flg_discapacidad = random.choice([0, 1])
        flg_interuniversitario = random.choice([0, 1])
        flg_coordinador = random.choice([0, 1])
        
        df_base.at[index, 'FLG_MULTIPLE_TITULACION'] = flg_multiple_titulacion
        df_base.at[index, 'SN_MULTIPLE_TITULACION'] = 'S' if flg_multiple_titulacion else 'N'
        df_base.at[index, 'FLG_DISCAPACIDAD'] = flg_discapacidad
        df_base.at[index, 'SN_DISCAPACIDAD'] = 'S' if flg_discapacidad else 'N'
        df_base.at[index, 'FLG_INTERUNIVERSITARIO'] = flg_interuniversitario
        df_base.at[index, 'SN_INTERUNIVERSITARIO'] = 'S' if flg_interuniversitario else 'N'
        df_base.at[index, 'FLG_COORDINADOR'] = flg_coordinador
        df_base.at[index, 'SN_COORDINADOR'] = 'S' if flg_coordinador else 'N'
        
        # 4. Asignación de edad estandarizada
        edad_est = random.choice(d_edad_est.to_dict('records'))
        df_base.at[index, 'ID_EDAD_EST'] = edad_est['ID_EDAD_EST']
        
        # 5. Título previo para máster (sólo para tipo estudio máster)
        if random.random() < 0.3:  # 30% de probabilidad de tener un título previo
            df_base.at[index, 'ID_TITULO_PREVIO_MASTER'] = random.randint(1, 100)
            df_base.at[index, 'ID_TITULO_PREVIO_MASTER_NK'] = f"T{random.randint(10000, 99999)}"
        else:
            df_base.at[index, 'ID_TITULO_PREVIO_MASTER'] = None
            df_base.at[index, 'ID_TITULO_PREVIO_MASTER_NK'] = None
        
        # 6. Plan de estudio año datos
        plan_ano = random.choice(d_plan_estudio_ano_datos.to_dict('records'))
        df_base.at[index, 'ID_PLAN_ESTUDIO_ANO_DATOS'] = plan_ano['ID_PLAN_ESTUDIO_ANO_DATOS']
        
        # 7. Máster habilitante
        is_master_habilitante = random.choice([0, 1])
        df_base.at[index, 'SN_MASTER_HABILITANTE'] = 'S' if is_master_habilitante else 'N'
        
        # 8. Detalle cupo general
        detalle_cupo = random.choice(d_detalle_cupo_general.to_dict('records'))
        df_base.at[index, 'ID_DETALLE_CUPO_GENERAL'] = detalle_cupo['ID_DETALLE_CUPO_GENERAL']
        df_base.at[index, 'ID_DETALLE_CUPO_GENERAL_NK'] = detalle_cupo['ID_DETALLE_CUPO_GENERAL_NK']
        
        # 9. Universidad de origen (sólo para estudiantes en movilidad)
        if row['FLG_EN_PROGRAMA_MOVILIDAD'] == 1:
            universidad_origen = random.choice(d_universidad.to_dict('records'))
            df_base.at[index, 'ID_UNIVERSIDAD_ORIGEN'] = universidad_origen['ID_UNIVERSIDAD']
            df_base.at[index, 'ID_UNIVERSIDAD_ORIGEN_NK'] = universidad_origen['ID_UNIVERSIDAD_NK']
            df_base.at[index, 'ID_PAIS_UNIVERSIDAD_ORIGEN'] = universidad_origen['ID_PAIS']
            df_base.at[index, 'ID_PAIS_UNIVERSIDAD_ORIGEN_NK'] = universidad_origen['ID_PAIS_NK']
            
            # Programa de movilidad
            programa = random.choice(d_programa_movilidad.to_dict('records'))
            df_base.at[index, 'ID_PROGRAMA_MOVILIDAD_NK'] = programa.get('ID_PROGRAMA_MOVILIDAD_NK', random.randint(1, 100))
            df_base.at[index, 'SN_PROGRAMA_INTERNACIONAL'] = programa.get('SN_PROGRAMA_INTERNACIONAL', random.choice(['S', 'N']))
        else:
            df_base.at[index, 'ID_UNIVERSIDAD_ORIGEN'] = None
            df_base.at[index, 'ID_UNIVERSIDAD_ORIGEN_NK'] = None
            df_base.at[index, 'ID_PAIS_UNIVERSIDAD_ORIGEN'] = None
            df_base.at[index, 'ID_PAIS_UNIVERSIDAD_ORIGEN_NK'] = None
            df_base.at[index, 'ID_PROGRAMA_MOVILIDAD_NK'] = None
            df_base.at[index, 'SN_PROGRAMA_INTERNACIONAL'] = None
        
        # 10. Estudiante internacional
        flg_estudiante_internacional = random.choice([0, 1])
        df_base.at[index, 'FLG_ESTUDIANTE_INTERNACIONAL'] = flg_estudiante_internacional
        df_base.at[index, 'SN_ESTUDIANTE_INTERNACIONAL'] = 'S' if flg_estudiante_internacional else 'N'
        
        # 11. Códigos postales
        df_base.at[index, 'COD_POSTAL_CURSO'] = fake.postcode()
        df_base.at[index, 'COD_POSTAL_FAMILIAR'] = fake.postcode()
        
        # 12. País familiar (puede ser el mismo que el de nacionalidad u otro)
        if random.random() < 0.8:  # 80% de probabilidad de tener el mismo país
            df_base.at[index, 'ID_PAIS_FAMILIAR'] = row['ID_PAIS_NACIONALIDAD']
            pais_familiar_nk = dimension_dfs['d_pais'][dimension_dfs['d_pais']['ID_PAIS'] == row['ID_PAIS_NACIONALIDAD']]['ID_PAIS_NK'].values[0]
            df_base.at[index, 'ID_PAIS_FAMILIAR_NK'] = pais_familiar_nk
        else:
            pais_familiar = random.choice(dimension_dfs['d_pais'].to_dict('records'))
            df_base.at[index, 'ID_PAIS_FAMILIAR'] = pais_familiar['ID_PAIS']
            df_base.at[index, 'ID_PAIS_FAMILIAR_NK'] = pais_familiar['ID_PAIS_NK']
    
    return df_base

def extended_generate_f_rendimiento(n=20000, dimension_dfs=None):
    """
    Versión extendida del generador de F_RENDIMIENTO que incluye todos los campos faltantes
    
    Campos faltantes implementados:
    - FLG_COMPENSADA: Flag para asignatura compensada
    - SN_COMPENSADA: Indicador S/N para asignatura compensada
    - ID_EDAD_EST: ID del rango de edad estandarizado
    - FLG_EN_PROGRAMA_MOVILIDAD: Flag para estudiante en programa de movilidad
    - SN_PROG_MOVILIDAD: Indicador S/N para estudiante en programa de movilidad
    - ORDEN_BOE_PLAN: Orden en el BOE del plan de estudios
    - SN_DOCTORADO_VIGENTE: Indicador S/N para doctorado vigente
    - ID_PLAN_GRUPO_MATRICULA: ID del grupo de matrícula
    - ID_PLAN_GRUPO_MATRICULA_NK: NK del grupo de matrícula
    - ID_CENTRO_IMPARTICION: ID del centro de impartición
    - ID_CENTRO_IMPARTICION_NK: NK del centro de impartición
    - SN_MOVILIDAD_IN: Indicador S/N para movilidad entrante
    - FLG_MOVILIDAD_IN: Flag para movilidad entrante
    - ID_RANGO_NOTA_EGRACONS: ID del rango de nota EGRACONS
    - ID_ESTUDIO_NK: NK del estudio
    - ID_PLAN_ESTUDIO_NK: NK del plan de estudio
    - ID_ASIGNATURA_NK: NK de la asignatura
    - ID_PAIS_FAMILIAR: ID del país familiar
    - ID_PAIS_FAMILIAR_NK: NK del país familiar
    
    Args:
        n (int): Número de registros a generar
        dimension_dfs (dict): Diccionario con DataFrames de dimensiones
        
    Returns:
        DataFrame: DataFrame con los datos generados
    """
    # Generar el DataFrame base con la función original
    df_base = generate_f_rendimiento(n, dimension_dfs)
    
    # Verificar que se proporcionaron todos los DataFrames de dimensiones necesarios
    required_dims = [
        'd_edad_est', 'd_rango_nota_egracons', 'd_estudio', 'd_centro'
    ]
    
    if dimension_dfs is None or not all(key in dimension_dfs for key in required_dims):
        raise ValueError(f"Se deben proporcionar todos los DataFrames de dimensiones adicionales necesarios: {required_dims}")
    
    # Obtener datos de dimensiones adicionales
    d_edad_est = dimension_dfs['d_edad_est']
    d_rango_nota_egracons = dimension_dfs['d_rango_nota_egracons']
    d_estudio = dimension_dfs['d_estudio']
    
    # Para cada registro, añadir los campos faltantes
    for index, row in tqdm(df_base.iterrows(), total=len(df_base), desc="Añadiendo campos faltantes a F_RENDIMIENTO"):
        # 1. Asignatura compensada
        flg_compensada = random.choice([0, 1]) if row['NOTA_NUMERICA'] >= 4.0 and row['NOTA_NUMERICA'] < 5.0 else 0
        df_base.at[index, 'FLG_COMPENSADA'] = flg_compensada
        df_base.at[index, 'SN_COMPENSADA'] = 'S' if flg_compensada else 'N'
        
        # 2. Asignación de edad estandarizada
        edad_est = random.choice(d_edad_est.to_dict('records'))
        df_base.at[index, 'ID_EDAD_EST'] = edad_est['ID_EDAD_EST']
        
        # 3. Estudiante en programa de movilidad
        flg_en_programa_movilidad = random.choice([0, 1])
        df_base.at[index, 'FLG_EN_PROGRAMA_MOVILIDAD'] = flg_en_programa_movilidad
        df_base.at[index, 'SN_PROG_MOVILIDAD'] = 'S' if flg_en_programa_movilidad else 'N'
        
        # 4. Orden BOE del plan
        df_base.at[index, 'ORDEN_BOE_PLAN'] = f"{random.randint(1000, 9999)}/{random.randint(2010, 2022)}"
        
        # 5. Doctorado vigente
        sn_doctorado_vigente = random.choice(['S', 'N'])
        df_base.at[index, 'SN_DOCTORADO_VIGENTE'] = sn_doctorado_vigente
        
        # 6. Grupo de matrícula
        plan_grupo_matricula_id = random.randint(1, 1000)
        df_base.at[index, 'ID_PLAN_GRUPO_MATRICULA'] = plan_grupo_matricula_id
        df_base.at[index, 'ID_PLAN_GRUPO_MATRICULA_NK'] = plan_grupo_matricula_id
        
        # 7. Centro de impartición (puede ser distinto del centro del plan)
        if random.random() < 0.7:  # 70% de probabilidad de ser el mismo centro
            df_base.at[index, 'ID_CENTRO_IMPARTICION'] = row['ID_CENTRO']
            centro_nk = dimension_dfs['d_centro'][dimension_dfs['d_centro']['ID_CENTRO'] == row['ID_CENTRO']]['ID_CENTRO_NK'].values[0]
            df_base.at[index, 'ID_CENTRO_IMPARTICION_NK'] = centro_nk
        else:
            centro_imp = random.choice(dimension_dfs['d_centro'].to_dict('records'))
            df_base.at[index, 'ID_CENTRO_IMPARTICION'] = centro_imp['ID_CENTRO']
            df_base.at[index, 'ID_CENTRO_IMPARTICION_NK'] = centro_imp['ID_CENTRO_NK']
        
        # 8. Movilidad entrante
        flg_movilidad_in = random.choice([0, 1])
        df_base.at[index, 'FLG_MOVILIDAD_IN'] = flg_movilidad_in
        df_base.at[index, 'SN_MOVILIDAD_IN'] = 'S' if flg_movilidad_in else 'N'
        
        # 9. Rango nota EGRACONS
        egracons = random.choice(d_rango_nota_egracons.to_dict('records'))
        df_base.at[index, 'ID_RANGO_NOTA_EGRACONS'] = egracons['ID_RANGO_NOTA_EGRACONS']
        
        # 10. IDs naturales
        estudio = random.choice(d_estudio.to_dict('records'))
        df_base.at[index, 'ID_ESTUDIO_NK'] = estudio['ID_ESTUDIO_NK']
        
        # Plan estudio NK
        plan_nk = dimension_dfs['d_plan_estudio'][dimension_dfs['d_plan_estudio']['ID_PLAN_ESTUDIO'] == row['ID_PLAN_ESTUDIO']]['ID_PLAN_ESTUDIO_NK'].values[0]
        df_base.at[index, 'ID_PLAN_ESTUDIO_NK'] = plan_nk
        
        # Asignatura NK
        asig_nk = dimension_dfs['d_asignatura'][dimension_dfs['d_asignatura']['ID_ASIGNATURA'] == row['ID_ASIGNATURA']]['ID_ASIGNATURA_NK'].values[0]
        df_base.at[index, 'ID_ASIGNATURA_NK'] = asig_nk
        
        # 11. País familiar
        if random.random() < 0.8:  # 80% de probabilidad de tener el mismo país
            df_base.at[index, 'ID_PAIS_FAMILIAR'] = row['ID_PAIS_NACIONALIDAD']
            pais_familiar_nk = dimension_dfs['d_pais'][dimension_dfs['d_pais']['ID_PAIS'] == row['ID_PAIS_NACIONALIDAD']]['ID_PAIS_NK'].values[0]
            df_base.at[index, 'ID_PAIS_FAMILIAR_NK'] = pais_familiar_nk
        else:
            pais_familiar = random.choice(dimension_dfs['d_pais'].to_dict('records'))
            df_base.at[index, 'ID_PAIS_FAMILIAR'] = pais_familiar['ID_PAIS']
            df_base.at[index, 'ID_PAIS_FAMILIAR_NK'] = pais_familiar['ID_PAIS_NK']
    
    return df_base 