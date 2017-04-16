from db import MyDB

class Ranking:
    '''Base class for ranking algorithms'''
    def __init__(self):
        self.db = MyDB()

    def rankDocuments(query_terms, max_results): 
        raise NotImplementedError()
