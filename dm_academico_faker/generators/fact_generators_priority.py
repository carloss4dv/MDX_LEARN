"""
Generadores de tablas de hechos prioritarias del Data Mart Académico

Este módulo contiene funciones para generar datos de hechos esenciales como:
- F_OFERTA_ADMISION
- F_SOLICITANTE_ADMISION  
- F_EGRESADO
- F_COHORTE
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

def generate_f_oferta_admision(n=500, dimension_dfs=None):
    """Genera datos para la tabla F_OFERTA_ADMISION"""
    data = []
    
    # Verificar que se proporcionaron los DataFrames de dimensiones necesarios
    if dimension_dfs is None or not all(key in dimension_dfs for key in [
        'd_curso_academico', 'd_plan_estudio', 'd_tipo_estudio', 'd_centro', 
        'd_tipo_acceso', 'd_estudio_previo', 'd_cupo_adjudicacion', 'd_poblacion',
        'd_rama_conocimiento', 'd_estudio', 'd_persona'
    ]):
        raise ValueError("Se deben proporcionar todos los DataFrames de dimensiones necesarios")
    
    # Obtener datos de dimensiones
    d_curso = dimension_dfs['d_curso_academico']
    d_plan = dimension_dfs['d_plan_estudio']
    d_tipo_estudio = dimension_dfs['d_tipo_estudio']
    d_centro = dimension_dfs['d_centro']
    d_tipo_acceso = dimension_dfs['d_tipo_acceso']
    d_estudio_previo = dimension_dfs['d_estudio_previo']
    d_cupo = dimension_dfs['d_cupo_adjudicacion']
    d_poblacion = dimension_dfs['d_poblacion']
    d_rama = dimension_dfs['d_rama_conocimiento']
    d_estudio = dimension_dfs['d_estudio']
    d_persona = dimension_dfs['d_persona']  # Para el coordinador
    
    # Generar datos de oferta de admisión
    for i in tqdm(range(1, n+1), desc="Generando ofertas de admisión"):
        # Seleccionar valores aleatorios de las dimensiones
        curso = random.choice(d_curso.to_dict('records'))
        plan = random.choice(d_plan.to_dict('records'))
        tipo_estudio = random.choice(d_tipo_estudio.to_dict('records'))
        centro = random.choice(d_centro.to_dict('records'))
        tipo_acceso = random.choice(d_tipo_acceso.to_dict('records'))
        estudio_previo = random.choice(d_estudio_previo.to_dict('records'))
        cupo = random.choice(d_cupo.to_dict('records'))
        poblacion_centro = random.choice(d_poblacion.to_dict('records'))
        rama = random.choice(d_rama.to_dict('records'))
        estudio = random.choice(d_estudio.to_dict('records'))
        coordinador = random.choice(d_persona.to_dict('records'))
        
        # Generar datos numéricos aleatorios para la oferta
        plazas_ofertadas = random.randint(20, 200)
        plazas_asignadas = random.randint(10, plazas_ofertadas)
        plazas_solicitadas = random.randint(plazas_asignadas, plazas_asignadas * 2)
        plazas_solicitadas_pref_1 = random.randint(plazas_asignadas, plazas_solicitadas)
        
        # Notas
        nota_agregada = round(random.uniform(5, 13.5), 3)
        nota_media_admision = round(random.uniform(5, 13.5), 3)
        nota_corte_adjudicacion_1 = round(random.uniform(5, 14), 3)
        nota_corte_adjudicacion_2 = round(random.uniform(5, nota_corte_adjudicacion_1), 3)
        nota_corte_definitiva_1 = round(random.uniform(nota_corte_adjudicacion_1 - 0.5, nota_corte_adjudicacion_1 + 0.5), 3)
        nota_corte_definitiva_2 = round(random.uniform(nota_corte_adjudicacion_2 - 0.5, nota_corte_adjudicacion_2 + 0.5), 3)
        
        # Flags booleanos (0/1)
        flg_interuniversitario = random.choice([0, 1])
        flg_coordinador = random.choice([0, 1])
        flg_multiple_titulacion = random.choice([0, 1])
        flg_master_hab = random.choice([0, 1])
        
        # Flags de admitidos todos
        flg_admitidos_todos_1 = 'S' if plazas_solicitadas <= plazas_ofertadas else 'N'
        flg_admitidos_todos_2 = 'S' if plazas_solicitadas <= plazas_ofertadas else 'N'
        
        # Valores de participación
        participa_1 = random.choice([0, 1])
        participa_2 = random.choice([0, 1])
        
        # Prelación de convocatorias
        prela_convo_nota_def = random.choice(['1', '2'])
        prela_convo_nota_def_1 = '1' if prela_convo_nota_def == '1' else '2'
        prela_convo_nota_def_2 = '2' if prela_convo_nota_def == '1' else '1'
        
        # Número de credenciales UNED
        num_credencial_uned = random.randint(0, plazas_asignadas // 4)
        
        # Generar correo del coordinador
        correo_coord = f"{coordinador['NOMBRE'].lower()}.{coordinador['APELLIDO1'].lower()}@universidad.es"
        
        # Datos de orden BOE
        orden_boe_plan = f"BOE-A-{random.randint(2010, 2022)}-{random.randint(1000, 9999)}"
        
        # Flag doctorado vigente
        sn_doctorado_vigente = 'S' if tipo_estudio['ID_TIPO_ESTUDIO'] == 5 else 'N'
        
        data.append({
            'ID_CURSO_ACADEMICO': curso['ID_CURSO_ACADEMICO'],
            'ID_PLAN_ESTUDIO': plan['ID_PLAN_ESTUDIO'],
            'ID_TIPO_ESTUDIO': tipo_estudio['ID_TIPO_ESTUDIO'],
            'ID_CENTRO': centro['ID_CENTRO'],
            'ID_TIPO_ACCESO': tipo_acceso['ID_TIPO_ACCESO'],
            'ID_ESTUDIO_PREVIO': estudio_previo['ID_ESTUDIO_PREVIO'],
            'ID_CUPO_ADJUDICACION': cupo['ID_CUPO_ADJUDICACION'],
            'PLAZAS_OFERTADAS': plazas_ofertadas,
            'PLAZAS_ASIGNADAS': plazas_asignadas,
            'PLAZAS_SOLICITADAS': plazas_solicitadas,
            'NOTA_AGREGADA': nota_agregada,
            'NOTA_CORTE_ADJUDICACION_1': nota_corte_adjudicacion_1,
            'NOTA_CORTE_ADJUDICACION_2': nota_corte_adjudicacion_2,
            'NOTA_CORTE_DEFINITIVA_1': nota_corte_definitiva_1,
            'NOTA_CORTE_DEFINITIVA_2': nota_corte_definitiva_2,
            'FLG_ADMITIDOS_TODOS_1': flg_admitidos_todos_1,
            'FLG_ADMITIDOS_TODOS_2': flg_admitidos_todos_2,
            'PARTICIPA_1': participa_1,
            'PARTICIPA_2': participa_2,
            'ID_CURSO_ACADEMICO_NK': curso['ID_CURSO_ACADEMICO_NK'],
            'FECHA_CARGA': generate_random_date(2020, 2023),
            'NOTA_MEDIA_ADMISION': nota_media_admision,
            'PRELA_CONVO_NOTA_DEF': prela_convo_nota_def,
            'PRELA_CONVO_NOTA_DEF_1': prela_convo_nota_def_1,
            'PRELA_CONVO_NOTA_DEF_2': prela_convo_nota_def_2,
            'NUM_CREDENCIAL_UNED': num_credencial_uned,
            'PLAZAS_SOLICITADAS_PREF_1': plazas_solicitadas_pref_1,
            'ID_FECHA_CARGA': int(generate_random_date(2020, 2023).replace('-', '')),
            'ID_TIPO_CENTRO': centro.get('ID_TIPO_CENTRO', random.randint(1, 3)),
            'ID_CAMPUS': centro.get('ID_CAMPUS', random.randint(1, 5)),
            'ID_POBLACION_CENTRO': poblacion_centro['ID_POBLACION'],
            'ID_ESTUDIO': estudio['ID_ESTUDIO'],
            'ID_RAMA_CONOCIMIENTO': rama['ID_RAMA_MACROAREA'],
            'ORDEN_BOE_PLAN': orden_boe_plan,
            'SN_DOCTORADO_VIGENTE': sn_doctorado_vigente,
            'ID_PERSONA_NIP_COORD_NK': coordinador['ID_PERSONA_NIP_NK'],
            'CORREO_COORD': correo_coord,
            'ID_PERSONA_COORD': coordinador['ID_PERSONA'],
            'FLG_INTERUNIVERSITARIO': flg_interuniversitario,
            'FLG_COORDINADOR': flg_coordinador,
            'FLG_MULTIPLE_TITULACION': flg_multiple_titulacion,
            'FLG_MASTER_HAB': flg_master_hab,
            'SN_MASTER_HABILITANTE': 'S' if flg_master_hab == 1 else 'N',
            'SN_MULTIPLE_TITULACION': 'S' if flg_multiple_titulacion == 1 else 'N',
            'SN_INTERUNIVERSITARIO': 'S' if flg_interuniversitario == 1 else 'N',
            'SN_COORDINADOR': 'S' if flg_coordinador == 1 else 'N'
        })
    
    return pd.DataFrame(data)

def generate_f_solicitante_admision(n=1000, dimension_dfs=None):
    """Genera datos para la tabla F_SOLICITANTE_ADMISION"""
    data = []
    
    # Verificar que se proporcionaron los DataFrames de dimensiones necesarios
    if dimension_dfs is None or not all(key in dimension_dfs for key in [
        'd_curso_academico', 'd_convocatoria', 'd_tipo_acceso_preinscripcion', 
        'd_tipo_procedimiento', 'd_estudio_previo', 'd_universidad', 'd_cupo_adjudicacion',
        'd_plan_estudio', 'd_persona', 'd_sexo', 'd_poblacion', 'd_pais', 'd_centro',
        'd_estado_adjudicacion', 'd_rango_nota_admision', 'd_estudio', 'd_tipo_estudio',
        'd_rama_conocimiento', 'd_detalle_cupo_general', 'd_edad_est'
    ]):
        raise ValueError("Se deben proporcionar todos los DataFrames de dimensiones necesarios")
    
    # Obtener datos de dimensiones
    d_curso = dimension_dfs['d_curso_academico']
    d_convocatoria = dimension_dfs['d_convocatoria']
    d_tipo_acceso_preins = dimension_dfs['d_tipo_acceso_preinscripcion']
    d_tipo_procedimiento = dimension_dfs['d_tipo_procedimiento']
    d_estudio_previo = dimension_dfs['d_estudio_previo']
    d_universidad = dimension_dfs['d_universidad']
    d_cupo = dimension_dfs['d_cupo_adjudicacion']
    d_plan = dimension_dfs['d_plan_estudio']
    d_persona = dimension_dfs['d_persona']
    d_sexo = dimension_dfs['d_sexo']
    d_poblacion = dimension_dfs['d_poblacion']
    d_pais = dimension_dfs['d_pais']
    d_centro = dimension_dfs['d_centro']
    d_estado_adjudicacion = dimension_dfs['d_estado_adjudicacion']
    d_rango_nota = dimension_dfs['d_rango_nota_admision']
    d_estudio = dimension_dfs['d_estudio']
    d_tipo_estudio = dimension_dfs['d_tipo_estudio']
    d_rama = dimension_dfs['d_rama_conocimiento']
    d_detalle_cupo = dimension_dfs['d_detalle_cupo_general']
    d_edad_est = dimension_dfs['d_edad_est']
    
    # Generar datos de solicitantes de admisión
    for i in tqdm(range(1, n+1), desc="Generando solicitantes de admisión"):
        # ID único de preinscripción
        id_preinscripcion = 100000 + i
        
        # Seleccionar valores aleatorios de las dimensiones
        curso = random.choice(d_curso.to_dict('records'))
        convocatoria = random.choice(d_convocatoria.to_dict('records'))
        tipo_acceso_preins = random.choice(d_tipo_acceso_preins.to_dict('records'))
        tipo_procedimiento = random.choice(d_tipo_procedimiento.to_dict('records'))
        estudio_previo = random.choice(d_estudio_previo.to_dict('records'))
        universidad = random.choice(d_universidad.to_dict('records'))
        cupo = random.choice(d_cupo.to_dict('records'))
        persona = random.choice(d_persona.to_dict('records'))
        plan = random.choice(d_plan.to_dict('records'))
        centro = random.choice(d_centro.to_dict('records'))
        estado_adjudicacion = random.choice(d_estado_adjudicacion.to_dict('records'))
        estudio = random.choice(d_estudio.to_dict('records'))
        tipo_estudio = random.choice(d_tipo_estudio.to_dict('records'))
        rama = random.choice(d_rama.to_dict('records'))
        detalle_cupo = random.choice(d_detalle_cupo.to_dict('records'))
        
        # Poblaciones
        poblacion_nacimiento = random.choice(d_poblacion.to_dict('records'))
        poblacion_familiar = random.choice(d_poblacion.to_dict('records'))
        poblacion_centro = random.choice(d_poblacion.to_dict('records'))
        
        # Países
        pais_nacimiento = random.choice(d_pais.to_dict('records'))
        pais_nacionalidad = random.choice(d_pais.to_dict('records'))
        pais_universidad = random.choice(d_pais.to_dict('records'))
        pais_familiar = random.choice(d_pais.to_dict('records'))
        
        # Obtener el sexo correspondiente
        sexo = d_sexo[d_sexo['ID_SEXO_NK'] == persona['SEXO']].to_dict('records')[0]
        
        # Edad y fecha de nacimiento
        fecha_nacimiento = fake.date_of_birth(minimum_age=17, maximum_age=65).strftime('%Y-%m-%d')
        edad = datetime.datetime.now().year - datetime.datetime.strptime(fecha_nacimiento, '%Y-%m-%d').year
        edad_est = random.choice(d_edad_est.to_dict('records'))
        
        # Asegurarse de que el nombre de la edad_est no supere los 10 caracteres
        nombre_edad_est = edad_est['NOMBRE_EDAD_EST']
        if len(nombre_edad_est) > 10:
            nombre_edad_est = nombre_edad_est[:7] + "..."
        
        # Datos de admisión
        nota_admision = round(random.uniform(5, 14), 2)
        nota_acceso = round(random.uniform(5, 14), 2)
        
        # Buscar el rango de nota que corresponde
        for _, rango in d_rango_nota.iterrows():
            rango_nombre = rango['NOMBRE_RANGO_NOTA_ADMISION']
            if '-' in rango_nombre:
                min_val, max_val = map(float, rango_nombre.split('-'))
                if min_val <= nota_admision <= max_val:
                    rango_nota = rango
                    break
        else:
            rango_nota = d_rango_nota.iloc[0]
        
        # Datos de la solicitud
        orden_preferencia = random.randint(1, 10)
        resolucion_solicitud = random.choice(['A', 'D', 'P'])  # Admitido, Denegado, Pendiente
        sn_admitido = 'S' if resolucion_solicitud == 'A' else 'N'
        orden_adjudicacion = random.randint(1, 5) if resolucion_solicitud == 'A' else None
        
        # Fechas
        fecha_preinscripcion = generate_random_date(int(curso['ID_CURSO_ACADEMICO_NK']), int(curso['ID_CURSO_ACADEMICO_NK']))
        
        # Datos de resolución
        resolucion_llamamiento = random.choice(['A1', 'A2', 'D1', 'D2', 'P1', 'P2'])
        num_llamamiento = resolucion_llamamiento[-1]
        resolucion_final = f"Resolución final para la solicitud {id_preinscripcion} del {fecha_preinscripcion}"
        
        # Flags
        sn_matriculado = random.choice(['S', 'N'])
        sn_participa_adjudicacion = random.choice(['S', 'N'])
        sn_credencial_uned = random.choice(['S', 'N'])
        flg_credencial_uned = 1 if sn_credencial_uned == 'S' else 0
        
        data.append({
            'ID_PREINSCRIPCION': id_preinscripcion,
            'ID_CURSO_ACADEMICO': curso['ID_CURSO_ACADEMICO'],
            'ID_CONVOCATORIA': convocatoria['ID_CONVOCATORIA'],
            'ID_TIPO_ACCESO_PREINS': tipo_acceso_preins['ID_TIPO_ACCESO_PREINS'],
            'ID_TIPO_PROCEDIMIENTO': tipo_procedimiento['ID_TIPO_PROCEDIMIENTO'],
            'ID_ESTUDIO_PREVIO': estudio_previo['ID_ESTUDIO_PREVIO'],
            'ID_UNIVERSIDAD': universidad['ID_UNIVERSIDAD'],
            'ID_CUPO_ADJUDICACION': cupo['ID_CUPO_ADJUDICACION'],
            'NOTA_ADMISION': nota_admision,
            'ID_PLAN_ESTUDIO': plan['ID_PLAN_ESTUDIO'],
            'ORDEN_PREFERENCIA': orden_preferencia,
            'RESOLUCION_SOLICITUD': resolucion_solicitud,
            'SN_ADMITIDO': sn_admitido,
            'ORDEN_ADJUDICACION': orden_adjudicacion,
            'FECHA_PREINSCRIPCION': fecha_preinscripcion,
            'ID_PERSONA': persona['ID_PERSONA'],
            'FECHA_NACIMIENTO': fecha_nacimiento,
            'ID_SEXO': sexo['ID_SEXO'],
            'SEXO': persona['SEXO'],
            'ID_POBLACION_NACIMIENTO': poblacion_nacimiento['ID_POBLACION'],
            'ID_PAIS_NACIMIENTO': pais_nacimiento['ID_PAIS'],
            'ID_PAIS_NACIONALIDAD': pais_nacionalidad['ID_PAIS'],
            'EDAD': edad,
            'FECHA_CARGA': generate_random_date(2020, 2023),
            'ID_CENTRO': centro['ID_CENTRO'],
            'ID_PAIS_UNIVERSIDAD_ORIGEN': pais_universidad['ID_PAIS'],
            'RESOLUCION_LLAMAMIENTO': resolucion_llamamiento,
            'NUM_LLAMAMIENTO': num_llamamiento,
            'RESOLUCION_FINAL': resolucion_final,
            'ID_ESTADO_ADJUDICACION': estado_adjudicacion['ID_ESTADO_ADJUDICACION'],
            'ID_CURSO_ACADEMICO_NK': curso['ID_CURSO_ACADEMICO_NK'],
            'ID_RANGO_NOTA_ADMISION': rango_nota['ID_RANGO_NOTA_ADMISION'],
            'SN_MATRICULADO': sn_matriculado,
            'SN_PARTICIPA_ADJUDICACION': sn_participa_adjudicacion,
            'ID_POBLACION_FAMILIAR': poblacion_familiar['ID_POBLACION'],
            'SN_CREDENCIAL_UNED': sn_credencial_uned,
            'FLG_CREDENCIAL_UNED': flg_credencial_uned,
            'NOTA_ACCESO': nota_acceso,
            'ID_FECHA_CARGA': int(generate_random_date(2020, 2023).replace('-', '')),
            'ID_TIPO_CENTRO': centro.get('ID_TIPO_CENTRO', random.randint(1, 3)),
            'ID_CAMPUS': centro.get('ID_CAMPUS', random.randint(1, 5)),
            'ID_POBLACION_CENTRO': poblacion_centro['ID_POBLACION'],
            'ID_TIPO_ESTUDIO': tipo_estudio['ID_TIPO_ESTUDIO'],
            'ID_ESTUDIO': estudio['ID_ESTUDIO'],
            'ID_RAMA_CONOCIMIENTO': rama['ID_RAMA_MACROAREA'],
            'ID_DETALLE_CUPO_GENERAL': detalle_cupo['ID_DETALLE_CUPO_GENERAL'],
            'ID_DETALLE_CUPO_GENERAL_NK': detalle_cupo.get('ID_DETALLE_CUPO_GENERAL_NK', ''),
            'ID_PAIS_FAMILIAR': pais_familiar['ID_PAIS'],
            'ID_PAIS_FAMILIAR_NK': pais_familiar.get('ID_PAIS_NK', ''),
            'EDAD_EST': nombre_edad_est,
            'ID_EDAD_EST': edad_est['ID_EDAD_EST']
        })
    
    return pd.DataFrame(data)

def generate_f_egresado(n=700, dimension_dfs=None):
    """Genera datos para la tabla F_EGRESADO"""
    data = []
    
    # Verificar que se proporcionaron los DataFrames de dimensiones necesarios
    if dimension_dfs is None or not all(key in dimension_dfs for key in [
        'd_curso_academico', 'd_tipo_abandono', 'd_tipo_egreso', 'd_plan_estudio', 
        'd_centro', 'd_tipo_acceso', 'd_titulacion', 'd_poblacion', 'd_sexo',
        'd_pais', 'd_estudio_previo', 'd_tipo_estudio', 'd_estudio', 'd_tipo_centro',
        'd_rama_conocimiento', 'd_edad_est', 'd_persona'
    ]):
        raise ValueError("Se deben proporcionar todos los DataFrames de dimensiones necesarios")
    
    # Obtener datos de dimensiones
    d_curso = dimension_dfs['d_curso_academico']
    d_tipo_abandono = dimension_dfs['d_tipo_abandono']
    d_tipo_egreso = dimension_dfs['d_tipo_egreso']
    d_plan = dimension_dfs['d_plan_estudio']
    d_centro = dimension_dfs['d_centro']
    d_tipo_acceso = dimension_dfs['d_tipo_acceso']
    d_titulacion = dimension_dfs['d_titulacion']
    d_poblacion = dimension_dfs['d_poblacion']
    d_sexo = dimension_dfs['d_sexo']
    d_pais = dimension_dfs['d_pais']
    d_estudio_previo = dimension_dfs['d_estudio_previo']
    d_tipo_estudio = dimension_dfs['d_tipo_estudio']
    d_estudio = dimension_dfs['d_estudio']
    d_tipo_centro = dimension_dfs['d_tipo_centro']
    d_rama = dimension_dfs['d_rama_conocimiento']
    d_edad_est = dimension_dfs['d_edad_est']
    d_persona = dimension_dfs['d_persona']
    
    # Ordenar los cursos académicos para asegurar que haya una secuencia
    cursos_ordenados = sorted(d_curso['ID_CURSO_ACADEMICO'].tolist())
    
    # Generar datos de egresados
    for i in tqdm(range(1, n+1), desc="Generando egresados"):
        # ID único de expediente
        id_expediente = 200000 + i
        
        # Seleccionar valores aleatorios de las dimensiones
        # Asegurar que el curso seleccionado no sea el primero para que haya cursos anteriores disponibles
        # Excluir el primer curso académico para asegurar que haya al menos un curso anterior
        if len(cursos_ordenados) > 1:
            # Seleccionar un curso que no sea el primero para garantizar que haya un curso anterior
            curso_idx = random.randint(1, len(cursos_ordenados) - 1)
            curso_id = cursos_ordenados[curso_idx]
            curso = d_curso[d_curso['ID_CURSO_ACADEMICO'] == curso_id].iloc[0].to_dict()
            
            # Obtener un curso anterior (cohorte)
            cursos_anteriores = cursos_ordenados[:curso_idx]
            curso_academico_cohorte = random.choice(cursos_anteriores)
        else:
            # Si solo hay un curso académico, usarlo y crear una cohorte ficticia
            curso = d_curso.iloc[0].to_dict()
            curso_academico_cohorte = curso['ID_CURSO_ACADEMICO']
        
        tipo_abandono = random.choice(d_tipo_abandono.to_dict('records'))
        tipo_egreso = random.choice(d_tipo_egreso.to_dict('records'))
        plan = random.choice(d_plan.to_dict('records'))
        centro = random.choice(d_centro.to_dict('records'))
        centro_origen = random.choice(d_centro.to_dict('records'))
        tipo_acceso = random.choice(d_tipo_acceso.to_dict('records'))
        titulacion = random.choice(d_titulacion.to_dict('records'))
        persona = random.choice(d_persona.to_dict('records'))
        estudio_previo = random.choice(d_estudio_previo.to_dict('records'))
        tipo_estudio = random.choice(d_tipo_estudio.to_dict('records'))
        estudio = random.choice(d_estudio.to_dict('records'))
        
        # Poblaciones
        poblacion_familiar = random.choice(d_poblacion.to_dict('records'))
        poblacion_centro = random.choice(d_poblacion.to_dict('records'))
        poblacion_centro_origen = random.choice(d_poblacion.to_dict('records'))
        
        # Países
        pais_nacionalidad = random.choice(d_pais.to_dict('records'))
        pais_familiar = random.choice(d_pais.to_dict('records'))
        
        # Obtener el sexo correspondiente
        sexo = d_sexo[d_sexo['ID_SEXO_NK'] == persona['SEXO']].to_dict('records')[0]
        
        # Edad
        edad = random.randint(20, 65)
        edad_est = random.choice(d_edad_est.to_dict('records'))
        
        # Flags de egreso - definir primero antes de usar
        graduado = random.choice([0, 1])
        traslado = 0 if graduado == 1 else random.choice([0, 1])
        abandono_generico = 0 if (graduado == 1 or traslado == 1) else random.choice([0, 1])
        abandono_oficial = abandono_generico * random.choice([0, 1])
        
        # Generar datos numéricos para egresados - evitar NaN
        cursos_matriculados = random.randint(1, 8)
        curso_mas_alto_matriculado = random.randint(1, min(cursos_matriculados, 6))
        cursos_extra_graduacion = max(0, cursos_matriculados - 4) if graduado == 1 else 0.0
        duracion = random.randint(3, 8)
        duracion_real = float(duracion + random.uniform(-0.5, 1.5))
        
        # Créditos - asegurar valores float válidos
        creditos_necesarios = float(random.randint(180, 360))
        creditos_matriculados = creditos_necesarios + float(random.randint(0, 60))
        creditos_superados = float(random.randint(int(creditos_necesarios - 60) if graduado == 0 else int(creditos_necesarios), int(creditos_matriculados)))
        creditos_reconocidos = float(random.randint(0, 30))
        
        # Calificación final - evitar NaN
        calificacion_final = float(round(random.uniform(5.0, 10.0), 3)) if graduado == 1 else 0.0
        
        # Flags adicionales
        flg_solicitud_titulo = random.choice([0, 1])
        flg_abandono_inicial = random.choice([0, 1])
        flg_calculo_tasa = random.choice([0, 1])
        flg_graduado_en_tiempo = 1 if graduado == 1 and cursos_matriculados <= 4 else 0
        flg_plan_oficial = random.choice([0, 1])
        flg_duracion_media = random.choice([0, 1])
        flg_multiple_titulacion = random.choice([0, 1])
        flg_movilidad_in = random.choice([0, 1])
        
        # Fechas - usar objetos date directos
        fecha_solicitud_titulo = int(datetime.date(2020 + random.randint(0, 3), random.randint(1, 12), random.randint(1, 28)).strftime('%Y%m%d'))
        fecha_egreso = int(datetime.date(2020 + random.randint(0, 3), random.randint(1, 12), random.randint(1, 28)).strftime('%Y%m%d'))
        
        # Datos de orden BOE
        orden_boe_plan = f"BOE-{random.randint(100, 999)}-{random.randint(2010, 2023)}"[:16]
        
        # Flags doctorado y movilidad
        sn_doctorado_vigente = random.choice(['S', 'N'])
        sn_movilidad_out_internacional = random.choice(['S', 'N'])
        sn_movilidad_out_nacional = random.choice(['S', 'N'])
        sn_unita = random.choice(['S', 'N'])
        sn_unita_geminae = random.choice(['S', 'N'])
        
        data.append({
            'ID_CURSO_ACADEMICO_NK': curso['ID_CURSO_ACADEMICO_NK'],
            'ID_EXPEDIENTE_ACADEMICO_NK': id_expediente,
            'ID_CURSO_ACADEMICO': curso['ID_CURSO_ACADEMICO'],
            'ID_ALUMNO': persona['ID_PERSONA'],
            'ID_EXPEDIENTE_ACADEMICO': id_expediente,
            'ID_TIPO_ABANDONO': tipo_abandono['ID_TIPO_ABANDONO'],
            'ID_TIPO_EGRESO': tipo_egreso['ID_TIPO_EGRESO'],
            'ID_PLAN_ESTUDIO': plan['ID_PLAN_ESTUDIO'],
            'ID_CENTRO': centro['ID_CENTRO'],
            'ID_CURSO_ACADEMICO_COHORTE': curso_academico_cohorte,
            'ID_TIPO_ACCESO': tipo_acceso['ID_TIPO_ACCESO'],
            'ID_TITULACION': titulacion['ID_TITULACION'],
            'ID_POBLACION_FAMILIAR': poblacion_familiar['ID_POBLACION'],
            'CURSOS_MATRICULADOS': cursos_matriculados,
            'CURSO_MAS_ALTO_MATRICULADO': curso_mas_alto_matriculado,
            'CURSOS_EXTRA_GRADUACION': cursos_extra_graduacion,
            'DURACION': duracion,
            'DURACION_REAL': duracion_real,
            'CREDITOS_MATRICULADOS': creditos_matriculados,
            'ID_RANGO_CREDITOS_MATRICULADOS': random.randint(1, 5),
            'CREDITOS_SUPERADOS': creditos_superados,
            'ID_RANGO_CREDITOS_SUPERADOS': random.randint(1, 5),
            'CREDITOS_NECESARIOS': creditos_necesarios,
            'ID_RANGO_CREDITOS_NECESARIOS': random.randint(1, 5),
            'CALIFICACION_FINAL': calificacion_final,
            'ID_RANGO_CALIFICACION_FINAL': random.randint(1, 5),
            'SEXO': persona['SEXO'],
            'ID_SEXO': sexo['ID_SEXO'],
            'EDAD': edad,
            'ID_FECHA_SOLICITUD_TITULO': fecha_solicitud_titulo,
            'ID_FECHA_EGRESO': fecha_egreso,
            'GRADUADO': graduado,
            'TRASLADO': traslado,
            'SN_SOLICITA_TITULO': 'S' if flg_solicitud_titulo == 1 else 'N',
            'SN_ABANDONO_INICIAL': 'S' if flg_abandono_inicial == 1 else 'N',
            'FLG_SOLICITUD_TITULO': flg_solicitud_titulo,
            'FLG_ABANDONO_INICIAL': flg_abandono_inicial,
            'FLG_CALCULO_TASA': flg_calculo_tasa,
            'FLG_GRADUADO_EN_TIEMPO': flg_graduado_en_tiempo,
            'FECHA_CARGA': generate_random_date(2020, 2023),
            'SN_GRADUADO_EN_TIEMPO': 'S' if flg_graduado_en_tiempo == 1 else 'N',
            'ABANDONO_GENERICO': abandono_generico,
            'ABANDONO_OFICIAL': abandono_oficial,
            'FLG_PLAN_OFICIAL': flg_plan_oficial,
            'CREDITOS_RECONOCIDOS': creditos_reconocidos,
            'ID_RANGO_CREDITOS_RECONOCIDOS': random.randint(1, 5),
            'SN_CAMBIO_CICLO_GRADO': random.choice(['S', 'N']),
            'FLG_DURACION_MEDIA': flg_duracion_media,
            'ID_ESTUDIO_PREVIO': estudio_previo['ID_ESTUDIO_PREVIO'],
            'ID_PAIS_NACIONALIDAD': pais_nacionalidad['ID_PAIS'],
            'ID_CENTRO_ORIGEN': centro_origen['ID_CENTRO'],
            'SN_MULTIPLE_TITULACION': 'S' if flg_multiple_titulacion == 1 else 'N',
            'SN_MOVILIDAD_IN': 'S' if flg_movilidad_in == 1 else 'N',
            'FLG_MULTIPLE_TITULACION': flg_multiple_titulacion,
            'FLG_MOVILIDAD_IN': flg_movilidad_in,
            'ID_FECHA_CARGA': int(generate_random_date(2020, 2023).replace('-', '')),
            'ID_TIPO_TITULACION': titulacion.get('ID_TIPO_TITULACION', random.randint(1, 5)),
            'ID_TIPO_ESTUDIO': tipo_estudio['ID_TIPO_ESTUDIO'],
            'ID_ESTUDIO': estudio['ID_ESTUDIO'],
            'ID_TIPO_CENTRO': centro.get('ID_TIPO_CENTRO', random.randint(1, 3)),
            'ID_CAMPUS_CENTRO': centro.get('ID_CAMPUS', random.randint(1, 5)),
            'ID_POBLACION_CENTRO': poblacion_centro['ID_POBLACION'],
            'ID_TIPO_CENTRO_ORI': centro_origen.get('ID_TIPO_CENTRO', random.randint(1, 3)),
            'ID_CAMPUS_CENTRO_ORI': centro_origen.get('ID_CAMPUS', random.randint(1, 5)),
            'ID_POBLACION_CENTRO_ORI': poblacion_centro_origen['ID_POBLACION'],
            'ID_RAMA_CONOCIMIENTO': random.choice(d_rama['ID_RAMA_MACROAREA'].tolist()),
            'ID_PERSONA_NIP_NK': persona['ID_PERSONA_NIP_NK'],
            'ORDEN_BOE_PLAN': orden_boe_plan,
            'SN_DOCTORADO_VIGENTE': sn_doctorado_vigente,
            'SN_MOVILIDAD_OUT_INTERNACIONAL': sn_movilidad_out_internacional,
            'SN_MOVILIDAD_OUT_NACIONAL': sn_movilidad_out_nacional,
            'ID_PAIS_FAMILIAR': pais_familiar['ID_PAIS'],
            'ID_PAIS_FAMILIAR_NK': pais_familiar.get('ID_PAIS_NK', ''),
            'ID_EDAD_EST': edad_est['ID_EDAD_EST'],
            'ID_ESTUDIO_OTRA_UNIV_DEST': random.randint(1, 50),
            'ID_CENTRO_OTRA_UNIV_DEST': random.randint(1, 50),
            'SN_UNITA': sn_unita,
            'SN_UNITA_GEMINAE': sn_unita_geminae
        })
    
    return pd.DataFrame(data)

def generate_f_cohorte(n=600, dimension_dfs=None):
    """Genera datos para la tabla F_COHORTE"""
    data = []
    
    # Verificar que se proporcionaron los DataFrames de dimensiones necesarios
    if dimension_dfs is None or not all(key in dimension_dfs for key in [
        'd_curso_academico', 'd_plan_estudio', 'd_centro', 'd_tipo_acceso', 
        'd_sexo', 'd_tipo_abandono', 'd_estudio_previo', 'd_pais', 'd_poblacion',
        'd_tipo_estudio', 'd_tipo_centro', 'd_campus', 'd_rama_conocimiento',
        'd_edad_est', 'd_persona'
    ]):
        raise ValueError("Se deben proporcionar todos los DataFrames de dimensiones necesarios")
    
    # Obtener datos de dimensiones
    d_curso = dimension_dfs['d_curso_academico']
    d_plan = dimension_dfs['d_plan_estudio']
    d_centro = dimension_dfs['d_centro']
    d_tipo_acceso = dimension_dfs['d_tipo_acceso']
    d_sexo = dimension_dfs['d_sexo']
    d_tipo_abandono = dimension_dfs['d_tipo_abandono']
    d_estudio_previo = dimension_dfs['d_estudio_previo']
    d_pais = dimension_dfs['d_pais']
    d_poblacion = dimension_dfs['d_poblacion']
    d_tipo_estudio = dimension_dfs['d_tipo_estudio']
    d_tipo_centro = dimension_dfs['d_tipo_centro']
    d_campus = dimension_dfs['d_campus']
    d_rama = dimension_dfs['d_rama_conocimiento']
    d_edad_est = dimension_dfs['d_edad_est']
    d_persona = dimension_dfs['d_persona']
    
    # Ordenar los cursos académicos para tener un orden cronológico
    cursos_ordenados = sorted(d_curso['ID_CURSO_ACADEMICO'].tolist())
    
    # Generar datos de cohorte
    for i in tqdm(range(1, n+1), desc="Generando cohortes"):
        # ID único de expediente
        id_expediente = 300000 + i
        
        # Seleccionar curso de cohorte (evitando el último para poder tener cursos posteriores)
        if len(cursos_ordenados) > 1:
            # Evitar seleccionar el último curso académico para garantizar que haya un curso posterior
            curso_idx = random.randint(0, len(cursos_ordenados) - 2)
            curso_cohorte_id = cursos_ordenados[curso_idx]
            curso_cohorte = d_curso[d_curso['ID_CURSO_ACADEMICO'] == curso_cohorte_id].iloc[0].to_dict()
            
            # Obtener posibles cursos posteriores para graduación, abandono, etc.
            cursos_posteriores = cursos_ordenados[curso_idx+1:]
        else:
            # Si solo hay un curso académico, usarlo
            curso_cohorte = d_curso.iloc[0].to_dict()
            cursos_posteriores = []
        
        # Seleccionar valores aleatorios de las dimensiones básicas
        plan = random.choice(d_plan.to_dict('records'))
        centro = random.choice(d_centro.to_dict('records'))
        tipo_acceso = random.choice(d_tipo_acceso.to_dict('records'))
        persona = random.choice(d_persona.to_dict('records'))
        sexo = d_sexo[d_sexo['ID_SEXO_NK'] == persona['SEXO']].to_dict('records')[0]
        tipo_abandono = random.choice(d_tipo_abandono.to_dict('records'))
        estudio_previo = random.choice(d_estudio_previo.to_dict('records'))
        
        # Poblaciones
        poblacion_familiar = random.choice(d_poblacion.to_dict('records'))
        poblacion_centro = random.choice(d_poblacion.to_dict('records'))
        
        # Países
        pais_nacionalidad = random.choice(d_pais.to_dict('records'))
        pais_familiar = random.choice(d_pais.to_dict('records'))
        
        # Datos de estudio
        estudio = random.choice(d_plan.to_dict('records'))
        tipo_estudio = random.choice(d_tipo_estudio.to_dict('records'))
        rama_conocimiento = random.choice(d_rama.to_dict('records'))
        
        # Datos de centro
        centro_inicio = random.choice(d_centro.to_dict('records'))
        tipo_centro = random.choice(d_tipo_centro.to_dict('records'))
        campus_centro = random.choice(d_campus.to_dict('records'))
        
        # Edad
        edad_ingreso = random.randint(17, 65)
        id_edad_est = random.choice(d_edad_est.to_dict('records'))['ID_EDAD_EST']
        
        # Datos de graduación y abandono
        curso_graduacion = None
        curso_abandono = None
        curso_traslado = None
        
        # Definir si el estudiante se ha graduado, abandonado o trasladado
        graduado = random.choice([0, 1])
        traslado = 0 if graduado == 1 else random.choice([0, 1])
        abandono_generico = 0 if (graduado == 1 or traslado == 1) else random.choice([0, 1])
        abandono_oficial = abandono_generico * random.choice([0, 1])
        
        # Fechas para cálculos
        fecha_actual = datetime.datetime.now().date()
        
        # Asignar cursos posteriores si hay disponibles
        if cursos_posteriores:
            if graduado == 1:
                curso_graduacion = random.choice(cursos_posteriores)
            if abandono_generico == 1:
                curso_abandono = random.choice(cursos_posteriores)
            if traslado == 1:
                curso_traslado = random.choice(cursos_posteriores)
        
        # Datos de rendimiento académico - evitar NaN
        creditos_necesarios = float(random.randint(180, 360))
        creditos_matriculados = creditos_necesarios + float(random.randint(0, 60))
        creditos_superados = float(random.randint(int(creditos_necesarios - 60) if graduado == 0 else int(creditos_necesarios), int(creditos_matriculados)))
        creditos_presentados = creditos_superados + float(random.randint(0, 30))
        creditos_suspendidos = creditos_presentados - creditos_superados
        creditos_reconocidos = float(random.randint(0, 30))
        creditos_transferidos = float(random.randint(0, 20))
        
        # Indicadores de rendimiento
        cursos_matriculados = random.randint(1, 6)
        curso_mas_alto_matriculado = random.randint(1, 6)
        cursos_extra_graduacion = max(0, cursos_matriculados - 4) if graduado == 1 else 0
        
        # Calificación final (solo para graduados) - evitar NaN
        calificacion_final = round(random.uniform(5.0, 10.0), 2) if graduado == 1 else 0.0
        
        # Flags booleanos
        flg_nuevo_ingreso = random.choice([0, 1])
        flg_abandono_inicial = 1 if abandono_generico == 1 and cursos_matriculados <= 2 else 0
        flg_graduado_en_tiempo = 1 if graduado == 1 and cursos_matriculados <= 4 else 0
        flg_plan_oficial = random.choice([0, 1])
        flg_tasa_abandono = 1 if abandono_generico == 1 else 0
        flg_tasa_graduacion = 1 if graduado == 1 else 0
        flg_calculo_tasa = random.choice([0, 1])
        flg_traslado_mismo_estudio = random.choice([0, 1]) if traslado == 1 else 0
        
        # Flags de cálculos para tasas de seguimiento
        flg_c_abandonoini = random.choice([0, 1])
        flg_c_abandono = random.choice([0, 1])
        flg_c_idoneidad = random.choice([0, 1])
        flg_c_graduacion = random.choice([0, 1])
        
        # Fechas para cálculos - usar objetos date directos
        fe_c_abandonoini = datetime.date(2020 + random.randint(0, 3), random.randint(1, 12), random.randint(1, 28)) if flg_c_abandonoini == 1 else None
        fe_c_abandono = datetime.date(2020 + random.randint(0, 3), random.randint(1, 12), random.randint(1, 28)) if flg_c_abandono == 1 else None
        fe_c_idoneidad = datetime.date(2020 + random.randint(0, 3), random.randint(1, 12), random.randint(1, 28)) if flg_c_idoneidad == 1 else None
        fe_c_graduacion = datetime.date(2020 + random.randint(0, 3), random.randint(1, 12), random.randint(1, 28)) if flg_c_graduacion == 1 else None
        
        # Nota de admisión
        nota_admision = round(random.uniform(5.0, 14.0), 2)
        
        # Flags adicionales para titulación múltiple
        flg_multiple_titulacion = random.choice([0, 1])
        flg_graduado_idoneo = 1 if graduado == 1 and flg_graduado_en_tiempo == 1 else 0
        
        data.append({
            'ID_CURSO_ACADEMICO_COHORTE_NK': curso_cohorte['ID_CURSO_ACADEMICO_NK'],
            'ID_EXPEDIENTE_ACADEMICO_NK': id_expediente,
            'ID_CURSO_ACADEMICO_COHORTE': curso_cohorte['ID_CURSO_ACADEMICO'],
            'ID_EXPEDIENTE_ACADEMICO': id_expediente,
            'ID_PLAN_ESTUDIO': plan['ID_PLAN_ESTUDIO'],
            'ID_CENTRO': centro['ID_CENTRO'],
            'ID_ALUMNO': persona['ID_PERSONA'],
            'ID_TIPO_ACCESO': tipo_acceso['ID_TIPO_ACCESO'],
            'ID_SEXO': sexo['ID_SEXO'],
            'ID_RANGO_CREDITOS_MATRICULADOS': random.randint(1, 5),
            'ID_RANGO_CREDITOS_SUPERADOS': random.randint(1, 5),
            'ID_CURSO_ACAD_GRADUACION': curso_graduacion or 0,
            'ID_CURSO_ACAD_ABANDONO': curso_abandono or 0,
            'ID_CURSO_ACAD_TRASLADO': curso_traslado or 0,
            'ID_RANGO_CALIFICACION_FINAL': random.randint(1, 5) if graduado == 1 else 0,
            'ID_TIPO_ABANDONO': tipo_abandono['ID_TIPO_ABANDONO'],
            'EDAD_INGRESO': edad_ingreso,
            'DURACION': random.randint(1, 8),
            'CREDITOS_NECESARIOS': creditos_necesarios,
            'CREDITOS_MATRICULADOS': creditos_matriculados,
            'CREDITOS_SUPERADOS': creditos_superados,
            'CREDITOS_PRESENTADOS': creditos_presentados,
            'CREDITOS_SUSPENDIDOS': creditos_suspendidos,
            'CREDITOS_RECONOCIDOS': creditos_reconocidos,
            'CREDITOS_TRANSFERIDOS': creditos_transferidos,
            'GRADUADO': graduado,
            'TRASLADO': traslado,
            'INGRESO': 1,  # Siempre es 1 para registros de cohorte
            'FLG_NUEVO_INGRESO': flg_nuevo_ingreso,
            'FLG_ABANDONO_INICIAL': flg_abandono_inicial,
            'FLG_GRADUADO_EN_TIEMPO': flg_graduado_en_tiempo,
            'FECHA_CARGA': datetime.date.today(),
            'SN_GRADUADO_EN_TIEMPO': 'S' if flg_graduado_en_tiempo == 1 else 'N',
            'NOTA_ADMISION': nota_admision,
            'ABANDONO_GENERICO': abandono_generico,
            'ABANDONO_OFICIAL': abandono_oficial,
            'FLG_PLAN_OFICIAL': flg_plan_oficial,
            'FLG_TASA_ABANDONO': flg_tasa_abandono,
            'FLG_TASA_GRADUACION': flg_tasa_graduacion,
            'FLG_CALCULO_TASA': flg_calculo_tasa,
            'ID_ESTUDIO_PREVIO': estudio_previo['ID_ESTUDIO_PREVIO'],
            'ID_PAIS_NACIONALIDAD': pais_nacionalidad['ID_PAIS'],
            'ID_POBLACION_FAMILIAR': poblacion_familiar['ID_POBLACION'],
            'ID_ESTUDIO': estudio['ID_PLAN_ESTUDIO'],  # Usando el mismo ID que el plan
            'ID_CENTRO_INICIO': centro_inicio['ID_CENTRO'],
            'FLG_TRASLADO_MISMO_ESTUDIO': flg_traslado_mismo_estudio,
            'ID_FECHA_CARGA': int(datetime.date.today().strftime('%Y%m%d')),
            'ID_TIPO_ESTUDIO': tipo_estudio['ID_TIPO_ESTUDIO'],
            'ID_TIPO_CENTRO': tipo_centro['ID_TIPO_CENTRO'],
            'ID_CAMPUS_CENTRO': campus_centro['ID_CAMPUS'],
            'ID_RAMA_CONOCIMIENTO': rama_conocimiento['ID_RAMA_MACROAREA'],
            'ID_POBLACION_CENTRO': poblacion_centro['ID_POBLACION'],
            'ID_PERSONA_NIP_NK': persona['ID_PERSONA_NIP_NK'],
            'CURSOS_MATRICULADOS': cursos_matriculados,
            'CURSO_MAS_ALTO_MATRICULADO': curso_mas_alto_matriculado,
            'CURSOS_EXTRA_GRADUACION': cursos_extra_graduacion,
            'CALIFICACION_FINAL': calificacion_final,
            'SN_ABANDONO_INICIAL': 'S' if flg_abandono_inicial == 1 else 'N',
            'SN_GRADUADO': 'S' if graduado == 1 else 'N',
            'SN_ABANDONO_OFICIAL': 'S' if abandono_oficial == 1 else 'N',
            'ID_PAIS_FAMILIAR': pais_familiar['ID_PAIS'],
            'ID_PAIS_FAMILIAR_NK': pais_familiar.get('ID_PAIS_NK', ''),
            'ID_EDAD_EST': id_edad_est,
            'FLG_GRADUADO_IDONEO': flg_graduado_idoneo,
            'SN_GRADUADO_IDONEO': 'S' if flg_graduado_idoneo == 1 else 'N',
            'FLG_MULTIPLE_TITULACION': flg_multiple_titulacion,
            'SN_MULTIPLE_TITULACION': 'S' if flg_multiple_titulacion == 1 else 'N',
            'FLG_C_ABANDONOINI': flg_c_abandonoini,
            'FLG_C_ABANDONO': flg_c_abandono,
            'FLG_C_IDONEIDAD': flg_c_idoneidad,
            'FLG_C_GRADUACION': flg_c_graduacion,
            'FE_C_ABANDONOINI': fe_c_abandonoini,
            'FE_C_ABANDONO': fe_c_abandono,
            'FE_C_IDONEIDAD': fe_c_idoneidad,
            'FE_C_GRADUACION': fe_c_graduacion,
            'FECHA_ACTUAL': generate_random_date(2020, 2023),
        })
    
    return pd.DataFrame(data) 