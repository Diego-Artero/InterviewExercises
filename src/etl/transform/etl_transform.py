import os
import pandas as pd
import yaml

# Define a raiz do projeto subindo 3 níveis a partir deste script
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Caminho para o arquivo de configuração
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.yaml")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

config = load_config()

# Diretórios
FORMATTED_DIR = os.path.join(BASE_DIR, config["scraping"]["save_path_processed_formatted"])


