import cx_Oracle
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

def get_connection():
    """
    Establece y retorna una conexión a la base de datos Oracle
    
    Returns:
        cx_Oracle.Connection: Objeto de conexión a Oracle
    """
    # Configuración de variables de entorno para Oracle Instant Client
    oracle_client_path = os.environ.get('ORACLE_CLIENT_PATH', 'C:\\oracle\\instantclient_19_11')
    if oracle_client_path:
        os.environ["PATH"] = os.environ["PATH"] + ";" + oracle_client_path
    
    # Datos de conexión desde variables de entorno o valores por defecto
    host = os.environ.get('ORACLE_HOST', 'localhost')
    port = os.environ.get('ORACLE_PORT', '1521')
    service_name = os.environ.get('ORACLE_SERVICE_NAME', 'XEPDB1')
    user = os.environ.get('ORACLE_USER', 'C##DM_ACADEMICO')
    password = os.environ.get('ORACLE_PASSWORD', 'YourPassword123@')
    
    # Crear DSN y conexión
    dsn = cx_Oracle.makedsn(host=host, port=port, service_name=service_name)
    connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
    
    # Configurar para manejar caracteres especiales correctamente
    connection.outputtypehandler = output_type_handler
    
    print(f"Conexión establecida con éxito a {user}@{host}:{port}/{service_name}")
    return connection

def output_type_handler(cursor, name, defaultType, size, precision, scale):
    """
    Manejador de tipos para asegurar que los caracteres especiales se manejen correctamente
    """
    if defaultType == cx_Oracle.CLOB:
        return cursor.var(cx_Oracle.LONG_STRING, arraysize=cursor.arraysize)
    if defaultType == cx_Oracle.BLOB:
        return cursor.var(cx_Oracle.LONG_BINARY, arraysize=cursor.arraysize)
    if defaultType == cx_Oracle.DB_TYPE_VARCHAR and size > 100:
        return cursor.var(str, size, cursor.arraysize) 