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

# Obter o caminho relativo para a pasta processed definido no YAML e construir o caminho absoluto para ela e suas subpastas
processed_relative = config["scraping"]["save_path_processed"] 
PROCESSED_DIR = os.path.join(BASE_DIR, processed_relative)
UNZIPPED_DIR = os.path.join(PROCESSED_DIR, "unzipped")
FORMATTED_DIR = os.path.join(PROCESSED_DIR, "formatted")

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
        df = pd.read_csv(file_path, encoding='latin1', delimiter=';')
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
    zip_path_list = [zip_file_obitos, zip_file_sinistros_nao_fatais, zip_file_sinistros_fatais]
    
    # Extrair o ZIP
    for zip_path in zip_path_list:
        extract_zip(zip_path, UNZIPPED_DIR)
    
    # Formatar corretamente os arquivos recém unzippados
    obitos_file_path = os.path.join(UNZIPPED_DIR, "obitos.csv")
    sinistros_nao_fatais_file_path2019 = os.path.join(UNZIPPED_DIR, "sinistros_nao_fatais_2019-2020.csv")
    sinistros_nao_fatais_file_path2021 = os.path.join(UNZIPPED_DIR, "sinistros_nao_fatais_2021-2024.csv")
    sinistros_fatais = os.path.join(UNZIPPED_DIR, "sinistros_fatais.csv")

    file_path_list = [obitos_file_path, sinistros_nao_fatais_file_path2019, sinistros_nao_fatais_file_path2021, sinistros_fatais]
    
    try:
        for file_path in file_path_list:
            df = parse_report(file_path)
            print("Preview dos dados:")
            print(df.head())
            
            if file_path == obitos_file_path:
                output_file = os.path.join(FORMATTED_DIR, "obitos.csv")
            elif file_path == sinistros_nao_fatais_file_path2019:
                output_file = os.path.join(FORMATTED_DIR, "sinistros_nao_fatais_2019-2020.csv")
            elif file_path == sinistros_nao_fatais_file_path2021:
                output_file = os.path.join(FORMATTED_DIR, "sinistros_nao_fatais_2021-2024.csv")
            elif file_path == sinistros_fatais:
                output_file = os.path.join(FORMATTED_DIR, "sinistros_fatais.csv")
            # Salvar o DataFrame processado
         
            df.to_csv(output_file, index=False)
            

            print(f"Relatório processado salvo em: {FORMATTED_DIR}")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
