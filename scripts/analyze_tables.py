import re
import os
from typing import Dict, List, Set, Optional, Tuple

class SQLAnalyzer:
    def __init__(self, file_path: str):
        """Inicializa el analizador SQL con la ruta del archivo.
        
        Args:
            file_path (str): Ruta al archivo SQL a analizar
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no existe")
        
        self.file_path = file_path
        self.content = self._read_file()
        self.tables = {}  # Almacenará todas las tablas encontradas
        self.primary_keys = {}  # Almacenará todas las PKs
        self.foreign_keys = {}  # Almacenará todas las FKs
        self.indexes = {}  # Almacenará todos los índices
        self.unique_indexes = {}  # Almacenará los índices únicos por nombre
        
    def _read_file(self) -> str:
        """Lee el contenido del archivo SQL.
        
        Returns:
            str: Contenido completo del archivo
        """
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()
        
    def _clean_data_type(self, data_type: str) -> str:
        """Limpia el tipo de datos para una presentación uniforme.
        
        Args:
            data_type (str): Tipo de datos sin procesar
            
        Returns:
            str: Tipo de datos limpio
        """
        # Eliminar espacios extras y comas al final
        data_type = data_type.strip().rstrip(',')
        
        # Corregir paréntesis desbalanceados
        open_parens = data_type.count('(')
        close_parens = data_type.count(')')
        
        # Si faltan paréntesis de cierre, añadirlos
        if open_parens > close_parens:
            data_type += ')' * (open_parens - close_parens)
            
        return data_type
    
    def _extract_tables(self):
        """Extrae todas las tablas y sus columnas del archivo SQL."""
        # Patrón para encontrar CREATE TABLE con las columnas
        table_pattern = r'CREATE TABLE "C##DM_ACADEMICO"\."([^"]+)"\s*\(\s*([^;]+?)\s*\)\s*SEGMENT CREATION'
        
        # Buscar todas las definiciones de tabla
        for match in re.finditer(table_pattern, self.content, re.DOTALL):
            table_name = match.group(1)
            columns_def = match.group(2)
            
            # Extraer columnas
            columns = []
            
            # Buscar PKs definidas dentro de CREATE TABLE
            inline_pk_columns = set()
            pk_pattern = r'CONSTRAINT\s+"[^"]+"\s+PRIMARY KEY\s*\(([^)]+)\)'
            pk_match = re.search(pk_pattern, columns_def, re.DOTALL)
            if pk_match:
                inline_pk_columns = set([col.strip().strip('"') for col in pk_match.group(1).split(',')])
                self.primary_keys[table_name] = inline_pk_columns
            
            # Buscar FKs definidas dentro de CREATE TABLE
            if table_name not in self.foreign_keys:
                self.foreign_keys[table_name] = {}
                
            fk_pattern = r'CONSTRAINT\s+"[^"]+"\s+FOREIGN KEY\s*\(([^)]+)\)\s*REFERENCES\s+"C##DM_ACADEMICO"\."([^"]+)"\s*\(([^)]+)\)'
            for fk_match in re.finditer(fk_pattern, columns_def, re.DOTALL):
                fk_columns = [col.strip().strip('"') for col in fk_match.group(1).split(',')]
                ref_table = fk_match.group(2)
                ref_columns = [col.strip().strip('"') for col in fk_match.group(3).split(',')]
                
                for i, fk_col in enumerate(fk_columns):
                    ref_col = ref_columns[min(i, len(ref_columns)-1)]  # Evitar índice fuera de rango
                    self.foreign_keys[table_name][fk_col] = {
                        'references_table': ref_table,
                        'references_column': ref_col
                    }
            
            # Dividir la definición de columnas por línea para procesarlas de manera más confiable
            lines = columns_def.split('\n')
            for line in lines:
                line = line.strip()
                
                # Ignorar líneas vacías o que no son definiciones de columnas
                if not line or line.startswith((')', 'CONSTRAINT', 'PRIMARY KEY', 'FOREIGN KEY')):
                    continue
                
                # Patrón para extraer nombre y tipo de columna
                col_match = re.match(r'"([^"]+)"\s+([^,]+)', line)
                if col_match:
                    col_name = col_match.group(1)
                    col_type_raw = col_match.group(2).strip().rstrip(',')
                    col_type = self._clean_data_type(col_type_raw)
                    
                    columns.append({
                        'name': col_name,
                        'type': col_type,
                        'is_pk': col_name in inline_pk_columns,
                        'is_fk': col_name in self.foreign_keys.get(table_name, {}),
                        'references': self.foreign_keys.get(table_name, {}).get(col_name)
                    })
            
            if columns:  # Solo guardar tabla si tiene columnas
                self.tables[table_name] = columns

    def _extract_indices(self):
        """Extrae todos los índices definidos en el archivo SQL."""
        # Patrón para encontrar CREATE INDEX
        index_pattern = r'CREATE\s+(?:UNIQUE\s+)?INDEX\s+"C##DM_ACADEMICO"\."([^"]+)"\s+ON\s+"C##DM_ACADEMICO"\."([^"]+)"\s*\(([^)]+)\)'
        
        for match in re.finditer(index_pattern, self.content, re.DOTALL):
            index_name = match.group(1)
            table_name = match.group(2)
            columns_str = match.group(3)
            columns = [col.strip().strip('"') for col in columns_str.split(',')]
            is_unique = 'UNIQUE' in match.group(0)
            
            if table_name not in self.indexes:
                self.indexes[table_name] = []
            
            self.indexes[table_name].append({
                'name': index_name,
                'columns': columns,
                'is_unique': is_unique
            })
            
            # Guardar índices únicos por nombre para uso posterior en la identificación de PKs
            if is_unique:
                self.unique_indexes[index_name] = {
                    'table': table_name,
                    'columns': columns
                }
                
                # Si el nombre del índice sugiere que es una PK (comienza con PK_ o contiene _PK_)
                # o si la tabla es de dimensión (D_) y el índice es único
                if (index_name.startswith('PK_') or '_PK_' in index_name or index_name.endswith('_PK')) or (table_name.startswith('D_')):
                    if table_name not in self.primary_keys:
                        self.primary_keys[table_name] = set(columns)
                    else:
                        self.primary_keys[table_name].update(columns)

    def _extract_primary_keys(self):
        """Extrae todas las claves primarias."""
        # Primero extraer los índices únicos que se utilizarán como PK
        self._extract_indices()
        
        # Buscar claves primarias definidas como ALTER TABLE ... ADD CONSTRAINT ... PRIMARY KEY
        # Este patrón busca restricciones de PK que hacen referencia a un índice existente
        pk_constraint_pattern = r'ALTER TABLE "C##DM_ACADEMICO"\."([^"]+)"\s+ADD\s+CONSTRAINT\s+"([^"]+)"\s+PRIMARY KEY\s*\(([^)]+)\)(?:\s*USING\s+INDEX\s+"C##DM_ACADEMICO"\."([^"]+)")?\s+ENABLE'
        
        for match in re.finditer(pk_constraint_pattern, self.content, re.DOTALL):
            table_name = match.group(1)
            constraint_name = match.group(2)
            pk_columns_str = match.group(3)
            pk_columns = [col.strip().strip('"') for col in pk_columns_str.split(',')]
            
            # Si hay un índice asociado
            if match.group(4):
                index_name = match.group(4)
                if index_name in self.unique_indexes:
                    index_info = self.unique_indexes[index_name]
                    if table_name == index_info['table']:  # Verificar que la tabla coincida
                        if table_name not in self.primary_keys:
                            self.primary_keys[table_name] = set(index_info['columns'])
                        else:
                            self.primary_keys[table_name].update(index_info['columns'])
            else:
                # Si no hay índice asociado, usar las columnas definidas directamente
                if table_name not in self.primary_keys:
                    self.primary_keys[table_name] = set(pk_columns)
                else:
                    self.primary_keys[table_name].update(pk_columns)
        
        # También buscar claves primarias definidas directamente en el ALTER TABLE
        direct_pk_pattern = r'ALTER TABLE "C##DM_ACADEMICO"\."([^"]+)"\s+ADD\s+CONSTRAINT\s+"[^"]+"\s+PRIMARY KEY\s*\(([^)]+)\)'
        
        for match in re.finditer(direct_pk_pattern, self.content, re.DOTALL):
            table_name = match.group(1)
            columns_str = match.group(2)
            columns = [col.strip().strip('"') for col in columns_str.split(',')]
            
            if table_name not in self.primary_keys:
                self.primary_keys[table_name] = set(columns)
            else:
                self.primary_keys[table_name].update(columns)
        
        # Identificar PKs a partir de índices únicos con nombres que sugieren que son PKs
        for index_name, index_info in self.unique_indexes.items():
            table_name = index_info['table']
            # Si el nombre del índice sugiere que es una PK y la tabla no tiene PK definida o es una tabla de dimensión
            if ('PK_' in index_name or index_name.endswith('_PK')) or (table_name.startswith('D_') and table_name not in self.primary_keys):
                if table_name not in self.primary_keys:
                    self.primary_keys[table_name] = set(index_info['columns'])
                else:
                    self.primary_keys[table_name].update(index_info['columns'])

    def _extract_foreign_keys(self):
        """Extrae todas las claves foráneas."""
        # Buscar claves foráneas en ALTER TABLE ... ADD CONSTRAINT ... FOREIGN KEY
        fk_constraint_pattern = r'ALTER TABLE "C##DM_ACADEMICO"\."([^"]+)"\s+ADD\s+CONSTRAINT\s+"[^"]+"\s+FOREIGN KEY\s*\(([^)]+)\)\s*REFERENCES\s+"C##DM_ACADEMICO"\."([^"]+)"\s*\(([^)]+)\)'
        
        for match in re.finditer(fk_constraint_pattern, self.content, re.DOTALL):
            table_name = match.group(1)
            fk_columns = [col.strip().strip('"') for col in match.group(2).split(',')]
            ref_table = match.group(3)
            ref_columns = [col.strip().strip('"') for col in match.group(4).split(',')]
            
            if table_name not in self.foreign_keys:
                self.foreign_keys[table_name] = {}
                
            for i, fk_col in enumerate(fk_columns):
                ref_col = ref_columns[min(i, len(ref_columns)-1)]  # Evitar índice fuera de rango
                self.foreign_keys[table_name][fk_col] = {
                    'references_table': ref_table,
                    'references_column': ref_col
                }
        
        # Inicializar diccionario de claves foráneas para todas las tablas
        for table_name in self.tables.keys():
            if table_name not in self.foreign_keys:
                self.foreign_keys[table_name] = {}
        
        # Identificar claves foráneas basadas en convenciones de nombres (complementario)
        for table_name, table_columns in self.tables.items():
            # Especialmente importante para tablas de hechos (F_)
            for col in table_columns:
                col_name = col['name']
                
                # Si ya es una FK explícita, continuar
                if col_name in self.foreign_keys.get(table_name, {}):
                    continue
                
                # Candidatos para FK
                if col_name.startswith('ID_') and col_name != 'ID_FECHA_CARGA' and col_name != 'ID_FECHA_REFERENCIA':
                    # 1. Buscar referencia directa al nombre de una tabla de dimensión
                    dimension_name = 'D_' + col_name[3:]
                    if dimension_name in self.tables and dimension_name in self.primary_keys:
                        pk_cols = list(self.primary_keys[dimension_name])
                        if pk_cols:  # Si la tabla tiene PK
                            self.foreign_keys[table_name][col_name] = {
                                'references_table': dimension_name,
                                'references_column': pk_cols[0]  # Usar primera columna de PK
                            }
                            continue
                    
                    # 2. Casos especiales con nombres diferentes
                    special_cases = {
                        'ID_TIPO_ACCESO_PREINS': 'D_TIPO_ACCESO_PREINSCRIPCION',
                        'ID_RANGO_CRED_SUPERADOS': 'D_RANGO_CREDITO',
                        'ID_RANGO_CRED_SUPERADOS_PREVIO': 'D_RANGO_CREDITO',
                        'ID_PAIS_NACIONALIDAD': 'D_PAIS',
                        'ID_PAIS_UNIVERSIDAD_DESTINO': 'D_PAIS',
                        'ID_PAIS_UNIVERSIDAD_ORIGEN': 'D_PAIS',
                        'ID_PAIS_UNIVERSIDAD_ACUERDO': 'D_PAIS',
                        'ID_PAIS_NACIMIENTO': 'D_PAIS',
                        'ID_PAIS_FAMILIAR': 'D_PAIS',
                        'ID_POBLACION_FAMILIAR': 'D_POBLACION',
                        'ID_POBLACION_NACIMIENTO': 'D_POBLACION',
                        'ID_POBLACION_CENTRO': 'D_POBLACION',
                        'ID_POBLACION_CURSO': 'D_POBLACION'
                    }
                    
                    if col_name in special_cases and special_cases[col_name] in self.tables:
                        target_table = special_cases[col_name]
                        if target_table in self.primary_keys:
                            pk_cols = list(self.primary_keys[target_table])
                            if pk_cols:
                                self.foreign_keys[table_name][col_name] = {
                                    'references_table': target_table,
                                    'references_column': pk_cols[0]
                                }
                                continue
                    
                    # 3. Referencias comunes en modelos dimensionales
                    special_refs = {
                        'ID_CENTRO': 'D_CENTRO',
                        'ID_ASIGNATURA': 'D_ASIGNATURA',
                        'ID_PLAN_ESTUDIO': 'D_PLAN_ESTUDIO',
                        'ID_CURSO_ACADEMICO': 'D_CURSO_ACADEMICO',
                        'ID_CALIFICACION': 'D_CALIFICACION',
                        'ID_CONVOCATORIA': 'D_CONVOCATORIA',
                        'ID_TIPO_ACCESO': 'D_TIPO_ACCESO',
                        'ID_SEXO': 'D_SEXO',
                        'ID_TIPO_ABANDONO': 'D_TIPO_ABANDONO',
                        'ID_TIPO_EGRESO': 'D_TIPO_EGRESO',
                        'ID_UNIVERSIDAD': 'D_UNIVERSIDAD',
                        'ID_GRUPO': 'D_GRUPO',
                        'ID_RANGO_NOTA_NUMERICA': 'D_RANGO_NOTA_NUMERICA',
                        'ID_RANGO_NOTA_ADMISION': 'D_RANGO_NOTA_ADMISION',
                        'ID_PERSONA': 'D_PERSONA',
                        'ID_PAIS': 'D_PAIS',
                        'ID_POBLACION': 'D_POBLACION',
                        'ID_CLASE_ASIGNATURA': 'D_CLASE_ASIGNATURA',
                        'ID_ESTUDIO_PREVIO': 'D_ESTUDIO_PREVIO',
                        'ID_CUPO_ADJUDICACION': 'D_CUPO_ADJUDICACION',
                        'ID_ESTADO_ADJUDICACION': 'D_ESTADO_ADJUDICACION',
                        'ID_TIPO_DOCENCIA': 'D_TIPO_DOCENCIA',
                        'ID_TIPO_RECONOCIMIENTO': 'D_TIPO_RECONOCIMIENTO',
                        'ID_TIPO_PROCEDIMIENTO': 'D_TIPO_PROCEDIMIENTO',
                        'ID_TITULACION': 'D_TITULACION'
                    }
                    
                    if col_name in special_refs and special_refs[col_name] in self.tables:
                        target_table = special_refs[col_name]
                        if target_table in self.primary_keys:
                            pk_cols = list(self.primary_keys[target_table])
                            if pk_cols:
                                self.foreign_keys[table_name][col_name] = {
                                    'references_table': target_table,
                                    'references_column': pk_cols[0]
                                }
                                continue
                    
                    # 4. Referencias entre tablas de hechos y F_TABLA_FUSION
                    if col_name == 'ID_PLAN_ESTUDIO' and table_name.startswith('F_') and 'F_TABLA_FUSION' in self.tables:
                        self.foreign_keys[table_name][col_name] = {
                            'references_table': 'F_TABLA_FUSION',
                            'references_column': 'ID_PLAN_ESTUDIO'
                        }
                        continue
                
                # 5. Claves naturales (NK)
                if col_name.endswith('_NK') and not col_name in self.foreign_keys.get(table_name, {}):
                    base_col = col_name[:-3]
                    for dim_table in self.tables.keys():
                        if dim_table.startswith('D_'):
                            for dim_col in [c['name'] for c in self.tables[dim_table]]:
                                if dim_col == base_col and dim_table in self.primary_keys:
                                    self.foreign_keys[table_name][col_name] = {
                                        'references_table': dim_table,
                                        'references_column': base_col
                                    }
                                    break

    def _extract_constraints(self):
        """Extrae todos los constraints definidos en el archivo SQL."""
        # Diccionario para almacenar constraints por tabla
        constraints = {}
        
        # Patrón para encontrar constraints en CREATE TABLE
        table_constraint_pattern = r'CREATE TABLE "C##DM_ACADEMICO"\."([^"]+)"\s*\((?:[^,]+,)*\s*CONSTRAINT\s+"([^"]+)"\s+(PRIMARY KEY|FOREIGN KEY|UNIQUE|CHECK)\s*\(([^)]+)\)(?:\s*REFERENCES\s+"C##DM_ACADEMICO"\."([^"]+)"\s*\(([^)]+)\))?'
        
        for match in re.finditer(table_constraint_pattern, self.content, re.DOTALL):
            table_name = match.group(1)
            constraint_name = match.group(2)
            constraint_type = match.group(3)
            columns = [col.strip().strip('"') for col in match.group(4).split(',')]
            
            if table_name not in constraints:
                constraints[table_name] = []
                
            constraint_info = {
                'name': constraint_name,
                'type': constraint_type,
                'columns': columns
            }
            
            # Si es una FK, añadir información de referencia
            if constraint_type == 'FOREIGN KEY' and match.group(5):
                ref_table = match.group(5)
                ref_columns = [col.strip().strip('"') for col in match.group(6).split(',')]
                constraint_info['references'] = {
                    'table': ref_table,
                    'columns': ref_columns
                }
                
            constraints[table_name].append(constraint_info)
        
        # Patrón para encontrar constraints en ALTER TABLE
        alter_constraint_pattern = r'ALTER TABLE "C##DM_ACADEMICO"\."([^"]+)"\s+ADD\s+CONSTRAINT\s+"([^"]+)"\s+(PRIMARY KEY|FOREIGN KEY|UNIQUE|CHECK)\s*\(([^)]+)\)(?:\s*REFERENCES\s+"C##DM_ACADEMICO"\."([^"]+)"\s*\(([^)]+)\))?'
        
        for match in re.finditer(alter_constraint_pattern, self.content, re.DOTALL):
            table_name = match.group(1)
            constraint_name = match.group(2)
            constraint_type = match.group(3)
            columns = [col.strip().strip('"') for col in match.group(4).split(',')]
            
            if table_name not in constraints:
                constraints[table_name] = []
                
            constraint_info = {
                'name': constraint_name,
                'type': constraint_type,
                'columns': columns
            }
            
            # Si es una FK, añadir información de referencia
            if constraint_type == 'FOREIGN KEY' and match.group(5):
                ref_table = match.group(5)
                ref_columns = [col.strip().strip('"') for col in match.group(6).split(',')]
                constraint_info['references'] = {
                    'table': ref_table,
                    'columns': ref_columns
                }
                
            constraints[table_name].append(constraint_info)
        
        return constraints
        
    def _process_constraints(self):
        """Procesa los constraints para actualizar PKs y FKs."""
        constraints = self._extract_constraints()
        
        for table_name, table_constraints in constraints.items():
            for constraint in table_constraints:
                if constraint['type'] == 'PRIMARY KEY':
                    # Actualizar primary keys
                    if table_name not in self.primary_keys:
                        self.primary_keys[table_name] = set(constraint['columns'])
                    else:
                        self.primary_keys[table_name].update(constraint['columns'])
                        
                elif constraint['type'] == 'FOREIGN KEY':
                    # Actualizar foreign keys
                    if table_name not in self.foreign_keys:
                        self.foreign_keys[table_name] = {}
                        
                    if 'references' in constraint:
                        ref_table = constraint['references']['table']
                        ref_columns = constraint['references']['columns']
                        
                        for i, fk_col in enumerate(constraint['columns']):
                            ref_col = ref_columns[min(i, len(ref_columns)-1)]
                            self.foreign_keys[table_name][fk_col] = {
                                'references_table': ref_table,
                                'references_column': ref_col
                            }

    def _mark_keys_in_tables(self):
        """Marca las columnas que son PK o FK."""
        for table_name, columns in self.tables.items():
            # Obtener claves primarias y foráneas para esta tabla
            pk_cols = self.primary_keys.get(table_name, set())
            fk_info = self.foreign_keys.get(table_name, {})
            
            for col in columns:
                col_name = col['name']
                
                # Marcar PK
                if col_name in pk_cols:
                    col['is_pk'] = True
                
                # Marcar FK y agregar referencia
                if col_name in fk_info:
                    col['is_fk'] = True
                    col['references'] = fk_info[col_name]
                    
        # Verificación adicional para tablas de dimensión (D_)
        for table_name, columns in self.tables.items():
            if table_name.startswith('D_'):
                # Si es una tabla de dimensión y no tiene PK definida, intentar inferirla
                if table_name not in self.primary_keys or not self.primary_keys[table_name]:
                    # Buscar columnas con nombre ID_[TABLA] o similar
                    potential_pk = None
                    for col in columns:
                        col_name = col['name']
                        if col_name.startswith('ID_') and (col_name == f"ID_{table_name[2:]}" or 
                                                          col_name == f"ID_{table_name[2:].replace('_', '')}" or
                                                          table_name[2:].startswith(col_name[3:])):
                            potential_pk = col_name
                            break
                    
                    # Si encontramos un candidato a PK
                    if potential_pk:
                        if table_name not in self.primary_keys:
                            self.primary_keys[table_name] = set([potential_pk])
                        else:
                            self.primary_keys[table_name].add(potential_pk)
                        
                        # Marcar la columna como PK
                        for col in columns:
                            if col['name'] == potential_pk:
                                col['is_pk'] = True
                                break

    def analyze(self):
        """Realiza el análisis completo del archivo SQL."""
        # Extraer información
        self._extract_tables()
        self._extract_primary_keys()
        self._extract_foreign_keys()
        self._process_constraints()  # Procesar constraints adicionales
        self._mark_keys_in_tables()
        
        # Separar tablas por tipo
        dimension_tables = {name: cols for name, cols in self.tables.items() if name.startswith('D_')}
        fact_tables = {name: cols for name, cols in self.tables.items() if name.startswith('F_')}
        
        return {
            'total_tables': len(self.tables),
            'dimension_tables': len(dimension_tables),
            'fact_tables': len(fact_tables),
            'dimension_tables_data': dimension_tables,
            'fact_tables_data': fact_tables
        }

    def generate_markdown_report(self):
        """Genera un informe en formato Markdown del análisis SQL."""
        analysis = self.analyze()
        
        report = ["# Análisis Detallado de Tablas DM_ACADEMICO\n"]
        
        # Sección de resumen
        report.append("## Resumen\n")
        report.append(f"- Número total de tablas: {analysis['total_tables']}")
        report.append(f"- Tablas D_ (Dimensiones): {analysis['dimension_tables']}")
        report.append(f"- Tablas F_ (Hechos): {analysis['fact_tables']}\n")
        
        # Sección de tablas de dimensión
        report.append("## Tablas de Dimensión\n")
        
        for table_name in sorted(analysis['dimension_tables_data'].keys()):
            columns = analysis['dimension_tables_data'][table_name]
            
            report.append(f"\n### {table_name}\n")
            report.append("| Columna | Tipo | PK | FK | Referencia |")
            report.append("|---------|------|----|----|------------|")
            
            for col in columns:
                pk_mark = "✓" if col['is_pk'] else ""
                fk_mark = "✓" if col['is_fk'] else ""
                reference = ""
                if col['references']:
                    reference = f"{col['references']['references_table']}({col['references']['references_column']})"
                
                report.append(f"| {col['name']} | {col['type']} | {pk_mark} | {fk_mark} | {reference} |")
        
        # Sección de tablas de hechos
        report.append("\n## Tablas de Hechos\n")
        
        for table_name in sorted(analysis['fact_tables_data'].keys()):
            columns = analysis['fact_tables_data'][table_name]
            
            report.append(f"\n### {table_name}\n")
            report.append("| Columna | Tipo | PK | FK | Referencia |")
            report.append("|---------|------|----|----|------------|")
            
            # Mostrar todas las columnas en las tablas de hechos
            for col in columns:
                pk_mark = "✓" if col['is_pk'] else ""
                fk_mark = "✓" if col['is_fk'] else ""
                reference = ""
                if col['references']:
                    reference = f"{col['references']['references_table']}({col['references']['references_column']})"
                
                report.append(f"| {col['name']} | {col['type']} | {pk_mark} | {fk_mark} | {reference} |")
        
        return "\n".join(report)

def main():
    """Función principal del script."""
    # Comprobar si se proporciona una ruta de archivo como argumento de línea de comandos
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Usar ruta por defecto si no se proporciona
        file_path = 'data/dm_academico_modified.sql'
    
    analyzer = SQLAnalyzer(file_path)
    report = analyzer.generate_markdown_report()
    
    # Escribir el informe en un archivo
    with open('tabla_analisis_detallado.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Análisis completado. Informe generado en 'tabla_analisis_detallado.md'.")

if __name__ == "__main__":
    main() 