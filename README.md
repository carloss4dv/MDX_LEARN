# Tutorial MDX con Atoti

Este repositorio contiene una serie de notebooks para aprender MDX (Multidimensional Expressions) utilizando Atoti y un esquema de base de datos universitario.

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Crear un entorno virtual:
```bash
python -m venv .venv
```

2. Activar el entorno virtual:
- Windows:
```bash
.venv\Scripts\activate
```
- Linux/Mac:
```bash
source .venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Estructura del Proyecto

- `notebooks/`: Contiene los notebooks de aprendizaje
- `data/`: Contiene los datos de ejemplo
- `create_schema_v3.sql`: Esquema de la base de datos

## Notebooks Disponibles

1. `01_introduccion_atoti.ipynb`: Introducción a Atoti y conceptos básicos
2. `02_cubos_multidimensionales.ipynb`: Creación y manipulación de cubos
3. `03_consultas_mdx_basicas.ipynb`: Consultas MDX básicas
4. `04_consultas_mdx_avanzadas.ipynb`: Consultas MDX avanzadas
5. `05_dashboards_interactivos.ipynb`: Creación de dashboards interactivos

## Cómo Usar

1. Iniciar Jupyter Lab:
```bash
jupyter lab
```

2. Navegar a la carpeta `notebooks/` y abrir los notebooks en orden.

## Recursos Adicionales

- [Documentación de Atoti](https://docs.activeviam.com/products/atoti/python-sdk/latest/)
- [Documentación MDX](https://docs.microsoft.com/en-us/sql/mdx/multidimensional-expressions-mdx-reference) 