import pymongo
from bson.objectid import ObjectId

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

def get_client_info(client_id):
  if not isinstance(client_id, ObjectId):
    client_id = ObjectId(client_id)
  
  return mydb.clients.find_one({'_id': client_id})

def get_merchant_info(merchant_id):
  if not isinstance(merchant_id, ObjectId):
    merchant_id = ObjectId(merchant_id)
  
  return mydb.merchants.find_one({'_id': merchant_id})

def get_service_info(service_id):
  if not isinstance(service_id, ObjectId):
    service_id = ObjectId(service_id)
  
  return mydb.services.find_one({'_id': service_id})

def get_voiceid_info(voiceid_id):
  if not isinstance(voiceid_id, ObjectId):
    voiceid_id = ObjectId(voiceid_id)
  
  return mydb.voiceids.find_one({'_id': voiceid_id})