import pymongo
from bson.objectid import ObjectId

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

def get_client_info(client_id):
  if not isinstance(client_id, ObjectId):
    client_id = ObjectId(client_id)
  
  return mydb.clients.find_one({'_id': client_id})