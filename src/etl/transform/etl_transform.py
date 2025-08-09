import os
import pandas as pd
import yaml

# Define a raiz do projeto subindo 3 níveis a partir deste script
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Caminho para o arquivo de configuração
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.yaml")


def load_config(CONFIG_PATH):
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

config = load_config()

# Diretórios

CLEANED_DIR = os.path.join(BASE_DIR, config["scraping"]["save_path_processed_cleaned"])
FORMATTED_DIR = os.path.join(BASE_DIR, config["scraping"]["save_path_processed_formatted"])
PESSOAS_PATH = os.path.join(FORMATTED_DIR, 'pessoas.csv')
SINISTROS_PATH = os.path.join(FORMATTED_DIR, 'sinistros.csv')
VEICULOS_PATH = os.path.join(FORMATTED_DIR, 'veiculos.csv')
PATHS = [PESSOAS_PATH,SINISTROS_PATH,VEICULOS_PATH]

def data_cleaner(PATHS):
    for PATH in PATHS:
        try:
            if PATH == PESSOAS_PATH:
                df = pd.read_csv(PATH)
                df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
                df = df[df['gravidade_lesao'] != 'NÃO DISPONIVEL']

            elif PATH == VEICULOS_PATH:
                df = pd.read_csv(PATH)
                df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
                df = df[df['tipo_veiculo'] != 'NAO DISPONIVEL']

            else:
                df = pd.read_csv(PATH)
                df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
                df = df[df['tipo_registro'] != 'NOTIFICACAO']    

            output_file = os.path.join(CLEANED_DIR, os.path.basename(PATH))
            df.to_csv(output_file, index=False)
        except Exception as e:
            print(f"Erro ao limpar o relatório: {e}")
            
if __name__ == '__main__':
    data_cleaner(PATHS)