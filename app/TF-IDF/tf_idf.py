from sklearn.feature_extraction.text import TfidfVectorizer
import math
from app.ranking import Ranking
from math import log
class TFIDFRanking(Ranking):
    def __init__(self):
        Ranking.__init__(self)

    def TF_IDF(self, term, freq, docid):
        tf = float(self.db.get_term_freq_doc(term, docid)) / float(self.db.get_doc_length(docid))
        idf = log(float(self.db.get_num_docs()) / float(self.db.get_term_freq_collection(term))) / log(2)
        return tf*idf

    def get_top_docs(self, results, max_results):
        top_results = sorted(results.iteritems(), key=operator.itemgetter(1), reverse=True)[:max_results]
        top_pages = []
        for result in top_results:
            if result[1] > 0:
                page = self.db.get_site_by_id(result[0])
                print (page[1], result[1])
                top_pages.append(page)
        return top_pages

    def rankDocuments(self, query, max_results):
        query_result = dict()
        for term in query:
            doc_dict= dict(self.db.get_word_occs(term))
            for docid, freq in doc_dict.iteritems(): #for each document and its word frequency
                score = self.TF_IDF(term, freq, docid) # calculate score

                if docid in query_result: #this document has already been scored once
                    query_result[docid] += score
                else:
                    query_result[docid] = score
                print "Document" + str(docid)
                print query_result[docid]
        return self.get_top_docs(query_result, max_results)


if __name__ == '__main__':
    ranking = TFIDFRanking()
    results = ranking.rankDocuments("these words", 10)

	# def get_comparisons(self, results):
	# 	results = dict()
	# 	for count_0, doc_0 in enumerate(tfidf.toarray()):
	# 		for count_1, doc_1 in enumerate(tfidf.toarray()):
	# 			if count_1 <= count_0:
	# 				continue
	# 			else:
	# 				results.append((cosine_similarity(doc_0, doc_1), count_0, count_1))
	# 	return results

	# self.doc_lengths = dict(self.db.get_doc_lengths())
	# self.dlt = dict(self.db.get_doc_lengths())

	# def cosine_similarity(self, vector1, vector2):
	# 	dot_product = sum(p*q for p,q in zip(vector1, vector2))
	# 	magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
	# 	if not magnitude:
	# 		return 0
	# 	return dot_product/magnitude
