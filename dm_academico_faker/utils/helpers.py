import cx_Oracle
import pandas as pd
from tqdm import tqdm
import random
import string
import datetime

def insert_dataframe_to_oracle(connection, df, table_name, batch_size=1000):
    """
    Inserta un DataFrame en una tabla Oracle
    
    Args:
        connection: Conexión a Oracle
        df: DataFrame con los datos a insertar
        table_name: Nombre de la tabla
        batch_size: Tamaño del lote para inserción
    
    Returns:
        int: Número de filas insertadas
    """
    cursor = connection.cursor()
    
    # Obtener columnas de la tabla
    columns = df.columns.tolist()
    placeholders = ':' + ', :'.join(columns)
    
    # Preparar consulta SQL
    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
    
    # Insertar en lotes
    rows_inserted = 0
    for i in tqdm(range(0, len(df), batch_size), desc=f"Insertando en {table_name}"):
        batch = df.iloc[i:i+batch_size]
        data_dicts = batch.to_dict('records')
        cursor.executemany(insert_query, data_dicts)
        connection.commit()
        rows_inserted += len(batch)
    
    cursor.close()
    print(f"Total de {rows_inserted} registros insertados en {table_name}")
    return rows_inserted

def get_table_columns(connection, table_name):
    """
    Obtiene la lista de columnas de una tabla
    
    Args:
        connection: Conexión a Oracle
        table_name: Nombre de la tabla
    
    Returns:
        list: Lista de columnas de la tabla
    """
    cursor = connection.cursor()
    cursor.execute(f"SELECT column_name, data_type, data_length FROM user_tab_columns WHERE table_name = '{table_name}' ORDER BY column_id")
    columns = cursor.fetchall()
    cursor.close()
    return columns

def clean_table(connection, table_name):
    """
    Elimina todos los registros de una tabla
    
    Args:
        connection: Conexión a Oracle
        table_name: Nombre de la tabla
    """
    cursor = connection.cursor()
    try:
        cursor.execute(f"DELETE FROM {table_name}")
        connection.commit()
        print(f"Tabla {table_name} limpiada con éxito")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Error al limpiar la tabla {table_name}: {error.message}")
    finally:
        cursor.close()

def generate_random_string(length=10):
    """
    Genera una cadena aleatoria de longitud especificada
    
    Args:
        length: Longitud de la cadena
    
    Returns:
        str: Cadena aleatoria
    """
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=length))

def generate_random_date(start_year, end_year):
    """
    Genera una fecha aleatoria entre start_year y end_year
    
    Args:
        start_year (int): Año de inicio
        end_year (int): Año de fin
    
    Returns:
        str: Fecha en formato YYYY-MM-DD
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
    
    # Formatear la fecha como YYYY-MM-DD
    return f"{year}-{month:02d}-{day:02d}"

def generate_dni():
    """
    Genera un DNI español aleatorio válido
    
    Returns:
        str: DNI en formato 12345678X
    """
    # Letras válidas para DNI español
    letters = "TRWAGMYFPDXBNJZSQVHLCKE"
    
    # Generar número aleatorio de 8 dígitos
    number = random.randint(10000000, 99999999)
    
    # Calcular letra correspondiente
    letter = letters[number % 23]
    
    return f"{number}{letter}"

def generate_nie():
    """
    Genera un NIE español aleatorio válido
    
    Returns:
        str: NIE en formato X1234567Y
    """
    # Letras válidas para el primer carácter del NIE
    first_letters = "XYZ"
    first_letter = random.choice(first_letters)
    
    # Letras válidas para el último carácter del NIE
    last_letters = "TRWAGMYFPDXBNJZSQVHLCKE"
    
    # Generar número aleatorio de 7 dígitos
    number = random.randint(1000000, 9999999)
    
    # Convertir la primera letra a su valor numérico correspondiente
    if first_letter == "X":
        value = 0
    elif first_letter == "Y":
        value = 1
    else:  # "Z"
        value = 2
    
    # Calcular letra correspondiente
    check_digit = (value * 10000000 + number) % 23
    last_letter = last_letters[check_digit]
    
    return f"{first_letter}{number}{last_letter}"

def get_existing_ids(connection, table_name, id_column):
    """
    Obtiene los IDs existentes en una tabla
    
    Args:
        connection: Conexión a Oracle
        table_name: Nombre de la tabla
        id_column: Nombre de la columna ID
    
    Returns:
        list: Lista de IDs existentes
    """
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT {id_column} FROM {table_name}")
        ids = [row[0] for row in cursor.fetchall()]
        return ids
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Error al obtener IDs de {table_name}: {error.message}")
        return []
    finally:
        cursor.close()

def check_table_exists(connection, table_name):
    """
    Verifica si una tabla existe en la base de datos
    
    Args:
        connection: Conexión a Oracle
        table_name: Nombre de la tabla
    
    Returns:
        bool: True si la tabla existe, False en caso contrario
    """
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT COUNT(*) FROM user_tables WHERE table_name = '{table_name}'")
        count = cursor.fetchone()[0]
        return count > 0
    except cx_Oracle.DatabaseError:
        return False
    finally:
        cursor.close()

def get_foreign_keys(connection, table_name):
    """
    Obtiene las claves foráneas de una tabla
    
    Args:
        connection: Conexión a Oracle
        table_name: Nombre de la tabla
    
    Returns:
        dict: Diccionario con las claves foráneas
    """
    cursor = connection.cursor()
    query = """
    SELECT a.column_name, a.constraint_name, c_pk.table_name r_table_name, c_pk.column_name r_column_name
    FROM user_cons_columns a
    JOIN user_constraints c ON a.constraint_name = c.constraint_name
    JOIN user_constraints c_pk ON c.r_constraint_name = c_pk.constraint_name
    JOIN user_cons_columns c_pk_col ON c_pk.constraint_name = c_pk_col.constraint_name
    WHERE c.constraint_type = 'R'
    AND a.table_name = :table_name
    """
    cursor.execute(query, table_name=table_name)
    fk_data = cursor.fetchall()
    
    foreign_keys = {}
    for column_name, constraint_name, ref_table, ref_column in fk_data:
        foreign_keys[column_name] = {
            'constraint_name': constraint_name,
            'ref_table': ref_table,
            'ref_column': ref_column
        }
    
    cursor.close()
    return foreign_keys 