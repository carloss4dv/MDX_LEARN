"""
Funciones auxiliares para generar fechas aleatorias sin dependencias externas problemáticas
"""

import random
import datetime

def generate_random_date(start_year, end_year):
    """Genera una fecha aleatoria entre los años especificados como string 'YYYY-MM-DD'"""
    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_date = start_date + datetime.timedelta(days=random_days)
    return random_date.strftime('%Y-%m-%d')

def generate_random_date_datetime(start_year, end_year):
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