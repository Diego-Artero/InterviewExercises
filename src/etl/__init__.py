"""
Pacote ETL — Ponto de entrada para extração, transformação e carregamento dos dados do Infosiga.
"""

from .extract import extract_infosiga_data
from .transform import clean_infosiga_data
from .load import save_dataframes_to_sqlite, process_and_load_data

__all__ = [
    "extract_infosiga_data",
    "clean_infosiga_data",
    "save_dataframes_to_sqlite",
    "process_and_load_data",
]