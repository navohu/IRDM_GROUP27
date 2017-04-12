from sklearn.feature_extraction.text import TfidfVectorizer
import math
from app.ranking import Ranking
from math import log
import operator
class TFIDFRanking(Ranking):
    def __init__(self):
        Ranking.__init__(self)
        self.doc_lengths = dict(self.db.get_doc_lengths())

    def TF_IDF(self, term, freq, docid, num_docs, term_freq_coll, doc_lengths, word_occs):
        tf = float(word_occs) / float(doc_lengths)
        idf = log(float(num_docs) / float(term_freq_coll)) / log(2)
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
        num_docs = self.db.get_num_docs()
        word_occs= {}
        for term in query:
            doc_dict= dict(self.db.get_word_occs(term))
            term_freq_coll = self.db.get_term_freq_collection(term)
            word_occs[term] = dict(self.db.get_word_occs(term))

            for docid, freq in doc_dict.iteritems(): #for each document and its word frequency
                score = self.TF_IDF(term, freq, docid, num_docs, term_freq_coll, self.doc_lengths[docid], word_occs[term][docid]) # calculate score

                if docid in query_result: #this document has already been scored once
                    query_result[docid] += score
                else:
                    query_result[docid] = score
        return self.get_top_docs(query_result, max_results)

if __name__ == '__main__':
    ranking = TFIDFRanking()
    results = ranking.rankDocuments("these words", 10)
