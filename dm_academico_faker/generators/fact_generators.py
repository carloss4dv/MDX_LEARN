import pandas as pd
import numpy as np
from tqdm import tqdm
import random
import datetime
from faker import Faker
from utils.helpers import generate_random_date

# Inicializar Faker con locale español
fake = Faker('es_ES')

def generate_f_matricula(n=10000, dimension_dfs=None):
    """Genera datos para la tabla F_MATRICULA"""
    data = []
    
    # Verificar que se proporcionaron los DataFrames de dimensiones necesarios
    if dimension_dfs is None or not all(key in dimension_dfs for key in ['d_curso_academico', 'd_persona', 'd_plan_estudio', 'd_centro', 'd_pais', 'd_asignatura', 'd_clase_asignatura', 'd_tipo_acceso', 'd_poblacion', 'd_sexo']):
        raise ValueError("Se deben proporcionar todos los DataFrames de dimensiones necesarios")
    
    # Obtener datos de dimensiones
    d_curso = dimension_dfs['d_curso_academico']
    d_persona = dimension_dfs['d_persona']
    d_plan = dimension_dfs['d_plan_estudio']
    d_centro = dimension_dfs['d_centro']
    d_pais = dimension_dfs['d_pais']
    d_asignatura = dimension_dfs['d_asignatura']
    d_clase = dimension_dfs['d_clase_asignatura']
    d_tipo_acceso = dimension_dfs['d_tipo_acceso']
    d_poblacion = dimension_dfs['d_poblacion']
    d_sexo = dimension_dfs['d_sexo']
    
    # Generar datos de matrícula
    for i in tqdm(range(1, n+1), desc="Generando matrículas"):
        # Seleccionar valores aleatorios de las dimensiones
        curso = random.choice(d_curso.to_dict('records'))
        persona = random.choice(d_persona.to_dict('records'))
        plan = random.choice(d_plan.to_dict('records'))
        centro = random.choice(d_centro.to_dict('records'))
        pais = random.choice(d_pais.to_dict('records'))
        asignatura = random.choice(d_asignatura.to_dict('records'))
        clase_asig = random.choice(d_clase.to_dict('records'))
        tipo_acceso = random.choice(d_tipo_acceso.to_dict('records'))
        poblacion = random.choice(d_poblacion.to_dict('records'))
        sexo = d_sexo[d_sexo['ID_SEXO_NK'] == persona['SEXO']].to_dict('records')[0]
        
        # Generar datos aleatorios para la matrícula
        creditos = round(random.uniform(3, 12), 1)
        curso_orden = str(random.randint(1, 4))
        curso_mas_alto = random.randint(1, 4)
        num_matriculas = random.randint(1, 3)
        
        # Flags booleanos (0/1)
        flg_nuevo_ingreso = random.choice([0, 1])
        flg_en_programa_movilidad = random.choice([0, 1])
        flg_cambio_ciclo_grado = random.choice([0, 1])
        flg_traslado_mismo_estudio = random.choice([0, 1])
        
        # Fecha de matrícula
        fecha_matricula = generate_random_date(int(curso['ID_CURSO_ACADEMICO_NK']), int(curso['ID_CURSO_ACADEMICO_NK']) + 1)
        
        # Edad del alumno en el momento de la matrícula
        edad = datetime.datetime.strptime(fecha_matricula, '%Y-%m-%d').year - persona['ANYO_NACIMIENTO']
        
        data.append({
            'ID_CURSO_ACADEMICO_NK': curso['ID_CURSO_ACADEMICO_NK'],
            'ID_EXPEDIENTE_ACADEMICO_NK': i,
            'ID_CURSO_ACADEMICO': curso['ID_CURSO_ACADEMICO'],
            'ID_ALUMNO': persona['ID_PERSONA'],
            'ID_EXPEDIENTE_ACADEMICO': i,
            'ID_PLAN_ESTUDIO': plan['ID_PLAN_ESTUDIO'],
            'ID_CENTRO': centro['ID_CENTRO'],
            'ID_PAIS_NACIONALIDAD': pais['ID_PAIS'],
            'ID_ASIGNATURA': asignatura['ID_ASIGNATURA'],
            'ID_CLASE_ASIGNATURA': clase_asig['ID_CLASE_ASIGNATURA'],
            'ID_TIPO_ACCESO': tipo_acceso['ID_TIPO_ACCESO'],
            'ID_CURSO_ACADEMICO_COHORTE': random.choice(d_curso['ID_CURSO_ACADEMICO'].tolist()),
            'ID_POBLACION_FAMILIAR': poblacion['ID_POBLACION'],
            'ID_FECHA_MATRICULA': int(fecha_matricula.replace('-', '')),
            'SEXO': persona['SEXO'],
            'ID_SEXO': sexo['ID_SEXO'],
            'EDAD': edad,
            'CREDITOS': creditos,
            'CURSO_ORDEN': curso_orden,
            'CURSO_MAS_ALTO_MATRICULADO': curso_mas_alto,
            'NUMERO_MATRICULAS': num_matriculas,
            'RANGO_NUM_MATRICULAS': f"{num_matriculas}",
            'FLG_NUEVO_INGRESO': flg_nuevo_ingreso,
            'SN_NUEVO_INGRESO': 'S' if flg_nuevo_ingreso == 1 else 'N',
            'FLG_EN_PROGRAMA_MOVILIDAD': flg_en_programa_movilidad,
            'SN_PROG_MOVILIDAD': 'S' if flg_en_programa_movilidad == 1 else 'N',
            'ANYO_ACCESO_SUE': random.randint(2010, int(curso['ID_CURSO_ACADEMICO_NK'])),
            'FLG_NUEVO_ACCESO_SUE': random.choice([0, 1]),
            'SN_NUEVO_ACCESO_SUE': random.choice(['S', 'N']),
            'FLG_CAMBIO_CICLO_GRADO': flg_cambio_ciclo_grado,
            'SN_CAMBIO_CICLO_GRADO': 'S' if flg_cambio_ciclo_grado == 1 else 'N',
            'FLG_TRASLADO_MISMO_ESTUDIO': flg_traslado_mismo_estudio,
            'SN_TRASLADO_MISMO_ESTUDIO': 'S' if flg_traslado_mismo_estudio == 1 else 'N',
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
    
    return pd.DataFrame(data)

def generate_f_rendimiento(n=20000, dimension_dfs=None):
    """Genera datos para la tabla F_RENDIMIENTO"""
    data = []
    
    # Verificar que se proporcionaron los DataFrames de dimensiones necesarios
    if dimension_dfs is None or not all(key in dimension_dfs for key in ['d_curso_academico', 'd_persona', 'd_asignatura', 'd_convocatoria', 'd_plan_estudio', 'd_centro', 'd_tipo_acceso', 'd_grupo', 'd_tipo_docencia', 'd_clase_asignatura', 'd_tipo_reconocimiento', 'd_calificacion', 'd_rango_nota_numerica', 'd_sexo', 'd_pais', 'd_poblacion']):
        raise ValueError("Se deben proporcionar todos los DataFrames de dimensiones necesarios")
    
    # Obtener datos de dimensiones
    d_curso = dimension_dfs['d_curso_academico']
    d_persona = dimension_dfs['d_persona']
    d_asignatura = dimension_dfs['d_asignatura']
    d_convocatoria = dimension_dfs['d_convocatoria']
    d_plan = dimension_dfs['d_plan_estudio']
    d_centro = dimension_dfs['d_centro']
    d_tipo_acceso = dimension_dfs['d_tipo_acceso']
    d_grupo = dimension_dfs['d_grupo']
    d_tipo_docencia = dimension_dfs['d_tipo_docencia']
    d_clase_asig = dimension_dfs['d_clase_asignatura']
    d_tipo_reconocimiento = dimension_dfs['d_tipo_reconocimiento']
    d_calificacion = dimension_dfs['d_calificacion']
    d_rango_nota = dimension_dfs['d_rango_nota_numerica']
    d_sexo = dimension_dfs['d_sexo']
    d_pais = dimension_dfs['d_pais']
    d_poblacion = dimension_dfs['d_poblacion']
    
    # Generar datos de rendimiento académico
    for i in tqdm(range(1, n+1), desc="Generando rendimientos"):
        # Seleccionar valores aleatorios de las dimensiones
        curso = random.choice(d_curso.to_dict('records'))
        persona = random.choice(d_persona.to_dict('records'))
        asignatura = random.choice(d_asignatura.to_dict('records'))
        convocatoria = random.choice(d_convocatoria.to_dict('records'))
        plan = random.choice(d_plan.to_dict('records'))
        centro = random.choice(d_centro.to_dict('records'))
        tipo_acceso = random.choice(d_tipo_acceso.to_dict('records'))
        grupo = random.choice(d_grupo.to_dict('records'))
        tipo_docencia = random.choice(d_tipo_docencia.to_dict('records'))
        clase_asig = random.choice(d_clase_asig.to_dict('records'))
        tipo_reconocimiento = random.choice(d_tipo_reconocimiento.to_dict('records'))
        
        # Generar una nota numérica entre 0 y 10
        nota_numerica = round(random.uniform(0, 10), 2)
        
        # Determinar la calificación basada en la nota numérica
        if nota_numerica < 5:
            calificacion = d_calificacion[d_calificacion['ID_CALIFICACION_NK'] == 'SS'].iloc[0]
        elif nota_numerica < 7:
            calificacion = d_calificacion[d_calificacion['ID_CALIFICACION_NK'] == 'AP'].iloc[0]
        elif nota_numerica < 9:
            calificacion = d_calificacion[d_calificacion['ID_CALIFICACION_NK'] == 'NT'].iloc[0]
        else:
            calificacion = d_calificacion[d_calificacion['ID_CALIFICACION_NK'] == 'SB'].iloc[0]
        
        # Determinar el rango de nota
        for _, rango in d_rango_nota.iterrows():
            if rango['NOMBRE_RANGO_NOTA_NUMERICA'].split('-')[0] <= str(nota_numerica) <= rango['NOMBRE_RANGO_NOTA_NUMERICA'].split('-')[1]:
                rango_nota = rango
                break
        else:
            rango_nota = d_rango_nota.iloc[0]
        
        # Obtener el sexo correspondiente
        sexo = d_sexo[d_sexo['ID_SEXO_NK'] == persona['SEXO']].to_dict('records')[0]
        
        # Seleccionar país y población
        pais = random.choice(d_pais.to_dict('records'))
        poblacion = random.choice(d_poblacion.to_dict('records'))
        
        # Generar datos aleatorios para el rendimiento
        creditos = round(random.uniform(3, 12), 1)
        orden_convocatoria = random.randint(1, 3)
        convocatorias_consumidas = random.randint(1, 6)
        numero_matriculas = random.randint(1, 3)
        
        # Flags booleanos (0/1)
        flg_superada = 1 if nota_numerica >= 5 else 0
        flg_presentada = 1 if calificacion['ID_CALIFICACION_NK'] != 'NP' else 0
        flg_suspendida = 1 if flg_presentada == 1 and flg_superada == 0 else 0
        flg_reconocida = random.choice([0, 1])
        flg_matriculada = 1
        flg_transferida = random.choice([0, 1])
        flg_ultima_convocatoria = 1 if convocatorias_consumidas >= 6 else 0
        
        # Fecha de calificación
        fecha_calificacion = generate_random_date(int(curso['ID_CURSO_ACADEMICO_NK']), int(curso['ID_CURSO_ACADEMICO_NK']) + 1)
        
        # Edad del alumno
        edad = datetime.datetime.strptime(fecha_calificacion, '%Y-%m-%d').year - persona['ANYO_NACIMIENTO']
        
        data.append({
            'ID_CURSO_ACADEMICO_NK': curso['ID_CURSO_ACADEMICO_NK'],
            'ID_EXPEDIENTE_ACADEMICO_NK': i,
            'ID_CURSO_ACADEMICO': curso['ID_CURSO_ACADEMICO'],
            'ID_EXPEDIENTE_ACADEMICO': i,
            'ID_ASIGNATURA': asignatura['ID_ASIGNATURA'],
            'ID_CONVOCATORIA': convocatoria['ID_CONVOCATORIA'],
            'ID_PLAN_ESTUDIO': plan['ID_PLAN_ESTUDIO'],
            'ID_CENTRO': centro['ID_CENTRO'],
            'ID_TIPO_ACCESO': tipo_acceso['ID_TIPO_ACCESO'],
            'ID_GRUPO': grupo['ID_GRUPO'],
            'ID_TIPO_DOCENCIA': tipo_docencia['ID_TIPO_DOCENCIA'],
            'ID_CLASE_ASIGNATURA': clase_asig['ID_CLASE_ASIGNATURA'],
            'ID_TIPO_RECONOCIMIENTO': tipo_reconocimiento['ID_TIPO_RECONOCIMIENTO'],
            'ID_CALIFICACION': calificacion['ID_CALIFICACION'],
            'ID_RANGO_NOTA_NUMERICA': rango_nota['ID_RANGO_NOTA_NUMERICA'],
            'ID_ALUMNO': persona['ID_PERSONA'],
            'ID_SEXO': sexo['ID_SEXO'],
            'ID_CURSO_ACADEMICO_COHORTE': random.choice(d_curso['ID_CURSO_ACADEMICO'].tolist()),
            'ID_PAIS_NACIONALIDAD': pais['ID_PAIS'],
            'ID_POBLACION_FAMILIAR': poblacion['ID_POBLACION'],
            'ID_FECHA_CALIFICACION': int(fecha_calificacion.replace('-', '')),
            'EDAD': edad,
            'NOTA_NUMERICA': nota_numerica,
            'CREDITOS': creditos,
            'ORDEN_CONVOCATORIA': orden_convocatoria,
            'CONVOCATORIAS_CONSUMIDAS': convocatorias_consumidas,
            'NUMERO_MATRICULAS': numero_matriculas,
            'RANGO_NUM_MATRICULAS': f"{numero_matriculas}",
            'CURSO_MAS_ALTO_MATRICULADO': random.randint(1, 4),
            'ANYO_ACCESO_SUE': random.randint(2010, int(curso['ID_CURSO_ACADEMICO_NK'])),
            'FLG_SUPERADA': flg_superada,
            'FLG_PRESENTADA': flg_presentada,
            'FLG_SUSPENDIDA': flg_suspendida,
            'FLG_RECONOCIDA': flg_reconocida,
            'FLG_MATRICULADA': flg_matriculada,
            'FLG_TRANSFERIDA': flg_transferida,
            'FLG_ULTIMA_CONVOCATORIA': flg_ultima_convocatoria,
            'FLG_CALCULO_TASAS': random.choice([0, 1]),
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
    
    return pd.DataFrame(data)

# TODO: Implementar los siguientes generadores de tablas de hechos:
# - generate_f_cohorte
# - generate_f_doctorado
# - generate_f_doctorado_admision
# - generate_f_egracons
# - generate_f_egresado
# - generate_f_estudiantes_movilidad_in
# - generate_f_estudiantes_movilidad_out
# - generate_f_estudio_propio_matricula
# - generate_f_oferta_acuerdo_bilateral
# - generate_f_oferta_admision
# - generate_f_solicitante_admision
# - generate_f_solicitudes_movilidad
# - generate_f_tabla_fusion
# - generate_f_tabla_fusion_estcen

# TODO: Implementar los siguientes generadores de tablas de dimensiones:
# - generate_d_acuerdo_bilateral
# - generate_d_area_estudios_movilidad
# - generate_d_articulo
# - generate_d_campus
# - generate_d_categoria_cuerpo_pdi
# - generate_d_centro
# - generate_d_centro_destino
# - generate_d_centro_estudio
# - generate_d_centro_otra_universidad
# - generate_d_clase_liquidacion
# - generate_d_colectivo_movilidad
# - generate_d_convocatoria_preinscripcion
# - generate_d_cupo_adjudicacion
# - generate_d_dedicacion
# - generate_d_dedicacion_profesor
# - generate_d_detalle_cupo_general
# - generate_d_doctorado_tipo_beca
# - generate_d_edad_est
# - generate_d_estado_acuerdo_bilateral
# - generate_d_estado_adjudicacion
# - generate_d_estado_solicitud_doctorado
# - generate_d_estudio
# - generate_d_estudio_destino
# - generate_d_estudio_jerarq
# - generate_d_estudio_otra_universidad
# - generate_d_estudio_propio
# - generate_d_estudio_propio_modalidad
# - generate_d_estudio_propio_organo_gest
# - generate_d_estudio_propio_tipo
# - generate_d_grupo
# - generate_d_idioma_movilidad
# - generate_d_idioma_nivel_movilidad
# - generate_d_modalidad_plan_estudio
# - generate_d_nacionalidad
# - generate_d_nivel_estudios_movilidad
# - generate_d_plan_estudio_ano_datos
# - generate_d_plan_estudio_asignatura
# - generate_d_poblacion_centro
# - generate_d_programa_movilidad
# - generate_d_proyecto_investigacion
# - generate_d_rama_macroarea
# - generate_d_rango_credito
# - generate_d_rango_credito_movilidad
# - generate_d_rango_edad
# - generate_d_rango_nota_admision
# - generate_d_rango_nota_crue
# - generate_d_rango_nota_egracons
# - generate_d_rango_nota_numerica
# - generate_d_tipo_abandono
# - generate_d_tipo_acceso_preinscripcion
# - generate_d_tipo_asignatura
# - generate_d_tipo_centro
# - generate_d_tipo_docencia
# - generate_d_tipo_egreso
# - generate_d_tipo_procedimiento
# - generate_d_titulacion
# - generate_d_universidad 