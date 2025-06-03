"""
Generadores de tablas de hechos de movilidad del Data Mart Académico

Este módulo contiene funciones para generar datos de hechos relacionados con movilidad:
- F_ESTUDIANTES_MOVILIDAD_IN
- F_ESTUDIANTES_MOVILIDAD_OUT  
- F_SOLICITUDES_MOVILIDAD
"""

import pandas as pd
import numpy as np
from tqdm import tqdm
import random
import datetime
from faker import Faker
from .date_helpers import generate_random_date

# Inicializar Faker con locale español
fake = Faker('es_ES')

def generate_f_estudiantes_movilidad_in(n=200, dimension_dfs=None):
    """Genera datos para la tabla F_ESTUDIANTES_MOVILIDAD_IN"""
    data = []
    
    # Verificar que se proporcionaron los DataFrames de dimensiones necesarios
    if dimension_dfs is None or not all(key in dimension_dfs for key in [
        'd_curso_academico', 'd_centro', 'd_plan_estudio', 'd_tipo_estudio',
        'd_universidad', 'd_pais', 'd_rango_credito', 'd_sexo',
        'd_estudio', 'd_rama_conocimiento', 'd_programa_movilidad', 'd_edad_est'
    ]):
        raise ValueError("Se deben proporcionar todos los DataFrames de dimensiones necesarios")
    
    # Obtener datos de dimensiones
    d_curso = dimension_dfs['d_curso_academico']
    d_centro = dimension_dfs['d_centro']
    d_plan_estudio = dimension_dfs['d_plan_estudio']
    d_tipo_estudio = dimension_dfs['d_tipo_estudio']
    d_universidad = dimension_dfs['d_universidad']
    d_pais = dimension_dfs['d_pais']
    d_rango_credito = dimension_dfs['d_rango_credito']
    d_sexo = dimension_dfs['d_sexo']
    d_estudio = dimension_dfs['d_estudio']
    d_rama_conocimiento = dimension_dfs['d_rama_conocimiento']
    d_programa_movilidad = dimension_dfs['d_programa_movilidad']
    d_edad_est = dimension_dfs['d_edad_est']
    
    # Generar datos de estudiantes de movilidad entrante
    for i in tqdm(range(1, n+1), desc="Generando estudiantes de movilidad entrante"):
        # Generar IDs base
        id_expediente_academico_nk = 200000 + i
        id_expediente_academico = 300000 + i
        id_alumno_nip_nk = 400000 + i
        id_alumno = 500000 + i
        
        # Seleccionar valores aleatorios de las dimensiones
        curso = random.choice(d_curso.to_dict('records'))
        centro = random.choice(d_centro.to_dict('records'))
        plan_estudio = random.choice(d_plan_estudio.to_dict('records'))
        tipo_estudio = random.choice(d_tipo_estudio.to_dict('records'))
        universidad_origen = random.choice(d_universidad.to_dict('records'))
        pais_universidad = random.choice(d_pais.to_dict('records'))
        tutor = random.randint(1, 1000)  # ID de tutor aleatorio
        rango_cred_superados = random.choice(d_rango_credito.to_dict('records'))
        sexo = random.choice(d_sexo.to_dict('records'))
        nacionalidad = random.choice(d_pais.to_dict('records'))
        estudio = random.choice(d_estudio.to_dict('records'))
        rama_conocimiento = random.choice(d_rama_conocimiento.to_dict('records'))
        programa_movilidad = random.choice(d_programa_movilidad.to_dict('records'))
        edad_est = random.choice(d_edad_est.to_dict('records'))
        plan_estudio_max = random.choice(d_plan_estudio.to_dict('records'))
        
        # Generar fechas de inicio y fin de estancia
        fecha_inicio = generate_random_date(2021, 2022)
        fecha_fin = generate_random_date(2022, 2023)
        
        # Calcular la duración de la estancia en meses
        inicio_dt = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fin_dt = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d')
        duracion_estancia = int((fin_dt - inicio_dt).days / 30)  # aproximación en meses
        
        # Edad del alumno entre 18 y 30 años
        edad = random.randint(18, 30)
        
        # Créditos
        creditos_matriculados = random.randint(10, 60)
        creditos_superados = random.randint(0, creditos_matriculados)
        
        # Centro de impartición (puede ser diferente del centro principal)
        if random.random() < 0.3:  # 30% de probabilidad de ser diferente
            centro_imparticion = random.choice(d_centro.to_dict('records'))
            id_centro_imparticion = centro_imparticion['ID_CENTRO']
            id_centro_imparticion_nk = centro_imparticion['ID_CENTRO_NK'] if 'ID_CENTRO_NK' in centro_imparticion else None
        else:
            id_centro_imparticion = centro['ID_CENTRO']
            id_centro_imparticion_nk = centro['ID_CENTRO_NK'] if 'ID_CENTRO_NK' in centro else None
        
        # Crear el registro para el estudiante de movilidad entrante
        data.append({
            'ID_CURSO_ACADEMICO_NK': curso['ID_CURSO_ACADEMICO_NK'],  # TODO: Usar valores válidos de D_CURSO_COHORTE,
            'ID_EXPEDIENTE_ACADEMICO_NK': id_expediente_academico_nk,
            'ID_ALUMNO_NIP_NK': id_alumno_nip_nk,
            'ID_CURSO_ACADEMICO': curso['ID_CURSO_ACADEMICO'],
            'ID_EXPEDIENTE_ACADEMICO': id_expediente_academico,
            'ID_ALUMNO': id_alumno,
            'ID_CENTRO': centro['ID_CENTRO'],
            'ID_PLAN_ESTUDIO': plan_estudio['ID_PLAN_ESTUDIO'],  # TODO: Usar valores válidos de F_TABLA_FUSION,
            'ID_TIPO_ESTUDIO': tipo_estudio['ID_TIPO_ESTUDIO'],
            'ID_UNIVERSIDAD_ORIGEN': universidad_origen['ID_UNIVERSIDAD'],
            'ID_PAIS_UNIVERSIDAD_ORIGEN': pais_universidad['ID_PAIS'],
            'ID_TUTOR': tutor,
            'ID_RANGO_CRED_SUPERADOS': rango_cred_superados['ID_RANGO_CREDITO'],
            'ID_FECHA_INICIO_ESTANCIA': int(fecha_inicio.replace('-', '')),
            'ID_FECHA_FIN_ESTANCIA': int(fecha_fin.replace('-', '')),
            'ID_SEXO': sexo['ID_SEXO'],
            'ID_PAIS_NACIONALIDAD': nacionalidad['ID_PAIS'],
            'EDAD': edad,
            'CREDITOS_SUPERA_DESTINO': creditos_superados,
            'DURACION_ESTANCIA': duracion_estancia,
            'FECHA_CARGA': generate_random_date(2022, 2023),
            'ID_PROGRAMA_MOVILIDAD_NK': programa_movilidad['ID_PROGRAMA_MOVILIDAD_NK'] if 'ID_PROGRAMA_MOVILIDAD_NK' in programa_movilidad else None,
            'ID_PROGRAMA_MOVILIDAD': programa_movilidad['ID_PROGRAMA_MOVILIDAD'],
            'ID_ESTUDIO': estudio['ID_ESTUDIO'],
            'ID_RAMA_CONOCIMIENTO': rama_conocimiento['ID_RAMA_CONOCIMIENTO'],
            'ID_FECHA_CARGA': int(generate_random_date(2022, 2023).replace('-', '')),
            'CREDITOS_MATRICULADOS': creditos_matriculados,
            'ID_CENTRO_NK': centro['ID_CENTRO_NK'] if 'ID_CENTRO_NK' in centro else None  # TODO: Usar valores válidos de D_CENTRO,
            'ID_CENTRO_IMPARTICION': id_centro_imparticion,
            'ID_CENTRO_IMPARTICION_NK': id_centro_imparticion_nk,
            'ID_EDAD_EST': edad_est['ID_EDAD_EST'],
            'ID_PLAN_ESTUDIO_MAX': plan_estudio_max['ID_PLAN_ESTUDIO']
        })
    
    return pd.DataFrame(data)

def generate_f_estudiantes_movilidad_out(n=300, dimension_dfs=None):
    """Genera datos para la tabla F_ESTUDIANTES_MOVILIDAD_OUT"""
    data = []
    
    # Lista de dimensiones requeridas
    required_dimensions = [
        'd_curso_academico', 'd_centro', 'd_plan_estudio', 'd_tipo_estudio',
        'd_universidad', 'd_pais', 'd_area_estudios_movilidad', 'd_nivel_estudios_movilidad',
        'd_tipo_acceso', 'd_rango_credito', 'd_sexo', 'd_rango_nota_admision', 
        'd_poblacion', 'd_programa_movilidad', 'd_estudio', 'd_rama_conocimiento', 'd_edad_est'
    ]
    
    # Verificar que se proporcionaron los DataFrames de dimensiones necesarios
    if dimension_dfs is None:
        raise ValueError("No se proporcionó el diccionario de DataFrames")
    
    # Comprobar cada dimensión requerida y mostrar las que faltan
    missing_dimensions = [dim for dim in required_dimensions if dim not in dimension_dfs]
    if missing_dimensions:
        raise ValueError(f"Faltan las siguientes dimensiones: {', '.join(missing_dimensions)}")
    
    # Obtener datos de dimensiones
    d_curso = dimension_dfs['d_curso_academico']
    d_centro = dimension_dfs['d_centro']
    d_plan_estudio = dimension_dfs['d_plan_estudio']
    d_tipo_estudio = dimension_dfs['d_tipo_estudio']
    d_universidad = dimension_dfs['d_universidad']
    d_pais = dimension_dfs['d_pais']
    d_area_estudios = dimension_dfs['d_area_estudios_movilidad']
    d_nivel_estudios = dimension_dfs['d_nivel_estudios_movilidad']
    d_tipo_acceso = dimension_dfs['d_tipo_acceso']
    d_rango_credito = dimension_dfs['d_rango_credito']
    d_sexo = dimension_dfs['d_sexo']
    d_rango_nota = dimension_dfs['d_rango_nota_admision']
    d_poblacion = dimension_dfs['d_poblacion']
    d_programa_movilidad = dimension_dfs['d_programa_movilidad']
    d_estudio = dimension_dfs['d_estudio']
    d_rama_conocimiento = dimension_dfs['d_rama_conocimiento']
    d_edad_est = dimension_dfs['d_edad_est']
    
    # Generar datos de estudiantes de movilidad saliente
    for i in tqdm(range(1, n+1), desc="Generando estudiantes de movilidad saliente"):
        # Generar IDs base
        id_expediente_academico_nk = 600000 + i
        id_expediente_academico = 700000 + i
        id_alumno_nip_nk = 800000 + i
        id_alumno = 900000 + i
        id_solicitud_movilidad_nk = 1000000 + i
        
        # Seleccionar valores aleatorios de las dimensiones
        curso = random.choice(d_curso.to_dict('records'))
        centro = random.choice(d_centro.to_dict('records'))
        plan_estudio = random.choice(d_plan_estudio.to_dict('records'))
        tipo_estudio = random.choice(d_tipo_estudio.to_dict('records'))
        universidad_destino = random.choice(d_universidad.to_dict('records'))
        pais_universidad = random.choice(d_pais.to_dict('records'))
        area_estudios = random.choice(d_area_estudios.to_dict('records'))
        nivel_estudios = random.choice(d_nivel_estudios.to_dict('records'))
        tipo_acceso = random.choice(d_tipo_acceso.to_dict('records'))
        rango_cred_superados = random.choice(d_rango_credito.to_dict('records'))
        rango_cred_superados_previo = random.choice(d_rango_credito.to_dict('records'))
        sexo = random.choice(d_sexo.to_dict('records'))
        rango_nota_admision = random.choice(d_rango_nota.to_dict('records'))
        nacionalidad = random.choice(d_pais.to_dict('records'))
        poblacion_familiar = random.choice(d_poblacion.to_dict('records'))
        programa_movilidad = random.choice(d_programa_movilidad.to_dict('records'))
        estudio = random.choice(d_estudio.to_dict('records'))
        rama_conocimiento = random.choice(d_rama_conocimiento.to_dict('records'))
        edad_est = random.choice(d_edad_est.to_dict('records'))
        
        # Tutor aleatorio
        tutor = random.randint(1, 1000)
        
        # Generar fechas de inicio y fin de estancia
        fecha_inicio = generate_random_date(2021, 2022)
        fecha_fin = generate_random_date(2022, 2023)
        
        # Calcular la duración de la estancia en meses
        inicio_dt = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fin_dt = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d')
        duracion_estancia = int((fin_dt - inicio_dt).days / 30)  # aproximación en meses
        
        # Edad del alumno entre 18 y 30 años
        edad = random.randint(18, 30)
        
        # Orden de preferencia (1-5)
        orden_preferencia = random.randint(1, 5)
        
        # Flag de acceso directo a movilidad
        flg_acceso_directo_movilidad = random.choice(['S', 'N'])
        flg_num_acceso_directo_movi = 1 if flg_acceso_directo_movilidad == 'S' else 0
        
        # Datos de rendimiento y estancia
        anos_cursados = random.randint(1, 4)
        curso_mas_alto_matriculado = random.randint(1, 4)
        creditos_superados_previo = random.randint(30, 180)
        creditos_supera_destino = random.randint(10, 60)
        
        # Nota de admisión
        nota_admision = round(random.uniform(5, 14), 2)
        
        # Crear el registro para el estudiante de movilidad saliente
        data.append({
            'ID_CURSO_ACADEMICO_NK': curso['ID_CURSO_ACADEMICO_NK'], # TODO: Usar valores válidos de D_CURSO_COHORTE,
            'ID_EXPEDIENTE_ACADEMICO_NK': id_expediente_academico_nk,
            'ID_ALUMNO_NIP_NK': id_alumno_nip_nk,
            'ID_SOLICITUD_MOVILIDAD_NK': id_solicitud_movilidad_nk,
            'ID_CURSO_ACADEMICO': curso['ID_CURSO_ACADEMICO'],
            'ID_EXPEDIENTE_ACADEMICO': id_expediente_academico,
            'ID_ALUMNO': id_alumno,
            'ID_CENTRO': centro['ID_CENTRO'],
            'ID_PLAN_ESTUDIO': plan_estudio['ID_PLAN_ESTUDIO'],  # TODO: Usar valores válidos de F_TABLA_FUSION,
            'ID_TIPO_ESTUDIO': tipo_estudio['ID_TIPO_ESTUDIO'],
            'ID_UNIVERSIDAD_DESTINO': universidad_destino['ID_UNIVERSIDAD'],
            'ID_PAIS_UNIVERSIDAD_DESTINO': pais_universidad['ID_PAIS'],
            'ID_TUTOR': tutor,
            'ID_AREA_ESTUDIOS_MOVILIDAD': area_estudios['ID_AREA_ESTUDIOS_MOVILIDAD'],
            'ID_NIVEL_ESTUDIOS_MOVILIDAD': nivel_estudios['ID_NIVEL_ESTUDIOS_MOVILIDAD'],
            'ID_TIPO_ACCESO': tipo_acceso['ID_TIPO_ACCESO'],
            'ID_RANGO_CRED_SUPERADOS': rango_cred_superados['ID_RANGO_CREDITO'],
            'ID_RANGO_CRED_SUPERADOS_PREVIO': rango_cred_superados_previo['ID_RANGO_CREDITO'],
            'ID_FECHA_INICIO_ESTANCIA': int(fecha_inicio.replace('-', '')),
            'ID_FECHA_FIN_ESTANCIA': int(fecha_fin.replace('-', '')),
            'ID_SEXO': sexo['ID_SEXO'],
            'ID_PAIS_NACIONALIDAD': nacionalidad['ID_PAIS'],
            'ID_RANGO_NOTA_ADMISION': rango_nota_admision['ID_RANGO_NOTA_ADMISION'],
            'EDAD': edad,
            'ORDEN_PREFERENCIA': orden_preferencia,
            'FLG_ACCESO_DIRECTO_MOVILIDAD': flg_acceso_directo_movilidad,
            'DURACION_ESTANCIA': duracion_estancia,
            'ANOS_CURSADOS': anos_cursados,
            'CURSO_MAS_ALTO_MATRICULADO': curso_mas_alto_matriculado,
            'CREDITOS_SUPERADOS_PREVIO': creditos_superados_previo,
            'CREDITOS_SUPERA_DESTINO': creditos_supera_destino,
            'NOTA_ADMISION': nota_admision,
            'FECHA_CARGA': generate_random_date(2022, 2023),
            'ID_POBLACION_FAMILIAR': poblacion_familiar['ID_POBLACION'],
            'ID_PROGRAMA_MOVILIDAD_NK': programa_movilidad['ID_PROGRAMA_MOVILIDAD_NK'] if 'ID_PROGRAMA_MOVILIDAD_NK' in programa_movilidad else None,
            'ID_PROGRAMA_MOVILIDAD': programa_movilidad['ID_PROGRAMA_MOVILIDAD'],
            'ID_ESTUDIO': estudio['ID_ESTUDIO'],
            'ID_RAMA_CONOCIMIENTO': rama_conocimiento['ID_RAMA_CONOCIMIENTO'],
            'ID_FECHA_CARGA': int(generate_random_date(2022, 2023).replace('-', '')),
            'FLG_NUM_ACCESO_DIRECTO_MOVI': flg_num_acceso_directo_movi,
            'ID_EDAD_EST': edad_est['ID_EDAD_EST']
        })
    
    return pd.DataFrame(data)

def generate_f_solicitudes_movilidad(n=400, dimension_dfs=None):
    """Genera datos para la tabla F_SOLICITUDES_MOVILIDAD"""
    data = []
    
    # Verificar que se proporcionaron los DataFrames de dimensiones necesarios
    if dimension_dfs is None or not all(key in dimension_dfs for key in [
        'd_curso_academico', 'd_centro', 'd_plan_estudio', 'd_tipo_estudio',
        'd_area_estudios_movilidad', 'd_nivel_estudios_movilidad', 'd_tipo_acceso', 
        'd_rango_credito', 'd_idioma_movilidad', 'd_pais', 'd_sexo', 'd_rango_nota_admision',
        'd_poblacion', 'd_programa_movilidad', 'd_estudio', 'd_rama_conocimiento', 'd_edad_est',
        'd_universidad'
    ]):
        raise ValueError("Se deben proporcionar todos los DataFrames de dimensiones necesarios")
    
    # Obtener datos de dimensiones
    d_curso = dimension_dfs['d_curso_academico']
    d_centro = dimension_dfs['d_centro']
    d_plan_estudio = dimension_dfs['d_plan_estudio']
    d_tipo_estudio = dimension_dfs['d_tipo_estudio']
    d_area_estudios = dimension_dfs['d_area_estudios_movilidad']
    d_nivel_estudios = dimension_dfs['d_nivel_estudios_movilidad']
    d_tipo_acceso = dimension_dfs['d_tipo_acceso']
    d_rango_credito = dimension_dfs['d_rango_credito']
    d_idioma_movilidad = dimension_dfs['d_idioma_movilidad']
    d_pais = dimension_dfs['d_pais']
    d_sexo = dimension_dfs['d_sexo']
    d_rango_nota = dimension_dfs['d_rango_nota_admision']
    d_poblacion = dimension_dfs['d_poblacion']
    d_programa_movilidad = dimension_dfs['d_programa_movilidad']
    d_estudio = dimension_dfs['d_estudio']
    d_rama_conocimiento = dimension_dfs['d_rama_conocimiento']
    d_edad_est = dimension_dfs['d_edad_est']
    d_universidad = dimension_dfs['d_universidad']
    
    # Generar datos de solicitudes de movilidad
    for i in tqdm(range(1, n+1), desc="Generando solicitudes de movilidad"):
        # Generar IDs base
        id_solicitud_movilidad_nk = 1100000 + i
        id_expediente_academico_nk = 1200000 + i
        id_expediente_academico = 1300000 + i
        id_alumno_nip_nk = 1400000 + i
        id_alumno = 1500000 + i
        
        # Seleccionar valores aleatorios de las dimensiones
        curso = random.choice(d_curso.to_dict('records'))
        centro = random.choice(d_centro.to_dict('records'))
        plan_estudio = random.choice(d_plan_estudio.to_dict('records'))
        tipo_estudio = random.choice(d_tipo_estudio.to_dict('records'))
        nacionalidad = random.choice(d_pais.to_dict('records'))
        sexo = random.choice(d_sexo.to_dict('records'))
        area_estudios = random.choice(d_area_estudios.to_dict('records'))
        nivel_estudios = random.choice(d_nivel_estudios.to_dict('records'))
        tipo_acceso = random.choice(d_tipo_acceso.to_dict('records'))
        idioma_movilidad = random.choice(d_idioma_movilidad.to_dict('records'))
        rango_nota_admision = random.choice(d_rango_nota.to_dict('records'))
        rango_cred_superados_previo = random.choice(d_rango_credito.to_dict('records'))
        poblacion_familiar = random.choice(d_poblacion.to_dict('records'))
        programa_movilidad = random.choice(d_programa_movilidad.to_dict('records'))
        estudio = random.choice(d_estudio.to_dict('records'))
        rama_conocimiento = random.choice(d_rama_conocimiento.to_dict('records'))
        edad_est = random.choice(d_edad_est.to_dict('records'))
        universidad_destino = random.choice(d_universidad.to_dict('records'))
        pais_universidad_destino = random.choice(d_pais.to_dict('records'))
        
        # Fecha de solicitud
        fecha_solicitud = generate_random_date(2020, 2022)
        
        # Orden de preferencia (1-5)
        orden_preferencia = random.randint(1, 5)
        
        # Flags de estado de solicitud
        flg_aceptada = random.choice(['S', 'N'])
        flg_renuncia = 'S' if flg_aceptada == 'S' and random.random() < 0.1 else 'N'  # 10% de renuncias entre las aceptadas
        
        # Convertir flags a valores numéricos
        aceptada = 1 if flg_aceptada == 'S' else 0
        renuncia = 1 if flg_renuncia == 'S' else 0
        
        # Datos personales y académicos
        edad = random.randint(18, 30)
        duracion_estancia = random.randint(3, 12)  # en meses
        anos_cursados = random.randint(1, 4)
        creditos_superados = random.randint(30, 180)
        nota_admision = round(random.uniform(5, 14), 2)
        
        # Crear el registro para la solicitud de movilidad
        data.append({
            'ID_SOLICITUD_MOVILIDAD_NK': id_solicitud_movilidad_nk,
            'ID_CURSO_ACADEMICO_NK': curso['ID_CURSO_ACADEMICO_NK'],  # TODO: Usar valores válidos de D_CURSO_COHORTE,
            'ID_EXPEDIENTE_ACADEMICO_NK': id_expediente_academico_nk,
            'ID_ALUMNO_NIP_NK': id_alumno_nip_nk,
            'ID_CURSO_ACADEMICO': curso['ID_CURSO_ACADEMICO'],
            'ID_EXPEDIENTE_ACADEMICO': id_expediente_academico,
            'ID_ALUMNO': id_alumno,
            'ID_PAIS_NACIONALIDAD': nacionalidad['ID_PAIS'],
            'ID_SEXO': sexo['ID_SEXO'],
            'ID_PLAN_ESTUDIO': plan_estudio['ID_PLAN_ESTUDIO'],  # TODO: Usar valores válidos de F_TABLA_FUSION,
            'ID_TIPO_ESTUDIO': tipo_estudio['ID_TIPO_ESTUDIO'],
            'ID_CENTRO': centro['ID_CENTRO'],
            'ID_TIPO_ACCESO': tipo_acceso['ID_TIPO_ACCESO'],
            'ID_AREA_ESTUDIOS_MOVILIDAD': area_estudios['ID_AREA_ESTUDIOS_MOVILIDAD'],
            'ID_NIVEL_ESTUDIOS_MOVILIDAD': nivel_estudios['ID_NIVEL_ESTUDIOS_MOVILIDAD'],
            'ID_IDIOMA_MOVILIDAD': idioma_movilidad['ID_IDIOMA_MOVILIDAD'],
            'ID_FECHA_SOLICITUD': int(fecha_solicitud.replace('-', '')),
            'ID_RANGO_NOTA_ADMISION': rango_nota_admision['ID_RANGO_NOTA_ADMISION'],
            'ID_RANGO_CRED_SUPERADOS_PREVIO': rango_cred_superados_previo['ID_RANGO_CREDITO'],
            'ORDEN_PREFERENCIA': orden_preferencia,
            'FLG_ACEPTADA': flg_aceptada,
            'FLG_RENUNCIA': flg_renuncia,
            'ACEPTADA': aceptada,
            'RENUNCIA': renuncia,
            'EDAD': edad,
            'DURACION_ESTANCIA': duracion_estancia,
            'ANOS_CURSADOS': anos_cursados,
            'CREDITOS_SUPERADOS': creditos_superados,
            'NOTA_ADMISION': nota_admision,
            'FECHA_CARGA': generate_random_date(2022, 2023),
            'ID_POBLACION_FAMILIAR': poblacion_familiar['ID_POBLACION'],
            'ID_PROGRAMA_MOVILIDAD': programa_movilidad['ID_PROGRAMA_MOVILIDAD'],
            'ID_ESTUDIO': estudio['ID_ESTUDIO'],
            'ID_RAMA_CONOCIMIENTO': rama_conocimiento['ID_RAMA_CONOCIMIENTO'],
            'ID_FECHA_CARGA': int(generate_random_date(2022, 2023).replace('-', '')),
            'ID_EDAD_EST': edad_est['ID_EDAD_EST'],
            'ID_UNIVERSIDAD_DESTINO': universidad_destino['ID_UNIVERSIDAD'],
            'ID_PAIS_UNIVERSIDAD_DESTINO': pais_universidad_destino['ID_PAIS']
        })
    
    return pd.DataFrame(data) 