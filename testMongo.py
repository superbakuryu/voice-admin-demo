import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
users_col = mydb['users']
clients_col = mydb['clients']
voiceids_col = mydb['voiceids']
sttfiles_col = mydb['sttfiles']
tags_col = mydb['tags']
services_col = mydb['services']


# for x in clients_col.find():
#     print(x)


# from validate_email import validate_email
# is_valid = validate_email("sdlkfabc", check_mx=True)
# print(is_valid)

from hashlib import md5
value= 'https://www.gravatar.com/avatar/' + md5(b'thai@example.com').hexdigest()
print(value)