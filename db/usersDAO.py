import pymongo

"""MongoDB Database Access Object"""
class Users():
	
	def __init__(self,db):
		users = pymongo.collection.Collection(db,'Users')

	def userValidation(self,userDict):
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