import pandas as pd
import yaml
from sqlalchemy import create_engine

def load_to_postgres(df, config_path="config/config.yaml"):
    # Read config
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    pg_conf = config["postgres"]

    # Connecting to database
    engine = create_engine(
        f"postgresql+psycopg2://{pg_conf['user']}:{pg_conf['password']}@{pg_conf['host']}:{pg_conf['port']}/{pg_conf['database']}"
    )

    # Loading the df into Postgres
    try:
        df.to_sql("cars", con=engine, if_exists="replace", index=False)
        print("✅ Data Loaded into Postgre successfully!")
    except Exception as e:
        print(f"❎ Data couldn't be loaded due to {e}")
        
if __name__ == "__main__":
    
    df = pd.read_csv("data/processed/cleaned/CarsData.csv")
    load_to_postgres(df)

