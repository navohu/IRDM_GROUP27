import operator

from app.ranking import Ranking

class QueryLikelihoodRanking(Ranking):
	def __init__(self):
		Ranking.__init__(self)
		self.doc_lengths = dict(self.db.get_doc_lengths())

	def rankDocuments(self, query_terms, max_results):
		likelihood_scores = {}
		word_occs = {}
		for term in query_terms:
			word_occs[term] = dict(self.db.get_word_occs(term))
			print term, 'appears in ', len(word_occs[term]), 'documents'
		for doc_id in self.doc_lengths:
			likelihood_scores[doc_id] = 1.0
			for term in query_terms:
				if doc_id in word_occs[term]:
					tf = word_occs[term][doc_id]
				else:
					# TODO: smoothing
					tf = 0
				doc_length = self.doc_lengths[doc_id]
				if doc_length is None:
					# no words found for doc
					max_likelihood = 0
				else:
					max_likelihood = float(tf) / doc_length
				likelihood_scores[doc_id] *= max_likelihood
		top_results = sorted(likelihood_scores.iteritems(), key=operator.itemgetter(1), reverse=True)[:max_results]
		top_pages = []
		for result in top_results:
			if result[1] > 0:
				page = self.db.get_site_by_id(result[0])
				print (page[1], result[1])
				top_pages.append(page)
		return top_pages

if __name__ == "__main__":
	ranking = QueryLikelihoodRanking()
	results = ranking.rankDocuments("these words", 10)
