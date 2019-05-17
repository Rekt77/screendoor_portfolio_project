import pymongo
import json

"""MongoDB Database Access Object"""
class Users():
	
	def __init__(self):
		with open("mongoDB.json") as Json:
    		user_doc = json.loads(Json.read())
		mongoURL = str("mongodb://%s:%s%s"%(user_doc['MongoID'],user_doc['MongoPassword'],user_doc["MongoURL"]))
		client = pymongo.MongoClient(mongoURL)
		db = pymongo.database.Database(client, 'zoin')
		users = pymongo.collection.Collection(db,'Users')

	def userValidation(self, userDict):
		if self.users.find_one(userDict) is not None:
			return False
		else:
			return True

	def userAuthentication(self,userDict):
		if self.users.find_one(userDict) is not None:
			return True
		else:
			return False

	def userCreate(self,userDict):
		if self.userValidation({"userEmail":userDict["userEmail"]}):
			try:
				self.users.insert_one(userDict)
				return True
			except:
				return False
		else :
			return False

	def userDelete(self,userDict):
		if self.userAuthentication(userDict):
			self.users.delete_one(userDict)
			return True
		else:
			return False