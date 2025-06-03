import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta, date
from tqdm import tqdm
from faker import Faker


def generate_random_date(start_year, end_year):
    """Genera una fecha aleatoria entre los años especificados como string 'YYYY-MM-DD'"""
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime('%Y-%m-%d')


fake = Faker(['es_ES'])


def generate_f_doctorado_admision(n=200, dimension_dfs=None):
    """
    Genera datos para la tabla F_DOCTORADO_ADMISION con todos sus atributos
    
    Args:
        n (int): Número de filas a generar
        dimension_dfs (dict): Diccionario con DataFrames de dimensiones necesarias
        
    Returns:
        DataFrame: DataFrame con los datos generados para la tabla F_DOCTORADO_ADMISION
    """
    data = []
    if dimension_dfs is None or not all(key in dimension_dfs for key in [
        'd_curso_academico', 'd_curso_cohorte', 'd_plan_estudio',
        'd_estudio', 'd_rama_conocimiento', 'd_centro', 'd_persona',
        'd_pais', 'd_sexo', 'd_estado_solicitud_doctorado', 'd_dedicacion',
        'd_universidad']):
        raise ValueError(
            'Se deben proporcionar todos los DataFrames de dimensiones necesarios'
            )
    d_curso = dimension_dfs['d_curso_academico']
    d_curso_cohorte = dimension_dfs['d_curso_cohorte']
    d_plan_estudio = dimension_dfs['d_plan_estudio']
    d_estudio = dimension_dfs['d_estudio']
    d_rama = dimension_dfs['d_rama_conocimiento']
    d_centro = dimension_dfs['d_centro']
    d_persona = dimension_dfs['d_persona']
    d_pais = dimension_dfs['d_pais']
    d_sexo = dimension_dfs['d_sexo']
    d_estado_sol = dimension_dfs['d_estado_solicitud_doctorado']
    d_dedicacion = dimension_dfs['d_dedicacion']
    d_universidad = dimension_dfs['d_universidad']
    fecha_referencia = datetime.now()
    for i in tqdm(range(1, n + 1), desc=
        'Generando solicitudes de admisión de doctorado'):
        curso = random.choice(d_curso.to_dict('records'))
        plan = random.choice(d_plan_estudio.to_dict('records'))
        estudio = random.choice(d_estudio.to_dict('records'))
        rama = random.choice(d_rama.to_dict('records'))
        centro = random.choice(d_centro.to_dict('records'))
        persona = random.choice(d_persona.to_dict('records'))
        estado_sol = random.choice(d_estado_sol.to_dict('records'))
        dedicacion = random.choice(d_dedicacion.to_dict('records'))
        universidad_origen = random.choice(d_universidad.to_dict('records'))
        id_solicitud_nk = i + 10000
        id_expediente_academico_nk = i + 20000
        flg_matriculado = random.choice([0, 1])
        sn_matriculado = 'S' if flg_matriculado == 1 else 'N'
        flg_nuevo_ingreso = random.choice([0, 1])
        sn_nuevo_ingreso = 'S' if flg_nuevo_ingreso == 1 else 'N'
        flg_complemento_formacion = random.choice([0, 1])
        sn_complemento_formacion = ('S' if flg_complemento_formacion == 1 else
            'N')
        flg_tiempo_parcial = random.choice([0, 1])
        pais_nacionalidad = random.choice(d_pais.to_dict('records'))
        flg_extranjero = 1 if pais_nacionalidad['ID_PAIS'] != 1 else 0
        flg_otra_universidad = random.choice([0, 1])
        flg_otra_universidad_denom = 1 if flg_otra_universidad == 1 else 0
        if persona['SEXO'] == 'H':
            id_sexo_alumno = 1
        else:
            id_sexo_alumno = 2
        data.append({'ID_CURSO_ACADEMICO_NK': curso['ID_CURSO_ACADEMICO_NK'
            ], 'ESTADO_INSCRIPCION': estado_sol[
            'ID_ESTADO_SOL_DOCTORADO_NK'], 'ID_SOLICITUD_NK':
            id_solicitud_nk, 'ID_EXPEDIENTE_ACADEMICO_NK':
            id_expediente_academico_nk, 'SN_MATRICULADO': sn_matriculado,
            'FECHA_REFERENCIA': fecha_referencia - timedelta(days=random.
            randint(0, 365)), 'ID_CURSO_ACADEMICO': curso[
            'ID_CURSO_ACADEMICO'], 'ID_PLAN_ESTUDIO': plan[
            'ID_PLAN_ESTUDIO'], 'ID_ESTUDIO': estudio['ID_ESTUDIO'],
            'ID_RAMA_CONOCIMIENTO': rama['ID_RAMA_MACROAREA'], 'ID_CENTRO':
            centro['ID_CENTRO'], 'ID_ALUMNO': persona['ID_PERSONA'],
            'SEXO_ALUMNO': persona['SEXO'], 'ID_PAIS_NACIONALIDAD_ALUMNO':
            pais_nacionalidad['ID_PAIS'], 'FECHA_CARGA': datetime.now(),
            'ID_FECHA_CARGA': int(datetime.now().strftime('%Y%m%d')),
            'ID_PERSONA_NIP_NK': persona['ID_PERSONA_NIP_NK'],
            'ID_CENTRO_NK': centro['ID_CENTRO_NK'], 'ID_PLAN_ESTUDIO_NK':
            plan['ID_PLAN_ESTUDIO_NK'], 'SN_NUEVO_INGRESO':
            sn_nuevo_ingreso, 'ID_ESTADO_SOL_DOCTORADO': estado_sol[
            'ID_ESTADO_SOL_DOCTORADO'], 'SN_COMPLEMENTO_FORMACION':
            sn_complemento_formacion, 'FLG_MATRICULADO': flg_matriculado,
            'FLG_NUEVO_INGRESO': flg_nuevo_ingreso,
            'FLG_COMPLEMENTO_FORMACION': flg_complemento_formacion,
            'FLG_TIEMPO_PARCIAL': flg_tiempo_parcial, 'ID_DEDICACION_NK':
            dedicacion['ID_DEDICACION_NK'], 'ID_DEDICACION': dedicacion[
            'ID_DEDICACION'], 'FLG_EXTRANJERO': flg_extranjero,
            'ID_PAIS_NACIONALIDAD_ALUMNO_NK': pais_nacionalidad[
            'ID_PAIS_NK'], 'FLG_OTRA_UNIVERSIDAD': flg_otra_universidad,
            'ID_UNIVERSIDAD_ORIGEN': universidad_origen['ID_UNIVERSIDAD'],
            'FLG_OTRA_UNIVERSIDAD_DENOM': flg_otra_universidad_denom,
            'ID_ESTUDIO_NK': estudio['ID_ESTUDIO_NK'],
            'ID_UNIVERSIDAD_ORIGEN_NK': universidad_origen[
            'ID_UNIVERSIDAD_NK'], 'ID_SEXO_ALUMNO': id_sexo_alumno})
    return pd.DataFrame(data)


def generate_f_egracons(n=300, dimension_dfs=None):
    """
    Genera datos para la tabla F_EGRACONS (European Grading System)
    
    Args:
        n (int): Número de filas a generar
        dimension_dfs (dict): Diccionario con DataFrames de dimensiones necesarias
        
    Returns:
        DataFrame: DataFrame con los datos generados para la tabla F_EGRACONS
    """
    data = []
    if dimension_dfs is None or not all(key in dimension_dfs for key in [
        'd_curso_academico', 'd_plan_estudio', 'd_centro', 'd_poblacion',
        'd_asignatura', 'd_clase_asignatura', 'd_calificacion',
        'd_rango_nota_numerica', 'd_rango_nota_egracons',
        'd_programa_movilidad', 'd_estudio']):
        raise ValueError(
            'Se deben proporcionar todos los DataFrames de dimensiones necesarios'
            )
    d_curso = dimension_dfs['d_curso_academico']
    d_plan_estudio = dimension_dfs['d_plan_estudio']
    d_centro = dimension_dfs['d_centro']
    d_poblacion = dimension_dfs['d_poblacion']
    d_asignatura = dimension_dfs['d_asignatura']
    d_clase_asignatura = dimension_dfs['d_clase_asignatura']
    d_calificacion = dimension_dfs['d_calificacion']
    d_rango_nota_numerica = dimension_dfs['d_rango_nota_numerica']
    d_rango_nota_egracons = dimension_dfs['d_rango_nota_egracons']
    d_programa_movilidad = dimension_dfs['d_programa_movilidad']
    d_estudio = dimension_dfs['d_estudio']
    for i in tqdm(range(1, n + 1), desc='Generando datos EGRACONS'):
        curso_egracons = random.choice(d_curso.to_dict('records'))
        curso_calificacion = random.choice(d_curso.to_dict('records'))
        alumno_id = random.randint(1, 1000)
        expediente_id = random.randint(10000, 20000)
        expediente_asignatura = random.randint(1, 500)
        plan = random.choice(d_plan_estudio.to_dict('records'))
        centro = random.choice(d_centro.to_dict('records'))
        poblacion_centro = random.choice(d_poblacion.to_dict('records'))
        asignatura = random.choice(d_asignatura.to_dict('records'))
        clase_asignatura = random.choice(d_clase_asignatura.to_dict('records'))
        calificacion = random.choice(d_calificacion.to_dict('records'))
        rango_nota_numerica = random.choice(d_rango_nota_numerica.to_dict(
            'records'))
        rango_nota_egracons = random.choice(d_rango_nota_egracons.to_dict(
            'records'))
        programa_movilidad = random.choice(d_programa_movilidad.to_dict(
            'records'))
        estudio = random.choice(d_estudio.to_dict('records'))
        tipo_estudio_id = random.randint(1, 5)
        tipo_asignatura_id = random.randint(1, 10)
        plan_grupo_matricula_id = random.randint(1, 100)
        centro_imparticion_id = random.randint(1, 50)
        estudio_asignatura_id = random.randint(1, 200)
        creditos = round(random.uniform(3.0, 12.0), 1)
        nota_numerica = round(random.uniform(0.0, 10.0), 2)
        flg_entrada = random.choice(['S', 'N'])
        sn_programa_internacional = 'S' if random.random() > 0.7 else 'N'
        data.append({'ID_CURSO_EGRACONS': curso_egracons[
            'ID_CURSO_ACADEMICO'], 'ID_CURSO_EGRACONS_NK': curso_egracons[
            'ID_CURSO_ACADEMICO_NK'], 'ID_CURSO_ACADEMICO_CALIFIC':
            curso_calificacion['ID_CURSO_ACADEMICO'],
            'ID_CURSO_ACADEMICO_CALIFIC_NK': curso_calificacion[
            'ID_CURSO_ACADEMICO_NK'], 'ID_ALUMNO': alumno_id,
            'ID_EXPEDIENTE_ACADEMICO': expediente_id,
            'ID_EXPEDIENTE_ACADEMICO_NK': expediente_id,
            'EXPEDIENTE_ASIGNATURA': expediente_asignatura,
            'ID_TIPO_ESTUDIO': tipo_estudio_id, 'ID_ESTUDIO': estudio[
            'ID_ESTUDIO'], 'ID_PLAN_ESTUDIO': plan['ID_PLAN_ESTUDIO'],
            'ID_RAMA_CONOCIMIENTO': random.randint(1, 5), 'ID_CENTRO':
            centro['ID_CENTRO'], 'ID_CENTRO_NK': centro['ID_CENTRO_NK'],
            'ID_POBLACION_CENTRO': poblacion_centro['ID_POBLACION'],
            'ID_ASIGNATURA': asignatura['ID_ASIGNATURA'],
            'ID_ASIGNATURA_NK': asignatura['ID_ASIGNATURA_NK'],
            'ID_TIPO_ASIGNATURA': tipo_asignatura_id, 'ID_CLASE_ASIGNATURA':
            clase_asignatura['ID_CLASE_ASIGNATURA'], 'CREDITOS': creditos,
            'NOTA_NUMERICA': nota_numerica, 'ID_CALIFICACION': calificacion
            ['ID_CALIFICACION'], 'ID_CALIFICACION_NK': calificacion[
            'ID_CALIFICACION_NK'], 'ID_RANGO_NOTA_NUMERICA':
            rango_nota_numerica['ID_RANGO_NOTA_NUMERICA'],
            'ID_RANGO_NOTA_EGRACONS': rango_nota_egracons[
            'ID_RANGO_NOTA_EGRACONS'], 'ID_PLAN_GRUPO_MATRICULA':
            plan_grupo_matricula_id, 'ID_PLAN_GRUPO_MATRICULA_NK':
            plan_grupo_matricula_id, 'ID_CENTRO_IMPARTICION':
            centro_imparticion_id, 'ID_CENTRO_IMPARTICION_NK':
            centro_imparticion_id, 'ID_ESTUDIO_ASIGNATURA':
            estudio_asignatura_id, 'ID_ESTUDIO_ASIGNATURA_NK':
            estudio_asignatura_id, 'ID_TIPO_ESTUDIO_ASIGNATURA':
            tipo_estudio_id, 'ID_TIPO_ESTUDIO_ASIGNATURA_NK':
            tipo_estudio_id, 'ID_RAMA_CONOCIMIENTO_ASIG': random.randint(1,
            5), 'ID_RAMA_CONOCIMIENTO_ASIG_NK': chr(random.randint(65, 69)),
            'ID_ESTUDIO_NK': estudio['ID_ESTUDIO_NK'],
            'ID_PROGRAMA_MOVILIDAD': programa_movilidad[
            'ID_PROGRAMA_MOVILIDAD'], 'ID_PROGRAMA_MOVILIDAD_NK':
            programa_movilidad['ID_PROGRAMA_MOVILIDAD_NK'], 'FLG_ENTRADA':
            flg_entrada, 'SN_PROGRAMA_INTERNACIONAL':
            sn_programa_internacional})
    return pd.DataFrame(data)


def generate_f_estudio_propio_matricula(n=300, dimension_dfs=None):
    """
    Genera datos para la tabla F_ESTUDIO_PROPIO_MATRICULA
    
    Args:
        n (int): Número de filas a generar
        dimension_dfs (dict): Diccionario con DataFrames de dimensiones necesarias
        
    Returns:
        DataFrame: DataFrame con los datos generados para F_ESTUDIO_PROPIO_MATRICULA
    """
    data = []
    if dimension_dfs is None or not all(key in dimension_dfs for key in [
        'd_curso_academico', 'd_curso_cohorte', 'd_persona',
        'd_estudio_propio', 'd_estudio_propio_tipo',
        'd_estudio_propio_modalidad', 'd_centro', 'd_pais', 'd_poblacion',
        'd_sexo', 'd_edad_est', 'd_estudio_propio_organo_gest']):
        raise ValueError(
            'Se deben proporcionar todos los DataFrames de dimensiones necesarios'
            )
    d_curso = dimension_dfs['d_curso_academico']
    d_curso_cohorte = dimension_dfs['d_curso_cohorte']
    d_persona = dimension_dfs['d_persona']
    d_estudio_propio = dimension_dfs['d_estudio_propio']
    d_estudio_propio_tipo = dimension_dfs['d_estudio_propio_tipo']
    d_estudio_propio_modalidad = dimension_dfs['d_estudio_propio_modalidad']
    d_centro = dimension_dfs['d_centro']
    d_pais = dimension_dfs['d_pais']
    d_poblacion = dimension_dfs['d_poblacion']
    d_sexo = dimension_dfs['d_sexo']
    d_edad_est = dimension_dfs['d_edad_est']
    d_organo_gest = dimension_dfs['d_estudio_propio_organo_gest']
    for i in tqdm(range(1, n + 1), desc=
        'Generando matrículas de estudios propios'):
        curso = random.choice(d_curso.to_dict('records'))
        persona = random.choice(d_persona.to_dict('records'))
        estudio_propio = random.choice(d_estudio_propio.to_dict('records'))
        tipo_estudio_propio = random.choice(d_estudio_propio_tipo.to_dict(
            'records'))
        modalidad_estudio_propio = random.choice(d_estudio_propio_modalidad
            .to_dict('records'))
        centro = random.choice(d_centro.to_dict('records'))
        pais_nacionalidad = random.choice(d_pais.to_dict('records'))
        pais_procedencia = random.choice(d_pais.to_dict('records'))
        poblacion_familiar = random.choice(d_poblacion.to_dict('records'))
        poblacion_curso = random.choice(d_poblacion.to_dict('records'))
        edad_est = random.choice(d_edad_est.to_dict('records'))
        organo_proponente = random.choice(d_organo_gest.to_dict('records'))
        id_expediente_est_propio_nk = i + 30000
        id_expediente_est_propio = i + 30000
        flg_nuevo_ingreso = random.choice([0, 1])
        sn_nuevo_ingreso = 'S' if flg_nuevo_ingreso == 1 else 'N'
        flg_estudiante_internacional = 1 if pais_nacionalidad['ID_PAIS'
            ] != 1 else 0
        sn_estudiante_internacional = ('S' if flg_estudiante_internacional ==
            1 else 'N')
        total_creditos_ep = random.randint(10, 120)
        numero_cursos_ep = random.randint(1, 4)
        creditos_matriculados = round(random.uniform(10, total_creditos_ep), 1)
        fecha_matricula = datetime.now() - timedelta(days=random.randint(0,
            365))
        id_fecha_matricula = int(fecha_matricula.strftime('%Y%m%d'))
        fecha_nacimiento = datetime.now() - timedelta(days=random.randint(
            8000, 25000))
        edad = (datetime.now() - fecha_nacimiento).days // 365
        cod_postal_familiar = (
            f'{random.randint(1, 52):02d}{random.randint(1, 999):03d}')
        cod_postal_curso = (
            f'{random.randint(1, 52):02d}{random.randint(1, 999):03d}')
        ano_acad_apertura = curso['ID_CURSO_ACADEMICO_NK'] - random.randint(
            0, 5)
        sexo = persona['SEXO']
        if sexo == 'H':
            id_sexo = 1
        else:
            id_sexo = 2
        data.append({'ID_CURSO_ACADEMICO_NK': curso['ID_CURSO_ACADEMICO_NK'
            ], 'ID_CURSO_ACADEMICO': curso['ID_CURSO_ACADEMICO'],
            'ID_EXPEDIENTE_EST_PROPIO_NK': id_expediente_est_propio_nk,
            'ID_EXPEDIENTE_EST_PROPIO': id_expediente_est_propio,
            'ID_PERSONA_NIP_NK': persona['ID_PERSONA_NIP_NK'], 'ID_PERSONA':
            persona['ID_PERSONA'], 'ID_ESTUDIO_PROPIO_NK': estudio_propio[
            'ID_ESTUDIO_PROPIO_NK'], 'ID_ESTUDIO_PROPIO_EDICION_NK':
            estudio_propio['ID_ESTUDIO_PROPIO_EDICION_NK'],
            'ID_ESTUDIO_PROPIO': estudio_propio['ID_ESTUDIO_PROPIO'],
            'ID_ESTUDIO_PROPIO_TIPO_NK': tipo_estudio_propio[
            'ID_ESTUDIO_PROPIO_TIPO_NK'], 'ID_ESTUDIO_PROPIO_TIPO':
            tipo_estudio_propio['ID_ESTUDIO_PROPIO_TIPO'],
            'ID_ESTUDIO_PROPIO_MODALIDAD_NK': modalidad_estudio_propio[
            'ID_ESTUDIO_PROPIO_MODALIDAD_NK'],
            'ID_ESTUDIO_PROPIO_MODALIDAD': modalidad_estudio_propio[
            'ID_ESTUDIO_PROPIO_MODALIDAD'], 'TOTAL_CREDITOS_EP':
            total_creditos_ep, 'NUMERO_CURSOS_EP': numero_cursos_ep,
            'ID_CENTRO_DEPT_GESTION_EP_NK': centro['ID_CENTRO_NK'],
            'ID_CENTRO_DEPT_GESTION_EP': centro['ID_CENTRO'],
            'ID_RAMA_CONOCIMIENTO_EP_NK': random.randint(1, 5),
            'ID_RAMA_ESTUDIO_PROPIO': random.randint(1, 5),
            'ANO_ACAD_APERTURA': ano_acad_apertura, 'CREDITOS_MATRICULADOS':
            creditos_matriculados, 'FECHA_MATRICULA': fecha_matricula,
            'ID_FECHA_MATRICULA': id_fecha_matricula, 'FLG_NUEVO_INGRESO':
            flg_nuevo_ingreso, 'SN_NUEVO_INGRESO': sn_nuevo_ingreso,
            'FLG_ESTUDIANTE_INTERNACIONAL': flg_estudiante_internacional,
            'SN_ESTUDIANTE_INTERNACIONAL': sn_estudiante_internacional,
            'ID_PAIS_NACIONALIDAD': pais_nacionalidad['ID_PAIS'],
            'ID_PAIS_NACIONALIDAD_NK': pais_nacionalidad['ID_PAIS_NK'],
            'DOCUMENTO_IDENTIDAD': persona['DOCUMENTO_IDENTIDAD'],
            'FECHA_NACIMIENTO': fecha_nacimiento, 'ID_PAIS_PROCEDENCIA':
            pais_procedencia['ID_PAIS'], 'ID_PAIS_PROCEDENCIA_NK':
            pais_procedencia['ID_PAIS_NK'], 'ID_POBLACION_FAMILIAR':
            poblacion_familiar['ID_POBLACION'], 'COD_POSTAL_FAMILIAR':
            cod_postal_familiar, 'ID_POBLACION_CURSO': poblacion_curso[
            'ID_POBLACION'], 'ID_PAIS_CURSO': poblacion_curso['ID_PAIS'],
            'COD_POSTAL_CURSO': cod_postal_curso, 'SEXO': sexo, 'ID_SEXO':
            id_sexo, 'EDAD': edad, 'FECHA_CARGA': datetime.now(),
            'ID_FECHA_CARGA': int(datetime.now().strftime('%Y%m%d')),
            'ID_ORGANO_PROPONENTE_EP_NK': organo_proponente[
            'ID_ORGANO_GESTION_EP_NK'], 'ID_ORGANO_PROPONENTE_EP':
            organo_proponente['ID_ORGANO_GESTION_EP'], 'EDAD_EST': edad_est
            ['ID_EDAD_EST_NK'], 'ID_EDAD_EST': edad_est['ID_EDAD_EST']})
    return pd.DataFrame(data)


def generate_f_doctorado(n=200, dimension_dfs=None):
    """
    Genera datos para la tabla F_DOCTORADO con todos sus atributos
    
    Args:
        n (int): Número de filas a generar
        dimension_dfs (dict): Diccionario con DataFrames de dimensiones necesarias
        
    Returns:
        DataFrame: DataFrame con los datos generados para la tabla F_DOCTORADO
    """
    data = []
    if dimension_dfs is None or not all(key in dimension_dfs for key in [
        'd_curso_academico', 'd_plan_estudio', 'd_estudio', 'd_persona',
        'd_centro', 'd_asignatura', 'd_tipo_asignatura', 'd_calificacion',
        'd_pais', 'd_sexo', 'd_dedicacion', 'd_doctorado_tipo_beca',
        'd_dedicacion_profesor', 'd_situacion_administrativa',
        'd_categoria_cuerpo_pdi', 'd_rama_conocimiento',
        'd_proyecto_investigacion']):
        raise ValueError(
            'Se deben proporcionar todos los DataFrames de dimensiones necesarios'
            )
    d_curso = dimension_dfs['d_curso_academico']
    d_plan_estudio = dimension_dfs['d_plan_estudio']
    d_estudio = dimension_dfs['d_estudio']
    d_persona = dimension_dfs['d_persona']
    d_centro = dimension_dfs['d_centro']
    d_asignatura = dimension_dfs['d_asignatura']
    d_tipo_asignatura = dimension_dfs['d_tipo_asignatura']
    d_calificacion = dimension_dfs['d_calificacion']
    d_pais = dimension_dfs['d_pais']
    d_sexo = dimension_dfs['d_sexo']
    d_dedicacion = dimension_dfs['d_dedicacion']
    d_tipo_beca = dimension_dfs['d_doctorado_tipo_beca']
    d_dedicacion_profesor = dimension_dfs['d_dedicacion_profesor']
    d_situacion_adva = dimension_dfs['d_situacion_administrativa']
    d_categoria_pdi = dimension_dfs['d_categoria_cuerpo_pdi']
    d_rama = dimension_dfs['d_rama_conocimiento']
    d_proyecto = dimension_dfs['d_proyecto_investigacion']
    for i in tqdm(range(1, n + 1), desc='Generando datos de doctorado'):
        curso_informe = random.choice(d_curso.to_dict('records'))
        curso_matricula = random.choice(d_curso.to_dict('records'))
        alumno = random.choice(d_persona.to_dict('records'))
        profesor = random.choice(d_persona.to_dict('records'))
        centro = random.choice(d_centro.to_dict('records'))
        plan_estudio = random.choice(d_plan_estudio.to_dict('records'))
        estudio = random.choice(d_estudio.to_dict('records'))
        asignatura = random.choice(d_asignatura.to_dict('records'))
        tipo_asignatura = random.choice(d_tipo_asignatura.to_dict('records'))
        calificacion = random.choice(d_calificacion.to_dict('records'))
        pais_nacionalidad_alumno = random.choice(d_pais.to_dict('records'))
        pais_nacionalidad_prof = random.choice(d_pais.to_dict('records'))
        dedicacion_alumno = random.choice(d_dedicacion.to_dict('records'))
        dedicacion_profesor = random.choice(d_dedicacion_profesor.to_dict(
            'records'))
        tipo_beca = random.choice(d_tipo_beca.to_dict('records'))
        situacion_adva = random.choice(d_situacion_adva.to_dict('records'))
        categoria_cuerpo = random.choice(d_categoria_pdi.to_dict('records'))
        rama = random.choice(d_rama.to_dict('records'))
        proyecto = random.choice(d_proyecto.to_dict('records'))
        flg_nuevo_ingreso = random.choice([0, 1])
        sn_nuevo_ingreso = 'S' if flg_nuevo_ingreso == 1 else 'N'
        flg_en_programa_movilidad = random.choice([0, 1])
        sn_en_programa_movilidad = ('S' if flg_en_programa_movilidad == 1 else
            'N')
        flg_tutor = random.choice([0, 1])
        sn_tutor = 'S' if flg_tutor == 1 else 'N'
        flg_director = random.choice([0, 1])
        sn_director = 'S' if flg_director == 1 else 'N'
        flg_sexenio_vivo = random.choice([0, 1])
        flg_tiempo_parcial = random.choice([0, 1])
        flg_extranjero = 1 if pais_nacionalidad_alumno['ID_PAIS'] != 1 else 0
        flg_profesor = 1
        flg_tesis_cum_laude = random.choice([0, 1])
        flg_tesis_leida = random.choice([0, 1])
        flg_presentada = random.choice([0, 1])
        flg_otra_universidad = random.choice([0, 1])
        flg_otra_universidad_denom = 1 if flg_otra_universidad == 1 else 0
        fecha_lectura = date(2020 + random.randint(0, 3), random.randint(1,
            12), random.randint(1, 28)) if flg_tesis_leida == 1 else None
        fecha_matricula = date(2018 + random.randint(0, 5), random.randint(
            1, 12), random.randint(1, 28))
        fecha_calificacion = date(2020 + random.randint(0, 3), random.
            randint(1, 12), random.randint(1, 28)
            ) if flg_presentada == 1 else None
        fecha_referencia = date.today()
        id_fecha_lectura = int(fecha_lectura.strftime('%Y%m%d')
            ) if fecha_lectura else 0
        id_fecha_matricula = int(fecha_matricula.strftime('%Y%m%d'))
        id_fecha_carga = int(date.today().strftime('%Y%m%d'))
        duracion_bruta_tesis = float(random.randint(800, 1500)
            ) if flg_tesis_leida == 1 else 0.0
        num_regs_tesis = random.randint(1, 3) if flg_tesis_leida == 1 else 0
        dias_baja = random.choice([0, 0, 0, random.randint(1, 180)])
        duracion_neta_tesis = float(duracion_bruta_tesis - dias_baja
            ) if duracion_bruta_tesis else 0.0
        calificacion_val = calificacion['ID_CALIFICACION_NK'
            ] if 'ID_CALIFICACION_NK' in calificacion else random.choice([
            'AP', 'NT', 'SB', 'SS'])
        flg_superada = 1 if calificacion_val in ['AP', 'NT', 'SB'] else 0
        flg_presentada = 1 if calificacion_val in ['AP', 'NT', 'SB', 'SS'
            ] else 0
        flg_reconocida = random.choice([0, 1])
        flg_transferida = random.choice([0, 1])
        flg_suspendida = 1 if calificacion_val == 'SS' else 0
        sexo_alumno = alumno['SEXO']
        sexo_profesor = profesor['SEXO']
        id_sexo_alumno = 1 if sexo_alumno == 'H' else 2
        id_sexo_profesor = 1 if sexo_profesor == 'H' else 2
        num_sexenios = random.randint(0, 6)
        num_sexenios_transf = random.randint(0, 3)
        num_quinquenios = random.randint(0, 8)
        num_directores_tesis = random.randint(1, 3)
        num_regs_tesis = random.randint(1, 5)
        num_art_idx_ano_curso_uz = random.randint(0, 5)
        num_art_no_idx_ano_curso_uz = random.randint(0, 3)
        num_art_idx_ano_sig_uz = random.randint(0, 5)
        num_art_no_idx_ano_sig_uz = random.randint(0, 3)
        tot_articulos_index_uz = (num_art_idx_ano_curso_uz +
            num_art_idx_ano_sig_uz)
        tot_articulos_no_index_uz = (num_art_no_idx_ano_curso_uz +
            num_art_no_idx_ano_sig_uz)
        num_art_idx_ano_curso_rama = random.randint(0, 10)
        num_art_no_idx_ano_curso_rama = random.randint(0, 6)
        num_art_idx_ano_sig_rama = random.randint(0, 10)
        num_art_no_idx_ano_sig_rama = random.randint(0, 6)
        tot_articulos_index_rama = (num_art_idx_ano_curso_rama +
            num_art_idx_ano_sig_rama)
        tot_articulos_no_index_rama = (num_art_no_idx_ano_curso_rama +
            num_art_no_idx_ano_sig_rama)
        num_art_idx_ano_curso_plan = random.randint(0, 15)
        num_art_no_idx_ano_curso_plan = random.randint(0, 8)
        num_art_idx_ano_sig_plan = random.randint(0, 15)
        num_art_no_idx_ano_sig_plan = random.randint(0, 8)
        tot_articulos_index_plan = (num_art_idx_ano_curso_plan +
            num_art_idx_ano_sig_plan)
        tot_articulos_no_index_plan = (num_art_no_idx_ano_curso_plan +
            num_art_no_idx_ano_sig_plan)
        encuesta_vals = [0, 1, 2, 3, 4, 5]
        encuesta_weights = [0.05, 0.1, 0.15, 0.25, 0.3, 0.15]
        numero_alu_encuesta_global_0 = random.randint(0, 5)
        numero_alu_encuesta_global_1 = random.randint(0, 8)
        numero_alu_encuesta_global_2 = random.randint(0, 10)
        numero_alu_encuesta_global_3 = random.randint(0, 15)
        numero_alu_encuesta_global_4 = random.randint(0, 20)
        numero_alu_encuesta_global_5 = random.randint(0, 15)
        numero_prof_encuesta_global_0 = random.randint(0, 2)
        numero_prof_encuesta_global_1 = random.randint(0, 3)
        numero_prof_encuesta_global_2 = random.randint(0, 5)
        numero_prof_encuesta_global_3 = random.randint(0, 8)
        numero_prof_encuesta_global_4 = random.randint(0, 10)
        numero_prof_encuesta_global_5 = random.randint(0, 7)
        situacion_adva = random.choice(d_situacion_adva.to_dict('records'))
        categoria_cuerpo = random.choice(d_categoria_pdi.to_dict('records'))
        id_categoria_nk = categoria_cuerpo.get('ID_CATEGORIA_CUERPO_ESCALA_NK',
            f'CC{random.randint(1, 99):02d}')
        if len(id_categoria_nk) > 5:
            id_categoria_nk = id_categoria_nk[:5]
        flg_cotutela_tesis = random.choice([0, 1])
        sn_cotutela_tesis = 'S' if flg_cotutela_tesis == 1 else 'N'
        flg_mencion_internac_tesis = random.choice([0, 1])
        sn_mencion_internac_tesis = ('S' if flg_mencion_internac_tesis == 1
             else 'N')
        sn_tesis_leida = 'S' if flg_tesis_leida == 1 else 'N'
        flg_abandono = random.choice([0, 1])
        sn_abandono = 'S' if flg_abandono == 1 else 'N'
        flg_abandono_denominador = 1 if flg_abandono == 1 else 0
        flg_profesor_uz = 1
        sn_profesor_uz = 'S' if flg_profesor_uz == 1 else 'N'
        flg_profesor_tiempo_completo = random.choice([0, 1])
        flg_becado = random.choice([0, 1])
        flg_mencion_industrial = random.choice([0, 1])
        sn_mencion_industrial = 'S' if flg_mencion_industrial == 1 else 'N'
        flg_compendio_publicaciones = random.choice([0, 1])
        sn_compendio_publicaciones = ('S' if flg_compendio_publicaciones ==
            1 else 'N')
        data.append({'ID_CURSO_INFORME_NK': curso_informe[
            'ID_CURSO_ACADEMICO_NK'], 'ID_CURSO_MATRICULA_NK':
            curso_matricula['ID_CURSO_ACADEMICO_NK'], 'ID_PERSONA_NIP_NK':
            alumno['ID_PERSONA_NIP_NK'], 'ID_CENTRO_NK': centro[
            'ID_CENTRO_NK'], 'ID_PLAN_ESTUDIO_NK': plan_estudio[
            'ID_PLAN_ESTUDIO_NK'], 'ID_EXPEDIENTE_ACADEMICO_NK': 1000000 +
            i, 'ID_DEDICACION_ALUMNO_NK': dedicacion_alumno[
            'ID_DEDICACION_NK'], 'FLG_NUEVO_INGRESO': flg_nuevo_ingreso,
            'FLG_EN_PROGRAMA_MOVILIDAD': flg_en_programa_movilidad,
            'FECHA_LECTURA_TESIS': fecha_lectura, 'SN_COTUTELA_TESIS':
            sn_cotutela_tesis, 'SN_MENCION_INTERNAC_TESIS':
            sn_mencion_internac_tesis, 'FECHA_MATRICULA': fecha_matricula,
            'ID_ASIGNATURA_NK': asignatura['ID_ASIGNATURA_NK'],
            'CALIFICACION': calificacion_val, 'FLG_SUPERADA': flg_superada,
            'FLG_PRESENTADA': flg_presentada, 'FLG_RECONOCIDA':
            flg_reconocida, 'FLG_TRANSFERIDA': flg_transferida,
            'FLG_SUSPENDIDA': flg_suspendida, 'FECHA_CALIFICACION':
            fecha_calificacion, 'ID_PROFESOR_NIP_NK': profesor[
            'ID_PERSONA_NIP_NK'], 'ID_DEDICACION_PROFESOR_NK':
            dedicacion_profesor['ID_DEDICACION_NK'], 'FLG_TUTOR': flg_tutor,
            'FLG_DIRECTOR': flg_director, 'FECHA_REFERENCIA':
            fecha_referencia, 'ID_CURSO_INFORME': curso_informe[
            'ID_CURSO_ACADEMICO'], 'ID_CURSO_MATRICULA': curso_matricula[
            'ID_CURSO_ACADEMICO'], 'ID_ALUMNO': alumno['ID_PERSONA'],
            'SEXO_ALUMNO': sexo_alumno, 'ID_PAIS_NACIONALIDAD_ALUMNO':
            pais_nacionalidad_alumno['ID_PAIS'], 'ID_DEDICACION_ALUMNO':
            dedicacion_alumno['ID_DEDICACION'], 'ID_PROFESOR': profesor[
            'ID_PERSONA'], 'SEXO_PROFESOR': sexo_profesor,
            'ID_PAIS_NACIONALIDAD_PROF': pais_nacionalidad_prof['ID_PAIS'],
            'ID_PLAN_ESTUDIO': plan_estudio['ID_PLAN_ESTUDIO'],
            'ID_ESTUDIO': estudio['ID_ESTUDIO'], 'ID_RAMA_CONOCIMIENTO':
            rama['ID_RAMA_MACROAREA'], 'ID_ASIGNATURA': asignatura[
            'ID_ASIGNATURA'], 'ID_TIPO_ASIGNATURA': tipo_asignatura[
            'ID_TIPO_ASIGNATURA'], 'ID_CALIFICACION': calificacion[
            'ID_CALIFICACION'], 'FLG_SEXENIO_VIVO': flg_sexenio_vivo,
            'ID_DEDICACION_PROFESOR': dedicacion_profesor['ID_DEDICACION'],
            'ID_FECHA_CARGA': id_fecha_carga, 'ID_CENTRO': centro[
            'ID_CENTRO'], 'SN_NUEVO_INGRESO': sn_nuevo_ingreso,
            'SN_EN_PROGRAMA_MOVILIDAD': sn_en_programa_movilidad,
            'SN_TUTOR': sn_tutor, 'SN_DIRECTOR': sn_director,
            'NUM_SEXENIOS': num_sexenios, 'FLG_TIEMPO_PARCIAL':
            flg_tiempo_parcial, 'ID_PAIS_NACIONALIDAD_ALUMNO_NK':
            pais_nacionalidad_alumno['ID_PAIS_NK'], 'FLG_EXTRANJERO':
            flg_extranjero, 'ID_FECHA_LECTURA_TESIS': id_fecha_lectura,
            'ID_FECHA_MATRICULA': id_fecha_matricula, 'FLG_PROFESOR':
            flg_profesor, 'FLG_TESIS_LEIDA': flg_tesis_leida,
            'NUM_DIRECTORES_TESIS': num_directores_tesis, 'ID_ESTUDIO_NK':
            estudio['ID_ESTUDIO_NK'], 'ID_TIPO_BECA_NK': tipo_beca[
            'ID_TIPO_BECA_NK'], 'ID_TIPO_BECA': tipo_beca['ID_TIPO_BECA'],
            'ID_TIPO_CONTRATO_NK': 'CTR' + str(random.randint(1, 99999)).
            zfill(6), 'FLG_PROFESOR_UZ': flg_profesor_uz,
            'FLG_PROFESOR_TIEMPO_COMPLETO': flg_profesor_tiempo_completo,
            'FLG_COTUTELA_TESIS': flg_cotutela_tesis,
            'FLG_MENCION_INTERNAC_TESIS': flg_mencion_internac_tesis,
            'FLG_BECADO': flg_becado, 'SN_TESIS_LEIDA': sn_tesis_leida,
            'FLG_ABANDONO': flg_abandono, 'SN_ABANDONO': sn_abandono,
            'FLG_ABANDONO_DENOMINADOR': flg_abandono_denominador,
            'DURACION_NETA_TESIS': duracion_neta_tesis,
            'FLG_TESIS_CUM_LAUDE': flg_tesis_cum_laude, 'SN_PROFESOR_UZ':
            sn_profesor_uz, 'ID_SITUACION_ADVA': situacion_adva[
            'ID_SITUACION_ADMINISTRATIVA'] if 'ID_SITUACION_ADMINISTRATIVA' in
            situacion_adva else random.randint(1, 3),
            'TOT_ARTICULOS_INDEX_UZ': fake.random_int(min=1, max=1000),
            'NUMERO_ALU_ENCUESTA_GLOBAL_0': fake.random_int(min=1, max=1000
            ), 'SN_MENCION_INDUSTRIAL': fake.random_element(elements=['S',
            'N']), 'FLG_COMPENDIO_PUBLICACIONES': fake.random_element(
            elements=[0, 1]), 'NUM_ART_IDX_ANO_SIG_UZ': fake.random_int(min
            =1, max=1000), 'TOT_ARTICULOS_NO_INDEX_PLAN': fake.random_int(
            min=1, max=1000), 'NUM_ART_NO_IDX_ANO_SIG_UZ': fake.random_int(
            min=1, max=1000), 'FECHA_RECON_SEXENIO_ESTATAL':
            generate_random_date(2020, 2023), 'ID_PROYECTO_INVESTIGACION':
            fake.random_int(min=1, max=1000), 'ID_UNIVERSIDAD_ORIGEN': fake
            .random_int(min=1, max=1000), 'FECHA_RECON_SEXENIO_AUTONOMICO':
            generate_random_date(2020, 2023), 'NUM_QUINQUENIOS': fake.
            random_int(min=1, max=1000), 'FLG_MENCION_INDUSTRIAL': fake.
            random_element(elements=[0, 1]), 'ID_CATEGORIA_CUERPO_ESCALA':
            fake.random_int(min=1, max=1000),
            'NUM_ART_NO_IDX_ANO_CURSO_RAMA': fake.random_int(min=1, max=
            1000), 'FECHA_CARGA': generate_random_date(2020, 2023),
            'NUM_ART_IDX_ANO_SIG_RAMA': fake.random_int(min=1, max=1000),
            'NUM_SEXENIO_ESTATAL': fake.random_int(min=1, max=1000),
            'FLG_SEXENIO_VIVO_CNEAI': fake.random_element(elements=[0, 1]),
            'ID_UNIVERSIDAD_ORIGEN_NK': fake.random_int(min=1, max=1000),
            'NUMERO_PROF_ENCUESTA_GLOBAL_2': fake.random_int(min=1, max=
            1000), 'NUM_SEXENIO_AUTONOMICO': fake.random_int(min=1, max=
            1000), 'FECHA_DEPOSITO_TESIS': generate_random_date(2020, 2023),
            'TOT_ARTICULOS_NO_INDEX_UZ': fake.random_int(min=1, max=1000),
            'NUMERO_ALU_ENCUESTA_GLOBAL_2': fake.random_int(min=1, max=1000
            ), 'NUMERO_ALU_ENCUESTA_GLOBAL_5': fake.random_int(min=1, max=
            1000), 'NUMERO_PROF_ENCUESTA_GLOBAL_4': fake.random_int(min=1,
            max=1000), 'TOT_ARTICULOS_INDEX_PLAN': fake.random_int(min=1,
            max=1000), 'FLG_SEXENIO_VIVO_ESTATAL': fake.random_element(
            elements=[0, 1]), 'SN_COMPENDIO_PUBLICACIONES': fake.
            random_element(elements=['S', 'N']),
            'NUMERO_PROF_ENCUESTA_GLOBAL_3': fake.random_int(min=1, max=
            1000), 'NUM_ART_NO_IDX_ANO_SIG_PLAN': fake.random_int(min=1,
            max=1000), 'FLG_SEXENIO_VIVO_AUTONOMICO': fake.random_element(
            elements=[0, 1]), 'NUM_ART_IDX_ANO_CURSO_PLAN': fake.random_int
            (min=1, max=1000), 'AMBITO_PROYECTO': fake.text(max_nb_chars=13
            ).replace('\n', ' '), 'ID_SEXO_PROFESOR': fake.random_int(min=1,
            max=1000), 'NUM_ART_NO_IDX_ANO_CURSO_PLAN': fake.random_int(min
            =1, max=1000), 'TOT_ARTICULOS_INDEX_RAMA': fake.random_int(min=
            1, max=1000), 'NUM_ART_IDX_ANO_CURSO_RAMA': fake.random_int(min
            =1, max=1000), 'SN_PRORROGA_1': fake.random_element(elements=[
            'S', 'N']), 'ID_SEXO_ALUMNO': fake.random_int(min=1, max=1000),
            'FLG_OTRA_UNIVERSIDAD_DENOM': fake.random_element(elements=[0, 
            1]), 'AUT_AMPLIACION_TESIS': fake.random_int(min=1, max=1000),
            'DIAS_BAJA': fake.random_int(min=1, max=1000),
            'NUMERO_ALU_ENCUESTA_GLOBAL_4': fake.random_int(min=1, max=1000
            ), 'ID_CATEGORIA_CUERPO_ESCALA_NK': fake.text(max_nb_chars=5).
            replace('\n', ' '), 'NUM_REGS_TESIS': fake.random_int(min=1,
            max=1000), 'ID_PROYECTO_INVESTIGACION_NK': fake.text(
            max_nb_chars=50).replace('\n', ' '),
            'NUMERO_ALU_ENCUESTA_GLOBAL_3': fake.random_int(min=1, max=1000
            ), 'NUM_ART_NO_IDX_ANO_CURSO_UZ': fake.random_int(min=1, max=
            1000), 'NUM_ART_NO_IDX_ANO_SIG_RAMA': fake.random_int(min=1,
            max=1000), 'FECHA_INSCRI_SOLICITUD_TESIS': generate_random_date
            (2020, 2023), 'FECHA_RECON_SEXENIO_CNEAI': generate_random_date
            (2020, 2023), 'DURACION_BRUTA_TESIS': fake.random_int(min=1,
            max=1000), 'NUMERO_PROF_ENCUESTA_GLOBAL_1': fake.random_int(min
            =1, max=1000), 'SN_PRORROGA_2': fake.random_element(elements=[
            'S', 'N']), 'NUM_SEXENIOS_TRANSF': fake.random_int(min=1, max=
            1000), 'FLG_OTRA_UNIVERSIDAD': fake.random_element(elements=[0,
            1]), 'NUMERO_ALU_ENCUESTA_GLOBAL_1': fake.random_int(min=1, max
            =1000), 'TOT_ARTICULOS_NO_INDEX_RAMA': fake.random_int(min=1,
            max=1000), 'NUMERO_PROF_ENCUESTA_GLOBAL_0': fake.random_int(min
            =1, max=1000), 'NUMERO_PROF_ENCUESTA_GLOBAL_5': fake.random_int
            (min=1, max=1000), 'NUM_ART_IDX_ANO_SIG_PLAN': fake.random_int(
            min=1, max=1000), 'NUM_SEXENIO_CNEAI': fake.random_int(min=1,
            max=1000), 'NUM_ART_IDX_ANO_CURSO_UZ': fake.random_int(min=1,
            max=1000), 'ID_SITUACION_ADVA_NK': situacion_adva[
            'ID_SITUACION_ADMINISTRATIVA_NK'] if 
            'ID_SITUACION_ADMINISTRATIVA_NK' in situacion_adva else
            f'{random.randint(1, 99):02d}'[:2]})
    return pd.DataFrame(data)
