import os
import yaml
import shutil
import pandas as pd
import kagglehub

def load_kaggle_csv(dataset_id: str, filename: str, download_dir: str) -> pd.DataFrame:
    
    cached_path = kagglehub.dataset_download(dataset_id)

    os.makedirs(download_dir, exist_ok=True)

    src_file = os.path.join(cached_path, filename)
    if not os.path.exists(src_file):
        raise FileNotFoundError(f"O arquivo {filename} não foi encontrado no dataset {dataset_id}")
    

    dst_file = os.path.join(download_dir, filename)

   
    if not os.path.exists(dst_file):
        shutil.copy2(src_file, dst_file)

    
    return pd.read_csv(dst_file)

# Project root

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Config path setup

CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.yaml")

def load_config(CONFIG_PATH):
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

config = load_config(CONFIG_PATH)
# Directories

KAGGLE_PATH = config["parsing"]["base_url"]
raw_relative = config["parsing"]["save_path"] 
DOWNLOAD_DIR = os.path.join(BASE_DIR, raw_relative)

df = load_kaggle_csv(KAGGLE_PATH,"CarsData.csv",DOWNLOAD_DIR)

print(df.head())
