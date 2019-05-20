import pymongo
import json

class ConnectDB():

	def __init__(self):
		with open("view/db/mongoDB.json") as Json:
			user_doc = json.loads(Json.read())
		self.mongoURL = str("mongodb+srv://%s:%s%s"%(user_doc['MongoID'],user_doc['MongoPassword'],user_doc["MongoURL"]))
		self.client = pymongo.MongoClient(self.mongoURL)
		self.db = pymongo.database.Database(self.client, 'zoin')

	def close(self):
		try:
			self.client.close()
			return True

		except:
			return False
