import time
from app.ranking import Ranking
from app.search_engine import SearchEngine
from app.query_likelihood.query_likelihood_ranking import QueryLikelihoodRanking
from app.BM25.bm25 import BM25Ranking
from app.TFIDF.tf_idf import TFIDFRanking

class Timing():
    def __init__(self):
        self.search = SearchEngine()

    def produce_time(self, queries, ranking, use_pagerank):
        timing = dict()
        for query in queries:
            query_terms = self.search.processQueryTerms(query)
            prev_time = time.time()
            results = ranking.rankDocuments(query_terms)
            if use_pagerank:
                pageranks = dict(ranking.db.get_pageranks())
                results = self.search.add_pageranks(pageranks, results)
            timing[query] = time.time() - prev_time
        return timing

if __name__ == "__main__":
    queries = ["jun wang", "degree", "moodle", "alphago", "information retrieval and data mining", "computer graphics syllabus"]
    rankings = [BM25Ranking(), TFIDFRanking(), QueryLikelihoodRanking()]
    timing = Timing()
    use_pagerank = True
    for ranking in rankings:
        print ranking.__class__.__name__
        print timing.produce_time(queries, ranking, use_pagerank)
