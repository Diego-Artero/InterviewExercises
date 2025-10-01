import pandas as pd
import yaml
from pymongo import MongoClient

def load_to_mongo(df, config_path="config/config.yaml"):
    # Read config
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    mongo_conf = config["mongodb"]

    client = MongoClient(mongo_conf["uri"])
    db = client[mongo_conf["database"]]
    collection = db[mongo_conf["collection"]]

    # DataFrame -> dict
    records = df.to_dict(orient="records")

    # insert with cleaning
    collection.delete_many({})
    try:
        collection.insert_many(records)

        print("✅ Data loaded into MongoDB successfully!")
    except Exception as e:
        print(f"❎ Data couldn't be loaded due to {e}")
if __name__ == "__main__":
    df = pd.read_csv("data/processed/cleaned/CarsData.csv")
    load_to_mongo(df)