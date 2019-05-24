import pymongo
from bson.objectid import ObjectId

"""MongoDB Database Access Object"""
class Posts():
	
	def __init__(self,db):
		self.posts = pymongo.collection.Collection(db,'Posts')

	def postCreate(self,postDict):
		try:
			obj_id = self.posts.insert_one(postDict).inserted_id
			return obj_id
		except:
			return False

	def postDelete(self,obj_id):
		try:
			self.posts.delete_one({"_id":ObjectId(obj_id)})
			return True
		except:
			return False

	def postUdate(self,postDict):
		try:
			self.posts.udb.counters.find_one_and_modify(
				query={"_id": ObjcetId(postDict["obj_id"])},
				update={"$set":{"postTitle":postDict["postTitle"],"postContent":postDict["postContent"]}},
				upsert=False
				)
			return True
		except:
			return False

	def getAllposts(self):
		try:
			result = self.posts.find({})
			return result
		except:
			return False
