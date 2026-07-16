from pymongo import MongoClient

MongoURL = "mongodb://localhost:27017/"
client = MongoClient(MongoURL)
db = client["privategpt"]
users_collection = db["users"]

