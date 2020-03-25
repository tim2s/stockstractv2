import os

import pymongo
from pymongo import uri_parser


class Repository:

    def __init__(self):
        mongo_uri = os.getenv('MONGODB_URI')
        connection = uri_parser.parse_uri(mongo_uri)
        self.db_client = pymongo.MongoClient(mongo_uri, retryWrites=False)
        self.db = self.db_client[connection.get('database', 'stockstract')]
        self.stock_collection = self.db["stocks"]

    def add_stock(self, stock_data):
        self.stock_collection.insert_one(stock_data)
