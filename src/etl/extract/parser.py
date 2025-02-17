import os
import zipfile
import pandas as pd
import yaml

# Define a raiz do projeto subindo 3 níveis a partir deste script
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
print("BASE_DIR:", BASE_DIR)
# Caminho para o arquivo de configuração (relativo à raiz do projeto)
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.yaml")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

config = load_config()

# Obter o caminho relativo para a pasta raw definido no YAML e construir o caminho absoluto
raw_relative = config["scraping"]["save_path"] 
DOWNLOAD_DIR = os.path.join(BASE_DIR, raw_relative)

# Obter o caminho relativo para a pasta processed definido no YAML e construir o caminho absoluto
processed_relative = config["scraping"]["save_path_processed"] 
PROCESSED_DIR = os.path.join(BASE_DIR, processed_relative)

def extract_zip(zip_path, extract_dir):
    """
    Extrai o conteúdo do arquivo ZIP para o diretório especificado.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    print(f"Arquivos extraídos para: {extract_dir}")

def parse_report(file_path):
    """
    Lê o arquivo de relatório (CSV ou Excel) e retorna um DataFrame.
    """
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path, encoding='utf-8')
    elif file_path.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path)
    else:
        raise ValueError(f"Formato de arquivo não suportado: {file_path}")
    return df

if __name__ == "__main__":
    # Exemplo: o arquivo ZIP baixado deve estar na pasta raw
    zip_file_obitos = os.path.join(DOWNLOAD_DIR, "obitos.zip")
    zip_file_sinistros_fatais = os.path.join(DOWNLOAD_DIR, "sinistros_fatais.zip")
    zip_file_sinistros_nao_fatais = os.path.join(DOWNLOAD_DIR, "sinistros_nao_fatais.zip")
    
    
    # Extrair o ZIP
    extract_zip(zip_file_obitos, PROCESSED_DIR)
    extract_zip(zip_file_sinistros_fatais, PROCESSED_DIR)
    extract_zip(zip_file_sinistros_nao_fatais, PROCESSED_DIR)


    # Supondo que o ZIP contenha um arquivo "obitos.csv"
    file_path = os.path.join(PROCESSED_DIR, "obitos.csv")
    try:
        df = parse_report(file_path)
        print("Preview dos dados:")
        print(df.head())
        
        processed_file = os.path.join(PROCESSED_DIR, "obitos_processado.csv")
        
        # Salvar o DataFrame processado
        df.to_csv(processed_file, index=False)
        print(f"Relatório processado salvo em: {processed_file}")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
