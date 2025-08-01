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

CLEANED_DIR = os.path.join(BASE_DIR, config["scraping"]["save_path_processed_cleaned"])
FORMATTED_DIR = os.path.join(BASE_DIR, config["scraping"]["save_path_processed_formatted"])
PESSOAS_DIR = os.path.join(FORMATTED_DIR, 'pessoas.csv')
SINISTROS_DIR = os.path.join(FORMATTED_DIR, 'sinistros.csv')
VEICULOS_DIR = os.path.join(FORMATTED_DIR, 'veiculos.csv')
DIRS = [PESSOAS_DIR,SINISTROS_DIR,VEICULOS_DIR]

for DIR in DIRS:
    if DIR == PESSOAS_DIR:
        df = pd.read_csv(DIR)
        df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
        df = df[df['gravidade_lesao'] != 'NÃO DISPONIVEL']

    elif DIR == VEICULOS_DIR:
        df = pd.read_csv(DIR)
        df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
        df = df[df['tipo_veiculo'] != 'NAO DISPONIVEL']

    else:
        df = pd.read_csv(DIR)
        df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
        df = df[df['tipo_registro'] != 'NOTIFICACAO']    

    output_file = os.path.join(CLEANED_DIR, os.path.basename(DIR))
    df.to_csv(output_file, index=False)