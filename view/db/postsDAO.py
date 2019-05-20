import pymongo

"""MongoDB Database Access Object"""
class Posts():
	
	def __init__(self,db):
		self.posts = pymongo.collection.Collection(db,'Posts')

	def postCreate(self,postDict):
		try:
			self.posts.insert_one(postDict)
			return True
		except:
			return False

	def postDelete(self,postDict):
		try:
			self.posts.delete_one(postsDict)
			return True
		except:
			return False

	def getAllposts(self):
		try:
			result = self.posts.find({})
			return result
		except:
			return False
