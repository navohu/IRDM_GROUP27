import operator

from app.ranking import Ranking

class QueryLikelihoodRanking(Ranking):
	def __init__(self):
		Ranking.__init__(self)
		self.doc_lengths = dict(self.db.get_doc_lengths())
		for k in self.doc_lengths:
			if self.doc_lengths[k] is None:
				self.doc_lengths[k] = 0
		self.words_in_collection = sum(self.doc_lengths.itervalues())

	def rankDocuments(self, query_terms):
		likelihood_scores = {}
		word_occs = {}
		lambdaRatio = 0.8
		for term in query_terms:
			word_occs[term] = dict(self.db.get_word_occs(term))
			print term, 'appears in ', len(word_occs[term]), 'documents'
			bg_prob = float(self.db.get_term_freq_collection(term)) / self.words_in_collection
		for doc_id in self.doc_lengths:
			doc_length = self.doc_lengths[doc_id]
			if doc_length is None or doc_length == 0:
				# no words found in doc
				continue
			likelihood_scores[doc_id] = 1.0
			for term in query_terms:
				if doc_id in word_occs[term]:
					tf = word_occs[term][doc_id]
				else:
					tf = 0
				term_likelihood = lambdaRatio * tf + (1 - lambdaRatio) * bg_prob
				max_likelihood = float(term_likelihood) / doc_length
				likelihood_scores[doc_id] *= max_likelihood
		return likelihood_scores

if __name__ == "__main__":
	ranking = QueryLikelihoodRanking()
	results = ranking.rankDocuments("these words", 10)
