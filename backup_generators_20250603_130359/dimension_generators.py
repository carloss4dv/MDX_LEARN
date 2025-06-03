from faker import Faker
import pandas as pd
import numpy as np
from tqdm import tqdm
import random
import datetime
# from utils.helpers import generate_random_date  # ELIMINADA - Causa problemas con cx_Oracle
import hashlib
import unicodedata
import re

# Inicializar Faker con locale español
fake = Faker('es_ES')

def generate_random_date(start_year, end_year):     
     
    """Genera una fecha aleatoria entre los años especificados como string 'YYYY-MM-DD'"""
    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_date = start_date + datetime.timedelta(days=random_days)
    return random_date.strftime('%Y-%m-%d')

def generate_random_date_datetime(start_year, end_year):  # COMENTADO: Tabla no existe en esquema
     """
     Genera una fecha aleatoria entre start_year y end_year como objeto datetime
    
     Args:
         start_year (int): Año de inicio
         end_year (int): Año de fin
    
     Returns:
         datetime.date: Fecha como objeto datetime
     """
     year = random.randint(start_year, end_year)
     month = random.randint(1, 12)
    
     # Ajustar el día máximo según el mes
     if month in [4, 6, 9, 11]:
         max_day = 30
     elif month == 2:
         # Comprobar si es año bisiesto
         if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
             max_day = 29
         else:
             max_day = 28
     else:
         max_day = 31
    
     day = random.randint(1, max_day)
    
     return datetime.date(year, month, day)

def generate_d_sexo(n=2):
    """Genera datos para la tabla D_SEXO"""
    data = []
    sexos = [('H', 'Hombre'), ('M', 'Mujer')]
    
    for i, (id_sexo_nk, nombre_sexo) in enumerate(sexos, 1):
        data.append({
            'ID_SEXO': i,
            'ID_SEXO_NK': id_sexo_nk,
            'NOMBRE_SEXO': nombre_sexo,
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
    
    return pd.DataFrame(data)

def generate_d_pais(n=100):
    """Genera datos para la tabla D_PAIS"""
    data = []
    
    # Asegurar que España esté en la lista
    espana = {
        'ID_PAIS': 1,
        'NOMBRE_PAIS': 'España',
        'ID_PAIS_NK': 'ESP',
        'NOMBRE_NACIONALIDAD': 'Española',
        'ID_PAIS_DESCR': 1,
        'SN_PERTENECE_EEES': 'S',
        'FLG_EXTRANJERO': 0,
        'SN_EXTRANJERO': 'N',
        'FECHA_CARGA': generate_random_date(2020, 2023)
    }
    data.append(espana)
    
    # Generar el resto de países
    for i in tqdm(range(2, n+1), desc="Generando países"):
        country = fake.unique.country()
        country_code = fake.unique.country_code(representation="alpha-3")
        
        # Determinar si pertenece al EEES (Espacio Europeo de Educación Superior)
        # Países europeos tienen más probabilidad de pertenecer
        is_eees = 'S' if fake.random_element(elements=[True, False, False, True, True]) else 'N'
        
        # Determinar si es extranjero (todos excepto España)
        is_extranjero = 1
        sn_extranjero = 'S'
        
        # Limitar el tamaño de NOMBRE_NACIONALIDAD a 45 caracteres para evitar errores en Oracle
        nombre_nacionalidad = f"Nacional de {country}"
        if len(nombre_nacionalidad) > 45:
            nombre_nacionalidad = nombre_nacionalidad[:42] + "..."
        
        data.append({
            'ID_PAIS': i,
            'NOMBRE_PAIS': country,
            'ID_PAIS_NK': country_code,
            'NOMBRE_NACIONALIDAD': nombre_nacionalidad,
            'ID_PAIS_DESCR': i,
            'SN_PERTENECE_EEES': is_eees,
            'FLG_EXTRANJERO': is_extranjero,
            'SN_EXTRANJERO': sn_extranjero,
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
    
    fake.unique.clear()  # Limpiar valores únicos
    return pd.DataFrame(data)

def generate_d_tiempo(start_year=2010, end_year=2023):
    """Genera datos para la tabla D_TIEMPO - solo columnas requeridas por esquema"""
    data = []
    
    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(end_year, 12, 31)
    
    current_date = start_date
    id_dia = 1
    
    # Diccionarios para mantener IDs de meses, trimestres y años
    meses_ids = {}  # (año, mes) -> id_mes
    trimestres_ids = {}  # (año, trimestre) -> id_trimestre
    años_ids = {}  # año -> id_año
    
    # Nombres de meses en español
    nombres_meses = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
        7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    
    # Asignar IDs para cada nivel temporal
    id_mes = 1
    id_trimestre = 1
    id_año = 1
    
    while current_date <= end_date:
        dia = current_date.day
        mes = current_date.month
        anyo = current_date.year
        trimestre = (mes - 1) // 3 + 1
        
        # Generar o recuperar IDs para cada nivel temporal
        if (anyo, mes) not in meses_ids:
            meses_ids[(anyo, mes)] = id_mes
            id_mes += 1
            
        if (anyo, trimestre) not in trimestres_ids:
            trimestres_ids[(anyo, trimestre)] = id_trimestre
            id_trimestre += 1
            
        if anyo not in años_ids:
            años_ids[anyo] = id_año
            id_año += 1
        
        # Obtener el ID para cada nivel
        id_mes_actual = meses_ids[(anyo, mes)]
        id_trimestre_actual = trimestres_ids[(anyo, trimestre)]
        id_anyo_actual = años_ids[anyo]
        
        # Crear registro solo con columnas del esquema
        data.append({
            'ID_DIA': id_dia,
            'NOMBRE_DIA': current_date.strftime('%d/%m/%Y'),
            'ID_MES': id_mes_actual,
            'NOMBRE_MES': nombres_meses[mes],
            'ID_TRIMESTRE': id_trimestre_actual,
            'NOMBRE_TRIMESTRE': f"T{trimestre}",
            'ID_ANYO': id_anyo_actual,
            'NOMBRE_ANYO': str(anyo)
        })
        
        current_date += datetime.timedelta(days=1)
        id_dia += 1
    
    return pd.DataFrame(data)

def generate_d_curso_academico(start_year=2010, n=15):
    """Genera datos para la tabla D_CURSO_ACADEMICO"""
    data = []
    
    for i in range(n):
        year = start_year + i
        id_curso = year * 10  # Por ejemplo, 2010 -> 20100
        nombre_curso = f"{year}/{year+1}"
        
        data.append({
            'ID_CURSO_ACADEMICO': id_curso,
            'NOMBRE_CURSO_ACADEMICO': nombre_curso,
            'ID_CURSO_ACADEMICO_NK': year  # TODO: Usar valores válidos de D_CURSO_COHORTE,
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
    
    return pd.DataFrame(data)

def generate_d_curso_cohorte(curso_academico_df=None, start_year=2010, n=15):
    """Genera datos para la tabla D_CURSO_COHORTE basados en D_CURSO_ACADEMICO"""
    if curso_academico_df is not None:
        # Usar los mismos datos que D_CURSO_ACADEMICO
        data = []
        for _, row in curso_academico_df.iterrows():
            data.append({
                'ID_CURSO_ACADEMICO': row['ID_CURSO_ACADEMICO'],
                'NOMBRE_CURSO_ACADEMICO': row['NOMBRE_CURSO_ACADEMICO'],
                'ID_CURSO_ACADEMICO_NK': row['ID_CURSO_ACADEMICO_NK']  # TODO: Usar valores válidos de D_CURSO_COHORTE,
                'FECHA_CARGA': generate_random_date(2020, 2023)
            })
        return pd.DataFrame(data)
    else:
        # Generar nuevos datos
        return generate_d_curso_academico(start_year, n)

def generate_d_tipo_estudio(n=10):
    """Genera datos para la tabla D_TIPO_ESTUDIO"""
    data = []
    
    tipos_estudio = [
        ('GR', 'Grado'),
        ('MA', 'Máster'),
        ('DO', 'Doctorado'),
        ('DI', 'Diploma'),
        ('LI', 'Licenciatura'),
        ('IN', 'Ingeniería'),
        ('AR', 'Arquitectura'),
        ('TE', 'Técnico Superior'),
        ('ES', 'Especialización'),
        ('CE', 'Curso de Especialización')
    ]
    
    for i, (id_nk, nombre) in enumerate(tipos_estudio, 1):
        data.append({
            'ID_TIPO_ESTUDIO': i,
            'NOMBRE_TIPO_ESTUDIO': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023),
            'ID_TIPO_ESTUDIO_NK': id_nk
        ,
            'ID_TIPO_ESTUDIO_DESCR': None  # AGREGADO: Columna requerida por esquema,
            'ORD_TIPO_ESTUDIO': None  # AGREGADO: Columna requerida por esquema,
            'ID_TIPO_ESTUDIO_DESCR': None  # AGREGADO: Columna requerida por esquema,
            'ORD_TIPO_ESTUDIO': None  # AGREGADO: Columna requerida por esquema})
    
    return pd.DataFrame(data)

def generate_d_calificacion(n=10):
    """Genera datos para la tabla D_CALIFICACION"""
    data = []
    
    calificaciones = [
        ('NP', 'No Presentado'),
        ('SS', 'Suspenso'),
        ('AP', 'Aprobado'),
        ('NT', 'Notable'),
        ('SB', 'Sobresaliente'),
        ('MH', 'Matrícula de Honor'),
        ('CO', 'Convalidada'),
        ('AD', 'Adaptada'),
        ('RE', 'Reconocida'),
        ('AN', 'Anulada')
    ]
    
    for i, (id_nk, nombre) in enumerate(calificaciones, 1):
        data.append({
            'ID_CALIFICACION': i,
            'NOMBRE_CALIFICACION': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023),
            'ID_CALIFICACION_NK': id_nk
        })
    
    return pd.DataFrame(data)

def generate_d_convocatoria(n=5):
    """Genera datos para la tabla D_CONVOCATORIA con todos los atributos completos"""
    data = []
    
    convocatorias = [
        ('P1', 'Primera convocatoria', 'Convocatoria ordinaria del primer semestre', 1, 'Enero'),
        ('P2', 'Segunda convocatoria', 'Convocatoria ordinaria del segundo semestre', 2, 'Junio'),
        ('EX', 'Convocatoria extraordinaria', 'Convocatoria para recuperación de asignaturas', 3, 'Julio'),
        ('ES', 'Convocatoria especial', 'Convocatoria para casos excepcionales', 4, 'Septiembre'),
        ('FE', 'Convocatoria de fin de estudios', 'Convocatoria para alumnos que finalizan estudios', 5, 'Diciembre')
    ]
    
    # Tomar solo el número de convocatorias solicitado
    convocatorias = convocatorias[:n]
    
    # Fecha base para convocatorias (se usará para calcular fechas)
    año_base = datetime.datetime.now().year
    
    for i, (id_nk, nombre, descripcion, orden, mes) in enumerate(convocatorias, 1):
        # Determinar fechas de inicio y fin de la convocatoria
        mes_num = {'Enero': 1, 'Junio': 6, 'Julio': 7, 'Septiembre': 9, 'Diciembre': 12}.get(mes, 1)
        fecha_inicio = datetime.date(año_base, mes_num, 1)
        
        # Último día del mes
        if mes_num == 12:
            fecha_fin = datetime.date(año_base, 12, 31)
        else:
            fecha_fin = datetime.date(año_base, mes_num + 1, 1) - datetime.timedelta(days=1)
        
        # Calcular duración en días
        duracion_dias = (fecha_fin - fecha_inicio).days + 1
        
        # Determinar si es ordinaria o extraordinaria
        es_ordinaria = 1 if id_nk in ['P1', 'P2'] else 0
        es_extraordinaria = 1 if id_nk == 'EX' else 0
        es_especial = 1 if id_nk in ['ES', 'FE'] else 0
        
        # Generar periodo académico (S1: Primer semestre, S2: Segundo semestre, AN: Anual)
        periodo_academico = 'S1' if mes_num <= 2 else 'S2' if 2 < mes_num <= 7 else 'AN'
        
        data.append({
            'ID_CONVOCATORIA': i,
            'NOMBRE_CONVOCATORIA': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023),# 
            'ORDEN_CONVOCATORIA': ...,  # ELIMINADO: No existe en esquema
        })
    return pd.DataFrame(data)

def generate_d_tipo_acceso(n=15):
    """Genera datos para la tabla D_TIPO_ACCESO"""
    data = []
    
    tipos_acceso = [
        ('PAU', 'Prueba de Acceso a la Universidad'),
        ('FP', 'Formación Profesional'),
        ('TIT', 'Titulados Universitarios'),
        ('M25', 'Mayores de 25 años'),
        ('M40', 'Mayores de 40 años'),
        ('M45', 'Mayores de 45 años'),
        ('DEP', 'Deportistas de alto nivel'),
        ('DIS', 'Personas con discapacidad'),
        ('INT', 'Estudios extranjeros'),
        ('TRA', 'Traslado de expediente'),
        ('CAM', 'Cambio de universidad'),
        ('ADA', 'Adaptación de plan de estudios'),
        ('ESE', 'Estudios superiores extranjeros'),
        ('OTR', 'Otros'),
        ('NOI', 'No informado')
    ]
    
    for i, (id_nk, nombre) in enumerate(tipos_acceso, 1):
        data.append({
            'ID_TIPO_ACCESO': i,
            'NOMBRE_TIPO_ACCESO': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023),# 
            'ID_TIPO_ACCESO_NK': ...,  # ELIMINADO: No existe en esquema
        })
    
    return pd.DataFrame(data)

def generate_d_clase_asignatura(n=5):
    """Genera datos para la tabla D_CLASE_ASIGNATURA"""
    data = []
    
    clases_asignatura = [
        ('T', 'Troncal'),
        ('O', 'Obligatoria'),
        ('P', 'Optativa'),
        ('B', 'Básica'),
        ('L', 'Libre elección')
    ]
    
    for i, (id_nk, nombre) in enumerate(clases_asignatura, 1):
        data.append({
            'ID_CLASE_ASIGNATURA': i,
            'NOMBRE_CLASE_ASIGNATURA': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023),
            'ID_CLASE_ASIGNATURA_NK': id_nk
        })
    
    return pd.DataFrame(data)

def generate_d_persona(n=10000, paises_df=None):
    """Genera datos para la tabla D_PERSONA"""
    data = []
    
    # Si no se proporciona un dataframe de países, crear uno mínimo
    if paises_df is None:
        paises_df = generate_d_pais(n=10)
        
    # Lista de países disponibles
    paises_ids = paises_df['ID_PAIS'].tolist()
    
    # Función para generar un DNI español válido manualmente
#     def generate_dni():  # COMENTADO: Tabla no existe en esquema
#         # Generar 8 dígitos aleatorios
#         num = ''.join([str(random.randint(0, 9)) for _ in range(8)])
#         # Calcular la letra del DNI
#         letras = 'TRWAGMYFPDXBNJZSQVHLCKE'
#         letra = letras[int(num) % 23]
#         return f"{num}{letra}"
    
#     # Generar NIPs únicos (pre-generados)
    print("Generando NIPs únicos...")
    used_nips = set()
    nips = []
    while len(used_nips) < n:
        nip = fake.random_number(digits=8)
        if nip not in used_nips:
            used_nips.add(nip)
            nips.append(nip)
    
    # Generar DNIs únicos (pre-generados)
    print("Generando DNIs únicos...")
    used_dnis = set()
    dnis = []
    while len(used_dnis) < n:
        dni = generate_dni()
        if dni not in used_dnis:
            used_dnis.add(dni)
            dnis.append(dni)
    
    print(f"Generando {n} registros de personas...")
    # Generación de datos mucho más rápida ahora que ya tenemos NIPs y DNIs únicos
    for i in range(1, n+1):
        nombre = fake.first_name()
        apellido1 = fake.last_name()
        apellido2 = fake.last_name()
        apellidos_nombre = f"{apellido1} {apellido2}, {nombre}"
        
        # Usar NIP y DNI pre-generados
        nip = nips[i-1]
        documento = dnis[i-1]
        
        # Sexo aleatorio
        sexo = random.choice(['H', 'M'])
        
        # País de nacionalidad
        id_pais_nacionalidad = random.choice(paises_ids)
        id_pais_nacionalidad_nk = paises_df[paises_df['ID_PAIS'] == id_pais_nacionalidad]['ID_PAIS_NK'].values[0]
        
        # Correo electrónico
        email = fake.email()
        
        # Fecha de nacimiento y año
        fecha_nacimiento = fake.date_of_birth(minimum_age=18, maximum_age=70)
        fecha_nacimiento_txt = fecha_nacimiento.strftime('%d/%m/%Y')
        anyo_nacimiento = fecha_nacimiento.year
        
        # Generar ID ofuscado (hash MD5 basado en NIP y documento)
        id_ofuscado = hashlib.md5(f"{nip}_{documento}".encode()).hexdigest()
        
        data.append({
            'ID_PERSONA': i,
            'ID_PERSONA_NIP_NK': nip,
            'DOCUMENTO_IDENTIDAD': documento,
            'APELLIDO1': apellido1,
            'APELLIDO2': apellido2,
            'NOMBRE': nombre,
            'APELLIDOS_NOMBRE': apellidos_nombre,
            'ID_OFUSCADO': id_ofuscado,
            'SEXO': sexo,
            'ID_PAIS_NACIONALIDAD_NK': id_pais_nacionalidad_nk,
            'EMAIL': email,
            'FECHA_NACIMIENTO_TXT': fecha_nacimiento_txt,
            'ANYO_NACIMIENTO': anyo_nacimiento
        ,
            'APELLIDO1': None  # AGREGADO: Columna requerida por esquema,
            'APELLIDO2': None  # AGREGADO: Columna requerida por esquema})
        
        # Mostrar progreso cada 100 registros
        if i % 100 == 0:
            print(f"Generados {i}/{n} registros de personas ({i/n*100:.1f}%)...")
    
    return pd.DataFrame(data)

def generate_d_poblacion(n=500, paises_df=None):
    """Genera datos para la tabla D_POBLACION"""
    data = []
    
    # Si no se proporciona un dataframe de países, crear uno mínimo
    if paises_df is None:
        paises_df = generate_d_pais(n=10)
    
    # Lista de provincias españolas con sus CCAA
    provincias_ccaa = [
        ("Álava", "País Vasco"),
        ("Albacete", "Castilla-La Mancha"),
        ("Alicante", "Comunidad Valenciana"),
        ("Almería", "Andalucía"),
        ("Asturias", "Principado de Asturias"),
        ("Ávila", "Castilla y León"),
        ("Badajoz", "Extremadura"),
        ("Barcelona", "Cataluña"),
        ("Burgos", "Castilla y León"),
        ("Cáceres", "Extremadura"),
        ("Cádiz", "Andalucía"),
        ("Cantabria", "Cantabria"),
        ("Castellón", "Comunidad Valenciana"),
        ("Ciudad Real", "Castilla-La Mancha"),
        ("Córdoba", "Andalucía"),
        ("Cuenca", "Castilla-La Mancha"),
        ("Gerona", "Cataluña"),
        ("Granada", "Andalucía"),
        ("Guadalajara", "Castilla-La Mancha"),
        ("Guipúzcoa", "País Vasco"),
        ("Huelva", "Andalucía"),
        ("Huesca", "Aragón"),
        ("Islas Baleares", "Islas Baleares"),
        ("Jaén", "Andalucía"),
        ("La Coruña", "Galicia"),
        ("La Rioja", "La Rioja"),
        ("Las Palmas", "Canarias"),
        ("León", "Castilla y León"),
        ("Lérida", "Cataluña"),
        ("Lugo", "Galicia"),
        ("Madrid", "Comunidad de Madrid"),
        ("Málaga", "Andalucía"),
        ("Murcia", "Región de Murcia"),
        ("Navarra", "Comunidad Foral de Navarra"),
        ("Orense", "Galicia"),
        ("Palencia", "Castilla y León"),
        ("Pontevedra", "Galicia"),
        ("Salamanca", "Castilla y León"),
        ("Santa Cruz de Tenerife", "Canarias"),
        ("Segovia", "Castilla y León"),
        ("Sevilla", "Andalucía"),
        ("Soria", "Castilla y León"),
        ("Tarragona", "Cataluña"),
        ("Teruel", "Aragón"),
        ("Toledo", "Castilla-La Mancha"),
        ("Valencia", "Comunidad Valenciana"),
        ("Valladolid", "Castilla y León"),
        ("Vizcaya", "País Vasco"),
        ("Zamora", "Castilla y León"),
        ("Zaragoza", "Aragón"),
        ("Ceuta", "Ceuta"),
        ("Melilla", "Melilla")
    ]
    
    # Lista de países disponibles
    paises_ids = paises_df['ID_PAIS'].tolist()
    paises_nombres = paises_df['NOMBRE_PAIS'].tolist()
    
    # Diccionario para mapear país a su ID
    pais_to_id = {paises_df.iloc[i]['NOMBRE_PAIS']: paises_df.iloc[i]['ID_PAIS'] for i in range(len(paises_df))}
    
    # Asegurarnos que España está en la lista
    if 'España' not in pais_to_id:
        pais_to_id['España'] = 1
        
    # Generar poblaciones españolas con datos de provincia y CCAA
    num_provincias = len(provincias_ccaa)
    ciudades_por_provincia = max(2, n // (2 * num_provincias))  # Al menos 2 ciudades por provincia
    num_ciudades_esp = num_provincias * ciudades_por_provincia

    # Función auxiliar para truncar texto a un máximo de caracteres
    def truncar_texto(texto, max_length=50):
        if len(texto) > max_length:
            return texto[:max_length-3] + "..."
        return texto
    
    # Contador para IDs de población
    id_poblacion = 1
    
    # Generar poblaciones españolas
    for provincia, ccaa in provincias_ccaa:
        id_provincia = random.randint(1000, 1999)
        id_ccaa = random.randint(1000, 1999)
        
        # Limitar el tamaño de los nombres
        nombre_provincia = truncar_texto(provincia, 50)
        nombre_ccaa = truncar_texto(ccaa, 50)
        
        # Crear el número de ciudades por provincia definido
        for j in range(ciudades_por_provincia):
            nombre_ciudad = fake.city()
            
            data.append({
                'ID_POBLACION': id_poblacion,
                'NOMBRE_POBLACION': nombre_ciudad,# 
                'ID_PROVINCIA': ...,  # ELIMINADO: No existe en esquema
                'NOMBRE_PROVINCIA': nombre_provincia,# 
                'ID_CCAA': ...,  # ELIMINADO: No existe en esquema# 
                'NOMBRE_CCAA': ...,  # ELIMINADO: No existe en esquema
                'ID_PAIS': pais_to_id['España'],
                'NOMBRE_PAIS': 'España',
                'FECHA_CARGA': generate_random_date(2020, 2023)
            })
            
            id_poblacion += 1
    
    # Generar poblaciones extranjeras sin datos de provincia/CCAA
    num_ciudades_ext = n - num_ciudades_esp
    
    # Excluir España de la lista para generar ciudades extranjeras
    paises_ids_ext = [pid for pid in paises_ids if pid != pais_to_id.get('España', 1)]
    paises_nombres_ext = [p for p in paises_nombres if p != 'España']
    
    if not paises_ids_ext:
        # Si no hay países extranjeros disponibles, usar solo España
        paises_ids_ext = [pais_to_id.get('España', 1)]
        paises_nombres_ext = ['España']
    
    for i in range(num_ciudades_ext):
        # Seleccionar un país aleatorio que no sea España
        idx = random.randint(0, len(paises_ids_ext) - 1) if len(paises_ids_ext) > 0 else 0
        
        # Verificar que el índice no está fuera de rango
        if len(paises_ids_ext) == 0:
            # Si no hay países disponibles, usar valores predeterminados
            id_pais = 1
            nombre_pais = "País por defecto"
        else:
            # Asegurarse de que el índice está dentro del rango
            idx = min(idx, len(paises_ids_ext) - 1)
            id_pais = paises_ids_ext[idx]
            nombre_pais = paises_nombres_ext[idx] if idx < len(paises_nombres_ext) else "País desconocido"
        
        # Generar datos ficticios de provincia y CCAA para países extranjeros
        nombre_provincia = truncar_texto(f"Provincia de {nombre_pais}", 50)
        nombre_ccaa = truncar_texto(f"Región de {nombre_pais}", 50)
        
        data.append({
            'ID_POBLACION': id_poblacion,
            'NOMBRE_POBLACION': fake.city(),
            'ID_PROVINCIA': random.randint(1000, 1999),# 
            'NOMBRE_PROVINCIA': ...,  # ELIMINADO: No existe en esquema
            'ID_CCAA': random.randint(1000, 1999),# 
            'NOMBRE_CCAA': ...,  # ELIMINADO: No existe en esquema
            'ID_PAIS': id_pais,
            'NOMBRE_PAIS': nombre_pais,
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
        
        id_poblacion += 1
    
    return pd.DataFrame(data)

def generate_d_asignatura(n=2000):
    """Genera datos para la tabla D_ASIGNATURA"""
    data = []
    
    # Lista de prefijos de asignaturas por área
    prefijos = {
        'Matemáticas': ['Álgebra', 'Cálculo', 'Estadística', 'Geometría', 'Análisis'],
        'Informática': ['Programación', 'Bases de Datos', 'Sistemas', 'Redes', 'Algoritmos'],
        'Física': ['Mecánica', 'Electromagnetismo', 'Termodinámica', 'Óptica', 'Cuántica'],
        'Química': ['Química Orgánica', 'Química Inorgánica', 'Bioquímica', 'Analítica', 'Fisicoquímica'],
        'Biología': ['Botánica', 'Zoología', 'Genética', 'Ecología', 'Microbiología'],
        'Economía': ['Macroeconomía', 'Microeconomía', 'Contabilidad', 'Finanzas', 'Marketing'],
        'Derecho': ['Derecho Civil', 'Derecho Penal', 'Derecho Administrativo', 'Derecho Laboral', 'Derecho Mercantil'],
        'Historia': ['Historia Antigua', 'Historia Medieval', 'Historia Moderna', 'Historia Contemporánea', 'Arqueología'],
        'Filología': ['Lingüística', 'Literatura', 'Gramática', 'Fonética', 'Semántica'],
        'Medicina': ['Anatomía', 'Fisiología', 'Patología', 'Farmacología', 'Cirugía']
    }
    
    # Sufijos y complementos para nombres de asignaturas
    sufijos = ['I', 'II', 'III', 'Avanzada', 'Básica', 'Aplicada', 'General', 'Especial', 'Fundamental']
    complementos = ['para Ingenieros', 'para Científicos', 'Computacional', 'Experimental', 'Teórica', 'Práctica']
    
    # Generar asignaturas
    for i in tqdm(range(1, n+1), desc="Generando asignaturas"):
        # Seleccionar área y prefijo
        area = random.choice(list(prefijos.keys()))
        prefijo = random.choice(prefijos[area])
        
        # Decidir si añadir sufijo y/o complemento
        add_suffix = random.random() > 0.3
        add_complement = random.random() > 0.7
        
        nombre = prefijo
        if add_suffix:
            nombre += " " + random.choice(sufijos)
        if add_complement:
            nombre += " " + random.choice(complementos)
        
        data.append({
            'ID_ASIGNATURA': i,
            'NOMBRE_ASIGNATURA': nombre,
            'ID_ASIGNATURA_NK': i
        })
    
    return pd.DataFrame(data)

def generate_d_tipo_acceso_preinscripcion(n=15):
    """Genera datos para la tabla D_TIPO_ACCESO_PREINSCRIPCION"""
    data = []
    
    tipos_acceso = [
        ('1PAU', 'Prueba de Acceso Universitaria'),
        ('2FP', 'Formación Profesional'),
        ('3TIT', 'Titulados Universitarios'),
        ('4M25', 'Mayores de 25 años'),
        ('5M45', 'Mayores de 45 años'),
        ('6EXT', 'Sistemas educativos extranjeros'),
        ('7DEP', 'Deportistas de alto nivel'),
        ('8DIS', 'Estudiantes con discapacidad'),
        ('9CRE', 'Credencial UNED'),
        ('10TR', 'Traslado de expediente'),
        ('11CV', 'Convalidación parcial'),
        ('12VM', 'Víctimas violencia'),
        ('13FA', 'Familia numerosa especial'),
        ('14RP', 'Reconocimiento profesional'),
        ('15OT', 'Otros')
    ]
    
    for i, (id_nk, nombre) in enumerate(tipos_acceso, 1):
        data.append({
            'ID_TIPO_ACCESO_PREINS': i,
            'NOMBRE_TIPO_ACCESO_PREINS': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023),# 
            'ID_TIPO_ACCESO_PREINS_NK': ...,  # ELIMINADO: No existe en esquema
        })
    
    return pd.DataFrame(data)

def generate_d_plan_estudio(n=500):
    """Genera datos para la tabla D_PLAN_ESTUDIO"""
    data = []
    
    # Lista de nombres de planes de estudio
    nombres_planes = [
        "Grado en Ingeniería Informática",
        "Grado en Administración y Dirección de Empresas",
        "Grado en Derecho",
        "Grado en Medicina",
        "Grado en Psicología",
        "Grado en Arquitectura",
        "Grado en Biología",
        "Grado en Química",
        "Grado en Física",
        "Grado en Matemáticas",
        "Grado en Historia",
        "Grado en Filología Hispánica",
        "Grado en Economía",
        "Grado en Enfermería",
        "Grado en Farmacia",
        "Grado en Veterinaria",
        "Grado en Periodismo",
        "Grado en Comunicación Audiovisual",
        "Grado en Bellas Artes",
        "Grado en Educación Primaria",
        "Máster Universitario en Inteligencia Artificial",
        "Máster Universitario en Administración de Empresas",
        "Máster Universitario en Abogacía",
        "Máster Universitario en Investigación Biomédica",
        "Máster Universitario en Psicología General Sanitaria",
        "Doctorado en Informática",
        "Doctorado en Economía y Empresa",
        "Doctorado en Derecho",
        "Doctorado en Medicina",
        "Doctorado en Psicología"
    ]
    
    # Multiplicar la lista para tener suficientes nombres
    nombres_planes = (nombres_planes * (n // len(nombres_planes) + 1))[:n]
    
    for i in range(1, n+1):
        nombre_plan = nombres_planes[i-1]
        
        data.append({
            'ID_PLAN_ESTUDIO': i  # TODO: Usar valores válidos de F_TABLA_FUSION,
            'ID_PLAN_ESTUDIO_NK': 10000 + i,
            'ORD_NOMBRE_PLAN_ESTUDIO': nombre_plan.upper(),
            'NOMBRE_PLAN_ESTUDIO': nombre_plan
        })
    
    return pd.DataFrame(data)

def generate_d_campus(n=10):
    """Genera datos para la tabla D_CAMPUS"""
    data = []
    
    campus_names = [
        'Campus Central',
        'Campus Norte',
        'Campus Sur',
        'Campus Este',
        'Campus Oeste',
        'Campus Río',
        'Campus Ciudad',
        'Campus Tecnológico',
        'Campus Científico',
        'Campus Humanidades'
    ]
    
    for i, nombre in enumerate(campus_names[:n], 1):
        data.append({
            'ID_CAMPUS': i,
            'NOMBRE_CAMPUS': nombre
        })
    
    return pd.DataFrame(data)

def generate_d_articulo(n=50):
    """Genera datos para la tabla D_ARTICULO"""
    data = []
    
    for i in range(1, n+1):
        titulo = fake.sentence(nb_words=6)
        
        data.append({
            'ID_ARTICULO': i,
            'NOMBRE_ARTICULO': titulo[:300]  # Limitar a 300 caracteres
        })
    
    return pd.DataFrame(data)

def generate_d_edad_est(n=10):
    """Genera datos para la tabla D_EDAD_EST
    
    Tabla de edad estadística para agrupaciones en informes.
    
    Args:
        n (int): Número de rangos de edad a generar (máx. 10)
    
    Returns:
        DataFrame: DataFrame con los datos generados
    """
    data = []
    
    # Rangos de edad comunes en entorno académico con descripciones detalladas
    rangos_edad = [
        ('16-18', 'Menor de edad', 'Estudiantes menores de edad legal'),
        ('19-21', 'Joven', 'Estudiantes jóvenes (19-21 años)'),
        ('22-25', 'Joven adulto', 'Estudiantes jóvenes adultos (22-25 años)'),
        ('26-30', 'Adulto joven', 'Adultos jóvenes (26-30 años)'),
        ('31-40', 'Adulto', 'Adultos (31-40 años)'),
        ('41-50', 'Adulto medio', 'Adultos de mediana edad (41-50 años)'),
        ('51-65', 'Adulto mayor', 'Adultos mayores (51-65 años)'),
        ('>65', 'Senior', 'Estudiantes senior (mayores de 65 años)'),
        ('NC', 'No consta', 'Edad no disponible en los sistemas'),
        ('DESC', 'Desconocido', 'Edad desconocida o no registrada')
    ]
    
    # Limitar al número solicitado
    rangos_edad = rangos_edad[:n]
    
    for i, (id_edad_est_nk, nombre_edad_est, descripcion) in enumerate(rangos_edad, 1):
        data.append({
            'ID_EDAD_EST': i,
            'ID_EDAD_EST_NK': id_edad_est_nk,
            'NOMBRE_EDAD_EST': nombre_edad_est,# 
            'DESCRIPCION_EDAD_EST': ...,  # ELIMINADO: No existe en esquema
            'EDAD_MINIMA': int(id_edad_est_nk.split('-')[0]) if '-' in id_edad_est_nk and id_edad_est_nk[0].isdigit() else None,# 
            'EDAD_MAXIMA': ...,  # ELIMINADO: No existe en esquema
        })
    
    return pd.DataFrame(data)

def generate_d_dedicacion(n=5):
    """Genera datos para la tabla D_DEDICACION con todos los atributos completos
    
    Esta función genera datos completos para la tabla D_DEDICACION, incluyendo
    todos los atributos descriptivos y técnicos necesarios.
    
    Args:
        n (int): Número de tipos de dedicación a generar (máx. 5)
        
    Returns:
        DataFrame: DataFrame con los datos generados
    """
    data = []
    
    dedicaciones = [
        ('TC', 'Tiempo completo', 'Dedicación completa a la actividad académica', 1, 100, 37.5, 'S', 'N'),
        ('TP', 'Tiempo parcial', 'Dedicación parcial, compatible con otras actividades', 2, 60, 20.0, 'N', 'S'),
        ('PH', 'Por horas', 'Dedicación por horas de actividad específica', 3, 30, 10.0, 'N', 'S'),
        ('CR', 'Por créditos', 'Dedicación por créditos asignados', 4, 40, 15.0, 'N', 'S'),
        ('SD', 'Sin determinar', 'Dedicación pendiente de asignar', 5, 0, 0.0, 'N', 'N')
    ]
    
    for i, (id_nk, nombre, descripcion, orden, porcentaje, horas, completa, parcial) in enumerate(dedicaciones[:n], 1):
        fecha_carga = generate_random_date_datetime(2018, 2023)
        fecha_vigencia = generate_random_date_datetime(2023, 2025)
        
        data.append({
            'ID_DEDICACION': i,
            'ID_DEDICACION_NK': id_nk,
            'NOMBRE_DEDICACION': nombre,# 
            'DESCRIPCION_DEDICACION': ...,  # ELIMINADO: No existe en esquema
            'ORDEN_VISUALIZACION': orden,# 
            'PORCENTAJE_DEDICACION': ...,  # ELIMINADO: No existe en esquema
            'HORAS_SEMANALES': horas,# 
            'FECHA_CARGA': ...,  # ELIMINADO: No existe en esquema# 
            'FECHA_FIN_VIGENCIA': ...,  # ELIMINADO: No existe en esquema# 
            'SN_TIEMPO_COMPLETO': ...,  # ELIMINADO: No existe en esquema
            'SN_TIEMPO_PARCIAL': parcial,# 
            'FLG_TIEMPO_COMPLETO': ...,  # ELIMINADO: No existe en esquema
            'FLG_TIEMPO_PARCIAL': 1 if parcial == 'S' else 0,# 
            'ES_ACTIVO': ...,  # ELIMINADO: No existe en esquema# 
            'SN_ACTIVO': ...,  # ELIMINADO: No existe en esquema
        })
    
    return pd.DataFrame(data)

def generate_d_dedicacion_profesor(n=5):
    """Genera datos para la tabla D_DEDICACION_PROFESOR con todos los atributos completos
    
    Esta función genera datos completos para la tabla D_DEDICACION_PROFESOR, incluyendo
    todos los atributos descriptivos y técnicos necesarios. Es similar a D_DEDICACION
    pero específica para profesores.
    
    Args:
        n (int): Número de tipos de dedicación a generar (máx. 5)
        
    Returns:
        DataFrame: DataFrame con los datos generados
    """
    data = []
    
    dedicaciones = [
        ('TC', 'Tiempo completo', 'Dedicación completa a la actividad docente', 1, 100, 37.5, 'S', 'N'),
        ('TP', 'Tiempo parcial', 'Dedicación parcial a la docencia', 2, 60, 20.0, 'N', 'S'),
        ('AS', 'Asociado', 'Profesor asociado con dedicación parcial', 3, 30, 12.0, 'N', 'S'),
        ('VI', 'Visitante', 'Profesor visitante con dedicación variable', 4, 40, 15.0, 'N', 'S'),
        ('OT', 'Otra', 'Otro tipo de dedicación', 5, 0, 0.0, 'N', 'N')
    ]
    
    for i, (id_nk, nombre, descripcion, orden, porcentaje, horas, completa, parcial) in enumerate(dedicaciones[:n], 1):
        fecha_carga = generate_random_date_datetime(2018, 2023)
        fecha_vigencia = generate_random_date_datetime(2023, 2025)
        
        data.append({
            'ID_DEDICACION': i,
            'ID_DEDICACION_NK': id_nk,
            'NOMBRE_DEDICACION': nombre,# 
            'DESCRIPCION_DEDICACION': ...,  # ELIMINADO: No existe en esquema
            'ORDEN_VISUALIZACION': orden,# 
            'PORCENTAJE_DEDICACION': ...,  # ELIMINADO: No existe en esquema
            'HORAS_SEMANALES': horas,# 
            'FECHA_CARGA': ...,  # ELIMINADO: No existe en esquema# 
            'FECHA_FIN_VIGENCIA': ...,  # ELIMINADO: No existe en esquema# 
            'SN_TIEMPO_COMPLETO': ...,  # ELIMINADO: No existe en esquema
            'SN_TIEMPO_PARCIAL': parcial,# 
            'FLG_TIEMPO_COMPLETO': ...,  # ELIMINADO: No existe en esquema
            'FLG_TIEMPO_PARCIAL': 1 if parcial == 'S' else 0,# 
            'ES_ACTIVO': ...,  # ELIMINADO: No existe en esquema# 
            'SN_ACTIVO': ...,  # ELIMINADO: No existe en esquema
        })
    
    return pd.DataFrame(data)

def generate_d_estado_adjudicacion(n=7):
    """Genera datos para la tabla D_ESTADO_ADJUDICACION"""
    data = []
    
    estados = [
        ('ADM', 'Admitido'),
        ('LIS', 'Lista de espera'),
        ('EXC', 'Excluido'),
        ('REN', 'Renuncia'),
        ('PTE', 'Pendiente'),
        ('REV', 'En revisión'),
        ('FIN', 'Finalizado')
    ]
    
    for i, (id_nk, nombre) in enumerate(estados, 1):
        data.append({
            'ID_ESTADO_ADJUDICACION': i,
            'NOMBRE_ESTADO_ADJUDICACION': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023),# 
            'ID_ESTADO_ADJUDICACION_NK': ...,  # ELIMINADO: No existe en esquema
        })
    
    return pd.DataFrame(data)

def generate_d_tipo_docencia(n=5):
    """Genera datos para la tabla D_TIPO_DOCENCIA"""
    data = []
    
    tipos_docencia = [
        'Presencial',
        'Semipresencial',
        'Virtual',
        'A distancia',
        'Híbrida'
    ]
    
    for i, nombre in enumerate(tipos_docencia[:n], 1):
        data.append({
            'ID_TIPO_DOCENCIA': i,
            'NOMBRE_TIPO_DOCENCIA': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
    
    return pd.DataFrame(data)

def generate_d_tipo_egreso(n=6):
    """Genera datos para la tabla D_TIPO_EGRESO"""
    data = []
    
    tipos_egreso = [
        'Graduación',
        'Finalización de estudios',
        'Traslado a otra universidad',
        'Baja voluntaria',
        'Baja administrativa',
        'Otros'
    ]
    
    for i, nombre in enumerate(tipos_egreso[:n], 1):
        data.append({
            'ID_TIPO_EGRESO': i,
            'NOMBRE_TIPO_EGRESO': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
    
    return pd.DataFrame(data)

def generate_d_tipo_abandono(n=7):
    """Genera datos para la tabla D_TIPO_ABANDONO"""
    data = []
    
    tipos_abandono = [
        'Abandono voluntario',
        'Abandono por rendimiento académico',
        'Abandono por motivos laborales',
        'Abandono por motivos personales',
        'Abandono por cambio de titulación',
        'Abandono por traslado a otra universidad',
        'Otros motivos'
    ]
    
    for i, nombre in enumerate(tipos_abandono[:n], 1):
        data.append({
            'ID_TIPO_ABANDONO': i,
            'NOMBRE_TIPO_ABANDONO': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
    
    return pd.DataFrame(data)

def generate_d_tipo_procedimiento(n=5):
    """Genera datos para la tabla D_TIPO_PROCEDIMIENTO"""
    data = []
    
    tipos_procedimiento = [
        'Admisión ordinaria',
        'Admisión por traslado',
        'Admisión por reconocimiento',
        'Admisión excepcional',
        'Admisión específica'
    ]
    
    for i, nombre in enumerate(tipos_procedimiento[:n], 1):
        data.append({
            'ID_TIPO_PROCEDIMIENTO': i,
            'NOMBRE_TIPO_PROCEDIMIENTO': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
    
    return pd.DataFrame(data)

def generate_d_tipo_reconocimiento(n=5):
    """Genera datos para la tabla D_TIPO_RECONOCIMIENTO"""
    data = []
    
    tipos_reconocimiento = [
        ('A', 'Reconocimiento académico'),
        ('P', 'Reconocimiento profesional'),
        ('E', 'Reconocimiento por experiencia laboral'),
        ('T', 'Reconocimiento por título propio'),
        ('O', 'Otros reconocimientos')
    ]
    
    for i, (id_nk, nombre) in enumerate(tipos_reconocimiento[:n], 1):
        data.append({
            'ID_TIPO_RECONOCIMIENTO': i,
            'NOMBRE_TIPO_RECONOCIMIENTO': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023),
            'ID_TIPO_RECONOCIMIENTO_NK': id_nk
        })
    
    return pd.DataFrame(data)

def generate_d_cupo_adjudicacion(n=6):
    """Genera datos para la tabla D_CUPO_ADJUDICACION"""
    data = []
    
    cupos = [
        ('GRAL', 'Cupo general'),
        ('M25A', 'Mayores de 25 años'),
        ('M40A', 'Mayores de 40 años'),
        ('M45A', 'Mayores de 45 años'),
        ('DISC', 'Discapacidad'),
        ('DALT', 'Deportistas alto nivel')
    ]
    
    for i, (id_nk, nombre) in enumerate(cupos[:n], 1):
        data.append({
            'ID_CUPO_ADJUDICACION': i,
            'NOMBRE_CUPO_ADJUDICACION': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023),
            'ID_CUPO_ADJUDICACION_NK': id_nk
        })
    
    return pd.DataFrame(data)

def generate_d_rango_credito(n=7):
    """Genera datos para la tabla D_RANGO_CREDITO"""
    data = []
    
    rangos = [
        ('0-5', '0 a 5 créditos'),
        ('6-10', '6 a 10 créditos'),
        ('11-20', '11 a 20 créditos'),
        ('21-30', '21 a 30 créditos'),
        ('31-45', '31 a 45 créditos'),
        ('46-60', '46 a 60 créditos'),
        ('>60', 'Más de 60 créditos')
    ]
    
    for i, (id_nk, nombre) in enumerate(rangos[:n], 1):
        data.append({
            'ID_RANGO_CREDITO': i,
            'ID_RANGO_CREDITO_NK': id_nk,
            'NOMBRE_RANGO_CREDITO': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
    
    return pd.DataFrame(data)

def generate_d_rango_edad(n=8):
    """Genera datos para la tabla D_RANGO_EDAD"""
    data = []
    
    rangos = [
        ('17-18', '17 a 18 años'),
        ('19-20', '19 a 20 años'),
        ('21-22', '21 a 22 años'),
        ('23-25', '23 a 25 años'),
        ('26-30', '26 a 30 años'),
        ('31-40', '31 a 40 años'),
        ('41-50', '41 a 50 años'),
        ('>50', 'Más de 50 años')
    ]
    
    for i, (id_nk, nombre) in enumerate(rangos[:n], 1):
        data.append({
            'ID_RANGO_EDAD': i,
            'ID_RANGO_EDAD_NK': id_nk,
            'NOMBRE_RANGO_EDAD': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
    
    return pd.DataFrame(data)

def generate_d_rango_nota_admision(n=5):
    """Genera datos para la tabla D_RANGO_NOTA_ADMISION"""
    data = []
    
    rangos = [
        (1, '5 a 6'),
        (2, '6 a 7'),
        (3, '7 a 8'),
        (4, '8 a 9'),
        (5, '9 a 10')
    ]
    
    for i, (id_nk, nombre) in enumerate(rangos[:n], 1):
        data.append({
            'ID_RANGO_NOTA_ADMISION': i,
            'ID_RANGO_NOTA_ADMISION_NK': id_nk,
            'NOMBRE_RANGO_NOTA_ADMISION': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
    
    return pd.DataFrame(data)

def generate_d_rango_nota_numerica(n=5):
    """Genera datos para la tabla D_RANGO_NOTA_NUMERICA"""
    data = []
    
    rangos = [
        ('0-4.9', 'Suspenso'),
        ('5-6.9', 'Aprobado'),
        ('7-8.9', 'Notable'),
        ('9-9.9', 'Sobresaliente'),
        ('10', 'Matrícula de Honor')
    ]
    
    for i, (id_nk, nombre) in enumerate(rangos[:n], 1):
        data.append({
            'ID_RANGO_NOTA_NUMERICA': i,
            'ID_RANGO_NOTA_NUMERICA_NK': id_nk,
            'NOMBRE_RANGO_NOTA_NUMERICA': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
    
    return pd.DataFrame(data)

def generate_d_rango_nota_crue(n=5):
    """Genera datos para la tabla D_RANGO_NOTA_CRUE"""
    data = []
    
    rangos = [
        ('0-4.9', 'Suspenso CRUE'),
        ('5-6.9', 'Aprobado CRUE'),
        ('7-8.9', 'Notable CRUE'),
        ('9-9.9', 'Sobresaliente CRUE'),
        ('10', 'MH CRUE')
    ]
    
    for i, (id_nk, nombre) in enumerate(rangos[:n], 1):
        data.append({
            'ID_RANGO_NOTA_CRUE': i,
            'ID_RANGO_NOTA_CRUE_NK': id_nk,
            'NOMBRE_RANGO_NOTA_CRUE': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
    
    return pd.DataFrame(data)

def generate_d_rango_nota_egracons(n=10):
    """Genera datos para la tabla D_RANGO_NOTA_EGRACONS con todos los atributos completos
    
    Esta función genera datos completos para la tabla D_RANGO_NOTA_EGRACONS, incluyendo
    todos los metadatos necesarios para el sistema europeo de calificaciones EGRACONS.
    
    Args:
        n (int): Número de rangos a generar (máx. 10)
        
    Returns:
        DataFrame: DataFrame con los datos generados
    """
    data = []
    
    # Definir rangos con nombres abreviados para cumplir con el límite de 20 caracteres
    rangos = [
        ('A', 'Excelente', 9.0, 10.0, 8.8, 'Resultados excepcionales', 'A+,A', 'Sobresaliente', 'BEST_10P'),
        ('B', 'Muy Bueno', 8.0, 8.8, 7.5, 'Resultados superiores a la media', 'B+,B', 'Notable alto', 'BEST_25P'),
        ('C', 'Bueno', 7.0, 7.5, 6.5, 'Trabajo sólido por encima de la media', 'C+,C', 'Notable', 'BEST_35P'),
        ('D', 'Satisfactorio', 6.0, 6.5, 5.5, 'Trabajo aceptable', 'D+,D', 'Aprobado alto', 'BEST_65P'),
        ('E', 'Suficiente', 5.0, 5.5, 5.0, 'Cumple con los requisitos mínimos', 'E', 'Aprobado', 'BEST_90P'),
        ('FX', 'Suspenso (FX)', 4.0, 4.9, 3.0, 'Se requiere trabajo adicional', 'FX', 'Suspenso alto', 'FAIL_FX'),
        ('F', 'Suspenso (F)', 2.5, 2.9, 0.0, 'Se requiere considerable trabajo adicional', 'F', 'Suspenso', 'FAIL_F'),
        ('NP', 'No Presentado', 0.0, 0.0, 0.0, 'No presentado a evaluación', '-', 'No Presentado', 'NP'),
        ('MH', 'Matrícula Honor', 10.0, 10.0, 10.0, 'Reconocimiento especial de excelencia', 'A+', 'Matrícula de Honor', 'MH'),
        ('PC', 'Pendiente Calif.', None, None, None, 'Calificación pendiente de emitir', '-', 'Pendiente', 'PC')
    ]
    
    # Asegurar que no excedemos el número solicitado
    rangos = rangos[:n]
    
    for i, (id_nk, nombre, nota_ref, limite_sup, limite_inf, desc, equiv_ects, equiv_esp, codigo_tipo) in enumerate(rangos, 1):
        fecha_carga = generate_random_date_datetime(2020, 2023)
        
        data.append({
            'ID_RANGO_NOTA_EGRACONS': i,
            'ID_RANGO_NOTA_EGRACONS_NK': id_nk,
            'NOMBRE_RANGO_NOTA_EGRACONS': nombre,
            'NOTA_REFERENCIA': nota_ref,
            'LIMITE_SUPERIOR': limite_sup,# 
            'LIMITE_INFERIOR': ...,  # ELIMINADO: No existe en esquema# 
            'DESCRIPCION_EGRACONS': ...,  # ELIMINADO: No existe en esquema# 
            'EQUIVALENCIA_ECTS': ...,  # ELIMINADO: No existe en esquema# 
            'EQUIVALENCIA_ESP': ...,  # ELIMINADO: No existe en esquema
            'CODIGO_TIPO_EGRACONS': codigo_tipo,# 
            'FECHA_CARGA': ...,  # ELIMINADO: No existe en esquema# 
            'ORDEN_VISUALIZACION': ...,  # ELIMINADO: No existe en esquema
            'ES_APROBADO': 1 if id_nk in ['A', 'B', 'C', 'D', 'E', 'MH'] else 0,
            'SN_APROBADO': 'S' if id_nk in ['A', 'B', 'C', 'D', 'E', 'MH'] else 'N'
        })
    
    return pd.DataFrame(data)

def generate_d_estudio_previo(n=10):
    """Genera datos para la tabla D_ESTUDIO_PREVIO"""
    data = []
    
    estudios_previos = [
        ('BACH', 'Bachillerato'),
        ('CFGS', 'Ciclo Formativo de Grado Superior'),
        ('CFGM', 'Ciclo Formativo de Grado Medio'),
        ('GRAD', 'Grado Universitario'),
        ('DIPL', 'Diplomatura'),
        ('LICE', 'Licenciatura'),
        ('MAST', 'Máster Universitario'),
        ('DOCT', 'Doctorado'),
        ('TPRO', 'Título Propio'),
        ('EXTR', 'Estudios extranjeros homologados')
    ]
    
    for i, (id_nk, nombre) in enumerate(estudios_previos[:n], 1):
        data.append({
            'ID_ESTUDIO_PREVIO': i,
            'NOMBRE_ESTUDIO_PREVIO': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023),
            'ID_ESTUDIO_PREVIO_NK': id_nk
        })
    
    return pd.DataFrame(data)

def generate_d_nacionalidad(n=50, paises_df=None):
    """Genera datos para la tabla D_NACIONALIDAD con el atributo NOMBRE_PAIS"""
    data = []
    
    # Si no se proporciona un dataframe de países, crear uno mínimo
    if paises_df is None:
        paises_df = generate_d_pais(n=50)
    
    # Seleccionar n países para generar nacionalidades
    paises_muestra = paises_df.sample(min(n, len(paises_df)))
    
    for i, pais in enumerate(paises_muestra.iterrows(), 1):
        nombre_pais = pais[1]['NOMBRE_PAIS']
        nombre_nacionalidad = pais[1]['NOMBRE_NACIONALIDAD']
        
        # Para el caso de España/Española, ajustar manualmente si es necesario
        if nombre_pais == 'España' and nombre_nacionalidad != 'Española':
            nombre_nacionalidad = 'Española'
        
        data.append({
            'ID_NACIONALIDAD': i,
            'NOMBRE_NACIONALIDAD': nombre_nacionalidad,
            'NOMBRE_PAIS': nombre_pais
        })
    
    return pd.DataFrame(data)

def generate_d_idioma_movilidad(n=15):
    """Genera datos para la tabla D_IDIOMA_MOVILIDAD"""
    data = []
    
    idiomas = [
        ('Español', 1),
        ('Inglés', 2),
        ('Francés', 3),
        ('Alemán', 4),
        ('Italiano', 5),
        ('Portugués', 6),
        ('Ruso', 7),
        ('Chino', 8),
        ('Japonés', 9),
        ('Árabe', 10),
        ('Neerlandés', 11),
        ('Sueco', 12),
        ('Noruego', 13),
        ('Danés', 14),
        ('Polaco', 15)
    ]
    
    for i, (nombre, id_nk) in enumerate(idiomas[:n], 1):
        data.append({
            'ID_IDIOMA_MOVILIDAD': i,
            'NOMBRE_IDIOMA_MOVILIDAD': nombre,
            'ID_IDIOMA_MOVILIDAD_NK': id_nk,
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
    
    return pd.DataFrame(data)

def generate_d_nivel_estudios_movilidad(n=8):
    """Genera datos para la tabla D_NIVEL_ESTUDIOS_MOVILIDAD"""
    data = []
    
    niveles = [
        ('GRADO', 'Grado'),
        ('MASTER', 'Máster'),
        ('DOCTO', 'Doctorado'),
        ('GRADO1', 'Grado - Primer ciclo'),
        ('GRADO2', 'Grado - Segundo ciclo'),
        ('POSGR', 'Posgrado'),
        ('SHORT', 'Short cycle'),
        ('OTHER', 'Otros estudios')
    ]
    
    for i, (id_nk, nombre) in enumerate(niveles[:n], 1):
        data.append({
            'ID_NIVEL_ESTUDIOS_MOVILIDAD': i,
            'NOMBRE_NIVEL_ESTUDIOS_MOV': nombre,
            'ID_NIVEL_ESTUDIOS_MOVILIDAD_NK': id_nk,
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
    
    return pd.DataFrame(data)

def generate_d_area_estudios_movilidad(n=20):
    """Genera datos para la tabla D_AREA_ESTUDIOS_MOVILIDAD"""
    data = []
    
    areas = [
        (1, 'Artes y Humanidades'),
        (2, 'Lenguas y Filologías'),
        (3, 'Ciencias Sociales'),
        (4, 'Economía y Empresa'),
        (5, 'Derecho'),
        (6, 'Ciencias'),
        (7, 'Ingeniería y Tecnología'),
        (8, 'Informática'),
        (9, 'Medicina'),
        (10, 'Enfermería y otras Ciencias de la Salud'),
        (11, 'Farmacia'),
        (12, 'Psicología'),
        (13, 'Arquitectura'),
        (14, 'Educación'),
        (15, 'Comunicación'),
        (16, 'Turismo'),
        (17, 'Deporte'),
        (18, 'Bellas Artes'),
        (19, 'Veterinaria'),
        (20, 'Agricultura y Ciencias Ambientales')
    ]
    
    for i, (id_nk, nombre) in enumerate(areas[:n], 1):
        data.append({
            'ID_AREA_ESTUDIOS_MOVILIDAD': i,
            'NOMBRE_AREA_ESTUDIOS_MOV': nombre,
            'ID_AREA_ESTUDIOS_MOVILIDAD_NK': id_nk,
        })
    
    return pd.DataFrame(data)

def generate_d_colectivo_movilidad(n=4):
    """Genera datos para la tabla D_COLECTIVO_MOVILIDAD"""
    data = []
    
    colectivos = [
        ('ST', 'Estudiantes'),
        ('TE', 'Personal docente'),
        ('TR', 'Personal no docente'),
        ('RE', 'Investigadores')
    ]
    
    for i, (id_nk, nombre) in enumerate(colectivos[:n], 1):
        data.append({
            'ID_COLECTIVO_MOVILIDAD': i,
            'ID_COLECTIVO_MOVILIDAD_NK': id_nk,
            'NOMBRE_COLECTIVO_MOVILIDAD': nombre,
        })
    
    return pd.DataFrame(data)

def generate_d_estado_acuerdo_bilateral(n=5):
    """Genera datos para la tabla D_ESTADO_ACUERDO_BILATERAL"""
    data = []
    
    estados = [
        ('ACT', 'Activo'),
        ('PEND', 'Pendiente de firma'),
        ('RENO', 'En renovación'),
        ('CADU', 'Caducado'),
        ('SUSP', 'Suspendido')
    ]
    
    for i, (id_nk, nombre) in enumerate(estados[:n], 1):
        data.append({
            'ID_ESTADO_ACUERDO': i,
            'ID_ESTADO_ACUERDO_NK': id_nk,
            'NOMBRE_ESTADO_ACUERDO': nombre,
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
    
    return pd.DataFrame(data)

def generate_d_centro_destino(n=50, universidad_df=None):
    """Genera datos para la tabla D_CENTRO_DESTINO"""
    data = []
    
    # Verificar DataFrame de universidades
    if universidad_df is None:
        universidad_df = generate_d_universidad(20)
    
    # Nombres genéricos de centros
    nombres_centros = [
        'Facultad de Ciencias',
        'Facultad de Derecho',
        'Facultad de Medicina',
        'Facultad de Letras',
        'Facultad de Economía',
        'Escuela de Ingeniería',
        'Facultad de Educación',
        'Facultad de Salud',
        'Escuela de Enfermería',
        'Facultad de Artes'
    ]
    
    # Multiplicar lista si es necesario
    nombres_centros = (nombres_centros * (n // len(nombres_centros) + 1))[:n]
    
    for i in range(1, n+1):
        # Seleccionar universidad aleatoria
        universidad = universidad_df.sample(1).iloc[0]
        
        nombre_centro = nombres_centros[i-1]
        centro_nk = f"{i:08d}"
        
        data.append({
            'ID_CENTRO_OTRA_UNIVERSIDAD': i,
            'NOMBRE_CENTRO_OTRA_UNIVERSIDAD': nombre_centro,
            'ID_UNIVERSIDAD': universidad['ID_UNIVERSIDAD'],
            'NOMBRE_UNIVERSIDAD': universidad['NOMBRE_UNIVERSIDAD'],
            'ID_CENTRO_OTRA_UNIVERSIDAD_NK': centro_nk,
            'ID_UNIVERSIDAD_NK': universidad['ID_UNIVERSIDAD_NK']  # TODO: Usar valores válidos de D_UNIVERSIDAD,
        })
    
    return pd.DataFrame(data)

def generate_d_centro_otra_universidad(centro_destino_df=None, n=50):
    """Genera datos para la tabla D_CENTRO_OTRA_UNIVERSIDAD basados en D_CENTRO_DESTINO"""
    if centro_destino_df is not None:
        data = []
        
        for _, row in centro_destino_df.iterrows():
            data.append({
                'ID_CENTRO_OTRA_UNIVERSIDAD': row['ID_CENTRO_OTRA_UNIVERSIDAD'],
                'ID_CENTRO_OTRA_UNIVERSIDAD_NK': row['ID_CENTRO_OTRA_UNIVERSIDAD_NK'],
                'NOMBRE_CENTRO_OTRA_UNIVERSIDAD': row['NOMBRE_CENTRO_OTRA_UNIVERSIDAD'],
                'ID_UNIVERSIDAD': row['ID_UNIVERSIDAD'],
                'ID_UNIVERSIDAD_NK': row['ID_UNIVERSIDAD_NK']  # TODO: Usar valores válidos de D_UNIVERSIDAD,
                'NOMBRE_UNIVERSIDAD': row['NOMBRE_UNIVERSIDAD'],

            })
            
        return pd.DataFrame(data)
    else:
        # Si no se proporciona el DataFrame, generar uno nuevo
        return generate_d_centro_destino(n)

def generate_d_centro_estudio(n=100, universidad_df=None, centro_df=None, plan_estudio_df=None):
    """Genera datos para la tabla D_CENTRO_ESTUDIO con todos los atributos completos"""
    data = []
    
    # Si no se proporcionan los dataframes necesarios, crear unos temporales
    if universidad_df is None:
        universidad_df = generate_d_universidad(n=10)
    
    if centro_df is None:
        centro_df = generate_d_centro(n=20)
        
    if plan_estudio_df is None:
        plan_estudio_df = generate_d_plan_estudio(n=30)
    
    # Listas para selección aleatoria
    universidad_ids = universidad_df['ID_UNIVERSIDAD'].tolist()
    universidad_nombres = universidad_df['NOMBRE_UNIVERSIDAD'].tolist()
    centro_ids = centro_df['ID_CENTRO'].tolist()
    centro_nombres = centro_df['NOMBRE_CENTRO'].tolist()
    plan_estudio_ids = plan_estudio_df['ID_PLAN_ESTUDIO'].tolist()
    plan_estudio_nombres = plan_estudio_df['NOMBRE_PLAN_ESTUDIO'].tolist()
    
    # Obtener valores adicionales si están disponibles
    try:
        plan_estudio_ord_nombres = plan_estudio_df['ORD_NOMBRE_PLAN_ESTUDIO'].tolist()
    except:
        plan_estudio_ord_nombres = [re.sub(r'^(El|La|Los|Las) ', '', nombre).upper() for nombre in plan_estudio_nombres]
    
    localidades = ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Zaragoza', 'Málaga', 'Bilbao', 
                   'Alicante', 'Córdoba', 'Valladolid', 'Vigo', 'Gijón', 'Oviedo', 'Murcia']
    
    for i in range(1, n+1):
        # Seleccionar universidad aleatoria
        idx_univ = random.randint(0, len(universidad_ids) - 1)
        id_universidad = universidad_ids[idx_univ]
        nombre_universidad = universidad_nombres[idx_univ]
        
        # Seleccionar centro aleatorio
        idx_centro = random.randint(0, len(centro_ids) - 1)
        id_centro = centro_ids[idx_centro]
        nombre_centro = centro_nombres[idx_centro]
        
        try:
            nombre_centro_ext = centro_df[centro_df['ID_CENTRO'] == id_centro]['NOMBRE_CENTRO_EXT'].values[0]
            ord_nombre_centro = centro_df[centro_df['ID_CENTRO'] == id_centro]['ORD_NOMBRE_CENTRO'].values[0]
        except:
            nombre_centro_ext = f"{nombre_centro} - {nombre_universidad}"
            ord_nombre_centro = re.sub(r'^(El|La|Los|Las) ', '', nombre_centro).upper()
            
        # Seleccionar localidad aleatoria para el centro
        localidad = random.choice(localidades)
            
        # Seleccionar plan de estudio aleatorio
        idx_plan = random.randint(0, len(plan_estudio_ids) - 1)
        id_plan_estudio = plan_estudio_ids[idx_plan]
        nombre_plan_estudio = plan_estudio_nombres[idx_plan]
        
        # Obtener nombre ordenado o generarlo
        try:
            ord_nombre_plan_estudio = plan_estudio_ord_nombres[idx_plan]
        except:
            ord_nombre_plan_estudio = re.sub(r'^(El|La|Los|Las) ', '', nombre_plan_estudio).upper()
        
        # Generar nombre extendido para el plan de estudio
        nombre_plan_estudio_ext = f"{nombre_plan_estudio} ({nombre_centro}, {localidad})"
        
        # Generar nombre con localidad
        nombre_plan_estudio_localidad = f"{nombre_plan_estudio} - {localidad}"
        
        # Generar fecha de carga
        fecha_carga = generate_random_date_datetime(2020, 2023)
        
        # Determinar aleatoriamente si es interuniversitario, coordinador, etc.
        flg_interuniversitario = random.choice([0, 0, 0, 1])  # 25% probabilidad
        flg_coordinador = 1 if flg_interuniversitario and random.random() > 0.5 else 0
        
        data.append({
            'ID_UNIVERSIDAD': id_universidad,
            'NOMBRE_UNIVERSIDAD': nombre_universidad,
            'ID_CENTRO': id_centro,
            'ID_PLAN_ESTUDIO': id_plan_estudio  # TODO: Usar valores válidos de F_TABLA_FUSION,
            'NOMBRE_CENTRO_EXT': nombre_centro_ext,# 
            'FECHA_CARGA': ...,  # ELIMINADO: No existe en esquema
            'NOMBRE_CENTRO': nombre_centro,
            'NOMBRE_PLAN_ESTUDIO': nombre_plan_estudio,
            'NOMBRE_PLAN_ESTUDIO_EXT': nombre_plan_estudio_ext,
        })  
    return pd.DataFrame(data)

def generate_d_estudio(n=100):
    """Genera datos para la tabla D_ESTUDIO con todos los atributos completos
    
    Esta función genera datos para la tabla D_ESTUDIO incluyendo todos los atributos
    necesarios, especialmente ORD_NOMBRE_ESTUDIO para ordenación.
    
    Args:
        n (int): Número de estudios a generar
        
    Returns:
        DataFrame: DataFrame con los datos generados
    """
    data = []
    
    # Prefijos para nombres de estudios
    prefijos = [
        "Grado en",
        "Máster Universitario en",
        "Doctorado en",
        "Doble Grado en",
        "Máster en"
    ]
    
    # Áreas de estudio
    areas = [
        "Administración y Dirección de Empresas",
        "Arquitectura",
        "Bellas Artes",
        "Biología",
        "Biotecnología",
        "Ciencia de Datos",
        "Ciencias Ambientales",
        "Ciencias de la Actividad Física y del Deporte",
        "Derecho",
        "Economía",
        "Educación Infantil",
        "Educación Primaria",
        "Enfermería",
        "Estudios Ingleses",
        "Farmacia",
        "Filología Hispánica",
        "Filosofía",
        "Física",
        "Historia",
        "Historia del Arte",
        "Ingeniería Aeroespacial",
        "Ingeniería Biomédica",
        "Ingeniería Civil",
        "Ingeniería de Telecomunicaciones",
        "Ingeniería Eléctrica",
        "Ingeniería Electrónica",
        "Ingeniería Informática",
        "Ingeniería Industrial",
        "Ingeniería Mecánica",
        "Ingeniería Química",
        "Marketing",
        "Matemáticas",
        "Medicina",
        "Nutrición Humana y Dietética",
        "Odontología",
        "Periodismo",
        "Psicología",
        "Publicidad y Relaciones Públicas",
        "Química",
        "Relaciones Internacionales",
        "Sociología",
        "Trabajo Social",
        "Turismo",
        "Veterinaria"
    ]
    
    # Conjunto para asegurar nombres únicos
    nombres_unicos = set()
    
    for i in range(1, n+1):
        # Generar nombre único de estudio
        while True:
            prefijo = random.choice(prefijos)
            area = random.choice(areas)
            
            # Si es un doble grado, combinar dos áreas
            if prefijo == "Doble Grado en":
                area2 = random.choice(areas)
                while area2 == area:  # Evitar repetir la misma área
                    area2 = random.choice(areas)
                nombre_estudio = f"{prefijo} {area} y {area2}"
            else:
                nombre_estudio = f"{prefijo} {area}"
            
            if nombre_estudio not in nombres_unicos:
                nombres_unicos.add(nombre_estudio)
                break
        
        # Versión ordenada del nombre (mayúsculas para ordenación sin acentos)
        ord_nombre_estudio = normalizar_texto(nombre_estudio).upper()
        
        # Generar código de estudio basado en iniciales
        palabras = nombre_estudio.split()
        codigo_estudio = ''.join([p[0] for p in palabras if len(p) > 2 and p.lower() not in ['en', 'de', 'la', 'los', 'las', 'del', 'y']])
        codigo_estudio = f"{codigo_estudio[:4]}{i:03d}"
        
        # Fecha de creación aleatoria entre 1990 y 2020
        fecha_creacion = generate_random_date_datetime(1990, 2020)
        fecha_carga = generate_random_date_datetime(2020, 2023)
        
        # Campos adicionales
        modalidad = random.choice(['PRESENCIAL', 'SEMIPRESENCIAL', 'VIRTUAL', 'HÍBRIDO'])
        idioma = random.choice(['ESPAÑOL', 'INGLES', 'ESPAÑOL/INGLES', 'CATALAN', 'ESPAÑOL/CATALAN'])
        
        data.append({
            'ID_ESTUDIO': i,
            'ID_ESTUDIO_NK': i * 100,
            'NOMBRE_ESTUDIO': nombre_estudio,
            'ORD_NOMBRE_ESTUDIO': ord_nombre_estudio,# 
            'CODIGO_ESTUDIO': ...,  # ELIMINADO: No existe en esquema
            'FECHA_CREACION': fecha_creacion,# 
            'FECHA_CARGA': ...,  # ELIMINADO: No existe en esquema
            'MODALIDAD_ESTUDIO': modalidad,# 
            'IDIOMA_IMPARTICION': ...,  # ELIMINADO: No existe en esquema
            'ES_OFICIAL': 1 if prefijo in ["Grado en", "Máster Universitario en", "Doctorado en", "Doble Grado en"] else 0,
            'SN_OFICIAL': 'S' if prefijo in ["Grado en", "Máster Universitario en", "Doctorado en", "Doble Grado en"] else 'N',# 
            'ES_INTERUNIVERSITARIO': ...,  # ELIMINADO: No existe en esquema
        })
    
    return pd.DataFrame(data)

def generate_d_estudio_jerarq(n=100, plan_estudio_df=None, estudio_df=None, tipo_estudio_df=None, rama_conocimiento_df=None):
    """Genera datos para la tabla D_ESTUDIO_JERARQ con todos los atributos completos"""
    data = []
    
    # Si no se proporcionan los dataframes necesarios, crear unos temporales
    if plan_estudio_df is None:
        plan_estudio_df = generate_d_plan_estudio(n=30)
    
    if estudio_df is None:
        estudio_df = generate_d_estudio(n=20)
        
    if tipo_estudio_df is None:
        tipo_estudio_df = generate_d_tipo_estudio(n=5)
        
    if rama_conocimiento_df is None:
        rama_conocimiento_df = generate_d_rama_macroarea(n=5)
    
    # Obtener IDs y nombres para selección aleatoria
    plan_estudio_ids = plan_estudio_df['ID_PLAN_ESTUDIO'].tolist()
    plan_estudio_nks = plan_estudio_df['ID_PLAN_ESTUDIO_NK'].tolist()
    plan_estudio_nombres = plan_estudio_df['NOMBRE_PLAN_ESTUDIO'].tolist()
    
    estudio_ids = estudio_df['ID_ESTUDIO'].tolist()
    estudio_nks = estudio_df['ID_ESTUDIO_NK'].tolist()
    estudio_nombres = estudio_df['NOMBRE_ESTUDIO'].tolist()
    
    tipo_estudio_ids = tipo_estudio_df['ID_TIPO_ESTUDIO'].tolist()
    tipo_estudio_nks = tipo_estudio_df['ID_TIPO_ESTUDIO_NK'].tolist()
    tipo_estudio_nombres = tipo_estudio_df['NOMBRE_TIPO_ESTUDIO'].tolist()
    
    rama_conocimiento_ids = rama_conocimiento_df['ID_RAMA_CONOCIMIENTO'].tolist()
    rama_conocimiento_nks = rama_conocimiento_df['ID_RAMA_CONOCIMIENTO_NK'].tolist()
    rama_conocimiento_nombres = rama_conocimiento_df['NOMBRE_RAMA_CONOCIMIENTO'].tolist()
    
    # Localidades para añadir a los nombres de planes
    localidades = [
        "Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza", 
        "Málaga", "Murcia", "Palma", "Las Palmas", "Bilbao", 
        "Alicante", "Córdoba", "Valladolid", "Vigo", "Gijón", 
        "Granada", "A Coruña", "Vitoria", "Elche", "Oviedo"
    ]
    
    # Diccionario para mapear estudio a su versión sin acentos
    estudio_to_sc = {}
    plan_to_sc = {}
    
    for i in range(1, n+1):
        # Seleccionar plan de estudio aleatorio
        idx_plan = random.randint(0, len(plan_estudio_ids) - 1)
        id_plan_estudio = plan_estudio_ids[idx_plan]
        id_plan_estudio_nk = plan_estudio_nks[idx_plan]
        nombre_plan_estudio = plan_estudio_nombres[idx_plan]
        
        # Seleccionar estudio aleatorio
        idx_estudio = random.randint(0, len(estudio_ids) - 1)
        id_estudio = estudio_ids[idx_estudio]
        id_estudio_nk = estudio_nks[idx_estudio]
        nombre_estudio = estudio_nombres[idx_estudio]
        
        # Seleccionar tipo de estudio aleatorio
        idx_tipo = random.randint(0, len(tipo_estudio_ids) - 1)
        id_tipo_estudio = tipo_estudio_ids[idx_tipo]
        id_tipo_estudio_nk = tipo_estudio_nks[idx_tipo]
        nombre_tipo_estudio = tipo_estudio_nombres[idx_tipo]
        id_tipo_estudio_descr = id_tipo_estudio * 10  # Valor descriptivo
        
        # Seleccionar rama de conocimiento aleatoria
        idx_rama = random.randint(0, len(rama_conocimiento_ids) - 1)
        id_rama_conocimiento = rama_conocimiento_ids[idx_rama]
        id_rama_conocimiento_nk = rama_conocimiento_nks[idx_rama]
        nombre_rama_conocimiento = rama_conocimiento_nombres[idx_rama]
        
        # Generar campos adicionales de ordenación
        localidad = random.choice(localidades)
        nombre_plan_estudio_localidad = f"{nombre_plan_estudio} ({localidad})"
        
        # Ordenación alfabética (mayúsculas)
        ord_nombre_estudio = nombre_estudio.upper()
        ord_nombre_plan_estudio = nombre_plan_estudio.upper()
        
        # Flag para plan interuniversitario (10% de probabilidad)
        flg_interuniversitario = 1 if random.random() < 0.1 else 0
        
        # Si es interuniversitario, puede ser coordinador o no
        flg_coordinador = 1 if flg_interuniversitario == 1 and random.random() < 0.5 else 0
        
        # Versiones sin acentos ni caracteres especiales
        if nombre_estudio not in estudio_to_sc:
            estudio_to_sc[nombre_estudio] = normalizar_texto(nombre_estudio)
        
        if nombre_plan_estudio not in plan_to_sc:
            plan_to_sc[nombre_plan_estudio] = normalizar_texto(nombre_plan_estudio)
        
        nombre_estudio_sc = estudio_to_sc[nombre_estudio]
        nombre_plan_estudio_sc = plan_to_sc[nombre_plan_estudio]
        
        data.append({
            'ID_PLAN_ESTUDIO': id_plan_estudio  # TODO: Usar valores válidos de F_TABLA_FUSION,
            'ID_PLAN_ESTUDIO_NK': id_plan_estudio_nk,
            'ID_ESTUDIO': id_estudio,
            'ID_ESTUDIO_NK': id_estudio_nk,
            'ID_TIPO_ESTUDIO': id_tipo_estudio,
            'NOMBRE_TIPO_ESTUDIO': nombre_tipo_estudio,# 
            'ID_RAMA_CONOCIMIENTO': ...,  # ELIMINADO: No existe en esquema# 
            'NOMBRE_RAMA_CONOCIMIENTO': ...,  # ELIMINADO: No existe en esquema
            'ID_TIPO_ESTUDIO_DESCR': id_tipo_estudio_descr,
            'NOMBRE_PLAN_ESTUDIO': nombre_plan_estudio,
            'ORD_NOMBRE_ESTUDIO': ord_nombre_estudio,
            'NOMBRE_ESTUDIO': nombre_estudio,
            'ORD_NOMBRE_PLAN_ESTUDIO': ord_nombre_plan_estudio,
            'NOMBRE_PLAN_ESTUDIO_LOCALIDAD': nombre_plan_estudio_localidad,
            'ID_TIPO_ESTUDIO_NK': id_tipo_estudio_nk,
            'ID_RAMA_CONOCIMIENTO_NK': id_rama_conocimiento_nk,
            'FLG_INTERUNIVERSITARIO': flg_interuniversitario,
            'FLG_COORDINADOR': flg_coordinador,
            'NOMBRE_PLAN_ESTUDIO_SC': nombre_plan_estudio_sc,
            'NOMBRE_ESTUDIO_SC': nombre_estudio_sc
        })
    
    return pd.DataFrame(data)

# Función auxiliar para normalizar texto
def normalizar_texto(texto):
    """Elimina acentos y caracteres especiales de un texto"""
    # Normalizar a formato NFD para separar caracteres base y combinaciones
    texto_normalizado = unicodedata.normalize('NFD', texto)
    # Eliminar los diacríticos (acentos, etc.)
    texto_sin_acentos = re.sub(r'[\u0300-\u036f]', '', texto_normalizado)
    # Eliminar otros caracteres especiales excepto letras, números y espacios
    texto_limpio = re.sub(r'[^\w\s]', '', texto_sin_acentos)
    return texto_limpio

def generate_d_estudio_destino(n=50):
    """Genera datos para la tabla D_ESTUDIO_DESTINO"""
    data = []
    
    # Prefijos para nombres de estudios
    prefijos = [
        "Grado en",
        "Laurea in",
        "Bachelor of",
        "Licenciatura en",
        "Master in",
        "Máster en",
        "Diploma in",
        "Mestrado em",
        "Licence en",
        "Doktor der"
    ]
    
    # Áreas de estudio internacionales
    areas = [
        "Arts", 
        "Humanities", 
        "Science", 
        "Social Sciences",
        "Law",
        "Medicine",
        "Engineering",
        "Business Administration",
        "Economics",
        "Computer Science",
        "Architecture",
        "Mathematics",
        "Physics",
        "Chemistry",
        "Biology",
        "Psychology",
        "Philosophy",
        "Linguistics",
        "History",
        "Political Science"
    ]
    
    for i in range(1, n+1):
        # Generar un nombre de estudio internacional
        prefijo = random.choice(prefijos)
        area = random.choice(areas)
        nombre_estudio = f"{prefijo} {area}"
        
        # NK (Natural Key) que identifica al estudio en universidad externa
        id_estudio_otra_universidad_nk = f"EXT{str(i).zfill(3)}{random.choice(['A', 'B', 'C', 'D', 'E'])}"
        
        # Valor descriptivo para el estudio
        id_estudio_otra_univ_descr = i * 100
        
        data.append({
            'ID_ESTUDIO_OTRA_UNIVERSIDAD': i,
            'NOMBRE_ESTUDIO_OTRA_UNIVERSIDA': nombre_estudio,
            'ID_ESTUDIO_OTRA_UNIV_DESCR': id_estudio_otra_univ_descr,
            'ID_ESTUDIO_OTRA_UNIVERSIDAD_NK': id_estudio_otra_universidad_nk
        })
    
    return pd.DataFrame(data)

def generate_d_estudio_otra_universidad(estudio_destino_df=None, n=50):
    """Genera datos para la tabla D_ESTUDIO_OTRA_UNIVERSIDAD basados en D_ESTUDIO_DESTINO"""
    if estudio_destino_df is not None:
        data = []
        for _, row in estudio_destino_df.iterrows():
            data.append({
                'ID_ESTUDIO_OTRA_UNIVERSIDAD': row['ID_ESTUDIO_OTRA_UNIVERSIDAD'],
                'ID_ESTUDIO_OTRA_UNIVERSIDAD_NK': row['ID_ESTUDIO_OTRA_UNIVERSIDAD_NK'],
                'NOMBRE_ESTUDIO_OTRA_UNIVERSIDA': row['NOMBRE_ESTUDIO_OTRA_UNIVERSIDA'],
                'ID_ESTUDIO_OTRA_UNIV_DESCR': row['ID_ESTUDIO_OTRA_UNIV_DESCR']
            })
        return pd.DataFrame(data)
    else:
        # Si no se proporciona el DataFrame de estudios destino, generar uno
        return generate_d_estudio_destino(n=n)

def generate_d_plan_estudio_asignatura(n=1000, asignatura_df=None, plan_estudio_df=None, clase_asignatura_df=None):
    """Genera datos para la tabla D_PLAN_ESTUDIO_ASIGNATURA"""
    data = []
    
    # Verificar DataFrames relacionados
    if asignatura_df is None:
        asignatura_df = generate_d_asignatura(100)
    
    if plan_estudio_df is None:
        plan_estudio_df = generate_d_plan_estudio(30)
    
    if clase_asignatura_df is None:
        clase_asignatura_df = generate_d_clase_asignatura()
    
    # Generar combinaciones hasta alcanzar n registros
    combinaciones = min(n, len(asignatura_df) * len(plan_estudio_df))
    
    for i in range(1, combinaciones + 1):
        # Seleccionar asignatura, plan de estudio y clase de asignatura aleatorios
        asignatura_idx = (i-1) % len(asignatura_df)
        plan_idx = ((i-1) // len(asignatura_df)) % len(plan_estudio_df)
        
        asignatura = asignatura_df.iloc[asignatura_idx]
        plan_estudio = plan_estudio_df.iloc[plan_idx]
        clase_asignatura = clase_asignatura_df.sample(1).iloc[0]
        
        # Generar curso y periodo
        curso_orden = str(random.randint(1, 4))
        tipo_periodo = random.choice(['A', 'S'])  # Anual o Semestral
        valor_periodo = '1' if tipo_periodo == 'A' else str(random.randint(1, 2))
        
        data.append({
            'ID_PLAN_ESTUDIO_ASIGNATURA': i,
            'ID_ASIGNATURA': asignatura['ID_ASIGNATURA'],
            'ID_ASIGNATURA_NK': asignatura['ID_ASIGNATURA_NK'],
            'ID_PLAN_ESTUDIO': plan_estudio['ID_PLAN_ESTUDIO']  # TODO: Usar valores válidos de F_TABLA_FUSION,
            'ID_PLAN_ESTUDIO_NK': plan_estudio['ID_PLAN_ESTUDIO_NK'],
            'ID_CLASE_ASIGNATURA': clase_asignatura['ID_CLASE_ASIGNATURA'],
            'ID_CLASE_ASIGNATURA_NK': clase_asignatura['ID_CLASE_ASIGNATURA_NK'],
            'CURSO_ORDEN': curso_orden,
            'TIPO_PERIODO': tipo_periodo,
            'VALOR_PERIODO': valor_periodo
        })
    
    return pd.DataFrame(data)

def generate_d_programa_movilidad(n=10):
    """Genera datos para la tabla D_PROGRAMA_MOVILIDAD"""
    data = []
    
    # Tipos de programas de movilidad
    tipos_programa = [
        (1, "Programa Erasmus+"),
        (2, "Programa de Intercambio Bilateral"),
        (3, "Programa de Movilidad Nacional SICUE"),
        (4, "Programa de Cooperación Internacional"),
        (5, "Programa de Movilidad Iberoamericana")
    ]
    
    # Programas de movilidad comunes
    programas = [
        ("ERAS+", "Erasmus+ Estudios", 1, "S"),
        ("ERASP", "Erasmus+ Prácticas", 1, "S"),
        ("SICUE", "Sistema de Intercambio entre Centros Universitarios Españoles", 3, "N"),
        ("AMERL", "Programa América Latina", 4, "S"),
        ("USACDN", "Programa EEUU-Canadá", 4, "S"),
        ("ASIA", "Programa Asia", 4, "S"),
        ("ISEP", "International Student Exchange Program", 2, "S"),
        ("CIEE", "Council on International Educational Exchange", 2, "S"),
        ("EUROP", "Programa Europeo No Erasmus", 2, "S"),
        ("IBERO", "Programa Iberoamérica Santander", 5, "S")
    ]
    
    # Asegurarse de no exceder el número solicitado
    programas = programas[:n]
    
    for i, (cod_programa, nombre_programa, id_tipo, internacional) in enumerate(programas, 1):
        # Obtener nombre del tipo de programa del diccionario
        nombre_tipo_programa = next((tipo[1] for tipo in tipos_programa if tipo[0] == id_tipo), "Otro tipo de programa")
        
        data.append({
            'ID_PROGRAMA_MOVILIDAD': i,
            'NOMBRE_PROGRAMA_MOVILIDAD': nombre_programa,
            'COD_PROGRAMA_INT': cod_programa,
            'ID_TIPO_PROGRAMA_MOVILIDAD': id_tipo,
            'NOMBRE_TIPO_PROGRAMA_MOV': nombre_tipo_programa,
            'ID_PROGRAMA_MOVILIDAD_NK': i * 10,
            'SN_PROGRAMA_INTERNACIONAL': internacional
        })
    
    return pd.DataFrame(data)

def generate_d_idioma_nivel_movilidad(n=20, idioma_movilidad_df=None):
    """Genera datos para la tabla D_IDIOMA_NIVEL_MOVILIDAD"""
    data = []
    
    # Verificar DataFrame de idiomas
    if idioma_movilidad_df is None:
        idioma_movilidad_df = generate_d_idioma_movilidad(5)
    
    # Niveles de idioma
    niveles = [1, 2, 3, 4, 5, 6]  # A1, A2, B1, B2, C1, C2
    
    id_contador = 1
    
    # Generar combinaciones de idioma y nivel
    for _, idioma in idioma_movilidad_df.iterrows():
        for nivel in niveles:
            if id_contador > n:
                break
                
            nivel_nombre = {1: 'A1', 2: 'A2', 3: 'B1', 4: 'B2', 5: 'C1', 6: 'C2'}[nivel]
            nombre_completo = f"{idioma['NOMBRE_IDIOMA_MOVILIDAD']} - {nivel_nombre}"
            
            data.append({
                'ID_IDIOMA_NIVEL_MOVILIDAD': id_contador,
                'ID_IDIOMA_MOVILIDAD_NK': idioma['ID_IDIOMA_MOVILIDAD_NK'],
                'ID_NIVEL_IDIOMA_MOVILIDAD_NK': nivel,
                'NOMBRE_IDIOMA_NIVEL_MOVILIDAD': nombre_completo
            })
            
            id_contador += 1
    
    return pd.DataFrame(data)

def generate_d_titulacion(n=50):
    """Genera datos para la tabla D_TITULACION"""
    data = []
    
    # Tipos de titulación
    tipos_titulacion = [
        (1, "Grado"),
        (2, "Máster Universitario"),
        (3, "Doctorado"),
        (4, "Título Propio"),
        (5, "Diplomatura"),
        (6, "Licenciatura"),
        (7, "Ingeniería"),
        (8, "Ingeniería Técnica"),
        (9, "Arquitectura"),
        (10, "Arquitectura Técnica")
    ]
    
    # Ramas y disciplinas para generar titulaciones
    ramas = {
        "Artes y Humanidades": [
            "Historia", "Filosofía", "Filología Hispánica", "Estudios Ingleses", 
            "Bellas Artes", "Traducción e Interpretación", "Música", "Historia del Arte"
        ],
        "Ciencias": [
            "Matemáticas", "Física", "Química", "Biología", "Geología", 
            "Biotecnología", "Ciencias Ambientales", "Estadística"
        ],
        "Ciencias de la Salud": [
            "Medicina", "Enfermería", "Farmacia", "Fisioterapia", "Odontología", 
            "Veterinaria", "Nutrición y Dietética", "Psicología"
        ],
        "Ciencias Sociales y Jurídicas": [
            "Derecho", "Economía", "Administración de Empresas", "Sociología", 
            "Ciencias Políticas", "Periodismo", "Educación", "Turismo"
        ],
        "Ingeniería y Arquitectura": [
            "Ingeniería Informática", "Ingeniería Industrial", "Ingeniería Civil", 
            "Arquitectura", "Ingeniería Química", "Ingeniería Aeroespacial", 
            "Ingeniería de Telecomunicaciones", "Ingeniería Agrónoma"
        ]
    }
    
    # Combinar tipos de titulación con disciplinas para crear titulaciones
    titulaciones = []
    for tipo_id, tipo_nombre in tipos_titulacion:
        for rama, disciplinas in ramas.items():
            for disciplina in disciplinas:
                if tipo_nombre in ["Grado", "Máster Universitario", "Doctorado", "Título Propio"]:
                    titulaciones.append((f"{tipo_nombre} en {disciplina}", tipo_id, tipo_nombre))
                else:
                    titulaciones.append((f"{tipo_nombre} de {disciplina}", tipo_id, tipo_nombre))
    
    # Asegurar que no excedemos el número solicitado
    random.shuffle(titulaciones)
    titulaciones = titulaciones[:n]
    
    for i, (nombre_titulacion, id_tipo_titulacion, nombre_tipo_titulacion) in enumerate(titulaciones, 1):
        data.append({
            'ID_TITULACION': i,
            'NOMBRE_TITULACION': nombre_titulacion,
            'ID_TIPO_TITULACION': id_tipo_titulacion,
            'NOMBRE_TIPO_TITULACION': nombre_tipo_titulacion,
            'FECHA_CARGA': generate_random_date(2020, 2023)
        })
    
    return pd.DataFrame(data)

def generate_d_acuerdo_bilateral(n=20):
    """Genera datos para la tabla D_ACUERDO_BILATERAL con los atributos completos"""
    data = []
    
    # Crear diferentes tipos de acuerdos
    tipos_acuerdo = [
        "Intercambio Académico",
        "Investigación Conjunta",
        "Doble Titulación",
        "Movilidad de Estudiantes",
        "Movilidad de Profesores",
        "Proyecto Erasmus+",
        "Cooperación Internacional",
        "Acuerdo Marco"
    ]
    
    for i in range(1, n+1):
        # Generar universidades para el acuerdo
        universidad_origen = fake.company()
        universidad_destino = fake.company()
        
        # Tipo de acuerdo
        tipo_acuerdo = random.choice(tipos_acuerdo)
        
        # Generar número único del acuerdo (YYYY-XXXX)
        anyo = random.randint(2010, 2023)
        num_acuerdo = random.randint(1000, 9999)
        id_acuerdo_bilateral_nk = f"{anyo}-{num_acuerdo}"
        
        # Nombre del acuerdo
        nombre_acuerdo = f"Acuerdo de {tipo_acuerdo} entre {universidad_origen} y {universidad_destino}"
        
        # ID descriptivo para el acuerdo
        id_acuerdo_bilateral_descr = i * 100
        
        data.append({
            'ID_ACUERDO_BILATERAL': i,
            'ID_ACUERDO_BILATERAL_NK': id_acuerdo_bilateral_nk,
            'NOMBRE_ACUERDO_BILATERAL': nombre_acuerdo,
            'ID_ACUERDO_BILATERAL_DESCR': id_acuerdo_bilateral_descr
        })
    
    return pd.DataFrame(data)

def generate_d_proyecto_investigacion(n=30):
    """Genera datos para la tabla D_PROYECTO_INVESTIGACION
    
    Args:
        n (int): Número de proyectos a generar
    
    Returns:
        DataFrame: DataFrame con los datos generados
    """
    data = []
    
    # Prefijos para códigos de proyectos por tipos/fuentes de financiación
    prefijos = {
        'PID': 'Plan Nacional I+D',# 
        'EUR': ...,  # ELIMINADO: No existe en esquema
        'REG': 'Proyecto Regional',# 
        'AEI': ...,  # ELIMINADO: No existe en esquema
        'CTR': 'Contrato con Empresa',# 
        'MIN': ...,  # ELIMINADO: No existe en esquema
    }
    
    # Años para los proyectos (últimos 5 años)
    año_actual = datetime.datetime.now().year
    años = list(range(año_actual-5, año_actual+1))
    
    for i in range(1, n+1):
        # Seleccionar un prefijo aleatorio y su descripción
        prefijo, descripcion_prefijo = random.choice(list(prefijos.items()))
        
        # Año aleatorio para el proyecto (como entero)
        año = random.choice(años)
        
        # Generar un código de proyecto realista
        numero_proyecto = fake.random_number(digits=5)
        sufijo = fake.random_letter().upper() + fake.random_letter().upper()
        
        # Formar el ID natural del proyecto (código)
        id_proyecto_nk = f"{prefijo}-{año}-{numero_proyecto}-{sufijo}"
        
        # Crear objetos datetime directamente
        fecha_inicio = datetime.datetime(año, random.randint(1, 6), random.randint(1, 28))
        fecha_fin = datetime.datetime(año + 3, random.randint(1, 12), random.randint(1, 28))
        
        data.append({
            'ID_PROYECTO_INVESTIGACION': i,
            'ID_PROYECTO_INVESTIGACION_NK': id_proyecto_nk,
            'NOMBRE_PROYECTO': f"Proyecto de {descripcion_prefijo} sobre {fake.bs()}",# 
            'FECHA_INICIO': ...,  # ELIMINADO: No existe en esquema# 
            'FECHA_FIN': ...,  # ELIMINADO: No existe en esquema
            'IMPORTE_CONCEDIDO': round(random.uniform(10000, 1000000), 2),# 
            'TIPO_PROYECTO': ...,  # ELIMINADO: No existe en esquema
        })
    
    return pd.DataFrame(data)

def generate_d_rama_macroarea(n=15):
    """Genera datos para la tabla D_RAMA_MACROAREA
    
    Esta tabla también actúa como D_RAMA_CONOCIMIENTO para compatibilidad
    """
    data = []
    
    macroareas = ['Ciencias', 'Artes', 'Ingeniería', 'Salud', 'Ciencias Sociales']
    
    for i in range(1, n+1):
        macroarea = random.choice(macroareas)
        nombre_rama_macroarea = f"{macroarea} - Especialidad {i}"
        id_rama_conocimiento_nk = random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'])
        id_macroarea_nk = random.choice(['A', 'B', 'C', 'D', 'E'])
        id_macroarea_area_nk = f"{id_macroarea_nk}{random.randint(1, 9)}"
        
        data.append({
            'ID_RAMA_MACROAREA': i,
            'NOMBRE_RAMA_MACROAREA': nombre_rama_macroarea,
            'ID_RAMA_CONOCIMIENTO_NK': id_rama_conocimiento_nk,
            'ID_MACROAREA_NK': id_macroarea_nk,
            'ID_MACROAREA_AREA_NK': id_macroarea_area_nk,
            # Campos alias para compatibilidad con D_RAMA_CONOCIMIENTO# 
            'ID_RAMA_CONOCIMIENTO': ...,  # ELIMINADO: No existe en esquema# 
            'NOMBRE_RAMA_CONOCIMIENTO': ...,  # ELIMINADO: No existe en esquema
        })
    
    return pd.DataFrame(data)

def generate_d_estado_solicitud_doctorado(n=10):
    """Genera datos para la tabla D_ESTADO_SOLICITUD_DOCTORADO
    
    Contiene los posibles estados de una solicitud de admisión a un programa de doctorado.
    
    Args:
        n (int): Número de estados de solicitud a generar (máx. 10)
    
    Returns:
        DataFrame: DataFrame con los datos generados
    """
    data = []
    
    estados = [
        # código, nombre, descripción, es aprobado, es rechazado, requiere acción
        ('P1', 'Pendiente de revisión', 'La solicitud ha sido registrada pero aún no se ha revisado', 0, 0, 0),
        ('RE', 'En revisión', 'La solicitud está siendo revisada por la comisión académica', 0, 0, 0),
        ('AD', 'Admitido', 'La solicitud ha sido aprobada y el candidato admitido', 1, 0, 0),
        ('RZ', 'Rechazado', 'La solicitud ha sido rechazada por la comisión académica', 0, 1, 0),
        ('DP', 'Documentación pendiente', 'Se requiere documentación adicional para continuar', 0, 0, 1),
        ('DC', 'Documentación completa', 'La documentación está completa y validada', 0, 0, 0),
        ('CE', 'Condicionado a entrevista', 'Admisión condicionada a superar entrevista', 0, 0, 1),
        ('PA', 'Pendiente autorización', 'Pendiente de autorización por órganos superiores', 0, 0, 0),
        ('MC', 'Matrícula completada', 'El estudiante ha formalizado su matrícula', 1, 0, 0),
        ('CA', 'Cancelada', 'Solicitud cancelada por el solicitante', 0, 1, 0)
    ]
    
    # Limitar al número solicitado
    estados = estados[:n]
    
    for i, (codigo, nombre, descripcion, es_aprobado, es_rechazado, requiere_accion) in enumerate(estados, 1):
        data.append({
            'ID_ESTADO_SOL_DOCTORADO': i,
            'ID_ESTADO_SOL_DOCTORADO_NK': codigo,
            'NOMBRE_ESTADO_SOL_DOCTORADO': nombre,
            'DESCRIPCION_ESTADO': descripcion,# 
            'FLG_ESTADO_APROBADO': ...,  # ELIMINADO: No existe en esquema
            'FLG_ESTADO_RECHAZADO': es_rechazado,# 
            'FLG_REQUIERE_ACCION': ...,  # ELIMINADO: No existe en esquema
            'FECHA_ALTA': generate_random_date(2015, 2020)
        })
    
    return pd.DataFrame(data)

def generate_d_grupo(n=20, curso_academico_df=None, centro_df=None, asignatura_df=None):
    """Genera datos para la tabla D_GRUPO"""
    data = []
    
    # Si no se proporcionan los DataFrames necesarios, crear unos temporales
    if curso_academico_df is None:
        curso_academico_df = generate_d_curso_academico(n=2)
    
    if centro_df is None:
        centro_df = generate_d_centro(n=5)
    
    if asignatura_df is None:
        asignatura_df = generate_d_asignatura(n=10)
    
    # Periodos lectivos posibles
    tipo_periodos = ['A', 'S']  # Anual, Semestral
    valor_periodos = ['1', '2']  # Primer semestre, Segundo semestre
    
    # Para cada asignatura, crear varios grupos
    grupos_por_asignatura = {}
    
    for idx in range(1, n+1):
        # Seleccionar curso, centro y asignatura aleatoriamente
        curso = curso_academico_df.sample(1).iloc[0]
        centro = centro_df.sample(1).iloc[0]
        asignatura = asignatura_df.sample(1).iloc[0]
        
        # Verificar si ya existe un grupo para esta asignatura para controlar el ID_GRUPO_NK
        key = (curso['ID_CURSO_ACADEMICO_NK'], centro['ID_CENTRO'], asignatura['ID_ASIGNATURA'])
        if key not in grupos_por_asignatura:
            grupos_por_asignatura[key] = 0
        
        grupos_por_asignatura[key] += 1
        id_grupo_nk = grupos_por_asignatura[key]
        
        # Generar valores aleatorios para tipo y valor de periodo
        tipo_periodo = random.choice(tipo_periodos)
        valor_periodo = random.choice(valor_periodos)
        
        # Nombre del grupo (A, B, C, etc. o números)
        nombre_grupo = chr(64 + id_grupo_nk) if id_grupo_nk <= 26 else str(id_grupo_nk - 26)
        
        data.append({
            'ID_GRUPO': idx,
            'NOMBRE_GRUPO': f"Grupo {nombre_grupo}",
            'ID_CURSO_ACADEMICO_NK': curso['ID_CURSO_ACADEMICO_NK']  # TODO: Usar valores válidos de D_CURSO_COHORTE,
            'ID_CENTRO_NK': centro['ID_CENTRO']  # TODO: Usar valores válidos de D_CENTRO,
            'ID_ASIGNATURA_NK': asignatura['ID_ASIGNATURA'],
            'ID_GRUPO_NK': id_grupo_nk,
            'ID_GRUPO_DESCR': idx,
            'ID_TIPO_PERIODO_LECTIVO_NK': tipo_periodo,
            'ID_VALOR_PERIODO_LECTIVO_NK': valor_periodo
        })
    
    return pd.DataFrame(data)

def generate_d_plan_estudio_ano_datos(n=50, curso_academico_df=None, plan_estudio_df=None, tipo_estudio_df=None, modalidad_plan_df=None):
    """Genera datos para la tabla D_PLAN_ESTUDIO_ANO_DATOS"""
    data = []
    
    # Si no se proporcionan los DataFrames necesarios, crear unos temporales
    if curso_academico_df is None:
        curso_academico_df = generate_d_curso_academico(n=3)
    
    if plan_estudio_df is None:
        plan_estudio_df = generate_d_plan_estudio(n=10)
    
    if tipo_estudio_df is None:
        tipo_estudio_df = generate_d_tipo_estudio()
    
    if modalidad_plan_df is None:
        modalidad_plan_df = generate_d_modalidad_plan_estudio()
    
    # Para cada combinación de curso académico y plan de estudio, crear un registro
    id_counter = 1
    for _, curso in curso_academico_df.iterrows():
        for _, plan in plan_estudio_df.sample(min(5, len(plan_estudio_df))).iterrows():
            tipo_estudio = tipo_estudio_df.sample(1).iloc[0]
            modalidad_plan = modalidad_plan_df.sample(1).iloc[0]
            
            # Generar valores aleatorios para los campos
            experimentalidad = random.randint(1, 5)
            creditos_ofertados = random.randint(180, 300)
            centro_oferta_nk = random.randint(1, 100)
            plazas_ofertadas = random.randint(30, 200)
            flg_oferta = 1
            centro_matricula_nk = random.randint(1, 100)
            expedientes_matriculados = random.randint(20, 180)
            flg_matricula = 1
            centro_cent_plan_nk = random.randint(1, 100)
            flg_cent_plan = 1
            
            # Ámbito de conocimiento
            id_ambito = random.randint(1, 20)
            id_ambito_nk = f"AM{id_ambito:03d}"
            nombre_ambito = f"Ámbito de conocimiento {id_ambito}"
            
            if id_counter <= n:
                data.append({
                    'ID_PLAN_ESTUDIO_ANO_DATOS': id_counter,
                    'ID_CURSO_ACADEMICO_NK': curso['ID_CURSO_ACADEMICO_NK']  # TODO: Usar valores válidos de D_CURSO_COHORTE,
                    'ID_PLAN_ESTUDIO_NK': plan['ID_PLAN_ESTUDIO_NK'],
                    'ID_TIPO_ESTUDIO_NK': tipo_estudio['ID_TIPO_ESTUDIO_NK'],
                    'ID_MODALIDAD_PLAN_NK': modalidad_plan['ID_MODALIDAD_PLAN_ESTUDIO_NK'],
                    'EXPERIMENTALIDAD': experimentalidad,
                    'CREDITOS_OFERTADOS': creditos_ofertados,
                    'ID_CENTRO_OFERTA_NK': centro_oferta_nk,
                    'NUM_PLAZAS_OFERTADAS': plazas_ofertadas,
                    'FLG_OFERTA': flg_oferta,
                    'ID_CENTRO_MATRICULA_NK': centro_matricula_nk,
                    'NUM_EXPEDIENTES_MATRI': expedientes_matriculados,
                    'FLG_MATRICULA': flg_matricula,
                    'ID_CENTRO_CENT_PLAN_NK': centro_cent_plan_nk,
                    'FLG_CENT_PLAN': flg_cent_plan,
                    'ID_AMBITO_CONOCIMIENTO': id_ambito,
                    'ID_AMBITO_CONOCIMIENTO_NK': id_ambito_nk,
                    'NOMBRE_AMBITO_CONOCIMIENTO': nombre_ambito
                })
                id_counter += 1
    
    return pd.DataFrame(data)

def generate_d_estudio_propio(n=30):
    """Genera datos para la tabla D_ESTUDIO_PROPIO con todos los atributos completos"""
    data = []
    
    # Disciplinas para estudios propios
    disciplinas = [
        "Marketing Digital",
        "Inteligencia Artificial",
        "Derecho Internacional",
        "Gestión Empresarial",
        "Sostenibilidad y Medio Ambiente",
        "Psicología Aplicada",
        "Comunicación Audiovisual",
        "Tecnologías de la Información",
        "Ciencias de la Salud",
        "Energías Renovables",
        "Traducción e Interpretación",
        "Estudios Culturales",
        "Finanzas y Contabilidad",
        "Recursos Humanos",
        "Logística y Cadena de Suministro"
    ]
    
    for i in range(1, n+1):
        # Identificadores
        id_estudio_propio = i
        id_estudio_propio_nk = i * 100
        id_estudio_propio_edicion_nk = random.randint(1, 10)
        
        # Disciplina aleatoria
        disciplina = random.choice(disciplinas)
        
        # Nombres
        nombre_base = f"Estudios en {disciplina}"
        nombre_estudio_propio = nombre_base
        nombre_estudio_propio_ext = f"{nombre_base} - Edición {id_estudio_propio_edicion_nk} ({fake.year()})"
        
        # ID Descriptivo
        id_estudio_propio_descr = i * 1000
        
        data.append({
            'ID_ESTUDIO_PROPIO': id_estudio_propio,
            'ID_ESTUDIO_PROPIO_NK': id_estudio_propio_nk,
            'ID_ESTUDIO_PROPIO_EDICION_NK': id_estudio_propio_edicion_nk,
            'NOMBRE_ESTUDIO_PROPIO': nombre_estudio_propio,
            'NOMBRE_ESTUDIO_PROPIO_EXT': nombre_estudio_propio_ext,
            'ID_ESTUDIO_PROPIO_DESCR': id_estudio_propio_descr
        })
    
    return pd.DataFrame(data)

def generate_d_rango_credito_movilidad(n=7, rango_credito_df=None):
    """Genera datos para la tabla D_RANGO_CREDITO_MOVILIDAD"""
    data = []
    
    # Si no se proporciona el DataFrame de rangos de crédito, crear uno temporal
    if rango_credito_df is None:
        rango_credito_df = generate_d_rango_credito()
    
    for i, rango in enumerate(rango_credito_df.iterrows(), 1):
        if i > n:
            break
            
        id_rango = rango[1]['ID_RANGO_CREDITO']
        nombre_rango = rango[1]['NOMBRE_RANGO_CREDITO']
        
        # Asignar un valor de crédito representativo para el rango
        if 'menos' in nombre_rango.lower():
            credito = random.randint(1, 6)
        elif 'entre' in nombre_rango.lower():
            partes = nombre_rango.split()
            min_val = int(partes[1])
            max_val = int(partes[3])
            credito = random.randint(min_val, max_val)
        else:
            credito = random.randint(30, 60)
        
        data.append({
            'ID_CREDITO': i * 10,
            'ID_RANGO_CREDITO': id_rango,
            'NOMBRE_RANGO_CREDITO': f"Movilidad: {nombre_rango}"
        })
    
    return pd.DataFrame(data)

def generate_d_convocatoria_preinscripcion(n=5, convocatoria_df=None):
    """Genera datos para la tabla D_CONVOCATORIA_PREINSCRIPCION"""
    data = []
    
    # Si no se proporciona el DataFrame de convocatorias, crear uno temporal
    if convocatoria_df is None:
        convocatoria_df = generate_d_convocatoria()
    
    for i, conv in enumerate(convocatoria_df.iterrows(), 1):
        if i > n:
            break
            
        id_convocatoria = conv[1]['ID_CONVOCATORIA']
        nombre_convocatoria = conv[1]['NOMBRE_CONVOCATORIA']
        id_convocatoria_nk = i * 10
        
        data.append({
            'ID_CONVOCATORIA': id_convocatoria,
            'NOMBRE_CONVOCATORIA': f"Preinscripción: {nombre_convocatoria}",
            'ID_CONVOCATORIA_NK': id_convocatoria_nk,
        })
    
    return pd.DataFrame(data)

def generate_d_categoria_cuerpo_pdi(n=15):
    """Genera datos para la tabla D_CATEGORIA_CUERPO_PDI con campos completos
    
    Implementación mejorada con todos los campos necesarios para análisis completo
    de las categorías de Personal Docente e Investigador.
    
    Args:
        n (int): Número de categorías a generar (máx. 15)
        
    Returns:
        DataFrame: DataFrame con los datos generados
    """
    data = []
    
    categorias = [
        ('CATED', 'Catedrático/a de Universidad', 'Funcionario', 'A1', True, True, True, 1),
        ('TITUL', 'Profesor/a Titular de Universidad', 'Funcionario', 'A1', True, True, True, 2),
        ('CONTR', 'Profesor/a Contratado/a Doctor/a', 'Laboral', 'L1', True, True, False, 3),
        ('AYUDO', 'Profesor/a Ayudante Doctor/a', 'Laboral', 'L1', True, False, False, 4),
        ('AYUDA', 'Profesor/a Ayudante', 'Laboral', 'L2', False, False, False, 5),
        ('ASOCI', 'Profesor/a Asociado/a', 'Laboral', 'L3', False, False, False, 6),
        ('COLAB', 'Profesor/a Colaborador/a', 'Laboral', 'L2', True, False, False, 7),
        ('EMERI', 'Profesor/a Emérito/a', 'Laboral', 'L1', True, True, False, 8),
        ('VISIT', 'Profesor/a Visitante', 'Laboral', 'L2', False, False, False, 9),
        ('INTER', 'Profesor/a Interino/a', 'Laboral', 'L2', False, False, False, 10),
        ('SUSTI', 'Profesor/a Sustituto/a', 'Laboral', 'L3', False, False, False, 11),
        ('INVES', 'Personal Investigador', 'Laboral', 'L2', False, False, False, 12),
        ('CATEU', 'Catedrático/a de Escuela Universitaria', 'Funcionario', 'A1', True, True, True, 13),
        ('TITEU', 'Profesor/a Titular de Escuela Universitaria', 'Funcionario', 'A2', True, True, True, 14),
        ('OTROS', 'Otras figuras docentes', 'Laboral', 'L3', False, False, False, 15)
    ]
    
    for i, (id_nk, nombre, tipo_contrato, grupo, doctor, sexenios, venia, orden) in enumerate(categorias[:n], 1):
        fecha_carga = generate_random_date_datetime(2018, 2023)
        
        data.append({
            'ID_CATEGORIA_CUERPO_ESCALA': i,
            'NOMBRE_CATEGORIA_CUERPO_ESCALA': nombre,
            'ID_CAT_CPO_ESC_DESCR': i * 10,# 
            'SN_REQUIERE_DOCTORADO': ...,  # ELIMINADO: No existe en esquema
        })
    return pd.DataFrame(data)

def generate_d_tipo_asignatura(n=10):
    """Genera datos para la tabla D_TIPO_ASIGNATURA con todos los atributos completos
    
    Esta función genera datos completos para la tabla D_TIPO_ASIGNATURA, incluyendo
    todos los atributos descriptivos y técnicos necesarios.
    
    Args:
        n (int): Número de tipos de asignatura a generar (máx. 10)
        
    Returns:
        DataFrame: DataFrame con los datos generados
    """
    data = []
    
    tipos_asignatura = [
        (1, 'B', 'Básica', 'Asignatura de formación básica', 100, 1, 'S', 'S', 'N'),
        (2, 'O', 'Obligatoria', 'Asignatura obligatoria en el plan', 200, 2, 'S', 'S', 'N'),
        (3, 'P', 'Optativa', 'Asignatura de elección opcional', 300, 3, 'N', 'S', 'N'),
        (4, 'E', 'Prácticas Externas', 'Prácticas profesionales', 400, 4, 'N', 'S', 'N'),
        (5, 'G', 'Trabajo Fin de Grado', 'Trabajo final de grado', 500, 5, 'N', 'S', 'S'),
        (6, 'M', 'Trabajo Fin de Máster', 'Trabajo final de máster', 600, 6, 'N', 'S', 'S'),
        (7, 'D', 'Tesis Doctoral', 'Tesis de doctorado', 700, 7, 'N', 'S', 'S'),
        (8, 'C', 'Complementos de Formación', 'Complementos formativos', 800, 8, 'N', 'S', 'N'),
        (9, 'L', 'Créditos de Libre Elección', 'Créditos de libre elección', 900, 9, 'N', 'N', 'N'),
        (10, 'T', 'Técnica', 'Asignatura de carácter técnico', 1000, 10, 'N', 'S', 'N')
    ]
    
    for i, (id_nk, codigo, nombre, descripcion, id_descr, orden, basic, obligatoria, proyecto) in enumerate(tipos_asignatura[:n], 1):
        fecha_carga = generate_random_date_datetime(2018, 2023)
        
        data.append({
            'ID_TIPO_ASIGNATURA': i,
            'NOMBRE_TIPO_ASIGNATURA': nombre,
            'ID_TIPO_ASIGNATURA_DESCR': id_descr,
            'ID_TIPO_ASIGNATURA_NK': id_nk,# 
            'CODIGO_TIPO_ASIGNATURA': ...,  # ELIMINADO: No existe en esquema
            'DESCRIPCION_TIPO_ASIGNATURA': descripcion,# 
            'FECHA_CARGA': ...,  # ELIMINADO: No existe en esquema# 
            'ORDEN_VISUALIZACION': ...,  # ELIMINADO: No existe en esquema
            'SN_FORMACION_BASICA': basic,# 
            'SN_COMPUTO_ACADEMICO': ...,  # ELIMINADO: No existe en esquema# 
            'SN_PROYECTO_FIN_CARRERA': ...,  # ELIMINADO: No existe en esquema
            'FLG_FORMACION_BASICA': 1 if basic == 'S' else 0,# 
            'FLG_COMPUTO_ACADEMICO': ...,  # ELIMINADO: No existe en esquema# 
            'FLG_PROYECTO_FIN_CARRERA': ...,  # ELIMINADO: No existe en esquema
        })
    
    return pd.DataFrame(data)

# def generate_d_modalidad_asignatura(n=8):  # COMENTADO: Tabla no existe en esquema
#     """Esta función se elimina porque la tabla D_MODALIDAD_ASIGNATURA no existe en el esquema"""
#     raise NotImplementedError(
#         "Tabla D_MODALIDAD_ASIGNATURA no existe en el esquema SQL. "
#         "Esta tabla fue eliminada durante la corrección de la estructura. "
#         "Verifique el esquema dm_academico.sql para ver las tablas disponibles."
#     )

def generate_d_tipo_centro(n=8):
    """Genera datos para la tabla D_TIPO_CENTRO con atributos completos
    
    Implementación mejorada que incluye todos los campos de la tabla
    y añade información más detallada sobre los tipos de centros.
    
    Args:
        n (int): Número de tipos de centro a generar (máx. 8)
        
    Returns:
        DataFrame: DataFrame con los datos generados
    """
    data = []
    
    tipos_centro = [
        ('FAC', 'Facultad', 'Centro universitario dedicado a la docencia e investigación', 1, True, True),
        ('ESC', 'Escuela', 'Centro universitario dedicado a estudios técnicos o profesionales', 2, True, True),
        ('ETSUP', 'Escuela Técnica Superior', 'Centro universitario especializado en formación técnica avanzada', 3, True, True),
        ('ETUNI', 'Escuela Universitaria', 'Centro universitario de estudios técnicos de primer ciclo', 4, True, True),
        ('INST', 'Instituto Universitario', 'Centro dedicado principalmente a la investigación', 5, True, False),
        ('CENT', 'Centro Adscrito', 'Centro no perteneciente a la universidad pero con convenio', 6, False, True),
        ('FUND', 'Fundación Universitaria', 'Entidad sin ánimo de lucro vinculada a la universidad', 7, False, False),
        ('OTRO', 'Otro tipo de centro', 'Otros centros universitarios no clasificados previamente', 8, False, False)
    ]
    
    for i, (id_nk, nombre, descripcion, orden, docencia, titulacion) in enumerate(tipos_centro[:n], 1):
        fecha_carga = generate_random_date_datetime(2018, 2023)
        
        data.append({
            'ID_TIPO_CENTRO': i,
            'NOMBRE_TIPO_CENTRO': nombre,
            'ID_TIPO_CENTRO_DESCR': i * 100,# 
            'ID_TIPO_CENTRO_NK': ...,  # ELIMINADO: No existe en esquema
            'DESCRIPCION_TIPO_CENTRO': descripcion,# 
            'ORDEN_TIPO_CENTRO': ...,  # ELIMINADO: No existe en esquema# 
            'FLG_DOCENCIA': ...,  # ELIMINADO: No existe en esquema
            'SN_DOCENCIA': 'S' if docencia else 'N',# 
            'FLG_TITULACION_OFICIAL': ...,  # ELIMINADO: No existe en esquema
            'SN_TITULACION_OFICIAL': 'S' if titulacion else 'N',# 
            'FECHA_CARGA': ...,  # ELIMINADO: No existe en esquema
        })
    
    return pd.DataFrame(data)

def generate_d_centro(n=50, campus_df=None, tipo_centro_df=None, poblacion_df=None):
    """Genera datos para la tabla D_CENTRO"""
    data = []
    
    # Si no se proporcionan los DataFrames necesarios, crear unos mínimos
    if campus_df is None:
        campus_df = generate_d_campus(n=10)
    
    if tipo_centro_df is None:
        tipo_centro_df = generate_d_tipo_centro(n=5)
    
    if poblacion_df is None:
        poblacion_df = generate_d_poblacion(n=200)
    
    # Listas de facultades y escuelas comunes
    facultades = [
        "Facultad de Medicina",
        "Facultad de Ciencias",
        "Facultad de Derecho",
        "Facultad de Filosofía y Letras",
        "Facultad de Ciencias Económicas y Empresariales",
        "Facultad de Farmacia",
        "Facultad de Veterinaria",
        "Facultad de Educación",
        "Facultad de Psicología",
        "Facultad de Enfermería",
        "Facultad de Información y Documentación",
        "Facultad de Trabajo Social",
        "Facultad de Bellas Artes",
        "Facultad de Traducción e Interpretación",
        "Facultad de Ciencias Sociales"
    ]
    
    escuelas = [
        "Escuela Técnica Superior de Ingeniería Informática",
        "Escuela Técnica Superior de Ingeniería Industrial",
        "Escuela Técnica Superior de Arquitectura",
        "Escuela Técnica Superior de Ingeniería Agronómica",
        "Escuela Técnica Superior de Ingeniería de Telecomunicación",
        "Escuela Técnica Superior de Ingeniería Civil",
        "Escuela Universitaria de Enfermería",
        "Escuela Universitaria de Magisterio",
        "Escuela Universitaria de Turismo",
        "Escuela Universitaria de Trabajo Social"
    ]
    
    # Otros tipos de centros
    otros_centros = [
        "Instituto Universitario de Investigación",
        "Centro de Estudios Superiores",
        "Centro Adscrito de Formación Profesional",
        "Departamento de Investigación",
        "Centro Internacional de Posgrado",
        "Centro de Formación Permanente",
        "Colegio Mayor Universitario"
    ]
    
    # Combinar todas las listas
    nombres_centros = facultades + escuelas + otros_centros
    
    # Si hay menos centros en la lista que el número solicitado, repetir nombres con sufijos
    if len(nombres_centros) < n:
        extra_nombres = []
        for i in range(n - len(nombres_centros)):
            nombre_base = random.choice(nombres_centros)
            extra_nombres.append(f"{nombre_base} {i+1}")
        nombres_centros.extend(extra_nombres)
    
    # Tomar solo los n nombres necesarios
    nombres_centros = nombres_centros[:n]
    
    # Obtener IDs disponibles
    campus_ids = campus_df['ID_CAMPUS'].tolist()
    tipo_centro_ids = tipo_centro_df['ID_TIPO_CENTRO'].tolist()
    
    # Filtrar poblaciones españolas
    poblaciones_esp = poblacion_df[poblacion_df['NOMBRE_PAIS'] == 'España']
    if len(poblaciones_esp) > 0:
        poblacion_ids = poblaciones_esp['ID_POBLACION'].tolist()
    else:
        poblacion_ids = poblacion_df['ID_POBLACION'].tolist()
    
    for i in range(1, n+1):
        # Seleccionar valores aleatorios
        id_campus = random.choice(campus_ids)
        nombre_campus = campus_df[campus_df['ID_CAMPUS'] == id_campus]['NOMBRE_CAMPUS'].values[0]
        
        id_tipo_centro = random.choice(tipo_centro_ids)
        nombre_tipo_centro = tipo_centro_df[tipo_centro_df['ID_TIPO_CENTRO'] == id_tipo_centro]['NOMBRE_TIPO_CENTRO'].values[0]
        
        id_poblacion = random.choice(poblacion_ids)
        nombre_poblacion = poblacion_df[poblacion_df['ID_POBLACION'] == id_poblacion]['NOMBRE_POBLACION'].values[0]
        
        # Seleccionar nombre de centro
        nombre_centro = nombres_centros[i-1]
        
        # Crear versión extendida del nombre que incluye la población
        nombre_centro_ext = f"{nombre_centro} ({nombre_poblacion})"
        
        # Crear campo para ordenación (sin artículos)
        ord_nombre_centro = re.sub(r'^(El|La|Los|Las) ', '', nombre_centro).upper()
        
        # Valores para claves foráneas
        id_centro_nk = i * 100
        id_centro_descr = i * 1000
        
        data.append({
            'ID_CENTRO': i,
            'ID_CAMPUS': id_campus,
            'NOMBRE_CAMPUS': nombre_campus,
            'ID_TIPO_CENTRO': id_tipo_centro,
            'NOMBRE_TIPO_CENTRO': nombre_tipo_centro,
            'ID_POBLACION': id_poblacion,
            'NOMBRE_POBLACION': nombre_poblacion,
            'ID_CENTRO_NK': id_centro_nk  # TODO: Usar valores válidos de D_CENTRO,
            'ID_CENTRO_DESCR': id_centro_descr,
            'NOMBRE_CENTRO': nombre_centro,
            'ORD_NOMBRE_CENTRO': ord_nombre_centro,
            'NOMBRE_CENTRO_EXT': nombre_centro_ext
        })
    
    return pd.DataFrame(data)

def generate_d_universidad(n=100, paises_df=None):
    """Genera datos para la tabla D_UNIVERSIDAD con todos los atributos completos"""
    data = []
    
    # Si no se proporciona un dataframe de países, crear uno mínimo
    if paises_df is None:
        paises_df = generate_d_pais(n=20)
    
    # Obtener IDs de países y sus nombres
    paises_ids = paises_df['ID_PAIS'].tolist()
    paises_nk = paises_df['ID_PAIS_NK'].tolist()
    paises_nombres = paises_df['NOMBRE_PAIS'].tolist()
    
    # Prefijos para nombres de universidades
    prefijos = [
        "Universidad de",
        "Universidad Nacional de",
        "Universidad Autónoma de",
        "Universidad Politécnica de",
        "Universidad Complutense de",
        "Universidad Técnica de",
        "Universidad Estatal de",
        "Universidad Católica de",
        "Universidad Internacional de",
        "Universidad Europea de"
    ]
    
    # Crea un conjunto para almacenar nombres únicos
    nombres_unicos = set()
    
    for i in range(1, n+1):
        # Seleccionar país aleatorio
        idx_pais = random.randint(0, len(paises_ids) - 1)
        id_pais = paises_ids[idx_pais]
        id_pais_nk = paises_nk[idx_pais]
        nombre_pais = paises_nombres[idx_pais]
        
        # Generar nombre de universidad único
        while True:
            if fake.random_element([True, False]):
                # Nombre con ciudad
                ciudad = fake.city()
                prefijo = random.choice(prefijos)
                nombre_universidad_sin_pais = f"{prefijo} {ciudad}"
            else:
                # Nombre con área de conocimiento o personaje histórico
                area = random.choice(["Ciencias", "Humanidades", "Medicina", "Artes", "Tecnología"])
                nombre_universidad_sin_pais = f"Universidad {area} de {fake.last_name()}"
            
            # Nombre completo con país
            nombre_universidad = f"{nombre_universidad_sin_pais} ({nombre_pais})"
            
            # Verificar que el nombre sea único
            if nombre_universidad not in nombres_unicos:
                nombres_unicos.add(nombre_universidad)
                break
        
        # Generar PIC code (Project Identification Code) - formato: EXXXXX
        id_universidad_pic_nk = f"{random.choice(['E', 'P', 'R'])}{random.randint(10000, 99999)}"
        
        # Determinar si pertenece a la red UNITA o UNITA GEMINAE
        # UNITA: Red de universidades europeas de regiones con lenguas romances
        # UNITA GEMINAE: Programa de colaboración específico dentro de UNITA
        es_unita = random.choice(['S', 'N'])
        # Si es UNITA, puede ser UNITA GEMINAE
        es_unita_geminae = 'S' if es_unita == 'S' and random.random() < 0.3 else 'N'
        
        # Generar ID descriptivo
        id_universidad_descr = i * 100
        
        data.append({
            'ID_UNIVERSIDAD': i,
            'ID_UNIVERSIDAD_NK': i * 10  # TODO: Usar valores válidos de D_UNIVERSIDAD,
            'ID_UNIVERSIDAD_DESCR': id_universidad_descr,
            'NOMBRE_UNIVERSIDAD': nombre_universidad,
            'NOMBRE_UNIVERSIDAD_SIN_PAIS': nombre_universidad_sin_pais,
            'ID_PAIS_NK': id_pais_nk,
            'ID_UNIVERSIDAD_PIC_NK': id_universidad_pic_nk,
            'ID_PAIS': id_pais,
            'NOMBRE_PAIS': nombre_pais,
            'SN_UNIVERSIDAD_UNITA': es_unita,
            'SN_UNIVERSIDAD_UNITA_GEMINAE': es_unita_geminae
        })
    
    return pd.DataFrame(data)

def generate_d_poblacion_centro(poblacion_df=None):
    """Genera datos para la tabla D_POBLACION_CENTRO 
    
    Esta tabla contiene información sobre las poblaciones donde hay centros universitarios,
    incluyendo datos completos de provincia y comunidad autónoma para mejorar las consultas.
    
    Args:
        poblacion_df (DataFrame): DataFrame con datos de poblaciones
        
    Returns:
        DataFrame: DataFrame con los datos generados
    """
    data = []
    
    # Verificar DataFrame de poblaciones
    if poblacion_df is None:
        poblacion_df = generate_d_poblacion(n=100)
    
    # Filtrar poblaciones españolas que tienen datos completos de provincia y CCAA
    # Esto garantiza que tengamos información completa para el análisis
    poblaciones_esp = poblacion_df[
        (poblacion_df['NOMBRE_PAIS'] == 'España') & 
        (poblacion_df['NOMBRE_PROVINCIA'].notna()) & 
        (poblacion_df['NOMBRE_CCAA'].notna())
    ]
    
    if len(poblaciones_esp) > 0:
        # Primero añadimos todas las poblaciones españolas que tienen datos completos
        for _, row in poblaciones_esp.iterrows():
            data.append({
                'ID_POBLACION': row['ID_POBLACION'],
                'NOMBRE_POBLACION': row['NOMBRE_POBLACION'],# 
                'ID_PROVINCIA': ...,  # ELIMINADO: No existe en esquema
                'NOMBRE_PROVINCIA': row['NOMBRE_PROVINCIA'],# 
                'ID_CCAA': ...,  # ELIMINADO: No existe en esquema# 
                'NOMBRE_CCAA': ...,  # ELIMINADO: No existe en esquema
                'COD_POSTAL': f"{random.randint(1, 52):02d}{random.randint(0, 999):03d}"
            })
    
    # Añadir algunas poblaciones extranjeras importantes para centros internacionales
    poblaciones_ext = poblacion_df[
        (poblacion_df['NOMBRE_PAIS'] != 'España') & 
        (poblacion_df['ID_POBLACION'].notna())
    ].sample(min(20, len(poblacion_df[poblacion_df['NOMBRE_PAIS'] != 'España'])))
    
    for _, row in poblaciones_ext.iterrows():
        # Para ciudades extranjeras, podemos tener o no datos de provincia
        provincia = row.get('NOMBRE_PROVINCIA', "")
        region = row.get('NOMBRE_CCAA', "")
        
        data.append({
            'ID_POBLACION': row['ID_POBLACION'],
            'NOMBRE_POBLACION': row['NOMBRE_POBLACION'],
            'ID_PROVINCIA': row.get('ID_PROVINCIA', 0),# 
            'NOMBRE_PROVINCIA': ...,  # ELIMINADO: No existe en esquema
            'ID_CCAA': row.get('ID_CCAA', 0),# 
            'NOMBRE_CCAA': ...,  # ELIMINADO: No existe en esquema
            'COD_POSTAL': f"INT-{random.randint(1000, 9999)}"
        })
    
    return pd.DataFrame(data)

# def generate_d_estado_credencial_acceso(n=7):  # COMENTADO: Tabla no existe en esquema
#     """Esta función se elimina porque la tabla D_ESTADO_CREDENCIAL_ACCESO no existe en el esquema"""
#     raise NotImplementedError(
#         "Tabla D_ESTADO_CREDENCIAL_ACCESO no existe en el esquema SQL. "
#         "Esta tabla fue eliminada durante la corrección de la estructura. "
#         "Verifique el esquema dm_academico.sql para ver las tablas disponibles."
#     )

# def generate_d_territorio(n=50, paises_df=None):  # COMENTADO: Tabla no existe en esquema
#     """Genera datos para la tabla D_TERRITORIO
    
#     Esta dimensión contiene la jerarquía territorial completa: país, comunidad autónoma, 
#     provincia, etc. para facilitar el análisis geográfico de los datos académicos.
    
#     Args:
#         n (int): Número de territorios a generar
#         paises_df (DataFrame): DataFrame con los países
        
#     Returns:
#         DataFrame: DataFrame con los datos generados
#     """
#     data = []
    
#     # Si no se proporciona el DataFrame de países, crear uno temporal
#     if paises_df is None:
#         paises_df = generate_d_pais(n=30)
    
#     # España será el país principal
#     espana_id = 1
#     espana_row = None
    
#     # Asegurar que España está en el dataframe
#     for _, row in paises_df.iterrows():
#         if row['NOMBRE_PAIS'] == 'España':
#             espana_row = row
#             espana_id = row['ID_PAIS']
#             break
    
#     # Si no encontramos España, tomamos el primer país para representar a España
#     if espana_row is None and not paises_df.empty:
#         espana_row = paises_df.iloc[0]
#         espana_id = espana_row['ID_PAIS']
    
#     # Datos de comunidades autónomas y provincias de España
#     comunidades_autonomas = {
#         "Andalucía": ["Almería", "Cádiz", "Córdoba", "Granada", "Huelva", "Jaén", "Málaga", "Sevilla"],
#         "Aragón": ["Huesca", "Teruel", "Zaragoza"],
#         "Asturias": ["Asturias"],
#         "Baleares": ["Islas Baleares"],
#         "Canarias": ["Las Palmas", "Santa Cruz de Tenerife"],
#         "Cantabria": ["Cantabria"],
#         "Castilla y León": ["Ávila", "Burgos", "León", "Palencia", "Salamanca", "Segovia", "Soria", "Valladolid", "Zamora"],
#         "Castilla-La Mancha": ["Albacete", "Ciudad Real", "Cuenca", "Guadalajara", "Toledo"],
#         "Cataluña": ["Barcelona", "Girona", "Lleida", "Tarragona"],
#         "Comunidad Valenciana": ["Alicante", "Castellón", "Valencia"],
#         "Extremadura": ["Badajoz", "Cáceres"],
#         "Galicia": ["A Coruña", "Lugo", "Ourense", "Pontevedra"],
#         "Madrid": ["Madrid"],
#         "Murcia": ["Murcia"],
#         "Navarra": ["Navarra"],
#         "País Vasco": ["Álava", "Guipúzcoa", "Vizcaya"],
#         "La Rioja": ["La Rioja"],
#         "Ceuta": ["Ceuta"],
#         "Melilla": ["Melilla"]
#     }
    
#     # Contador para IDs
#     id_territorio = 1
#     id_nivel_1 = 1  # País
    
#     # España como país principal (nivel 1)
#     data.append({
#         'ID_TERRITORIO': id_territorio,
#         'ID_NIVEL_TERRITORIAL': 1,
#         'NOMBRE_TERRITORIO': 'España',
#         'ID_TERRITORIO_PADRE': None,
#         'NOMBRE_TERRITORIO_PADRE': None,
#         'ID_PAIS': espana_id,
#         'CODIGO_TERRITORIO': 'ES',
#         'ID_TERRITORIO_NK': 'ES',
#         'ID_TERRITORIO_DESCR': id_territorio
#     })
    
#     # Mapear relaciones para facilitar referencias posteriores
#     territorio_map = {'España': id_territorio}
#     id_territorio += 1
    
#     # Generar comunidades autónomas (nivel 2)
#     for ccaa, provincias in comunidades_autonomas.items():
#         id_nivel_2 = id_territorio
        
#         data.append({
#             'ID_TERRITORIO': id_territorio,
#             'ID_NIVEL_TERRITORIAL': 2,
#             'NOMBRE_TERRITORIO': ccaa,
#             'ID_TERRITORIO_PADRE': territorio_map['España'],
#             'NOMBRE_TERRITORIO_PADRE': 'España',
#             'ID_PAIS': espana_id,
#             'CODIGO_TERRITORIO': f'ES-{id_territorio:02d}',
#             'ID_TERRITORIO_NK': f'CCAA-{id_territorio:02d}',
#             'ID_TERRITORIO_DESCR': id_territorio
#         })
        
#         territorio_map[ccaa] = id_territorio
#         id_territorio += 1
        
#         # Generar provincias (nivel 3)
#         for provincia in provincias:
#             data.append({
#                 'ID_TERRITORIO': id_territorio,
#                 'ID_NIVEL_TERRITORIAL': 3,
#                 'NOMBRE_TERRITORIO': provincia,
#                 'ID_TERRITORIO_PADRE': territorio_map[ccaa],
#                 'NOMBRE_TERRITORIO_PADRE': ccaa,
#                 'ID_PAIS': espana_id,
#                 'CODIGO_TERRITORIO': f'ES-{territorio_map[ccaa]:02d}-{id_territorio:03d}',
#                 'ID_TERRITORIO_NK': f'PROV-{id_territorio:03d}',
#                 'ID_TERRITORIO_DESCR': id_territorio
#             })
            
#             territorio_map[provincia] = id_territorio
#             id_territorio += 1
    
#     # Añadir otros países del dataframe como territorios de nivel 1
#     otros_paises_count = 0
#     for _, pais in paises_df.iterrows():
#         if pais['NOMBRE_PAIS'] != 'España' and otros_paises_count < 20:  # Limitar a 20 países adicionales
#             id_nivel_1 = id_territorio
#             nombre_pais = pais['NOMBRE_PAIS']
#             codigo_pais = pais.get('CODIGO_PAIS', f'INT{id_territorio:03d}')
            
#             data.append({
#                 'ID_TERRITORIO': id_territorio,
#                 'ID_NIVEL_TERRITORIAL': 1,
#                 'NOMBRE_TERRITORIO': nombre_pais,
#                 'ID_TERRITORIO_PADRE': None,
#                 'NOMBRE_TERRITORIO_PADRE': None,
#                 'ID_PAIS': pais['ID_PAIS'],
#                 'CODIGO_TERRITORIO': codigo_pais,
#                 'ID_TERRITORIO_NK': f'PAIS-{pais["ID_PAIS"]:03d}',
#                 'ID_TERRITORIO_DESCR': id_territorio
#             })
            
#             territorio_map[nombre_pais] = id_territorio
#             id_territorio += 1
#             otros_paises_count += 1
            
#             # Para algunos países, añadir regiones fictícias (nivel 2)
#             if random.random() < 0.3:  # Solo para el 30% de países
#                 num_regiones = random.randint(2, 5)
#                 for j in range(1, num_regiones + 1):
#                     nombre_region = f"Región {j} de {nombre_pais}"
                    
#                     data.append({
#                         'ID_TERRITORIO': id_territorio,
#                         'ID_NIVEL_TERRITORIAL': 2,
#                         'NOMBRE_TERRITORIO': nombre_region,
#                         'ID_TERRITORIO_PADRE': territorio_map[nombre_pais],
#                         'NOMBRE_TERRITORIO_PADRE': nombre_pais,
#                         'ID_PAIS': pais['ID_PAIS'],
#                         'CODIGO_TERRITORIO': f'{codigo_pais}-R{j:02d}',
#                         'ID_TERRITORIO_NK': f'REG-{id_territorio:03d}',
#                         'ID_TERRITORIO_DESCR': id_territorio
#                     })
                    
#                     territorio_map[nombre_region] = id_territorio
#                     id_territorio += 1
    
#     # Limitar el número de territorios si es necesario
#     if len(data) > n:
#         data = data[:n]
    
#     return pd.DataFrame(data)

# def generate_d_nivel_idioma(n=10):  # COMENTADO: Tabla no existe en esquema
#     """Genera datos para la tabla D_NIVEL_IDIOMA
    
#     Esta tabla define los niveles de idioma según el Marco Común Europeo de Referencia
#     para las lenguas (MCER) y otros sistemas equivalentes.
    
#     Args:
#         n (int): Número de niveles a generar (máx. 10)
        
#     Returns:
#         DataFrame: DataFrame con los datos generados
#     """
#     data = []
    
#     niveles = [
#         ('A1', 'Acceso', 'Básico - Acceso', 'Principiante'),
#         ('A2', 'Plataforma', 'Básico - Plataforma', 'Elemental'),
#         ('B1', 'Intermedio', 'Intermedio - Umbral', 'Intermedio'),
#         ('B2', 'Intermedio alto', 'Intermedio - Avanzado', 'Intermedio alto'),
#         ('C1', 'Dominio eficaz', 'Competente - Dominio', 'Avanzado'),
#         ('C2', 'Maestría', 'Competente - Maestría', 'Proficiencia'),
#         ('N1', 'Nativo', 'Lengua materna', 'Nativo'),
#         ('NC', 'No consta', 'Sin nivel definido', 'No especificado'),
#         ('NA', 'No aplica', 'No requiere nivel', 'No aplica'),
#         ('XX', 'Otros', 'Otro sistema de certificación', 'Otros')
#     ]
    
#     # Asegurar que no excedemos el número solicitado
#     niveles = niveles[:n]
    
#     for i, (id_nk, nombre, descripcion, equiv) in enumerate(niveles, 1):
#         data.append({
#             'ID_NIVEL_IDIOMA': i,
#             'ID_NIVEL_IDIOMA_NK': id_nk,
#             'NOMBRE_NIVEL_IDIOMA': nombre,
#             'DESCRIPCION_NIVEL_IDIOMA': descripcion,
#             'EQUIVALENCIA_SISTEMA_MCER': equiv,
#             'ORDEN_NIVEL_IDIOMA': i,
#             'FECHA_CARGA': generate_random_date(2020, 2023)
#         })
    
#     return pd.DataFrame(data)

# def generate_d_situacion_administrativa(n=10):  # COMENTADO: Tabla no existe en esquema
#     """Genera datos para la tabla D_SITUACION_ADMINISTRATIVA
    
#     Esta tabla contiene las posibles situaciones administrativas del personal
#     docente e investigador de la universidad.
    
#     Args:
#         n (int): Número de situaciones a generar (máx. 10)
        
#     Returns:
#         DataFrame: DataFrame con los datos generados
#     """
#     data = []
    
#     situaciones = [
#         ('ACT', 'Servicio activo', 'Situación de servicio activo normal'),
#         ('EXC', 'Excedencia', 'Excedencia voluntaria'),
#         ('EXCF', 'Excedencia forzosa', 'Excedencia forzosa'),
#         ('EXCS', 'Excedencia por servicios', 'Excedencia por servicios especiales'),
#         ('EXCFC', 'Excedencia familiar', 'Excedencia por cuidado de familiares'),
#         ('EXCHI', 'Excedencia hijos', 'Excedencia por cuidado de hijos'),
#         ('SUS', 'Suspensión', 'Suspensión de funciones'),
#         ('COM', 'Comisión servicios', 'En comisión de servicios'),
#         ('JUB', 'Jubilación', 'Jubilación'),
#         ('BAJ', 'Baja', 'Baja temporal')
#     ]
    
#     # Asegurar que no excedemos el número solicitado
#     situaciones = situaciones[:n]
    
#     for i, (id_nk, nombre, descripcion) in enumerate(situaciones, 1):
#         data.append({
#             'ID_SITUACION_ADMINISTRATIVA': i,
#             'ID_SITUACION_ADMINISTRATIVA_NK': id_nk,
#             'NOMBRE_SITUACION_ADVA': nombre,
#             'DESCRIPCION_SITUACION': descripcion,
#             'FECHA_CARGA': generate_random_date(2020, 2023),
#             'FLG_ACTIVO': 1 if id_nk == 'ACT' else 0,# 
#             'SN_ACTIVO': ...,  # ELIMINADO: No existe en esquema
#         })
    
#     return pd.DataFrame(data)

# def generate_d_tipo_contrato(n=15):  # COMENTADO: Tabla no existe en esquema
#     """Genera datos para la tabla D_TIPO_CONTRATO
    
#     Esta tabla contiene los diferentes tipos de contrato del personal
#     docente e investigador de la universidad.
    
#     Args:
#         n (int): Número de tipos de contrato a generar (máx. 15)
        
#     Returns:
#         DataFrame: DataFrame con los datos generados
#     """
#     data = []
    
#     contratos = [
#         ('FUN', 'Funcionario', 'Personal funcionario de carrera'),
#         ('LAB', 'Laboral', 'Personal laboral'),
#         ('LABF', 'Laboral fijo', 'Personal laboral fijo'),
#         ('LABI', 'Laboral indefinido', 'Personal laboral indefinido no fijo'),
#         ('LABT', 'Laboral temporal', 'Personal laboral temporal'),
#         ('INT', 'Interino', 'Personal funcionario interino'),
#         ('AYU', 'Ayudante', 'Profesor Ayudante'),
#         ('AYUD', 'Ayudante Doctor', 'Profesor Ayudante Doctor'),
#         ('ASO', 'Asociado', 'Profesor Asociado'),
#         ('COL', 'Colaborador', 'Profesor Colaborador'),
#         ('CD', 'Contratado Doctor', 'Profesor Contratado Doctor'),
#         ('SUP', 'Sustituto', 'Profesor Sustituto'),
#         ('EME', 'Emérito', 'Profesor Emérito'),
#         ('VIS', 'Visitante', 'Profesor Visitante'),
#         ('INV', 'Investigador', 'Personal investigador')
#     ]
    
#     # Asegurar que no excedemos el número solicitado
#     contratos = contratos[:n]
    
#     for i, (id_nk, nombre, descripcion) in enumerate(contratos, 1):
#         data.append({
#             'ID_TIPO_CONTRATO': i,
#             'ID_TIPO_CONTRATO_NK': id_nk,
#             'NOMBRE_TIPO_CONTRATO': nombre,
#             'DESCRIPCION_TIPO_CONTRATO': descripcion,
#             'FECHA_CARGA': generate_random_date(2020, 2023)
#         })
    
#     return pd.DataFrame(data)

# def generate_d_periodo_lectivo(n=10):  # COMENTADO: Tabla no existe en esquema
#     """Genera datos para la tabla D_PERIODO_LECTIVO
    
#     Esta tabla contiene información sobre los periodos lectivos del calendario académico.
    
#     Args:
#         n (int): Número de periodos a generar (máx. 10)
        
#     Returns:
#         DataFrame: DataFrame con los datos generados
#     """
#     data = []
    
#     periodos = [
#         ('S1', 'Primer semestre', '01/09', '31/01', 'Regular', 1),
#         ('S2', 'Segundo semestre', '01/02', '30/06', 'Regular', 2),
#         ('E1', 'Exámenes primer semestre', '15/01', '31/01', 'Exámenes', 3),
#         ('E2', 'Exámenes segundo semestre', '15/06', '30/06', 'Exámenes', 4),
#         ('ER', 'Exámenes recuperación', '01/07', '15/07', 'Exámenes', 5),
#         ('EE', 'Exámenes extraordinarios', '01/09', '15/09', 'Exámenes', 6),
#         ('NL', 'No lectivo', '16/07', '31/08', 'No lectivo', 7),
#         ('NV', 'Navidad', '23/12', '07/01', 'Vacaciones', 8),
#         ('SS', 'Semana Santa', '01/04', '08/04', 'Vacaciones', 9),
#         ('VE', 'Verano', '15/07', '31/08', 'Vacaciones', 10)
#     ]
    
#     # Asegurar que no excedemos el número solicitado
#     periodos = periodos[:n]
    
#     for i, (id_nk, nombre, fecha_inicio, fecha_fin, tipo, orden) in enumerate(periodos, 1):
#         es_lectivo = 1 if tipo == 'Regular' else 0
#         es_examenes = 1 if tipo == 'Exámenes' else 0
#         es_vacaciones = 1 if tipo == 'Vacaciones' else 0
        
#         data.append({
#             'ID_PERIODO_LECTIVO': i,
#             'ID_PERIODO_LECTIVO_NK': id_nk,
#             'NOMBRE_PERIODO_LECTIVO': nombre,
#             'FECHA_INICIO_ESTANDAR': fecha_inicio,
#             'FECHA_FIN_ESTANDAR': fecha_fin,
#             'TIPO_PERIODO': tipo,
#             'ORDEN_PERIODO': orden,
#             'ES_LECTIVO': es_lectivo,
#             'ES_EXAMENES': es_examenes,
#             'ES_VACACIONES': es_vacaciones,
#             'SN_LECTIVO': 'S' if es_lectivo == 1 else 'N',
#             'SN_EXAMENES': 'S' if es_examenes == 1 else 'N',
#             'SN_VACACIONES': 'S' if es_vacaciones == 1 else 'N',
#             'FECHA_CARGA': generate_random_date(2020, 2023)
#         })
    
#     return pd.DataFrame(data)

def generate_d_modalidad_plan_estudio(n=5):
    """Genera datos para la tabla D_MODALIDAD_PLAN_ESTUDIO con todos los atributos completos
    
    Esta función genera datos completos para la tabla D_MODALIDAD_PLAN_ESTUDIO, incluyendo
    el atributo ID_MODALIDAD_PLAN_ESTUDIO_NK y otros campos descriptivos.
    
    Args:
        n (int): Número de modalidades a generar (máx. 5)
        
    Returns:
        DataFrame: DataFrame con los datos generados
    """
    data = []
    
    modalidades = [
        ('PRE', 'Presencial', 'Modalidad con asistencia física obligatoria', 1),
        ('SEM', 'Semipresencial', 'Modalidad mixta presencial y virtual', 2),
        ('VIR', 'Virtual', 'Modalidad completamente virtual', 3),
        ('DIS', 'A distancia', 'Modalidad sin presencialidad ni sincronía', 4),
        ('HYB', 'Híbrida', 'Modalidad con elección de formato', 5)
    ]
    
    # Asegurar que no excedemos el número solicitado
    modalidades = modalidades[:n]
    
    for i, (id_nk, nombre, descripcion, orden) in enumerate(modalidades, 1):
        fecha_carga = generate_random_date(2020, 2023)
        
        data.append({
            'ID_MODALIDAD_PLAN_ESTUDIO': i,
            'NOMBRE_MODALIDAD_PLAN': nombre,
            'ID_MODALIDAD_PLAN_ESTUDIO_NK': id_nk,# 
            'DESCRIPCION_MODALIDAD': ...,  # ELIMINADO: No existe en esquema
            'ORDEN_VISUALIZACION': orden,# 
            'FECHA_CARGA': ...,  # ELIMINADO: No existe en esquema
            'ES_PRESENCIAL': 1 if id_nk in ['PRE', 'SEM', 'HYB'] else 0,
            'SN_PRESENCIAL': 'S' if id_nk in ['PRE', 'SEM', 'HYB'] else 'N',
            'ES_VIRTUAL': 1 if id_nk in ['VIR', 'SEM', 'HYB'] else 0,
            'SN_VIRTUAL': 'S' if id_nk in ['VIR', 'SEM', 'HYB'] else 'N'
        })
    
    return pd.DataFrame(data)

# def generate_d_asignatura_origen(n=200, asignatura_df=None, universidad_df=None):  # COMENTADO: Tabla no existe en esquema
#     """Genera datos para la tabla D_ASIGNATURA_ORIGEN
    
#     Contiene las asignaturas de origen en procesos de reconocimiento y transferencia.
    
#     Args:
#         n (int): Número de asignaturas de origen a generar
#         asignatura_df (DataFrame): DataFrame con asignaturas de referencia
#         universidad_df (DataFrame): DataFrame con universidades de referencia
        
#     Returns:
#         DataFrame: DataFrame con los datos generados
#     """
#     data = []
    
#     # Si no se proporcionan DataFrames de referencia, crear algunos mínimos
#     if asignatura_df is None:
#         # Crear una lista de nombres de asignaturas base
#         nombres_asignaturas = [
#             "Matemáticas", "Física", "Química", "Biología", "Historia", 
#             "Literatura", "Filosofía", "Economía", "Derecho", "Informática",
#             "Estadística", "Álgebra", "Cálculo", "Programación", "Bases de Datos"
#         ]
#         # Expandir con variantes
#         variantes = ["I", "II", "III", "Básica", "Avanzada", "Aplicada", "General", "Específica"]
#         asignaturas_completas = []
#         for nombre in nombres_asignaturas:
#             asignaturas_completas.append(nombre)
#             for variante in variantes:
#                 asignaturas_completas.append(f"{nombre} {variante}")
#     else:
#         # Usar nombres de asignaturas existentes con algunas variaciones
#         asignaturas_completas = asignatura_df['NOMBRE_ASIGNATURA'].tolist()
    
#     # Si no se proporciona DataFrame de universidades, crear nombres de ejemplo
#     if universidad_df is None:
#         universidades = [
#             "Universidad de Madrid", "Universidad de Barcelona", "Universidad de Valencia",
#             "Universidad de Sevilla", "Universidad de Zaragoza", "Universidad de Salamanca",
#             "Universidad de Granada", "Universidad de Murcia", "Universidad de Santiago",
#             "Universidad de Oviedo", "Universidad de Valladolid", "Universidad de Málaga"
#         ]
#     else:
#         universidades = universidad_df['NOMBRE_UNIVERSIDAD'].tolist()
    
#     # Generar asignaturas de origen con datos aleatorios
#     for i in range(1, n+1):
#         nombre_asignatura = random.choice(asignaturas_completas)
#         universidad = random.choice(universidades)
        
#         # Asignar créditos aleatorios (típicamente entre 3 y 12)
#         creditos = random.choice([3, 4, 4.5, 5, 6, 7.5, 9, 10, 12])
        
#         # Algunos planes de estudio de origen inventados
#         plan_estudio_origen = f"Plan {2000 + random.randint(0, 20)}"
        
#         # Crear código único para asignatura de origen
#         codigo_asignatura = f"{random.randint(10000, 99999)}"
        
#         data.append({
#             'ID_ASIGNATURA_ORIGEN': i,
#             'ID_ASIGNATURA_ORIGEN_NK': codigo_asignatura,
#             'NOMBRE_ASIGNATURA_ORIGEN': nombre_asignatura,
#             'NOMBRE_UNIVERSIDAD_ORIGEN': universidad,
#             'PLAN_ESTUDIO_ORIGEN': plan_estudio_origen,
#             'CREDITOS_ORIGEN': creditos,
#             'TIPO_CREDITO_ORIGEN': random.choice(['ECTS', 'LRU', 'Otro']),
#             'CALIFICACION_ORIGEN': random.choice(['Aprobado', 'Notable', 'Sobresaliente', 'Matrícula de Honor']),
#             'FECHA_CURSADA': generate_random_date(2000, 2022),
#             'FECHA_CARGA': generate_random_date(2020, 2023)
#         })
    
#     return pd.DataFrame(data)

# def generate_d_tipo_inscripcion(n=8):  # COMENTADO: Tabla no existe en esquema
#     """Genera datos para la tabla D_TIPO_INSCRIPCION
    
#     Contiene los diferentes tipos de inscripción en actividades académicas.
    
#     Args:
#         n (int): Número de tipos de inscripción a generar (máx. 8)
        
#     Returns:
#         DataFrame: DataFrame con los datos generados
#     """
#     data = []
    
#     tipos_inscripcion = [
#         # ID_NK, Nombre, Descripción
#         ('ORDI', 'Ordinaria', 'Inscripción estándar en período ordinario'),
#         ('EXTR', 'Extraordinaria', 'Inscripción en período extraordinario'),
#         ('PRCT', 'Prácticas', 'Inscripción para prácticas curriculares'),
#         ('EXTC', 'Extracurricular', 'Inscripción en actividades extracurriculares'),
#         ('TRAB', 'Trabajo Fin', 'Inscripción en TFG/TFM/Tesis'),
#         ('PEXT', 'Prácticas Externas', 'Inscripción en prácticas externas no curriculares'),
#         ('MOVI', 'Movilidad', 'Inscripción asociada a programa de movilidad'),
#         ('ESPC', 'Especial', 'Inscripción en condiciones especiales')
#     ]
    
#     # Limitar al número solicitado
#     tipos_inscripcion = tipos_inscripcion[:n]
    
#     for i, (id_nk, nombre, descripcion) in enumerate(tipos_inscripcion, 1):
#         data.append({
#             'ID_TIPO_INSCRIPCION': i,
#             'ID_TIPO_INSCRIPCION_NK': id_nk,
#             'NOMBRE_TIPO_INSCRIPCION': nombre,
#             'DESCRIPCION_TIPO_INSCRIPCION': descripcion,
#             'FLG_ACTIVO': 1,
#             'FECHA_CARGA': generate_random_date(2015, 2023)
#         })
    
#     return pd.DataFrame(data)

# def generate_d_ambito_conocimiento(n=20):  # COMENTADO: Tabla no existe en esquema
#     """Genera datos para la tabla D_AMBITO_CONOCIMIENTO
    
#     Contiene los ámbitos de conocimiento según la clasificación ISCED.
    
#     Args:
#         n (int): Número de ámbitos de conocimiento a generar (máx. 20)
        
#     Returns:
#         DataFrame: DataFrame con los datos generados
#     """
#     data = []
    
#     ambitos = [
#         # Código, Nombre, Rama
#         ('00', 'Programas generales', 'Multidisciplinar'),
#         ('01', 'Educación', 'Ciencias Sociales y Jurídicas'),
#         ('02', 'Artes y humanidades', 'Artes y Humanidades'),
#         ('021', 'Artes', 'Artes y Humanidades'),
#         ('022', 'Humanidades', 'Artes y Humanidades'),
#         ('023', 'Lenguas', 'Artes y Humanidades'),
#         ('03', 'Ciencias sociales, periodismo e información', 'Ciencias Sociales y Jurídicas'),
#         ('031', 'Ciencias sociales y del comportamiento', 'Ciencias Sociales y Jurídicas'),
#         ('032', 'Periodismo e información', 'Ciencias Sociales y Jurídicas'),
#         ('04', 'Negocios, administración y derecho', 'Ciencias Sociales y Jurídicas'),
#         ('041', 'Negocios y administración', 'Ciencias Sociales y Jurídicas'),
#         ('042', 'Derecho', 'Ciencias Sociales y Jurídicas'),
#         ('05', 'Ciencias naturales, matemáticas y estadística', 'Ciencias'),
#         ('051', 'Biología y bioquímica', 'Ciencias'),
#         ('052', 'Medio ambiente', 'Ciencias'),
#         ('053', 'Ciencias físicas, químicas y geológicas', 'Ciencias'),
#         ('054', 'Matemáticas y estadística', 'Ciencias'),
#         ('06', 'Tecnologías de la información y comunicación', 'Ingeniería y Arquitectura'),
#         ('061', 'Tecnologías de la información y comunicación', 'Ingeniería y Arquitectura'),
#         ('07', 'Ingeniería, industria y construcción', 'Ingeniería y Arquitectura'),
#         ('071', 'Ingeniería y profesiones afines', 'Ingeniería y Arquitectura'),
#         ('072', 'Industria y producción', 'Ingeniería y Arquitectura'),
#         ('073', 'Arquitectura y construcción', 'Ingeniería y Arquitectura'),
#         ('08', 'Agricultura, silvicultura, pesca y veterinaria', 'Ciencias'),
#         ('081', 'Agricultura', 'Ciencias'),
#         ('082', 'Silvicultura', 'Ciencias'),
#         ('083', 'Pesca', 'Ciencias'),
#         ('084', 'Veterinaria', 'Ciencias de la Salud'),
#         ('09', 'Salud y bienestar', 'Ciencias de la Salud'),
#         ('091', 'Salud', 'Ciencias de la Salud'),
#         ('092', 'Bienestar', 'Ciencias de la Salud'),
#         ('10', 'Servicios', 'Ciencias Sociales y Jurídicas'),
#         ('101', 'Servicios personales', 'Ciencias Sociales y Jurídicas'),
#         ('102', 'Servicios de higiene y salud ocupacional', 'Ciencias de la Salud'),
#         ('103', 'Servicios de seguridad', 'Ciencias Sociales y Jurídicas'),
#         ('104', 'Servicios de transporte', 'Ingeniería y Arquitectura')
#     ]
    
#     # Limitar al número solicitado
#     ambitos = ambitos[:n]
    
#     for i, (codigo, nombre, rama) in enumerate(ambitos, 1):
#         nivel = len(codigo) // 3 + 1  # Nivel jerárquico basado en la longitud del código
#         data.append({
#             'ID_AMBITO_CONOCIMIENTO': i,
#             'ID_AMBITO_CONOCIMIENTO_NK': codigo,
#             'NOMBRE_AMBITO_CONOCIMIENTO': nombre,
#             'RAMA_CONOCIMIENTO': rama,
#             'NIVEL_JERARQUICO': nivel,
#             'ID_AMBITO_PADRE_NK': codigo[:3] if len(codigo) > 3 else None,
#             'ID_AMBITO_PADRE': next((j+1 for j, (c, _, _) in enumerate(ambitos) if c == codigo[:3]), None) if len(codigo) > 3 else None,
#             'FECHA_CARGA': generate_random_date(2015, 2023)
#         })
    
#     return pd.DataFrame(data)

# def generate_d_evento_academico(n=30):  # COMENTADO: Tabla no existe en esquema
#     """Genera datos para la tabla D_EVENTO_ACADEMICO
    
#     Contiene eventos académicos como apertura de curso, período de matrícula, etc.
    
#     Args:
#         n (int): Número de eventos académicos a generar
        
#     Returns:
#         DataFrame: DataFrame con los datos generados
#     """
#     data = []
    
#     # Tipos básicos de eventos académicos
#     tipos_eventos = [
#         'Apertura de curso', 'Cierre de curso', 'Período de matrícula', 
#         'Período de exámenes', 'Asignación de TFG/TFM', 'Defensa de TFG/TFM',
#         'Solicitud de reconocimientos', 'Solicitud de convocatoria extraordinaria',
#         'Período de prácticas', 'Acto de graduación', 'Jornada de puertas abiertas',
#         'Período de preinscripción', 'Asignación de tribunal', 'Período de reclamaciones',
#         'Publicación de calificaciones'
#     ]
    
#     # Crear eventos para diferentes años académicos
#     for i in range(1, n+1):
#         año_base = 2015 + (i % 8)  # Distribuir entre 2015-2022
        
#         # Elegir tipo de evento
#         tipo_evento = random.choice(tipos_eventos)
        
#         # Generar fechas de inicio y fin coherentes según el tipo de evento
#         if 'matrícula' in tipo_evento.lower() or 'preinscripción' in tipo_evento.lower():
#             # Los periodos de matrícula suelen ser en septiembre o febrero
#             mes_inicio = random.choice([2, 9])
#             if mes_inicio == 9:  # Matrícula primer semestre
#                 fecha_inicio = datetime.date(año_base, mes_inicio, random.randint(1, 15))
#                 fecha_fin = fecha_inicio + datetime.timedelta(days=random.randint(10, 20))
#             else:  # Matrícula segundo semestre
#                 fecha_inicio = datetime.date(año_base + 1, mes_inicio, random.randint(1, 15))
#                 fecha_fin = fecha_inicio + datetime.timedelta(days=random.randint(10, 20))
        
#         elif 'exámenes' in tipo_evento.lower():
#             # Exámenes en enero/febrero o junio/julio
#             mes_inicio = random.choice([1, 6])
#             if mes_inicio == 1:  # Exámenes primer semestre
#                 fecha_inicio = datetime.date(año_base + 1, mes_inicio, random.randint(15, 25))
#                 fecha_fin = datetime.date(año_base + 1, 2, random.randint(5, 15))
#             else:  # Exámenes segundo semestre
#                 fecha_inicio = datetime.date(año_base + 1, mes_inicio, random.randint(15, 25))
#                 fecha_fin = datetime.date(año_base + 1, 7, random.randint(5, 15))
        
#         elif 'apertura' in tipo_evento.lower():
#             # Apertura de curso en septiembre/octubre
#             fecha_inicio = datetime.date(año_base, random.choice([9, 10]), random.randint(15, 30))
#             fecha_fin = fecha_inicio  # Mismo día
        
#         elif 'cierre' in tipo_evento.lower():
#             # Cierre de curso en junio/julio
#             fecha_inicio = datetime.date(año_base + 1, random.choice([6, 7]), random.randint(15, 30))
#             fecha_fin = fecha_inicio  # Mismo día
        
#         else:
#             # Otros eventos distribuidos durante el curso
#             mes_inicio = random.randint(9, 12) if random.random() < 0.5 else random.randint(1, 6)
#             if mes_inicio >= 9:  # Primer semestre
#                 fecha_inicio = datetime.date(año_base, mes_inicio, random.randint(1, 28))
#             else:  # Segundo semestre
#                 fecha_inicio = datetime.date(año_base + 1, mes_inicio, random.randint(1, 28))
            
#             # La duración varía según el tipo de evento
#             if 'defensa' in tipo_evento.lower() or 'graduación' in tipo_evento.lower():
#                 fecha_fin = fecha_inicio  # Eventos de un solo día
#             else:
#                 fecha_fin = fecha_inicio + datetime.timedelta(days=random.randint(5, 15))
        
#         # Generar código único para evento
#         codigo_evento = f"EV{año_base % 100}{random.randint(100, 999)}"
        
#         # Determinar si es período lectivo
#         es_lectivo = 0 if ('exámenes' in tipo_evento.lower() or 
#                            'matrícula' in tipo_evento.lower() or 
#                            'preinscripción' in tipo_evento.lower()) else 1
        
#         data.append({
#             'ID_EVENTO_ACADEMICO': i,
#             'ID_EVENTO_ACADEMICO_NK': codigo_evento,
#             'NOMBRE_EVENTO': tipo_evento,
#             'DESCRIPCION_EVENTO': f"{tipo_evento} del curso {año_base}/{año_base+1}",# 
#             'FECHA_INICIO': ...,  # ELIMINADO: No existe en esquema# 
#             'FECHA_FIN': ...,  # ELIMINADO: No existe en esquema
#             'CURSO_ACADEMICO': f"{año_base}/{año_base+1}",
#             'ES_PERIODO_LECTIVO': es_lectivo,
#             'ES_PERIODO_EVALUACION': 1 if 'exámenes' in tipo_evento.lower() else 0,
#             'ES_PERIODO_MATRICULA': 1 if 'matrícula' in tipo_evento.lower() else 0,
#             'FECHA_CARGA': generate_random_date(año_base + 1, 2023)
#         })
    
#     return pd.DataFrame(data)

# def generate_d_dedicacion_alumno(n=5):  # COMENTADO: Tabla no existe en esquema
#     """Esta función se elimina porque la tabla D_DEDICACION_ALUMNO no existe en el esquema"""
#     raise NotImplementedError(
#         "Tabla D_DEDICACION_ALUMNO no existe en el esquema SQL. "
#         "Esta tabla fue eliminada durante la corrección de la estructura. "
#         "Use D_DEDICACION en su lugar. "
#         "Verifique el esquema dm_academico.sql para ver las tablas disponibles."
#     )

def generate_d_detalle_cupo_general(n=10):
    """Genera datos para la tabla D_DETALLE_CUPO_GENERAL"""
    data = []
    
    for i in range(1, n+1):
        codigo = f"DC{i:02d}"
        nombre = f"Detalle cupo general {i}"
        
        data.append({
            'ID_DETALLE_CUPO_GENERAL': i,
            'ID_DETALLE_CUPO_GENERAL_NK': codigo,
            'NOMBRE_DETALLE_CUPO_GENERAL': nombre
        })
    
    return pd.DataFrame(data)

def generate_d_clase_liquidacion(n=8, curso_academico_df=None):
    """Genera datos para la tabla D_CLASE_LIQUIDACION"""
    data = []
    
    # Si no se proporciona el DataFrame de cursos académicos, crear uno temporal
    if curso_academico_df is None:
        curso_academico_df = generate_d_curso_academico(n=5)
    
    # Para cada curso académico, crear varias clases de liquidación
    for idx, curso in curso_academico_df.iterrows():
        for i in range(1, n+1):
            id_clase = (idx * 10) + i
            id_clase_nk = i
            nombre_clase = f"Liquidación tipo {i} - {curso['NOMBRE_CURSO_ACADEMICO']}"
            
            data.append({
                'ID_CLASE_LIQUIDACION': id_clase,
                'ID_CURSO_ACADEMICO_NK': curso['ID_CURSO_ACADEMICO_NK']  # TODO: Usar valores válidos de D_CURSO_COHORTE,
                'ID_CLASE_LIQUIDACION_NK': id_clase_nk,
                'NOMBRE_CLASE_LIQUIDACION': nombre_clase,
                'ID_CLASE_LIQUIDACION_DESCR': id_clase
            })
    
    return pd.DataFrame(data)

def generate_d_estudio_propio_tipo(n=6):
    """Genera datos para la tabla D_ESTUDIO_PROPIO_TIPO"""
    data = []
    
    tipos = [
        "Máster Propio",
        "Experto Universitario",
        "Diploma de Especialización",
        "Certificación de Extensión Universitaria",
        "Título Propio de Grado",
        "Formación Continua"
    ]
    
    for i in range(1, n+1):
        if i <= len(tipos):
            nombre = tipos[i-1]
        else:
            nombre = f"Tipo de Estudio Propio {i}"
        
        codigo = f"EP{i:02d}"
        
        data.append({
            'ID_ESTUDIO_PROPIO_TIPO': i,
            'ID_ESTUDIO_PROPIO_TIPO_NK': codigo,
            'NOMBRE_ESTUDIO_PROPIO_TIPO': nombre
        })
    
    return pd.DataFrame(data)

def generate_d_estudio_propio_modalidad(n=5):
    """Genera datos para la tabla D_ESTUDIO_PROPIO_MODALIDAD"""
    data = []
    
    modalidades = [
        "Presencial",
        "Semipresencial",
        "Online",
        "A distancia",
        "Híbrido"
    ]
    
    for i in range(1, n+1):
        if i <= len(modalidades):
            nombre = modalidades[i-1]
        else:
            nombre = f"Modalidad {i}"
        
        codigo = f"MOD{i:02d}"
        
        data.append({
            'ID_ESTUDIO_PROPIO_MODALIDAD': i,
            'ID_ESTUDIO_PROPIO_MODALIDAD_NK': codigo,
            'NOMBRE_ESTUDIO_PROPIO_MODALID': nombre
        })
    
    return pd.DataFrame(data)

def generate_d_estudio_propio_organo_gest(n=8):
    """Genera datos para la tabla D_ESTUDIO_PROPIO_ORGANO_GEST"""
    data = []
    
    for i in range(1, n+1):
        nombre = f"Órgano de Gestión {fake.company()}"
        codigo = f"OG{i:03d}"
        
        data.append({
            'ID_ORGANO_GESTION_EP': i,
            'ID_ORGANO_GESTION_EP_NK': codigo,
            'NOMBRE_ORGANO_GESTION_EP': nombre,
            'ORD_NOMBRE_ORGANO_GESTION_EP': nombre.upper(),
            'ID_ORGANO_GESTION_EP_DESCR': i
        })
    
    return pd.DataFrame(data)

def generate_d_doctorado_tipo_beca(n=7, curso_academico_df=None):
    """Genera datos para la tabla D_DOCTORADO_TIPO_BECA
    
    Args:
        n (int): Número de tipos de beca por curso académico
        curso_academico_df (DataFrame): DataFrame con los cursos académicos
    
    Returns:
        DataFrame: DataFrame con los datos generados
    """
    data = []
    
    # Si no se proporciona el DataFrame de cursos académicos, crear uno temporal
    if curso_academico_df is None:
        curso_academico_df = generate_d_curso_academico(n=3)
    
    tipos_beca = [
        {"codigo": "FP", "nombre": "Beca FPU Ministerio", "descripcion": "Formación Profesorado Universitario"},
        {"codigo": "FI", "nombre": "Beca FPI Ministerio", "descripcion": "Formación Personal Investigador"},
        {"codigo": "PD", "nombre": "Beca PREDOC Universidad", "descripcion": "Predoctoral Universidad"},
        {"codigo": "MC", "nombre": "Beca MINECO", "descripcion": "Ministerio de Economía y Competitividad"},
        {"codigo": "AU", "nombre": "Beca AUTONÓMICA", "descripcion": "Gobierno Autonómico"},
        {"codigo": "PR", "nombre": "Beca PROPIA Universidad", "descripcion": "Financiación propia universidad"},
        {"codigo": "IN", "nombre": "Beca INTERNACIONAL", "descripcion": "Programas internacionales"}
    ]
    
    # Ampliar la lista si necesitamos más tipos
    while len(tipos_beca) < n:
        nuevo_id = len(tipos_beca) + 1
        tipos_beca.append({
            "codigo": f"TB{nuevo_id}",
            "nombre": f"Tipo de Beca {nuevo_id}",
            "descripcion": f"Otras becas tipo {nuevo_id}"
        })
    
    # Para cada curso académico, crear varios tipos de beca
    for idx, curso in curso_academico_df.iterrows():
        for i in range(n):
            if i < len(tipos_beca):
                tipo_beca = tipos_beca[i]
                id_tipo_beca = (idx * 10) + i + 1
                
                data.append({
                    'ID_TIPO_BECA': id_tipo_beca,
                    'ID_CURSO_ACADEMICO_NK': curso['ID_CURSO_ACADEMICO_NK']  # TODO: Usar valores válidos de D_CURSO_COHORTE,
                    'ID_TIPO_BECA_NK': tipo_beca["codigo"],
                    'ID_TIPO_BECA_DESCR': id_tipo_beca,
                    'NOMBRE_TIPO_BECA': tipo_beca["nombre"]
                })
    
    return pd.DataFrame(data)