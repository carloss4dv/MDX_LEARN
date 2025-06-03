import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from tqdm import tqdm
from faker import Faker

# Inicializar Faker
fake = Faker(['es_ES'])

def generate_f_oferta_acuerdo_bilateral(n=200, dimension_dfs=None):
    """
    Genera datos para la tabla F_OFERTA_ACUERDO_BILATERAL
    
    Args:
        n (int): Número de filas a generar
        dimension_dfs (dict): Diccionario con DataFrames de dimensiones necesarias
        
    Returns:
        DataFrame: DataFrame con los datos generados para F_OFERTA_ACUERDO_BILATERAL
    """
    data = []
    
    # Verificar que se proporcionaron los DataFrames de dimensiones necesarias
    if dimension_dfs is None or not all(key in dimension_dfs for key in [
        'd_curso_academico', 'd_curso_cohorte', 'd_acuerdo_bilateral',
        'd_area_estudios_movilidad', 'd_nivel_estudios_movilidad', 'd_pais',
        'd_colectivo_movilidad', 'd_programa_movilidad', 'd_centro',
        'd_universidad', 'd_idioma_nivel_movilidad'
    ]):
        raise ValueError("Se deben proporcionar todos los DataFrames de dimensiones necesarios")
    
    # Obtener datos de dimensiones
    d_curso = dimension_dfs['d_curso_academico']
    d_curso_cohorte = dimension_dfs['d_curso_cohorte']
    d_acuerdo = dimension_dfs['d_acuerdo_bilateral']
    d_area_estudios = dimension_dfs['d_area_estudios_movilidad']
    d_nivel_estudios = dimension_dfs['d_nivel_estudios_movilidad']
    d_pais = dimension_dfs['d_pais']
    d_colectivo = dimension_dfs['d_colectivo_movilidad']
    d_programa = dimension_dfs['d_programa_movilidad']
    d_centro = dimension_dfs['d_centro']
    d_universidad = dimension_dfs['d_universidad']
    d_idioma_nivel = dimension_dfs['d_idioma_nivel_movilidad']
    
    # Generar datos para cada acuerdo bilateral
    for i in tqdm(range(1, n+1), desc="Generando ofertas de acuerdos bilaterales"):
        # Seleccionar valores aleatorios de las dimensiones
        curso = random.choice(d_curso.to_dict('records'))
        acuerdo = random.choice(d_acuerdo.to_dict('records'))
        area_estudios = random.choice(d_area_estudios.to_dict('records'))
        nivel_estudios = random.choice(d_nivel_estudios.to_dict('records'))
        universidad = random.choice(d_universidad.to_dict('records'))
        pais_universidad = random.choice(d_pais.to_dict('records'))
        colectivo = random.choice(d_colectivo.to_dict('records'))
        programa = random.choice(d_programa.to_dict('records'))
        centro = random.choice(d_centro.to_dict('records'))
        
        # Seleccionar idiomas y niveles
        idioma_nivel_principal = random.choice(d_idioma_nivel.to_dict('records'))
        idioma_nivel_secundario = random.choice(d_idioma_nivel.to_dict('records'))
        
        # Generar cursos académicos de inicio y fin
        curso_inicio = random.choice(d_curso.to_dict('records'))
        curso_fin = random.choice(d_curso.to_dict('records'))
        # Asegurar que el curso fin es posterior o igual al inicio
        while curso_fin['ID_CURSO_ACADEMICO_NK'] < curso_inicio['ID_CURSO_ACADEMICO_NK']:
            curso_fin = random.choice(d_curso.to_dict('records'))
        
        # Generar valores específicos
        fecha_referencia = datetime.now() - timedelta(days=random.randint(0, 365))
        id_fecha_referencia = int(fecha_referencia.strftime('%Y%m%d'))
        
        # Duración de estancias
        duracion_estancia_alumnos = random.choice([5, 6, 9, 10, 12])
        duracion_estancia_docentes = random.choice([1, 2, 3, 4, 5])
        horas_clase_semana = random.randint(1, 20)
        
        # Determinar si es entrada o salida
        in_out = random.choice(['IN', 'OUT'])
        entrada_salida = 'E' if in_out == 'IN' else 'S'
        
        # Código de plaza
        cod_plaza_ofertada = f"PLAZA-{programa['ID_PROGRAMA_MOVILIDAD_NK']}-{random.randint(100, 999)}"
        
        # Determinar colectivo de oferta
        colectivo_oferta = random.choice(['ESTUDIANTES', 'PDI', 'PAS', 'MIXTO'])
        
        # Banderas de oferta
        flg_oferta_alumnos = 1 if colectivo_oferta in ['ESTUDIANTES', 'MIXTO'] else 0
        flg_oferta_docentes = 1 if colectivo_oferta in ['PDI', 'MIXTO'] else 0
        flg_plaza_ficticia = random.choice([0, 1])
        
        # Añadir registro
        data.append({
            'ID_CURSO_ACADEMICO_NK': curso['ID_CURSO_ACADEMICO_NK']  # TODO: Usar valores válidos de D_CURSO_COHORTE,
            'ID_ACUERDO_BILATERAL_NK': acuerdo['ID_ACUERDO_BILATERAL_NK'],
            'ID_AREA_ESTUDIOS_NK': area_estudios['ID_AREA_ESTUDIOS_MOVILIDAD_NK'],
            'ID_NIVEL_ESTUDIOS_NK': nivel_estudios['ID_NIVEL_ESTUDIOS_MOVILIDAD_NK'],
            'ID_CURSO_ACADEMICO': curso['ID_CURSO_ACADEMICO'],
            'ID_ACUERDO_BILATERAL': acuerdo['ID_ACUERDO_BILATERAL'],
            'ID_AREA_ESTUDIOS_MOVILIDAD': area_estudios['ID_AREA_ESTUDIOS_MOVILIDAD'],
            'ID_NIVEL_ESTUDIOS_MOVILIDAD': nivel_estudios['ID_NIVEL_ESTUDIOS_MOVILIDAD'],
            'IN_OUT': in_out,
            'ID_UNIVERSIDAD_ACUERDO': universidad['ID_UNIVERSIDAD'],
            'ID_PAIS_UNIVERSIDAD_ACUERDO': pais_universidad['ID_PAIS'],
            'ID_COLECTIVO_MOVILIDAD': colectivo['ID_COLECTIVO_MOVILIDAD'],
            'ID_CURSO_INICIO_VIGENCIA': curso_inicio['ID_CURSO_ACADEMICO'],
            'ID_CURSO_FIN_VIGENCIA': curso_fin['ID_CURSO_ACADEMICO'],
            'ID_FECHA_REFERENCIA': id_fecha_referencia,
            'DURACION_ESTANCIA_ALUMNOS': duracion_estancia_alumnos,
            'DURACION_ESTANCIA_DOCENTES': duracion_estancia_docentes,
            'HORAS_CLASE_SEMANA': horas_clase_semana,
            'FECHA_CARGA': datetime.now(),
            'ID_PROGRAMA_MOVILIDAD': programa['ID_PROGRAMA_MOVILIDAD'],
            'ID_IDIOMA_NIVEL_PRINCIPAL': idioma_nivel_principal['ID_IDIOMA_NIVEL_MOVILIDAD'],
            'ID_IDIOMA_NIVEL_SECUNDARIO': idioma_nivel_secundario['ID_IDIOMA_NIVEL_MOVILIDAD'],
            'ID_CENTRO': centro['ID_CENTRO'],
            'ID_FECHA_CARGA': int(datetime.now().strftime('%Y%m%d')),
            'ID_COLECTIVO_NK': colectivo['ID_COLECTIVO_MOVILIDAD_NK'],
            'ID_PROGRAMA_MOVILIDAD_NK': programa['ID_PROGRAMA_MOVILIDAD_NK'],
            'ID_UNIVERSIDAD_DESTINO_NK': universidad['ID_UNIVERSIDAD_NK'],
            'ID_CURSO_ACADEMICO_INICIO_NK': curso_inicio['ID_CURSO_ACADEMICO_NK'],
            'ID_CURSO_ACADEMICO_FIN_NK': curso_fin['ID_CURSO_ACADEMICO_NK'],
            'ENTRADA_SALIDA': entrada_salida,
            'COD_PLAZA_OFERTADA': cod_plaza_ofertada,
            'COLECTIVO_OFERTA': colectivo_oferta,
            'ID_CENTRO_NK': centro['ID_CENTRO_NK']  # TODO: Usar valores válidos de D_CENTRO,
            'ID_IDIOMA_1_NK': idioma_nivel_principal['ID_IDIOMA_MOVILIDAD_NK'],
            'ID_NIVEL_IDIOMA_1_NK': idioma_nivel_principal['ID_NIVEL_IDIOMA_MOVILIDAD_NK'],
            'ID_IDIOMA_2_NK': idioma_nivel_secundario['ID_IDIOMA_MOVILIDAD_NK'],
            'ID_NIVEL_IDIOMA_2_NK': idioma_nivel_secundario['ID_NIVEL_IDIOMA_MOVILIDAD_NK'],
            'ID_ALUMNO': random.randint(1, 1000),
            'ID_ALUMNO_NIP_NK': random.randint(10000, 99999),
            'FLG_OFERTA_ALUMNOS': flg_oferta_alumnos,
            'FLG_OFERTA_DOCENTES': flg_oferta_docentes,
            'FECHA_REFERENCIA': fecha_referencia,
            'FLG_PLAZA_FICTICIA': flg_plaza_ficticia
        ,
            'ID_IDIOMA_1_NK': None  # AGREGADO: Columna requerida por esquema,
            'ID_IDIOMA_2_NK': None  # AGREGADO: Columna requerida por esquema,
            'ID_NIVEL_IDIOMA_1_NK': None  # AGREGADO: Columna requerida por esquema,
            'ID_NIVEL_IDIOMA_2_NK': None  # AGREGADO: Columna requerida por esquema})
    
    return pd.DataFrame(data) 