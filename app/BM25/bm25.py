from app.ranking import Ranking
from math import log
import operator
class BM25Ranking(Ranking):
    def __init__(self):
        Ranking.__init__(self)
        self.doc_lengths = dict(self.db.get_doc_lengths())
        self.dlt = dict(self.db.get_doc_lengths())
        
    def score_BM25(self, n, f, qf, r, N, dl, avdl):
        k1 = 1.2
        k2 = 100
        b = 0.75
        R = 0.0
        K = self.compute_K(dl, avdl, k1, b)
        first = log( ( (r + 0.5) / (R - r + 0.5) ) / ( (n - r + 0.5) / (N - n - R + r + 0.5)) )
        second = ((k1 + 1) * f) / (K + f)
        third = ((k2+1) * qf) / (k2 + qf)
        return first * second * third

    def compute_K(self, dl, avdl, k1, b):
        return k1 * ((1-b) + b * (float(dl)/float(avdl)))

    def get_length(self, table, docid):
        if docid in table:
            return table[docid]
        else:
            raise LookupError('%s not found in table' % str(docid))

    def get_average_length(self, table):
        sum = 0
        for length in table.itervalues():
            if length == None:
                continue
            sum += length
        return float(sum) / float(len(table))

    def rankDocuments(self, query):
        query_result = dict()

        for term in query:
            doc_dict= dict(self.db.get_word_occs(term))
            n = len(doc_dict)
            for docid, freq in doc_dict.iteritems(): #for each document and its word frequency
                score = self.score_BM25(n, freq, 1, 0, len(self.dlt), self.get_length(self.dlt,docid), self.get_average_length(self.dlt)) # calculate score
                if docid in query_result: #this document has already been scored once
                    query_result[docid] += score
                else:
                    query_result[docid] = score
        return query_result

if __name__ == "__main__":
    ranking = BM25Ranking()
    results = ranking.rankDocuments("syllabus 2017")

