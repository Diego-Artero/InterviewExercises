import os
import pandas as pd
import yaml

# Project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Config path setup
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.yaml")

def load_config(CONFIG_PATH):
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

config = load_config(CONFIG_PATH)

# Directories

RAW_DIR = os.path.join(BASE_DIR, config["parsing"]["save_path"])
CLEANED_DIR = os.path.join(BASE_DIR,config["parsing"]["save_path_processed_cleaned"])
DATA_PATH = os.path.join(RAW_DIR, 'CarsData.csv')


def data_cleaner(DATA_PATH):
    
    df = pd.read_csv(DATA_PATH)
    
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')

    df["manufacturer"] = df["manufacturer"].str.capitalize()
    
    df["manufacturer"] = df["manufacturer"].replace({
    "Hyundi": "Hyundai",
    "Merc": "Mercedes-Benz"
    })

    df["car_age"] = 2025 - df["year"]
    df["price_per_engine"] = df["price"] / df["enginesize"]

    os.makedirs(CLEANED_DIR, exist_ok=True)
    output_file = os.path.join(CLEANED_DIR, os.path.basename(DATA_PATH))
    df.to_csv(output_file, index=False)
    
            
if __name__ == '__main__':
    data_cleaner(DATA_PATH)