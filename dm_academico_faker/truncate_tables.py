#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para truncar todas las tablas del Data Mart Académico
Soporte para Oracle Database y PostgreSQL
"""

import sys
from pathlib import Path

# Importar la clase DatabaseUploader del script principal
try:
    from upload_to_db import DatabaseUploader, load_upload_config, setup_logging, JDBC_AVAILABLE
except ImportError:
    print("Error: No se pudo importar upload_to_db.py")
    sys.exit(1)

def main():
    """Función principal para truncar tablas"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Trunca todas las tablas del DM Académico')
    parser.add_argument('--db', choices=['oracle', 'postgresql'], 
                       default='oracle', help='Tipo de base de datos')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO', help='Nivel de logging')
    parser.add_argument('--log-file', default='truncate_tables.log',
                       help='Archivo de log')
    parser.add_argument('--confirm', action='store_true',
                       help='Confirmar operación sin preguntar')
    
    args = parser.parse_args()
    
    # Configurar logging
    logger = setup_logging(args.log_level, args.log_file)
    
    if not JDBC_AVAILABLE:
        logger.error("JayDeBeApi no está disponible")
        logger.info("💡 pip install JayDeBeApi>=1.2.3")
        return 1
    
    logger.info(f"🗑️  Script de truncado para {args.db.upper()}")
    logger.info(f"📝 Log: {args.log_file}")
    
    # Inicializar uploader
    uploader = DatabaseUploader(args.db, args.log_level)
    
    try:
        # Conectar
        uploader.connect()
        
        # Obtener tablas dinámicamente desde la base de datos
        logger.info("🔍 Obteniendo lista de tablas del DM académico...")
        upload_order = uploader.get_dm_tables_from_database()
        total_tables = sum(len(tables) for tables in upload_order.values())
        
        logger.info(f"📊 Se truncarán {total_tables} tablas del DM Académico")
        
        # Confirmar operación si no se especificó --confirm
        if not args.confirm:
            print("\n⚠️  ADVERTENCIA: Esta operación eliminará TODOS los datos de las siguientes tablas:")
            for category, tables in upload_order.items():
                if tables:
                    print(f"\n{category.replace('_', ' ').title()}:")
                    for table in tables:
                        print(f"  - {table}")
            
            response = input("\n¿Está seguro de que desea continuar? (sí/no): ").strip().lower()
            if response not in ['sí', 'si', 'yes', 'y', 's']:
                logger.info("❌ Operación cancelada por el usuario")
                return 0
        
        # Truncar todas las tablas
        logger.info("🗑️  Iniciando truncado de todas las tablas...")
        success = uploader.truncate_all_tables(upload_order)
        
        if success:
            logger.info("🎉 ¡Truncado completado exitosamente!")
            return 0
        else:
            logger.warning("⚠️  Truncado completado con algunos errores")
            return 1
            
    except Exception as e:
        logger.error(f"Error crítico: {e}")
        return 1
        
    finally:
        uploader.close()

if __name__ == "__main__":
    sys.exit(main()) 