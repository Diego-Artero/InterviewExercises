import yaml
import os

# Caminho do arquivo de configuração
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")

# Função para carregar o YAML
def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

# Carregar as configurações
config = load_config()

# Definição das variáveis globais
PROJECT_NAME = config["project"]["name"]
VERSION = config["project"]["version"]
DESCRIPTION = config["project"]["description"]
AUTHOR = config["project"]["author"]

# Configurações de Web Scraping
SCRAPING_URL = config["scraping"]["base_url"]
HEADERS = config["scraping"]["request_headers"]
OUTPUT_FORMAT = config["scraping"]["output_format"]
SAVE_PATH = config["scraping"]["save_path"]

# Configurações do Banco de Dados
DB_TYPE = config["database"]["type"]
DB_HOST = config["database"]["host"]
DB_PORT = config["database"]["port"]
DB_USER = config["database"]["user"]
DB_PASSWORD = config["database"]["password"]
DB_NAME = config["database"]["dbname"]

# Configurações de Machine Learning
MODEL_TYPE = config["ml"]["model_type"]
TEST_SIZE = config["ml"]["test_size"]
RANDOM_STATE = config["ml"]["random_state"]
FEATURES = config["ml"]["features"]

# Configurações de Logging
LOG_LEVEL = config["logging"]["level"]
LOG_FILE = config["logging"]["log_file"]

# Configurações de Visualização
VISUALIZATION_TOOL = config["visualization"]["tool"]
VISUALIZATION_THEME = config["visualization"]["theme"]

if __name__ == "__main__":
    # Testando a carga do settings.py
    print(f"Projeto: {PROJECT_NAME} - Versão: {VERSION}")
    print(f"Banco de Dados: {DB_TYPE} em {DB_HOST}:{DB_PORT}")
    print(f"Modelo de ML: {MODEL_TYPE} | Features: {FEATURES}")
