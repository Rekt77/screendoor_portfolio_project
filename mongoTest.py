import pymongo
import json

with open("mongoDB.json") as Json:
    user_doc = json.loads(Json.read())

mongoURL = str("mongodb://%s:%s%s"%(user_doc['MongoID'],user_doc['MongoPassword'],user_doc["MongoURL"]))
client = pymongo.MongoClient(mongoURL)
db = pymongo.database.Database(client, 'zoin')
users = pymongo.collection.Collection(db,'Users')


print(users.insert_one({"hi":"1234"}).inserted_id)