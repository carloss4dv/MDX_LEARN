#!/usr/bin/env python3
"""
Script para descargar automáticamente los drivers JDBC necesarios.

Este script descarga los drivers JDBC de Oracle y PostgreSQL desde sus repositorios
oficiales y los coloca en el directorio lib/ para su uso con JayDeBeApi.

Drivers descargados:
- ojdbc8.jar (Oracle JDBC para Java 8+)
- ojdbc11.jar (Oracle JDBC para Java 11+) 
- ojdbc17.jar (Oracle JDBC para Java 17+)
- postgresql-42.5.0.jar (PostgreSQL JDBC)

Uso:
    python download_jdbc_drivers.py
"""

import os
import sys
import requests
from pathlib import Path
import hashlib
from typing import Dict, Tuple

# Configuración de drivers a descargar
DRIVERS_CONFIG = {
    'ojdbc8.jar': {
        'url': 'https://repo1.maven.org/maven2/com/oracle/database/jdbc/ojdbc8/21.9.0.0/ojdbc8-21.9.0.0.jar',
        'description': 'Oracle JDBC Driver (Java 8+)',
        'size_mb': 4.2
    },
    'ojdbc11.jar': {
        'url': 'https://repo1.maven.org/maven2/com/oracle/database/jdbc/ojdbc11/21.9.0.0/ojdbc11-21.9.0.0.jar',
        'description': 'Oracle JDBC Driver (Java 11+)',
        'size_mb': 4.2
    },
    'ojdbc17.jar': {
        'url': 'https://repo1.maven.org/maven2/com/oracle/database/jdbc/ojdbc10/19.18.0.0/ojdbc10-19.18.0.0.jar',
        'description': 'Oracle JDBC Driver (Java 17+)',
        'size_mb': 3.9
    },
    'postgresql-42.5.0.jar': {
        'url': 'https://repo1.maven.org/maven2/org/postgresql/postgresql/42.5.0/postgresql-42.5.0.jar',
        'description': 'PostgreSQL JDBC Driver',
        'size_mb': 1.1
    }
}

def get_lib_directory() -> Path:
    """Obtiene el directorio lib donde guardar los drivers."""
    script_dir = Path(__file__).parent
    lib_dir = script_dir / 'lib'
    lib_dir.mkdir(exist_ok=True)
    return lib_dir

def format_size(size_bytes: int) -> str:
    """Formatea el tamaño en bytes a una cadena legible."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"

def download_file(url: str, destination: Path, description: str) -> bool:
    """
    Descarga un archivo desde una URL.
    
    Args:
        url: URL del archivo a descargar
        destination: Ruta donde guardar el archivo
        description: Descripción del archivo para mostrar
        
    Returns:
        True si la descarga fue exitosa, False en caso contrario
    """
    try:
        print(f"📥 Descargando {description}...")
        print(f"   URL: {url}")
        print(f"   Destino: {destination}")
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    
                    # Mostrar progreso cada 1MB
                    if downloaded_size % (1024 * 1024) == 0 or downloaded_size == total_size:
                        if total_size > 0:
                            progress = (downloaded_size / total_size) * 100
                            print(f"   Progreso: {format_size(downloaded_size)}/{format_size(total_size)} ({progress:.1f}%)")
                        else:
                            print(f"   Descargado: {format_size(downloaded_size)}")
        
        print(f"✅ {description} descargado exitosamente")
        print(f"   Tamaño final: {format_size(destination.stat().st_size)}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error descargando {description}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado descargando {description}: {e}")
        return False

def check_existing_files(lib_dir: Path) -> Dict[str, bool]:
    """
    Verifica qué archivos ya existen en el directorio lib.
    
    Args:
        lib_dir: Directorio lib donde buscar
        
    Returns:
        Diccionario con el estado de cada archivo
    """
    existing_files = {}
    for driver_name in DRIVERS_CONFIG.keys():
        file_path = lib_dir / driver_name
        existing_files[driver_name] = file_path.exists()
        
        if existing_files[driver_name]:
            size = format_size(file_path.stat().st_size)
            print(f"📁 {driver_name} ya existe ({size})")
    
    return existing_files

def main():
    """Función principal del script."""
    print("🚀 Iniciando descarga de drivers JDBC")
    print("=" * 50)
    
    # Verificar que requests esté disponible
    try:
        import requests
    except ImportError:
        print("❌ Error: La librería 'requests' no está instalada.")
        print("   Instale con: pip install requests")
        sys.exit(1)
    
    # Obtener directorio lib
    lib_dir = get_lib_directory()
    print(f"📂 Directorio de destino: {lib_dir}")
    print()
    
    # Verificar archivos existentes
    existing_files = check_existing_files(lib_dir)
    
    # Preguntar si desea sobrescribir archivos existentes
    existing_count = sum(existing_files.values())
    if existing_count > 0:
        print(f"\n⚠️  Se encontraron {existing_count} driver(s) existente(s).")
        response = input("¿Desea sobrescribirlos? (s/N): ").lower().strip()
        overwrite = response in ['s', 'si', 'sí', 'y', 'yes']
        print()
    else:
        overwrite = True
    
    # Descargar drivers
    successful_downloads = 0
    total_drivers = len(DRIVERS_CONFIG)
    
    for driver_name, config in DRIVERS_CONFIG.items():
        file_path = lib_dir / driver_name
        
        # Saltar si existe y no se quiere sobrescribir
        if existing_files[driver_name] and not overwrite:
            print(f"⏭️  Saltando {driver_name} (ya existe)")
            successful_downloads += 1
            continue
        
        # Descargar el archivo
        if download_file(config['url'], file_path, config['description']):
            successful_downloads += 1
        
        print()  # Línea en blanco entre descargas
    
    # Resumen final
    print("=" * 50)
    print("📊 Resumen de descarga:")
    print(f"   ✅ Exitosas: {successful_downloads}/{total_drivers}")
    print(f"   ❌ Fallidas: {total_drivers - successful_downloads}/{total_drivers}")
    
    if successful_downloads == total_drivers:
        print("\n🎉 ¡Todos los drivers JDBC han sido descargados exitosamente!")
        print("   Ya puede usar upload_to_db.py para cargar datos.")
    else:
        print(f"\n⚠️  Algunas descargas fallaron. Revise los errores arriba.")
        print("   Puede ejecutar este script nuevamente para reintentar.")
    
    # Mostrar contenido final del directorio lib
    print(f"\n📁 Contenido final de {lib_dir}:")
    jar_files = list(lib_dir.glob("*.jar"))
    if jar_files:
        for jar_file in sorted(jar_files):
            size = format_size(jar_file.stat().st_size)
            print(f"   📄 {jar_file.name} ({size})")
    else:
        print("   (No se encontraron archivos .jar)")

if __name__ == "__main__":
    main()
