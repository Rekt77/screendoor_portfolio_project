import pymongo
import json
import bson

with open("./view/db/mongoDB.json") as Json:
    user_doc = json.loads(Json.read())

mongoURL = str("mongodb://%s:%s%s"%(user_doc['MongoID'],user_doc['MongoPassword'],user_doc["MongoURL"]))
client = pymongo.MongoClient(mongoURL)
db = pymongo.database.Database(client, 'zoin')
users = pymongo.collection.Collection(db,'Users')


print(users.count())
[i for i in dbm.neo_nodes.find({"_id": ObjectId(obj_id_to_find)})]
print(users.insert_id)
print(users.find_one({"_id"}))
