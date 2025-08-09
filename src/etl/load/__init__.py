"""
Módulo de transformação e limpeza dos dados do Infosiga.
"""

from .etl_loader import process_and_load_data

__all__ = ["process_and_load_data"]