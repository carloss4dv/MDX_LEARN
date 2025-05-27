import os
import pandas as pd
from generators.dimension_generators import (
    generate_d_sexo,
    generate_d_pais,
    generate_d_tiempo,
    generate_d_curso_academico,
    generate_d_curso_cohorte,
    generate_d_tipo_estudio,
    generate_d_rama_conocimiento,
    generate_d_calificacion,
    generate_d_convocatoria,
    generate_d_tipo_acceso,
    generate_d_clase_asignatura,
    generate_d_persona,
    generate_d_poblacion,
    generate_d_asignatura,
    generate_d_plan_estudio,
    generate_d_tipo_acceso_preinscripcion,
    generate_d_tipo_docencia,
    generate_d_tipo_egreso,
    generate_d_tipo_abandono,
    generate_d_tipo_procedimiento,
    generate_d_tipo_reconocimiento,
    generate_d_cupo_adjudicacion,
    generate_d_rango_credito,
    generate_d_rango_edad,
    generate_d_rango_nota_admision,
    generate_d_rango_nota_numerica,
    generate_d_rango_nota_crue,
    generate_d_rango_nota_egracons,
    generate_d_estudio_previo,
    generate_d_nacionalidad,
    generate_d_dedicacion_alumno,
    generate_d_categoria_cuerpo_pdi,
    generate_d_tipo_asignatura,
    generate_d_tipo_centro,
    generate_d_modalidad_plan_estudio,
    generate_d_campus,
    generate_d_articulo,
    generate_d_edad_est,
    generate_d_dedicacion,
    generate_d_dedicacion_profesor,
    generate_d_estado_adjudicacion,
    generate_d_poblacion_centro,
    generate_d_centro,
    generate_d_universidad,
    generate_d_idioma_movilidad,
    generate_d_nivel_estudios_movilidad,
    generate_d_area_estudios_movilidad,
    generate_d_colectivo_movilidad,
    generate_d_estado_acuerdo_bilateral,
    generate_d_centro_destino,
    generate_d_centro_otra_universidad,
    generate_d_centro_estudio,
    generate_d_estudio,
    generate_d_estudio_jerarq,
    generate_d_estudio_destino,
    generate_d_estudio_otra_universidad,
    generate_d_plan_estudio_asignatura,
    generate_d_programa_movilidad,
    generate_d_idioma_nivel_movilidad,
    generate_d_titulacion,
    generate_d_acuerdo_bilateral,
    generate_d_proyecto_investigacion,
    generate_d_rama_macroarea,
    generate_d_detalle_cupo_general,
    generate_d_clase_liquidacion,
    generate_d_estudio_propio_tipo,
    generate_d_estudio_propio_modalidad,
    generate_d_estudio_propio_organo_gest,
    generate_d_doctorado_tipo_beca,
    generate_d_estado_solicitud_doctorado,
    generate_d_grupo,
    generate_d_plan_estudio_ano_datos,
    generate_d_estudio_propio,
    generate_d_rango_credito_movilidad,
    generate_d_convocatoria_preinscripcion,
    generate_d_estado_credencial_acceso,
    generate_d_territorio,
    generate_d_nivel_idioma,
    generate_d_situacion_administrativa,
    generate_d_tipo_contrato,
    generate_d_modalidad_asignatura,
    generate_d_periodo_lectivo,
    generate_d_area_conocimiento
)
from generators.fact_generators import (
    generate_f_matricula,
    generate_f_rendimiento
)
# Importar las nuevas funciones extendidas
from generators.fact_generators_extended import (
    extended_generate_f_matricula,
    extended_generate_f_rendimiento
)
# Importar las nuevas funciones de tablas de hechos prioritarias
from generators.fact_generators_priority import (
    generate_f_oferta_admision,
    generate_f_solicitante_admision,
    generate_f_egresado,
    generate_f_cohorte
)
# Importar las nuevas funciones de tablas de hechos de movilidad
from generators.fact_generators_mobility import (
    generate_f_estudiantes_movilidad_in,
    generate_f_estudiantes_movilidad_out,
    generate_f_solicitudes_movilidad
)
# Importar las nuevas funciones de tablas de hechos de doctorado
from generators.fact_generators_doctorado import (
    generate_f_doctorado_admision,
    generate_f_egracons,
    generate_f_estudio_propio_matricula,
    generate_f_doctorado
)
# Importar las nuevas funciones de tablas de hechos de acuerdos
from generators.fact_generators_acuerdos import (
    generate_f_oferta_acuerdo_bilateral
)
# Importar las nuevas funciones de tablas de fusión
from generators.fact_generators_fusion import (
    generate_f_tabla_fusion,
    generate_f_tabla_fusion_estcen
)

def create_output_dir():
    """Crea el directorio de salida si no existe"""
    os.makedirs('output', exist_ok=True)
    os.makedirs('output/dimensions', exist_ok=True)
    os.makedirs('output/facts', exist_ok=True)

def save_dataframe(df, filename, folder='dimensions'):
    """Guarda un DataFrame en un archivo CSV"""
    path = f'output/{folder}/{filename}.csv'
    df.to_csv(path, index=False)
    print(f"Archivo guardado: {path}")

def main():
    """Función principal que genera y guarda los datos"""
    print("Generando datos para el Data Mart Académico...")
    create_output_dir()
    
    # Generar dimensiones
    print("\nGenerando tablas de dimensión...")
    
    # Dimensiones básicas (sin dependencias)
    d_sexo = generate_d_sexo()
    save_dataframe(d_sexo, 'd_sexo')
    
    # Generar paises con tamaño de NOMBRE_NACIONALIDAD limitado a 45 caracteres
    d_pais = generate_d_pais()
    save_dataframe(d_pais, 'd_pais')
    
    d_tiempo = generate_d_tiempo()
    save_dataframe(d_tiempo, 'd_tiempo')
    
    d_curso_academico = generate_d_curso_academico()
    save_dataframe(d_curso_academico, 'd_curso_academico')
    
    d_curso_cohorte = generate_d_curso_cohorte(d_curso_academico)
    save_dataframe(d_curso_cohorte, 'd_curso_cohorte')
    
    d_tipo_estudio = generate_d_tipo_estudio()
    save_dataframe(d_tipo_estudio, 'd_tipo_estudio')
    
    d_rama_conocimiento = generate_d_rama_conocimiento()
    save_dataframe(d_rama_conocimiento, 'd_rama_conocimiento')
    
    d_calificacion = generate_d_calificacion()
    save_dataframe(d_calificacion, 'd_calificacion')
    
    d_convocatoria = generate_d_convocatoria()
    save_dataframe(d_convocatoria, 'd_convocatoria')
    
    d_tipo_acceso = generate_d_tipo_acceso()
    save_dataframe(d_tipo_acceso, 'd_tipo_acceso')
    
    d_tipo_acceso_preinscripcion = generate_d_tipo_acceso_preinscripcion()
    save_dataframe(d_tipo_acceso_preinscripcion, 'd_tipo_acceso_preinscripcion')
    
    d_clase_asignatura = generate_d_clase_asignatura()
    save_dataframe(d_clase_asignatura, 'd_clase_asignatura')
    
    # Nuevas dimensiones básicas
    d_tipo_docencia = generate_d_tipo_docencia()
    save_dataframe(d_tipo_docencia, 'd_tipo_docencia')
    
    d_tipo_egreso = generate_d_tipo_egreso()
    save_dataframe(d_tipo_egreso, 'd_tipo_egreso')
    
    d_tipo_abandono = generate_d_tipo_abandono()
    save_dataframe(d_tipo_abandono, 'd_tipo_abandono')
    
    d_tipo_procedimiento = generate_d_tipo_procedimiento()
    save_dataframe(d_tipo_procedimiento, 'd_tipo_procedimiento')
    
    d_tipo_reconocimiento = generate_d_tipo_reconocimiento()
    save_dataframe(d_tipo_reconocimiento, 'd_tipo_reconocimiento')
    
    d_cupo_adjudicacion = generate_d_cupo_adjudicacion()
    save_dataframe(d_cupo_adjudicacion, 'd_cupo_adjudicacion')
    
    d_rango_credito = generate_d_rango_credito()
    save_dataframe(d_rango_credito, 'd_rango_credito')
    
    d_rango_edad = generate_d_rango_edad()
    save_dataframe(d_rango_edad, 'd_rango_edad')
    
    d_rango_nota_admision = generate_d_rango_nota_admision()
    save_dataframe(d_rango_nota_admision, 'd_rango_nota_admision')
    
    d_rango_nota_numerica = generate_d_rango_nota_numerica()
    save_dataframe(d_rango_nota_numerica, 'd_rango_nota_numerica')
    
    d_rango_nota_crue = generate_d_rango_nota_crue()
    save_dataframe(d_rango_nota_crue, 'd_rango_nota_crue')
    
    # Generar rango_nota_egracons con nombres limitados a 20 caracteres
    d_rango_nota_egracons = generate_d_rango_nota_egracons()
    save_dataframe(d_rango_nota_egracons, 'd_rango_nota_egracons')
    
    d_estudio_previo = generate_d_estudio_previo()
    save_dataframe(d_estudio_previo, 'd_estudio_previo')
    
    d_campus = generate_d_campus()
    save_dataframe(d_campus, 'd_campus')
    
    d_articulo = generate_d_articulo()
    save_dataframe(d_articulo, 'd_articulo')
    
    # Generar edad_est con nombres limitados a 10 caracteres para F_SOLICITANTE_ADMISION
    d_edad_est = generate_d_edad_est()
    save_dataframe(d_edad_est, 'd_edad_est')
    
    d_dedicacion = generate_d_dedicacion()
    save_dataframe(d_dedicacion, 'd_dedicacion')
    
    d_dedicacion_profesor = generate_d_dedicacion_profesor()
    save_dataframe(d_dedicacion_profesor, 'd_dedicacion_profesor')
    
    d_dedicacion_alumno = generate_d_dedicacion_alumno()
    save_dataframe(d_dedicacion_alumno, 'd_dedicacion_alumno')
    
    d_categoria_cuerpo_pdi = generate_d_categoria_cuerpo_pdi()
    save_dataframe(d_categoria_cuerpo_pdi, 'd_categoria_cuerpo_pdi')
    
    d_tipo_asignatura = generate_d_tipo_asignatura()
    save_dataframe(d_tipo_asignatura, 'd_tipo_asignatura')
    
    d_tipo_centro = generate_d_tipo_centro()
    save_dataframe(d_tipo_centro, 'd_tipo_centro')
    
    d_modalidad_plan_estudio = generate_d_modalidad_plan_estudio()
    save_dataframe(d_modalidad_plan_estudio, 'd_modalidad_plan_estudio')
    
    d_estado_adjudicacion = generate_d_estado_adjudicacion()
    save_dataframe(d_estado_adjudicacion, 'd_estado_adjudicacion')
    
    d_idioma_movilidad = generate_d_idioma_movilidad()
    save_dataframe(d_idioma_movilidad, 'd_idioma_movilidad')
    
    d_nivel_estudios_movilidad = generate_d_nivel_estudios_movilidad()
    save_dataframe(d_nivel_estudios_movilidad, 'd_nivel_estudios_movilidad')
    
    d_area_estudios_movilidad = generate_d_area_estudios_movilidad()
    save_dataframe(d_area_estudios_movilidad, 'd_area_estudios_movilidad')
    
    d_colectivo_movilidad = generate_d_colectivo_movilidad()
    save_dataframe(d_colectivo_movilidad, 'd_colectivo_movilidad')
    
    d_estado_acuerdo_bilateral = generate_d_estado_acuerdo_bilateral()
    save_dataframe(d_estado_acuerdo_bilateral, 'd_estado_acuerdo_bilateral')
    
    # Nuevas dimensiones básicas (completando TODOs)
    d_acuerdo_bilateral = generate_d_acuerdo_bilateral()
    save_dataframe(d_acuerdo_bilateral, 'd_acuerdo_bilateral')
    
    d_proyecto_investigacion = generate_d_proyecto_investigacion()
    save_dataframe(d_proyecto_investigacion, 'd_proyecto_investigacion')
    
    d_rama_macroarea = generate_d_rama_macroarea()
    save_dataframe(d_rama_macroarea, 'd_rama_macroarea')
    
    d_detalle_cupo_general = generate_d_detalle_cupo_general()
    save_dataframe(d_detalle_cupo_general, 'd_detalle_cupo_general')
    
    d_clase_liquidacion = generate_d_clase_liquidacion(curso_academico_df=d_curso_academico)
    save_dataframe(d_clase_liquidacion, 'd_clase_liquidacion')
    
    d_estudio_propio_tipo = generate_d_estudio_propio_tipo()
    save_dataframe(d_estudio_propio_tipo, 'd_estudio_propio_tipo')
    
    d_estudio_propio_modalidad = generate_d_estudio_propio_modalidad()
    save_dataframe(d_estudio_propio_modalidad, 'd_estudio_propio_modalidad')
    
    d_estudio_propio_organo_gest = generate_d_estudio_propio_organo_gest()
    save_dataframe(d_estudio_propio_organo_gest, 'd_estudio_propio_organo_gest')
    
    d_doctorado_tipo_beca = generate_d_doctorado_tipo_beca(curso_academico_df=d_curso_academico)
    save_dataframe(d_doctorado_tipo_beca, 'd_doctorado_tipo_beca')
    
    d_estado_solicitud_doctorado = generate_d_estado_solicitud_doctorado()
    save_dataframe(d_estado_solicitud_doctorado, 'd_estado_solicitud_doctorado')
    
    # Nuevas dimensiones básicas (2023)
    d_estado_credencial_acceso = generate_d_estado_credencial_acceso()
    save_dataframe(d_estado_credencial_acceso, 'd_estado_credencial_acceso')
    
    # Generar las tablas que faltaban según las trazas
    d_nivel_idioma = generate_d_nivel_idioma()
    save_dataframe(d_nivel_idioma, 'd_nivel_idioma')
    
    d_situacion_administrativa = generate_d_situacion_administrativa()
    save_dataframe(d_situacion_administrativa, 'd_situacion_administrativa')
    
    d_tipo_contrato = generate_d_tipo_contrato()
    save_dataframe(d_tipo_contrato, 'd_tipo_contrato')
    
    # Nuevas dimensiones implementadas (2024)
    d_modalidad_asignatura = generate_d_modalidad_asignatura()
    save_dataframe(d_modalidad_asignatura, 'd_modalidad_asignatura')
    
    d_periodo_lectivo = generate_d_periodo_lectivo()
    save_dataframe(d_periodo_lectivo, 'd_periodo_lectivo')
    
    d_area_conocimiento = generate_d_area_conocimiento()
    save_dataframe(d_area_conocimiento, 'd_area_conocimiento')
    
    # Dimensiones con dependencias
    d_poblacion = generate_d_poblacion(n=500, paises_df=d_pais)
    save_dataframe(d_poblacion, 'd_poblacion')
    
    d_nacionalidad = generate_d_nacionalidad(n=50, paises_df=d_pais)
    save_dataframe(d_nacionalidad, 'd_nacionalidad')
    
    d_poblacion_centro = generate_d_poblacion_centro(poblacion_df=d_poblacion)
    save_dataframe(d_poblacion_centro, 'd_poblacion_centro')
    
    d_centro = generate_d_centro(n=50, campus_df=d_campus, tipo_centro_df=d_tipo_centro, poblacion_df=d_poblacion)
    save_dataframe(d_centro, 'd_centro')
    
    d_universidad = generate_d_universidad(n=100, paises_df=d_pais)
    save_dataframe(d_universidad, 'd_universidad')
    
    d_centro_destino = generate_d_centro_destino(n=50, universidad_df=d_universidad)
    save_dataframe(d_centro_destino, 'd_centro_destino')
    
    d_centro_otra_universidad = generate_d_centro_otra_universidad(centro_destino_df=d_centro_destino)
    save_dataframe(d_centro_otra_universidad, 'd_centro_otra_universidad')
    
    d_persona = generate_d_persona(n=100, paises_df=d_pais)
    save_dataframe(d_persona, 'd_persona')
    
    d_asignatura = generate_d_asignatura(n=500)
    save_dataframe(d_asignatura, 'd_asignatura')
    
    d_plan_estudio = generate_d_plan_estudio(n=100)
    save_dataframe(d_plan_estudio, 'd_plan_estudio')
    
    d_estudio = generate_d_estudio(n=50)
    save_dataframe(d_estudio, 'd_estudio')
    
    d_centro_estudio = generate_d_centro_estudio(n=100, universidad_df=d_universidad, centro_df=d_centro, plan_estudio_df=d_plan_estudio)
    save_dataframe(d_centro_estudio, 'd_centro_estudio')
    
    d_estudio_jerarq = generate_d_estudio_jerarq(n=100, plan_estudio_df=d_plan_estudio, estudio_df=d_estudio, tipo_estudio_df=d_tipo_estudio, rama_conocimiento_df=d_rama_conocimiento)
    save_dataframe(d_estudio_jerarq, 'd_estudio_jerarq')
    
    d_estudio_destino = generate_d_estudio_destino(n=50)
    save_dataframe(d_estudio_destino, 'd_estudio_destino')
    
    d_estudio_otra_universidad = generate_d_estudio_otra_universidad(estudio_destino_df=d_estudio_destino)
    save_dataframe(d_estudio_otra_universidad, 'd_estudio_otra_universidad')
    
    d_plan_estudio_asignatura = generate_d_plan_estudio_asignatura(n=1000, asignatura_df=d_asignatura, plan_estudio_df=d_plan_estudio, clase_asignatura_df=d_clase_asignatura)
    save_dataframe(d_plan_estudio_asignatura, 'd_plan_estudio_asignatura')
    
    d_programa_movilidad = generate_d_programa_movilidad(n=10)
    save_dataframe(d_programa_movilidad, 'd_programa_movilidad')
    
    d_idioma_nivel_movilidad = generate_d_idioma_nivel_movilidad(n=20, idioma_movilidad_df=d_idioma_movilidad)
    save_dataframe(d_idioma_nivel_movilidad, 'd_idioma_nivel_movilidad')
    
    d_titulacion = generate_d_titulacion(n=50)
    save_dataframe(d_titulacion, 'd_titulacion')
    
    # Nuevas dimensiones con dependencias (completando TODOs)
    d_grupo = generate_d_grupo(n=20, curso_academico_df=d_curso_academico, centro_df=d_centro, asignatura_df=d_asignatura)
    save_dataframe(d_grupo, 'd_grupo')
    
    d_plan_estudio_ano_datos = generate_d_plan_estudio_ano_datos(n=50, curso_academico_df=d_curso_academico, plan_estudio_df=d_plan_estudio, tipo_estudio_df=d_tipo_estudio, modalidad_plan_df=d_modalidad_plan_estudio)
    save_dataframe(d_plan_estudio_ano_datos, 'd_plan_estudio_ano_datos')
    
    d_estudio_propio = generate_d_estudio_propio(n=30)
    save_dataframe(d_estudio_propio, 'd_estudio_propio')
    
    d_rango_credito_movilidad = generate_d_rango_credito_movilidad(n=7, rango_credito_df=d_rango_credito)
    save_dataframe(d_rango_credito_movilidad, 'd_rango_credito_movilidad')
    
    d_convocatoria_preinscripcion = generate_d_convocatoria_preinscripcion(n=5, convocatoria_df=d_convocatoria)
    save_dataframe(d_convocatoria_preinscripcion, 'd_convocatoria_preinscripcion')
    
    d_territorio = generate_d_territorio(n=100, paises_df=d_pais)
    save_dataframe(d_territorio, 'd_territorio')
    
    # Generar tablas de hechos
    print("\nGenerando tablas de hechos...")
    
    # Crear diccionario con todas las dimensiones generadas
    dimension_dfs = {
        'd_sexo': d_sexo,
        'd_pais': d_pais,
        'd_tiempo': d_tiempo,
        'd_curso_academico': d_curso_academico,
        'd_curso_cohorte': d_curso_cohorte,
        'd_tipo_estudio': d_tipo_estudio,
        'd_rama_conocimiento': d_rama_conocimiento,
        'd_calificacion': d_calificacion,
        'd_convocatoria': d_convocatoria,
        'd_tipo_acceso': d_tipo_acceso,
        'd_tipo_acceso_preinscripcion': d_tipo_acceso_preinscripcion,
        'd_clase_asignatura': d_clase_asignatura,
        'd_persona': d_persona,
        'd_poblacion': d_poblacion,
        'd_asignatura': d_asignatura,
        'd_plan_estudio': d_plan_estudio,
        'd_tipo_docencia': d_tipo_docencia,
        'd_tipo_egreso': d_tipo_egreso,
        'd_tipo_abandono': d_tipo_abandono,
        'd_tipo_procedimiento': d_tipo_procedimiento,
        'd_tipo_reconocimiento': d_tipo_reconocimiento,
        'd_cupo_adjudicacion': d_cupo_adjudicacion,
        'd_rango_credito': d_rango_credito,
        'd_rango_edad': d_rango_edad,
        'd_rango_nota_admision': d_rango_nota_admision,
        'd_rango_nota_numerica': d_rango_nota_numerica,
        'd_rango_nota_crue': d_rango_nota_crue,
        'd_rango_nota_egracons': d_rango_nota_egracons,
        'd_estudio_previo': d_estudio_previo,
        'd_campus': d_campus,
        'd_articulo': d_articulo,
        'd_edad_est': d_edad_est,
        'd_dedicacion': d_dedicacion,
        'd_dedicacion_profesor': d_dedicacion_profesor,
        'd_dedicacion_alumno': d_dedicacion_alumno,
        'd_categoria_cuerpo_pdi': d_categoria_cuerpo_pdi,
        'd_tipo_asignatura': d_tipo_asignatura,
        'd_tipo_centro': d_tipo_centro,
        'd_modalidad_plan_estudio': d_modalidad_plan_estudio,
        'd_estado_adjudicacion': d_estado_adjudicacion,
        'd_poblacion_centro': d_poblacion_centro,
        'd_centro': d_centro,
        'd_universidad': d_universidad,
        'd_centro_destino': d_centro_destino,
        'd_centro_otra_universidad': d_centro_otra_universidad,
        'd_centro_estudio': d_centro_estudio,
        'd_estudio': d_estudio,
        'd_estudio_jerarq': d_estudio_jerarq,
        'd_estudio_destino': d_estudio_destino,
        'd_estudio_otra_universidad': d_estudio_otra_universidad,
        'd_plan_estudio_asignatura': d_plan_estudio_asignatura,
        'd_programa_movilidad': d_programa_movilidad,
        'd_area_estudios_movilidad': d_area_estudios_movilidad,
        'd_nivel_estudios_movilidad': d_nivel_estudios_movilidad,
        'd_idioma_movilidad': d_idioma_movilidad,
        'd_colectivo_movilidad': d_colectivo_movilidad,
        'd_idioma_nivel_movilidad': d_idioma_nivel_movilidad,
        'd_titulacion': d_titulacion,
        'd_nacionalidad': d_nacionalidad,
        'd_acuerdo_bilateral': d_acuerdo_bilateral,
        'd_proyecto_investigacion': d_proyecto_investigacion,
        'd_rama_macroarea': d_rama_macroarea,
        'd_detalle_cupo_general': d_detalle_cupo_general,
        'd_clase_liquidacion': d_clase_liquidacion,
        'd_estudio_propio_tipo': d_estudio_propio_tipo,
        'd_estudio_propio_modalidad': d_estudio_propio_modalidad,
        'd_estudio_propio_organo_gest': d_estudio_propio_organo_gest,
        'd_doctorado_tipo_beca': d_doctorado_tipo_beca,
        'd_estado_solicitud_doctorado': d_estado_solicitud_doctorado,
        'd_grupo': d_grupo,
        'd_plan_estudio_ano_datos': d_plan_estudio_ano_datos,
        'd_estudio_propio': d_estudio_propio,
        'd_rango_credito_movilidad': d_rango_credito_movilidad,
        'd_convocatoria_preinscripcion': d_convocatoria_preinscripcion,
        'd_estado_credencial_acceso': d_estado_credencial_acceso,
        'd_nivel_idioma': d_nivel_idioma,
        'd_situacion_administrativa': d_situacion_administrativa,
        'd_tipo_contrato': d_tipo_contrato,
        'd_territorio': d_territorio,
        'd_modalidad_asignatura': d_modalidad_asignatura,
        'd_periodo_lectivo': d_periodo_lectivo,
        'd_area_conocimiento': d_area_conocimiento
    }
    
    # Generar F_MATRICULA con un número reducido para pruebas
    print("\nGenerando tabla F_MATRICULA completa con todos los campos...")
    f_matricula = extended_generate_f_matricula(n=500, dimension_dfs=dimension_dfs)
    save_dataframe(f_matricula, 'f_matricula', folder='facts')
    
    # Generar F_RENDIMIENTO con un número reducido para pruebas
    print("\nGenerando tabla F_RENDIMIENTO completa con todos los campos...")
    f_rendimiento = extended_generate_f_rendimiento(n=1000, dimension_dfs=dimension_dfs)
    save_dataframe(f_rendimiento, 'f_rendimiento', folder='facts')
    
    # Generar tablas de hechos prioritarias adicionales
    
    # Generar F_OFERTA_ADMISION
    print("\nGenerando tabla F_OFERTA_ADMISION con todos los campos...")
    f_oferta_admision = generate_f_oferta_admision(n=250, dimension_dfs=dimension_dfs)
    save_dataframe(f_oferta_admision, 'f_oferta_admision', folder='facts')
    
    # Generar F_SOLICITANTE_ADMISION
    print("\nGenerando tabla F_SOLICITANTE_ADMISION con todos los campos...")
    f_solicitante_admision = generate_f_solicitante_admision(n=500, dimension_dfs=dimension_dfs)
    save_dataframe(f_solicitante_admision, 'f_solicitante_admision', folder='facts')
    
    # Generar F_EGRESADO
    print("\nGenerando tabla F_EGRESADO con todos los campos...")
    f_egresado = generate_f_egresado(n=300, dimension_dfs=dimension_dfs)
    save_dataframe(f_egresado, 'f_egresado', folder='facts')
    
    # Generar F_COHORTE
    print("\nGenerando tabla F_COHORTE con todos los campos...")
    f_cohorte = generate_f_cohorte(n=300, dimension_dfs=dimension_dfs)
    save_dataframe(f_cohorte, 'f_cohorte', folder='facts')
    
    # Generar tablas de hechos relacionadas con movilidad
    
    # Generar F_ESTUDIANTES_MOVILIDAD_IN
    print("\nGenerando tabla F_ESTUDIANTES_MOVILIDAD_IN con todos los campos...")
    f_estudiantes_movilidad_in = generate_f_estudiantes_movilidad_in(n=200, dimension_dfs=dimension_dfs)
    save_dataframe(f_estudiantes_movilidad_in, 'f_estudiantes_movilidad_in', folder='facts')
    
    # Generar F_ESTUDIANTES_MOVILIDAD_OUT
    print("\nGenerando tabla F_ESTUDIANTES_MOVILIDAD_OUT con todos los campos...")
    f_estudiantes_movilidad_out = generate_f_estudiantes_movilidad_out(n=300, dimension_dfs=dimension_dfs)
    save_dataframe(f_estudiantes_movilidad_out, 'f_estudiantes_movilidad_out', folder='facts')
    
    # Generar F_SOLICITUDES_MOVILIDAD
    print("\nGenerando tabla F_SOLICITUDES_MOVILIDAD con todos los campos...")
    f_solicitudes_movilidad = generate_f_solicitudes_movilidad(n=400, dimension_dfs=dimension_dfs)
    save_dataframe(f_solicitudes_movilidad, 'f_solicitudes_movilidad', folder='facts')
    
    # Generar tablas de hechos de doctorado y estudios propios
    
    # Generar F_DOCTORADO_ADMISION
    print("\nGenerando tabla F_DOCTORADO_ADMISION con todos los campos...")
    f_doctorado_admision = generate_f_doctorado_admision(n=200, dimension_dfs=dimension_dfs)
    save_dataframe(f_doctorado_admision, 'f_doctorado_admision', folder='facts')
    
    # Generar F_EGRACONS
    print("\nGenerando tabla F_EGRACONS con todos los campos...")
    f_egracons = generate_f_egracons(n=300, dimension_dfs=dimension_dfs)
    save_dataframe(f_egracons, 'f_egracons', folder='facts')
    
    # Generar F_ESTUDIO_PROPIO_MATRICULA
    print("\nGenerando tabla F_ESTUDIO_PROPIO_MATRICULA con todos los campos...")
    f_estudio_propio_matricula = generate_f_estudio_propio_matricula(n=300, dimension_dfs=dimension_dfs)
    save_dataframe(f_estudio_propio_matricula, 'f_estudio_propio_matricula', folder='facts')
    
    # Generar F_OFERTA_ACUERDO_BILATERAL
    print("\nGenerando tabla F_OFERTA_ACUERDO_BILATERAL con todos los campos...")
    f_oferta_acuerdo_bilateral = generate_f_oferta_acuerdo_bilateral(n=200, dimension_dfs=dimension_dfs)
    save_dataframe(f_oferta_acuerdo_bilateral, 'f_oferta_acuerdo_bilateral', folder='facts')
    
    # Generar F_DOCTORADO
    print("\nGenerando tabla F_DOCTORADO con todos los campos...")
    f_doctorado = generate_f_doctorado(n=200, dimension_dfs=dimension_dfs)
    save_dataframe(f_doctorado, 'f_doctorado', folder='facts')
    
    # Generar tablas de hechos agregadas
    
    # Generar F_TABLA_FUSION
    print("\nGenerando tabla F_TABLA_FUSION con todos los campos...")
    f_tabla_fusion = generate_f_tabla_fusion(n=150, dimension_dfs=dimension_dfs)
    save_dataframe(f_tabla_fusion, 'f_tabla_fusion', folder='facts')
    
    # Generar F_TABLA_FUSION_ESTCEN
    print("\nGenerando tabla F_TABLA_FUSION_ESTCEN con todos los campos...")
    f_tabla_fusion_estcen = generate_f_tabla_fusion_estcen(n=200, dimension_dfs=dimension_dfs)
    save_dataframe(f_tabla_fusion_estcen, 'f_tabla_fusion_estcen', folder='facts')
    
    print("\n¡Generación de datos completada!")

if __name__ == "__main__":
    main() 

# Progreso de implementación:
# 
# RESUMEN DE IMPLEMENTACIÓN: 
# - Tablas de dimensión implementadas: 70/70 (100%) 
# - Tablas de hechos implementadas: 16/16 (100%) - Todas las tablas completadas con todos los atributos 
# 
# TABLAS DE DIMENSIÓN IMPLEMENTADAS (70):
# - D_ACUERDO_BILATERAL (4 atributos)
# - D_AREA_ESTUDIOS_MOVILIDAD (3 atributos)
# - D_ARTICULO (2 atributos)
# - D_ASIGNATURA (3 atributos)
# - D_CALIFICACION (4 atributos)
# - D_CAMPUS (2 atributos)
# - D_CATEGORIA_CUERPO_PDI (3 atributos)
# - D_CENTRO (12 atributos)
# - D_CENTRO_DESTINO (6 atributos)
# - D_CENTRO_ESTUDIO (9 atributos)
# - D_CENTRO_OTRA_UNIVERSIDAD (6 atributos)
# - D_CLASE_ASIGNATURA (4 atributos)
# - D_CLASE_LIQUIDACION (5 atributos)
# - D_COLECTIVO_MOVILIDAD (3 atributos)
# - D_CONVOCATORIA (3 atributos)
# - D_CONVOCATORIA_PREINSCRIPCION (3 atributos)
# - D_CUPO_ADJUDICACION (4 atributos)
# - D_CURSO_ACADEMICO (3 atributos)
# - D_CURSO_COHORTE (3 atributos)
# - D_DEDICACION (3 atributos)
# - D_DEDICACION_PROFESOR (3 atributos)
# - D_DETALLE_CUPO_GENERAL (3 atributos)
# - D_DOCTORADO_TIPO_BECA (5 atributos)
# - D_EDAD_EST (3 atributos)
# - D_ESTADO_ACUERDO_BILATERAL (3 atributos)
# - D_ESTADO_ADJUDICACION (3 atributos)
# - D_ESTADO_SOLICITUD_DOCTORADO (3 atributos)
# - D_ESTUDIO (4 atributos)
# - D_ESTUDIO_DESTINO (4 atributos)
# - D_ESTUDIO_JERARQ (20 atributos)
# - D_ESTUDIO_OTRA_UNIVERSIDAD (4 atributos)
# - D_ESTUDIO_PREVIO (4 atributos)
# - D_ESTUDIO_PROPIO (6 atributos)
# - D_ESTUDIO_PROPIO_MODALIDAD (3 atributos)
# - D_ESTUDIO_PROPIO_ORGANO_GEST (5 atributos)
# - D_ESTUDIO_PROPIO_TIPO (3 atributos)
# - D_GRUPO (9 atributos)
# - D_IDIOMA_MOVILIDAD (3 atributos)
# - D_IDIOMA_NIVEL_MOVILIDAD (4 atributos)
# - D_MODALIDAD_PLAN_ESTUDIO (3 atributos)
# - D_NACIONALIDAD (3 atributos)
# - D_NIVEL_ESTUDIOS_MOVILIDAD (3 atributos)
# - D_PAIS (8 atributos)
# - D_PERSONA (13 atributos)
# - D_PLAN_ESTUDIO (4 atributos)
# - D_PLAN_ESTUDIO_ANO_DATOS (18 atributos)
# - D_PLAN_ESTUDIO_ASIGNATURA (10 atributos)
# - D_POBLACION (9 atributos)
# - D_POBLACION_CENTRO (2 atributos)
# - D_PROGRAMA_MOVILIDAD (7 atributos)
# - D_PROYECTO_INVESTIGACION (2 atributos)
# - D_RAMA_CONOCIMIENTO (1 atributo)
# - D_RAMA_MACROAREA (5 atributos)
# - D_RANGO_CREDITO (4 atributos)
# - D_RANGO_CREDITO_MOVILIDAD (3 atributos)
# - D_RANGO_EDAD (4 atributos)
# - D_RANGO_NOTA_ADMISION (4 atributos)
# - D_RANGO_NOTA_CRUE (4 atributos)
# - D_RANGO_NOTA_EGRACONS (4 atributos)
# - D_RANGO_NOTA_NUMERICA (4 atributos)
# - D_SEXO (4 atributos)
# - D_TIEMPO (8 atributos)
# - D_TIPO_ABANDONO (3 atributos)
# - D_TIPO_ACCESO (3 atributos)
# - D_TIPO_ACCESO_PREINSCRIPCION (3 atributos)
# - D_TIPO_ASIGNATURA (4 atributos)
# - D_TIPO_CENTRO (3 atributos)
# - D_TIPO_DOCENCIA (3 atributos)
# - D_TIPO_EGRESO (3 atributos)
# - D_TIPO_ESTUDIO (5 atributos)
# - D_TIPO_PROCEDIMIENTO (3 atributos)
# - D_TIPO_RECONOCIMIENTO (4 atributos)
# - D_TITULACION (5 atributos)
# - D_UNIVERSIDAD (11 atributos)
#
# TABLAS DE HECHOS IMPLEMENTADAS (16/16):
# - F_MATRICULA (86 atributos - IMPLEMENTADA COMPLETAMENTE):
#   * Incluye todos los atributos necesarios para seguimiento de matrículas
#   * Relacionada con múltiples dimensiones académicas, personales y demográficas
#   * Implementados todos los campos clave: ID_CURSO_ACADEMICO, ID_ALUMNO, ID_EXPEDIENTE_ACADEMICO,
#     ID_PLAN_ESTUDIO, ID_CENTRO, ID_ASIGNATURA, etc.
#
# - F_RENDIMIENTO (81 atributos - IMPLEMENTADA COMPLETAMENTE):
#   * Incluye todos los atributos necesarios para seguimiento de rendimiento académico
#   * Relacionada con múltiples dimensiones académicas, personales y de evaluación
#   * Implementados todos los campos clave: ID_CURSO_ACADEMICO, ID_EXPEDIENTE_ACADEMICO, ID_ASIGNATURA,
#     ID_CONVOCATORIA, ID_CALIFICACION, etc.
#
# - F_COHORTE (89 atributos - IMPLEMENTADA COMPLETAMENTE):
#   * Incluye indicadores de seguimiento de cohorte, como abandonos, graduación, tasas.
#   * Relacionada con dimensiones temporales, académicas y demográficas.
#   * Implementados todos los campos clave: ID_CURSO_ACADEMICO_COHORTE, ID_EXPEDIENTE_ACADEMICO, 
#     ID_PLAN_ESTUDIO, ID_CENTRO, ID_TIPO_ACCESO, ID_SEXO, ID_TIPO_ABANDONO, ID_ESTUDIO_PREVIO, etc.
#
# - F_EGRESADO (89 atributos - IMPLEMENTADA COMPLETAMENTE):
#   * Incluye información detallada sobre titulación, calificación final, etc.
#   * Relacionada con dimensiones para seguimiento de egresados y titulados.
#   * Implementados todos los campos clave: ID_CURSO_ACADEMICO, ID_ALUMNO, ID_EXPEDIENTE_ACADEMICO, 
#     ID_TIPO_EGRESO, ID_PLAN_ESTUDIO, ID_TITULACION, indicadores de duración, etc.
#
# - F_SOLICITANTE_ADMISION (69 atributos - IMPLEMENTADA COMPLETAMENTE):
#   * Información detallada de cada solicitante y sus preferencias.
#   * Relacionada con dimensiones de admisión, estudios y centros.
#   * Implementados todos los campos clave: ID_PREINSCRIPCION, ID_CURSO_ACADEMICO, 
#     ID_CONVOCATORIA, ID_TIPO_ACCESO_PREINS, ID_PERSONA, ID_PLAN_ESTUDIO, etc.
#
# - F_OFERTA_ADMISION (51 atributos - IMPLEMENTADA COMPLETAMENTE):
#   * Incluye plazas, notas de corte y demanda por plan de estudio.
#   * Relacionada con dimensiones de admisión y oferta académica.
#   * Implementados todos los campos clave: ID_CURSO_ACADEMICO, ID_PLAN_ESTUDIO, 
#     ID_CENTRO, ID_TIPO_ACCESO, ID_CUPO_ADJUDICACION, indicadores de plazas, etc.
#
# - F_ESTUDIANTES_MOVILIDAD_IN (31 atributos - IMPLEMENTADA COMPLETAMENTE):
#   * Incluye información de estudiantes de movilidad entrante con sus universidades de origen
#   * Relacionada con dimensiones para seguimiento de movilidad internacional
#   * Implementados todos los campos clave: ID_CURSO_ACADEMICO, ID_EXPEDIENTE_ACADEMICO, ID_ALUMNO,
#     ID_UNIVERSIDAD_ORIGEN, ID_PLAN_ESTUDIO, creditos, estancias, etc.
#
# - F_ESTUDIANTES_MOVILIDAD_OUT (47 atributos - IMPLEMENTADA COMPLETAMENTE):
#   * Incluye información de estudiantes propios que realizan movilidad a otras universidades
#   * Relacionada con dimensiones de destinos y programas de movilidad
#   * Implementados todos los campos clave: ID_CURSO_ACADEMICO, ID_EXPEDIENTE_ACADEMICO, 
#     ID_UNIVERSIDAD_DESTINO, ID_AREA_ESTUDIOS_MOVILIDAD, creditos, estancias, etc.
#
# - F_SOLICITUDES_MOVILIDAD (38 atributos - IMPLEMENTADA COMPLETAMENTE):
#   * Información sobre solicitudes de movilidad antes de ser aceptadas
#   * Relacionada con dimensiones de programas de movilidad y preferencias
#   * Implementados todos los campos clave: ID_SOLICITUD_MOVILIDAD_NK, ID_CURSO_ACADEMICO,
#     ID_AREA_ESTUDIOS_MOVILIDAD, flags de aceptación y renuncia, etc.
#
# - F_DOCTORADO_ADMISION (36 atributos - IMPLEMENTADA COMPLETAMENTE):
#   * Información sobre solicitudes de admisión a programas de doctorado
#   * Relacionada con dimensiones de planes de estudio de doctorado y estado de solicitudes
#   * Implementados todos los campos clave: ID_CURSO_ACADEMICO, ID_SOLICITUD_NK, 
#     ID_EXPEDIENTE_ACADEMICO_NK, ID_PLAN_ESTUDIO, etc.
#   
# - F_EGRACONS (42 atributos - IMPLEMENTADA COMPLETAMENTE):
#   * Sistema europeo de calificaciones para reconocimiento internacional
#   * Relacionada con dimensiones de calificaciones y rangos de notas específicos
#   * Implementados todos los campos clave: ID_CURSO_EGRACONS, ID_EXPEDIENTE_ACADEMICO,
#     ID_ASIGNATURA, notas y creditos, etc.
#   
# - F_ESTUDIO_PROPIO_MATRICULA (51 atributos - IMPLEMENTADA COMPLETAMENTE):
#   * Matrículas en estudios propios de la universidad (no oficiales)
#   * Relacionada con dimensiones específicas de estudios propios y tipos/modalidades
#   * Implementados todos los campos clave: ID_CURSO_ACADEMICO, ID_EXPEDIENTE_EST_PROPIO,
#     ID_PERSONA, ID_ESTUDIO_PROPIO, información académica, etc.
#
# - F_OFERTA_ACUERDO_BILATERAL (45 atributos - IMPLEMENTADA COMPLETAMENTE):
#   * Información sobre acuerdos bilaterales con otras universidades para movilidad
#   * Relacionada con dimensiones de movilidad y acuerdos bilaterales
#   * Implementados todos los campos clave: ID_CURSO_ACADEMICO, ID_ACUERDO_BILATERAL,
#     ID_AREA_ESTUDIOS_MOVILIDAD, ID_NIVEL_ESTUDIOS_MOVILIDAD, IN_OUT, etc.
#
# - F_DOCTORADO (138 atributos - IMPLEMENTADA COMPLETAMENTE):
#   * Información completa sobre estudiantes de doctorado y sus tesis
#   * Relacionada con múltiples dimensiones académicas, personales y de investigación
#   * Implementados todos los campos clave: ID_CURSO_INFORME, ID_EXPEDIENTE_ACADEMICO,
#     ID_PLAN_ESTUDIO, ID_CENTRO, datos de tesis, profesorado, publicaciones, etc.
#
# - F_TABLA_FUSION (13 atributos - IMPLEMENTADA COMPLETAMENTE):
#   * Tabla agregada con indicadores por plan de estudio y curso académico
#   * Incluye tasas de éxito, rendimiento, eficiencia y métricas de alumnos
#
# - F_TABLA_FUSION_ESTCEN (21 atributos - IMPLEMENTADA COMPLETAMENTE):
#   * Tabla agregada con indicadores por centro, estudio y curso académico
#   * Incluye tasas de éxito, rendimiento, valoraciones y métricas específicas de doctorado
#
# CONSTRAINTS IMPLEMENTADOS:
# - Todas las tablas de dimensión tienen sus claves primarias correctamente definidas mediante índices únicos
# - Se han implementado índices adicionales para las tablas de hechos, principalmente en F_RENDIMIENTO
# - No se han detectado restricciones faltantes en el modelo de datos 