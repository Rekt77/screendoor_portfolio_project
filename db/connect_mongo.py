import pymongo
import json

class ConnectDB():

	def __init__(self):
		with open("mongoDB.json") as Json:
    		user_doc = json.loads(Json.read())
		mongoURL = str("mongodb://%s:%s%s"%(user_doc['MongoID'],user_doc['MongoPassword'],user_doc["MongoURL"]))
		client = pymongo.MongoClient(mongoURL)
		db = pymongo.database.Database(client, 'zoin')

	def close(self):
		try:
			self.client.close()
			return True

		except:
			return False