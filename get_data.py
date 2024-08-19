import os
import sys
import pandas as pd
import numpy as np
import pymongo

from src.logger.logger import logging
from src.exception.exception import NetworkException
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class NetworkDataExtract:
    
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkException(e,sys)
        

    def csv_to_json_converter(self):
        try:
            logging.info("Started with CSV to JSON conversion")
            df = pd.read_csv(r"data/NetworkData.csv")
            records = df.to_dict(orient="records")
            return records
        except Exception as e:
            logging.info("Error occurred during CSV to JSON conversion")
            raise NetworkException(e,sys)
        
    def push_data_mongodb(self,records,database,collection):
        try:
            logging.info("Started with pushing data from local to MongoDB")
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)

        except Exception as e:
            logging.info("Error occurred while pushing data from local to MongoDB")
            raise NetworkException(e,sys)
        

if __name__ == "__main__":
    DB_NAME = "Phishing_DB"
    COLLECTION_NAME = "NetworkData"
    obj = NetworkDataExtract()
    records = obj.csv_to_json_converter()
    obj.push_data_mongodb(records,DB_NAME,COLLECTION_NAME)
