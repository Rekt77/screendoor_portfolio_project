import pymongo

"""MongoDB Database Access Object"""
class Books():
	
	def __init__(self,db):
		self.books = pymongo.collection.Collection(db,'Books')

	def bookCreate(self,bookDict):
		try:
			self.books.insert_one(bookDict)
			return True
		except:
			return False

	def bookDelete(self,bookDict):
		try:
			self.users.delete_one(bookDict)
			return True
		except:
			return False

	def getAllbooks(self):
		try:
			result = self.books.find({})
			return result
		except:
			return False