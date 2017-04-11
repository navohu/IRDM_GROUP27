
class BM25Ranking(Ranking):
    def __init__(self):
        Ranking.__init__(self)
        self.doc_lengths = dict(self.db.get_doc_lengths())
        self.dlt = dict(self.db.get_doc_lengths())

    def score_BM25(n, f, qf, r, N, dl, avdl):
    K = compute_K(dl, avdl)
    first = log( ( (r + 0.5) / (R - r + 0.5) ) / ( (n - r + 0.5) / (N - n - R + r + 0.5)) )
    second = ((k1 + 1) * f) / (K + f)
    third = ((k2+1) * qf) / (k2 + qf)
    return first * second * third

    def compute_K(dl, avdl):
        return k1 * ((1-b) + b * (float(dl)/float(avdl)))

    def rankDocuments(self, query):
        query_result = dict()

        for term in query:
            index = dict(self.db.get_word_occs(term))
            if term in index:
                doc_dict = index[term] # retrieve index entry
                for docid, freq in doc_dict.iteritems(): #for each document and its word frequency
                    score = score_BM25(n=len(doc_dict), f=freq, qf=1, r=0, N=len(self.dlt), dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length()) # calculate score
                    if docid in query_result: #this document has already been scored once
                        query_result[docid] += score
                    else:
                        query_result[docid] = score

        return query_result

if __name__ == "__main__":
    ranking = BM25Ranking()
    results = ranking.rankDocuments("these words")


