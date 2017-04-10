from db import MyDB

class Ranking:
	'''Base class for ranking algorithms'''
	def __init__(self):
		self.db = MyDB()

	def rankDocuments(query_terms, max_results):
		'''Returns (title, URL) pairs for documents that best match the query terms'''
		raise NotImplementedError()