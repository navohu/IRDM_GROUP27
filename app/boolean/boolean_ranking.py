from app.ranking import Ranking

class BooleanRanking(Ranking):
	def __init__(self):
		Ranking.__init__(self)

	def rankDocuments(self, query_terms):
		results = {}
		docs = self.documentsWithAllTerms(query_terms)
		for d in docs:
			results[int(d[0])] = len(query_terms)
		return results

	def documentsWithAnyTerm(self, query_terms, excluded_urls=[]):
		if len(excluded_urls) == 0:
			self.db.cur.execute("""SELECT document_id FROM (cs_dictionary AS d JOIN cs_word_occurrences AS w ON w.word_id = d.word_id) AS wd JOIN cs_sites AS s ON s.id = wd.document_id WHERE word = ANY(%s)""", (query_terms,))
		else:
			self.db.cur.execute("""SELECT document_id FROM (cs_dictionary AS d JOIN cs_word_occurrences AS w ON w.word_id = d.word_id) AS wd JOIN cs_sites AS s ON s.id = wd.document_id WHERE word = ANY(%s) AND NOT s.link = ANY(%s)""", (query_terms, excluded_urls))
		return self.db.cur.fetchall()

	def documentsWithAllTerms(self, query_terms):
		self.db.cur.execute("""SELECT document_id FROM (SELECT w.word_id, document_id, occurrences FROM cs_dictionary AS d JOIN cs_word_occurrences AS w ON d.word_id = w.word_id WHERE word = ANY(%s)) AS wd JOIN cs_sites AS s ON wd.document_id = s.id GROUP BY document_id, title, link HAVING count(word_id) = %s""", (query_terms, len(query_terms),))
		return self.db.cur.fetchall()
